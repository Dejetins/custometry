import enFoundation from "../locales/en/foundation.json";
import enRouteTitles from "../locales/en/route-titles.json";
import ruFoundation from "../locales/ru/foundation.json";
import ruRouteTitles from "../locales/ru/route-titles.json";

export const supportedLanguages = ["en", "ru"] as const;
export type SupportedLanguage = (typeof supportedLanguages)[number];

export const foundationCatalogs = {
  en: enFoundation,
  ru: ruFoundation,
} as const;

export const routeTitleCatalogs = {
  en: enRouteTitles,
  ru: ruRouteTitles,
} as const;
