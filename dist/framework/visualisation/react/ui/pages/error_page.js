import { jsx as _jsx, Fragment as _Fragment, jsxs as _jsxs } from "react/jsx-runtime";
import { Footer } from './templates/footer';
// import LogoSvg from '../../../../../assets/images/logo.svg'
import { Page } from './templates/page';
import TextBundle from '../../../../text_bundle';
import { Translator } from '../../../../translator';
import { BodyLarge, Title1 } from '../elements/text';
export var ErrorPage = function (props) {
    // render to top of the page on reload
    window.scrollTo(0, 0);
    var stacktrace = props.stacktrace;
    var _a = prepareCopy(props), title = _a.title, text = _a.text;
    var footer = _jsx(Footer, {});
    var body = (_jsxs(_Fragment, { children: [_jsx(Title1, { text: title }), _jsx(BodyLarge, { text: text }), _jsx(BodyLarge, { text: stacktrace })] }));
    return (_jsx(Page, { body: body, footer: footer }));
};
function prepareCopy(_a) {
    var locale = _a.locale;
    return {
        title: Translator.translate(title, locale),
        text: Translator.translate(text, locale)
    };
}
var title = new TextBundle()
    .add('en', 'Error, not your fault!')
    .add('nl', 'Foutje, niet jouw schuld!');
var text = new TextBundle()
    .add('en', 'Consult the researcher, or close the page')
    .add('nl', 'Raadpleeg de onderzoeker of sluit de pagina');
