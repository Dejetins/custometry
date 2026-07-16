import i18n from "i18next";
import { initReactI18next } from "react-i18next";

import { foundationCatalogs, routeTitleCatalogs } from "@custometry/localization";

const storedLanguage = window.localStorage.getItem("custometry-language");
const language = storedLanguage === "ru" ? "ru" : "en";

void i18n.use(initReactI18next).init({
  resources: {
    en: { foundation: foundationCatalogs.en, routeTitles: routeTitleCatalogs.en },
    ru: { foundation: foundationCatalogs.ru, routeTitles: routeTitleCatalogs.ru },
  },
  lng: language,
  fallbackLng: "en",
  defaultNS: "foundation",
  interpolation: { escapeValue: false },
});

export default i18n;
