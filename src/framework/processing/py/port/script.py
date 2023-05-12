import logging
import json
import io

import port.api.props as props
from port.api.commands import (CommandSystemDonate, CommandUIRender)
import port.whatsapp

LOG_STREAM = io.StringIO()

logging.basicConfig(
    stream=LOG_STREAM,  # comment this line if you want the logs in std out
    level=logging.INFO,  # change to DEBUG for debugging logs
    format="%(asctime)s --- %(name)s --- %(levelname)s --- %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S%z",
)

LOGGER = logging.getLogger(__name__)

def process(sessionId):
    LOGGER.info("Starting the donation flow")
    yield donate_logs(f"{sessionId}-tracking")

    platforms = ["Whatsapp","Whatsapp","Whatsapp","Whatsapp","Whatsapp"]

    subflows = len(platforms)
    steps = 2
    step_percentage = (100/subflows)/steps
    counter = 0
    # progress in %
    progress = 0

    donatedFileFlag = [False, False, False, False, False]
    selectedUsername = ''
    donatedFileNames = []

    for _, platform in enumerate(platforms):

        data = None
        username_partner = ""
        progress += step_percentage
        counter = counter + 1

        while True:
            promptFile = prompt_file(platform,counter, "application/zip, text/plain",donatedFileFlag)
            fileResult = yield render_donation_page(platform, counter, promptFile, progress)
            if fileResult.__type__ == 'PayloadString':
                LOGGER.info("Valid file payload")
                yield donate_logs(f"{sessionId}-tracking")

                df_with_chats = port.whatsapp.parse_chat(fileResult.value)
                df_with_chats = port.whatsapp.reverse_dataframe(df_with_chats)

                # If data extracted was successful
                if not df_with_chats.empty and fileResult.value not in donatedFileNames:

                    df_with_chats = port.whatsapp.remove_empty_chats(df_with_chats)
                    list_with_users = port.whatsapp.extract_users(df_with_chats)

                    # Check how many users are found in chat should be checked before initial user selection
                    if len(list_with_users) > 2:
                        retry_result = yield render_donation_page(platform, counter, retry_no_group_chat(), progress)
                        if retry_result.__type__ == "PayloadTrue":
                            continue
                        else:
                            break

                    # Determine username upon first donation
                    if selectedUsername == "":
                        selection = yield prompt_radio_menu(platform, counter, progress, list_with_users)
                        # If user skips during this process, selectedUsername remains equal to ""
                        if selection.__type__ == "PayloadString":
                            selectedUsername = selection.value

                    # If selected does not occur in chat
                    if selectedUsername not in list_with_users:
                        retry_result = yield render_donation_page(platform, counter, retry_different_username(selectedUsername), progress)
                        if retry_result.__type__ == "PayloadTrue":
                            continue
                        else:
                            break

                    # Happy flow !
                    else:
                        (username_partner, ) = set(list_with_users) - set([selectedUsername])
                        df_with_chats = port.whatsapp.filter_username(df_with_chats, selection.value)
                        df_with_chats = port.whatsapp.remove_name_column(df_with_chats)
                        df_with_chats = port.whatsapp.remove_date_column(df_with_chats)
                        list_with_df_with_chats = port.whatsapp.split_dataframe(df_with_chats, 5000)
                        data = list_with_df_with_chats
                        break

                # Check if file was not previously donated
                if fileResult.value in donatedFileNames:
                    retry_result = yield render_donation_page(platform, counter, retry_different_file(fileResult.value), progress)
                    if retry_result.__type__ == "PayloadTrue":
                        continue
                    else:
                        break

                # If not enter retry flow
                else:
                    retry_result = yield render_donation_page(platform, counter, retry_confirmation(platform), progress)
                    if retry_result.__type__ == "PayloadTrue":
                        continue
                    else:
                        break
            else:
                break

        progress += step_percentage

        # This check should be here to account for the skip button being
        # This button can be pressed at any moment
        if data is not None:
            # STEP 2: ask for consent
            prompt = prompt_consent(data, username_partner)
            consent_result = yield render_donation_page(platform, counter, prompt, progress)
            if consent_result.__type__ == "PayloadJSON":
                yield donate(f"{sessionId}-{platform}", consent_result.value)
                donatedFileFlag[counter-1] = True
                donatedFileNames.append(fileResult.value)
                LOGGER.info("Data donated: %s %s", platform, counter)
                yield donate_logs(f"{sessionId}-tracking")
            else:
                LOGGER.info("Skipped ater reviewing consent: %s %s", platform, counter)
                yield donate_logs(f"{sessionId}-tracking")

    yield render_end_page()


def prompt_radio_menu(platform, counter, progress, list_with_users):

    title = props.Translatable({
        "en": f"",
        "nl": f""
    })
    description = props.Translatable({
        "en": f"Please select your username",
        "nl": f"Selecteer uw gebruikersnaam"
    })
    header = props.PropsUIHeader(props.Translatable({
        "en": 'Conversation ' + str(counter),
        "nl": 'Gesprek ' + str(counter)
    }))

    radio_input = [{"id": index, "value": username} for index, username in enumerate(list_with_users)]
    body = props.PropsUIPromptRadioInput(title, description, radio_input)
    footer = props.PropsUIFooter(progress)
    page = props.PropsUIPageDonation(platform, header, body, footer)
    return CommandUIRender(page)


def render_end_page():
    page = props.PropsUIPageEnd()
    return CommandUIRender(page)


def render_donation_page(platform,counter, body, progress):
    header = props.PropsUIHeader(props.Translatable({
        "en": 'Conversation ' + str(counter) + ' of 5',
        "nl": 'Conversation ' + str(counter) + ' of 5'
    }))

    footer = props.PropsUIFooter(progress)
    page = props.PropsUIPageDonation(platform, header, body, footer)
    return CommandUIRender(page)


