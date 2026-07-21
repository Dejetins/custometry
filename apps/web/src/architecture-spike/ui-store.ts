import {
  defaultUiThemeId,
  isThemeId,
  type ThemeId,
} from "@custometry/ui-foundation";
import { makeAutoObservable } from "mobx";

export const sidebarGeometry = {
  minimum: 208,
  maximum: 320,
  default: 240,
  step: 8,
} as const;

const themeStorageKey = "custometry-spike-theme";
const sidebarStorageKey = "custometry-spike-sidebar-width";

function clampSidebarWidth(width: number): number {
  return Math.min(sidebarGeometry.maximum, Math.max(sidebarGeometry.minimum, width));
}

export class SpikeUiStore {
  public themeId: ThemeId;
  public sidebarWidth: number;

  public constructor(private readonly storage?: Pick<Storage, "getItem" | "setItem">) {
    const storedTheme = storage?.getItem(themeStorageKey) ?? null;
    const storedWidth = Number(storage?.getItem(sidebarStorageKey));
    this.themeId = isThemeId(storedTheme) ? storedTheme : defaultUiThemeId;
    this.sidebarWidth = Number.isFinite(storedWidth) && storedWidth > 0
      ? clampSidebarWidth(storedWidth)
      : sidebarGeometry.default;
    makeAutoObservable(this, {}, { autoBind: true });
  }

  public setTheme(themeId: ThemeId): void {
    this.themeId = themeId;
    this.storage?.setItem(themeStorageKey, themeId);
  }

  public setSidebarWidth(width: number): void {
    this.sidebarWidth = clampSidebarWidth(Math.round(width));
    this.storage?.setItem(sidebarStorageKey, String(this.sidebarWidth));
  }

  public stepSidebar(direction: -1 | 1): void {
    this.setSidebarWidth(this.sidebarWidth + direction * sidebarGeometry.step);
  }

  public resetSidebar(): void {
    this.setSidebarWidth(sidebarGeometry.default);
  }
}
