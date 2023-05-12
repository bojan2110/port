var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import React from 'react';
import TextBundle from '../../../../text_bundle';
import { Translator } from '../../../../translator';
import { PrimaryButton } from '../elements/button';
import { CheckBox } from '../elements/check_box';
import { Label, Title1 } from '../elements/text';
import LogoSvg from '../../../../../assets/images/logo.svg';
import { Footer } from './templates/footer';
import { Page } from './templates/page';
import { Bullet } from '../elements/bullet';
function prepareCopy(_a) {
    var locale = _a.locale;
    return {
        title: Translator.translate(title, locale),
        continueButton: Translator.translate(continueButton, locale),
        privacyLabel: Translator.translate(privacyLabel, locale)
    };
}
export var SplashScreen = function (props) {
    var _a = React.useState(false), checked = _a[0], setChecked = _a[1];
    var _b = React.useState(false), waiting = _b[0], setWaiting = _b[1];
    var _c = prepareCopy(props), title = _c.title, continueButton = _c.continueButton, privacyLabel = _c.privacyLabel;
    var locale = props.locale, resolve = props.resolve;
    function handleContinue() {
        if (checked && !waiting) {
            setWaiting(true);
            resolve === null || resolve === void 0 ? void 0 : resolve({ __type__: 'PayloadVoid', value: undefined });
        }
    }
    function handleCheck() {
        setChecked(true);
    }
    function renderDescription() {
        if (locale === 'nl')
            return nlDescription;
        return enDescription;
    }
    var enDescription = (_jsx(_Fragment, { children: _jsxs("div", __assign({ className: 'text-bodylarge font-body text-grey1' }, { children: [_jsx("div", __assign({ className: 'mb-4 text-bodylarge font-body text-grey1' }, { children: "You are about to start the process of donating your data to research institute ASCoR at Amsterdam University. The data that we ask you to donate will be used for academic research to gain insight into how social media platforms work." })), _jsx("div", __assign({ className: 'mb-4 text-bodylarge font-body text-grey1' }, { children: "We will walk you through this process step by step. During this process no data is stored or sent to ASCoR. You can delete rows from the data before donating. Data will only be donated and stored when you click the button \u201CYes, donate\u201D on the page that shows your data." })), _jsxs("div", __assign({ className: 'mb-6 text-bodylarge font-body text-grey1' }, { children: ["By clicking the button \u201C", _jsx("span", __assign({ className: 'font-bodybold' }, { children: "Yes, donate" })), "\u201D:"] })), _jsxs("div", __assign({ className: 'flex flex-col gap-3 mb-6' }, { children: [_jsx(Bullet, { children: _jsx("div", { children: "you fully and voluntarily agree to donate your data for this research." }) }), _jsx(Bullet, { children: _jsx("div", { children: "you are aware that when your data is used for academic publications, or made publicly available in some other form, this will be anonymous." }) }), _jsx(Bullet, { children: _jsx("div", { children: "you are aware that you have the right to withdraw your permission within 7 days by contacting Panel Inzicht." }) })] })), _jsx("div", __assign({ className: 'mb-10' }, { children: "This website keeps track of your activity - for example on which pages of this website you click - as part of this research. More information can be found on our privacy page." }))] })) }));
    var nlDescription = (_jsx(_Fragment, { children: _jsxs("div", __assign({ className: 'text-bodylarge font-body text-grey1' }, { children: [_jsx("div", __assign({ className: 'mb-4' }, { children: "Via deze website kun je veilig je sociale media gesprekken delen met de onderzoekers van de Erasmus Universiteit Rotterdam." })), _jsx("div", __assign({ className: 'mb-4' }, { children: "We leggen eerst stap voor stap wat er van je verwacht wordt. In de vragenlijst heb je aangegeven met welke mensen in je klas je het meest omgaat.  Daarin werd ook gevraagd om van deze mensen de WhatsApp chats te exporteren." })), _jsxs("div", __assign({ className: 'flex flex-col gap-3 mb-6' }, { children: [_jsx(Bullet, { children: _jsx("div", { children: "Aller eerst  selecteer je jouw naam. Het is belangrijk dat je je eigen naam selecteert zodat je niet per ongeluk de gegevens van iemand anders met ons deelt. " }) }), _jsx(Bullet, { children: _jsx("div", { children: "Vervolgens zie je de data zoals deze gedeeld zal worden, waarin informatie zoals namen verwijderd zijn. Hier kun je ook kiezen om berichten niet te delen met ons door ze te verwijderen. Ook kun je de zoekfunctie gebruiken om bepaalde berichten te zoeken en te verwijderen.  " }) }), _jsx(Bullet, { children: _jsx("div", { children: "Pas als je op de knop \"Versturen\" klikt, worden de gegevens verstuurd en opgeslagen. Door op de knop \u201CVersturen\u201D te klikken geef je aan goed ge\u00EFnformeerd te zijn over het onderzoek en vrijwillig je WhatsApp chats te delen. " }) })] }))] })) }));
    var footer = _jsx(Footer, {});
    var body = (_jsxs(_Fragment, { children: [_jsx("div", __assign({ className: 'flex justify-center' }, { children: _jsx("img", { src: LogoSvg, className: 'w-40 mb-10' }) })), _jsx(Title1, { text: title }), renderDescription(), _jsxs("div", __assign({ className: 'flex flex-col gap-8' }, { children: [_jsxs("div", __assign({ className: 'flex flex-row gap-4 items-center' }, { children: [_jsx(CheckBox, { id: '0', selected: checked, onSelect: function () { return handleCheck(); } }), _jsx(Label, { text: privacyLabel })] })), _jsx("div", __assign({ className: "flex flex-row gap-4 ".concat(checked ? '' : 'opacity-30') }, { children: _jsx(PrimaryButton, { label: continueButton, onClick: handleContinue, enabled: checked, spinning: waiting }) }))] }))] }));
    return (_jsx(Page, { body: body, footer: footer }));
};
var title = new TextBundle()
    .add('en', 'Welcome')
    .add('nl', 'Welkom');
var continueButton = new TextBundle()
    .add('en', 'Start')
    .add('nl', 'Start');
var privacyLabel = new TextBundle()
    .add('en', 'I have read and agree with the above terms.')
    .add('nl', 'Ik heb deze voorwaarden gelezen en ben hiermee akkoord.');