def retry_different_file(file_name):
    text = props.Translatable({
        "en": f"Je hebt {file_name} al gedoneerd, probeer een ander bestand",
        "nl": f"Je hebt {file_name} al gedoneerd, probeer een ander bestand"
    })
    ok = props.Translatable({
        "en": "Try again",
        "nl": "Probeer opnieuw"
    })
    cancel = props.Translatable({
        "en": "",
        "nl": ""
    })
    return props.PropsUIPromptConfirm(text, ok, cancel)


def retry_confirmation(platform):
    text = props.Translatable({
        "en": f"Unfortunately, we cannot process your {platform} file. Continue, if you are sure that you selected the right file. Try again to select a different file.",
        "nl": f"Helaas, kunnen we uw {platform} bestand niet verwerken. Weet u zeker dat u het juiste bestand heeft gekozen? Ga dan verder. Probeer opnieuw als u een ander bestand wilt kiezen."
    })
    ok = props.Translatable({
        "en": "Try again",
        "nl": "Probeer opnieuw"
    })
    cancel = props.Translatable({
        "en": "Continue",
        "nl": "Verder"
    })
    return props.PropsUIPromptConfirm(text, ok, cancel)


def retry_no_group_chat():
    text = props.Translatable({
        "en": f"Oeps je hebt per ongeluk een groupchat geselecteerd, probeer opnieuw",
        "nl": f"Oeps je hebt per ongeluk een groupchat geselecteerd, probeer opnieuw"
    })
    ok = props.Translatable({
        "en": "Try again",
        "nl": "Probeer opnieuw"
    })
    cancel = props.Translatable({
        "en": "",
        "nl": ""
    })
    return props.PropsUIPromptConfirm(text, ok, cancel)


def retry_different_username(username):
    text = props.Translatable({
        "en": f"Your username {username} was not found in the uploaded file. Please try again by uploading a valid file. Otherwise, restart the data donation process by reloading the website.",
        "nl": f"Uw gebruikersnaam {username} is niet gevonden in het geüploade bestand. Probeer het opnieuw door een geldig bestand te uploaden. Start anders het gegevensdonatieproces opnieuw door de website opnieuw te laden."
    })
    ok = props.Translatable({
        "en": "Try again",
        "nl": "Probeer opnieuw"
    })
    cancel = props.Translatable({
        "en": "",
        "nl": ""
    })
    return props.PropsUIPromptConfirm(text, ok, cancel)


def confirm_username(platform):
    text = props.Translatable({
        "en": f"Confirm that you are X?",
        "nl": f"Confirm that you are X?"
    })
    ok = props.Translatable({
        "en": "No",
        "nl": "No"
    })
    cancel = props.Translatable({
        "en": "Yes",
        "nl": "Yes"
    })
    return props.PropsUIPromptConfirm(text, ok, cancel)

def prompt_file(platform,counter, extensions,donatedFileFlag):
    promptStringsSuccess = ['He, Je kunt nu je eerste WhatsApp chat met ons delen.',
   'Gelukt! Je hebt je eerste chat gedeeld. Tijd voor de tweede.',
   'Nice, de tweede is ook gelukt. Op naar de derde chat.',
   'Mooi, Die hebben we ook ontvangen. Nog twee chats te gaan. We verwachte nu je vierde chat',
   'Vierde chat is klaar! We zijn er bijna, maar nog niet helemaal. Je mag nu je laatste chat met ons delen.']

    # only valid from the second round.
    promptStringNoSuscess = ['Oops, in de vorige stap (bestand 1) is er geen (juist) bestand gedeeld. Wil je het opnieuw proberen?',
    'Oops, in de vorige stap (bestand 2) is er geen (juist) bestand gedeeld. Wil je het opnieuw proberen?',
    'Oops, in de vorige stap (bestand 3) is er geen (juist) bestand gedeeld. Wil je het opnieuw proberen?',
    'Oops, in de vorige stap (bestand 4) is er geen (juist) bestand gedeeld. Wil je het opnieuw proberen?']

    descriptionString = ''

    print('prompt_file counter: ', counter)
    print('prompt_file promptStrings: ', promptStringsSuccess[counter-1])
    print('prompt_file donatedFileFlag: ', donatedFileFlag)

    if(counter >=2 and donatedFileFlag[counter-2] == False):
        descriptionString = promptStringNoSuscess[counter-2]
    else:
        descriptionString = promptStringsSuccess[counter-1]


    description = props.Translatable({
        "en": f"Please follow the download instructions and choose the file that you stored on your device. Click “Skip” at the right bottom, if you do not have a {platform} file. ",
        "nl": descriptionString
    })

    return props.PropsUIPromptFileInput(description, extensions)



def prompt_consent(list_with_df_with_chats, username_partner):

    table_title = props.Translatable({
        "en": f"Chats die je naar {username_partner} hebt gestuurd",
        "nl": f"Chats die je naar {username_partner} hebt gestuurd",
    })

    table_list = [props.PropsUIPromptConsentFormTable(f"zip_content: {index}", table_title, df)
        for index, df in enumerate(list_with_df_with_chats)]

    return props.PropsUIPromptConsentForm(table_list, [])


def donate(key, json_string):
    return CommandSystemDonate(key, json_string)


def donate_logs(key):
    log_string = LOG_STREAM.getvalue()  # read the log stream

    if log_string:
        log_data = log_string.split("\n")
    else:
        log_data = ["no logs"]

    return donate(key, json.dumps(log_data))
