#!/usr/bin/env python3
"""Run canonical Playwright CLI QA for the current G4 r6 auth review board."""

from __future__ import annotations

import run_g4_auth_r5_board_qa as qa


qa.ART = qa.DIR / "artifacts/g4-r6/family-auth-shell-auth-baseline-exception-auth"
qa.EVID = qa.DIR / "evidence/g4-r6/family-auth-shell-auth-baseline-exception-auth"
qa.BOARD = qa.ART / "review-board.html"
qa.TARGET = qa.ART / "screens/auth-family.html"
qa.OUTPUT = qa.EVID / "browser-board-qa.json"
qa.WINDOW_BASELINE = (
    qa.DIR
    / "evidence/g4-r5/family-auth-shell-auth-baseline-exception-auth/window-geometry-before-r5-03.json"
)
qa.SESSION = "g4-auth-r6-board-qa"
qa.SCREENSHOT_DEFAULT = qa.EVID / "review-board-1440.png"
qa.SCREENSHOT_RECOVERY = qa.EVID / "review-board-recovery-validation-error-1440.png"
qa.SCREENSHOT_EN = qa.EVID / "review-board-sign-in-en-1440.png"
qa.REVISION_TAG = "r6"
qa.STAGE_ID = "G4@family.auth.shell-auth.baseline-exception-auth-r6"


if __name__ == "__main__":
    raise SystemExit(qa.main())
