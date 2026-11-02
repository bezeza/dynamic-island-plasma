"""Persistent user configuration for Dynamic Island.

The config lives in ``~/.config/dynamic-island/config.json``.  Unknown keys in
the file are preserved, missing keys fall back to :data:`DEFAULTS`.
"""

from __future__ import annotations

import json
import os
from typing import Any

from PySide6.QtCore import (
    QFileSystemWatcher,
    QObject,
    Property,
    QTimer,
    Signal,
    Slot,
)

CONFIG_DIR = os.path.join(
    os.environ.get("XDG_CONFIG_HOME") or os.path.expanduser("~/.config"),
    "dynamic-island",
)
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

DEFAULTS: dict[str, Any] = {
    # --- placement -----------------------------------------------------
    # Distance between the top screen edge and the island. 0 keeps it flush
    # with the edge: the body is drawn past the top of the screen so its upper
    # corners are cut off and the pill grows out of the bezel instead of
    # floating below it.
    "topMargin": 0,
    # "active" follows the screen with the pointer/focus, otherwise the
    # connector name of a specific output (e.g. "DP-1").
    "screen": "active",

    # --- geometry ------------------------------------------------------
    "position": "top-center",  # top-left, top-center, top-right
    "sideMargin": 24,
    # --- animation -----------------------------------------------------
    "animationStyle": "slide",  # slide, fade, zoom, spring
    "compactHeight": 40,
    "compactMinWidth": 160,
    "compactMaxWidth": 480,
    "expandedWidth": 600,
    "expandedRadius": 30,
    # Vertical room reserved for the surface. Anything taller than this is
    # scrolled inside the island.
    "maxHeight": 460,

    # --- behaviour -----------------------------------------------------
    # Fallback display time in ms when the sender does not request one.
    "defaultTimeout": 6000,
    "lowUrgencyTimeout": 4000,
    # Critical notifications never expire on their own.
    "criticalNeverExpires": True,
    # Hovering the island freezes its countdown.
    "pauseOnHover": True,
    # How many notifications stay stacked behind the front one.
    "stackDepth": 3,
    # Swipe distance in px before a drag dismisses the island.
    "dismissThreshold": 26,

    # --- look ----------------------------------------------------------
    # What the island is made of:
    #   "amoled"  true black, which is what it was designed around
    #   "dark"    a dark grey body, for panels where black smears or blooms
    #   "light"   dark type on white
    #   "system"  the desktop's own colour scheme
    "theme": "system",
    # Derive the accent glow from the notification icon/image.
    "accentFromIcon": True,
    "fallbackAccent": "#0A84FF",
    # 0 disables the coloured bloom behind the island entirely.
    "glowOpacity": 0.55,
    # Hairline border on the pill.
    "strokeOpacity": 0.10,
    "fontFamily": "",  # empty -> system default

    # --- history -------------------------------------------------------
    # How many past notifications the panel applet can show. 0 disables it.
    "historyLength": 100,

    # --- file operations -----------------------------------------------
    # Show copy/move/delete progress in the island, with pause and cancel.
    # False leaves those with Plasma's own progress display.
    "showJobs": True,

    # --- on-screen displays ---------------------------------------------
    # Volume, brightness and friends in the island instead of Plasma's grey
    # box. install.sh switches Plasma's own OSD off for this; setting this to
    # False and turning that back on gives it back.
    "showOsd": True,
    "osdTimeout": 2000,

    # --- media ----------------------------------------------------------
    # Show what starts playing, with previous/play/next. Listening only: the
    # Plasma media applet is untouched either way.
    "showMedia": True,
    # ...but not while the player's own window has the focus: whoever watches
    # the video or sits in Spotify sees the track change right there. The
    # banner is for music coming from somewhere in the back.
    "mediaHideWhenFocused": True,
    "mediaTimeout": 5000,

    # --- sound ---------------------------------------------------------
    # Play the sound-file / sound-name hints that applications send. Taking
    # the notification service over means taking this job over too.
    "soundEnabled": True,
    # XDG sound-theme event played when an app asks for no particular sound.
    # Empty keeps those notifications silent, which is what Plasma did.
    "defaultSound": "",

    # --- language ------------------------------------------------------
    # What the island's own handful of words are in: "auto" follows the
    # session, otherwise a tag from strings.py (en, de, zh, ja). The panel
    # applet is a KDE package and follows the desktop language instead — see
    # the README.
    "language": "auto",

    # --- sources -------------------------------------------------------
    # Everything that puts a card up without being an application: RSS and
    # Atom feeds, JSON endpoints polled on a timer, and a webhook server other
    # machines can push to. See dynamicisland/sources/__init__.py for the
    # shape of an entry; an empty list means the island only serves the bus.
    "sources": [],

    # --- filtering -----------------------------------------------------
    # desktop-entry / app-name values that are never shown.
    "blacklist": [],
    # Per-app overrides keyed by desktop-entry ID or namespaced fallback.
    # notifications=inherit|allow|mute|block; sound=inherit|on|off; timeout=ms.
    "applicationRules": {},
    "doNotDisturb": False,
    # Telegram-only smart filtering is opt-in to preserve existing behaviour.
    "telegramSmartFilter": False,
    # Case-insensitive substrings in a Telegram title/body to suppress.
    "telegramFilterKeywords": [],
    # Matching any of these keeps a Telegram notification visible and prevents
    # it from being merged into a duplicate card. Critical urgency always passes.
    "telegramImportantKeywords": [],
    # Merge identical Telegram notifications within this many seconds.
    "telegramDeduplicate": True,
    "telegramDeduplicateSeconds": 30,
}

_INT_LIMITS: dict[str, tuple[int, int]] = {
    "topMargin": (0, 500), "sideMargin": (0, 500),
    "compactHeight": (24, 120), "compactMinWidth": (80, 600),
    "compactMaxWidth": (100, 1000), "expandedWidth": (200, 1200),
    "expandedRadius": (0, 120), "maxHeight": (120, 1200),
    "defaultTimeout": (0, 120000), "lowUrgencyTimeout": (0, 120000),
    "stackDepth": (0, 20), "dismissThreshold": (4, 200),
    "historyLength": (0, 10000), "osdTimeout": (0, 60000),
    "mediaTimeout": (0, 120000), "telegramDeduplicateSeconds": (1, 600),
}
_FLOAT_LIMITS: dict[str, tuple[float, float]] = {
    "glowOpacity": (0.0, 1.0), "strokeOpacity": (0.0, 1.0),
}
_BOOL_KEYS = {
    "criticalNeverExpires", "pauseOnHover", "accentFromIcon", "showJobs",
    "showOsd", "showMedia", "mediaHideWhenFocused", "soundEnabled",
    "doNotDisturb", "telegramSmartFilter", "telegramDeduplicate",
}
_ALLOWED_VALUES = {
    "position": {"top-left", "top-center", "top-right"},
    "animationStyle": {"slide", "fade", "zoom", "spring"},
    "theme": {"amoled", "dark", "light", "system", "glass"},
}


def _bounded_number(value: Any, default: Any, lower: float, upper: float, integer: bool) -> Any:
    import math

    if isinstance(value, bool):
        value = default
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError):
        number = float(default)
    if not math.isfinite(number):
        number = float(default)
    number = min(upper, max(lower, number))
    return int(number) if integer else number


def normalise_config(values: dict[str, Any]) -> dict[str, Any]:
    """Validate known settings while preserving forward-compatible unknown keys."""
    result = dict(values)
    for key, (lower, upper) in _INT_LIMITS.items():
        result[key] = _bounded_number(result.get(key, DEFAULTS[key]), DEFAULTS[key], lower, upper, True)
    for key, (lower, upper) in _FLOAT_LIMITS.items():
        result[key] = _bounded_number(result.get(key, DEFAULTS[key]), DEFAULTS[key], lower, upper, False)
    for key in _BOOL_KEYS:
        if not isinstance(result.get(key), bool):
            result[key] = DEFAULTS[key]
    for key, allowed in _ALLOWED_VALUES.items():
        if result.get(key) not in allowed:
            result[key] = DEFAULTS[key]
    result["compactMaxWidth"] = max(result["compactMinWidth"], result["compactMaxWidth"])
    result["expandedWidth"] = max(result["compactMinWidth"], result["expandedWidth"])

    for key in ("screen", "language", "fontFamily", "defaultSound"):
        if not isinstance(result.get(key), str):
            result[key] = DEFAULTS[key]
    import re
    accent = result.get("fallbackAccent")
    if not isinstance(accent, str) or not re.fullmatch(r"#[0-9A-Fa-f]{6}", accent):
        result["fallbackAccent"] = DEFAULTS["fallbackAccent"]

    for key in ("blacklist", "telegramFilterKeywords", "telegramImportantKeywords"):
        value = result.get(key)
        if not isinstance(value, list):
            result[key] = list(DEFAULTS[key])
        else:
            result[key] = [str(item) for item in value if isinstance(item, (str, int, float))]
    if not isinstance(result.get("sources"), list):
        result["sources"] = []
    else:
        result["sources"] = [item for item in result["sources"] if isinstance(item, dict)]

    rules = result.get("applicationRules")
    clean_rules: dict[str, dict[str, Any]] = {}
    if isinstance(rules, dict):
        for app_id, raw_rule in rules.items():
            if not isinstance(app_id, str) or not isinstance(raw_rule, dict):
                continue
            rule = dict(raw_rule)
            if rule.get("notifications") not in ("inherit", "allow", "mute", "block"):
                rule.pop("notifications", None)
            if rule.get("sound") not in ("inherit", "on", "off"):
                rule.pop("sound", None)
            if "timeout" in rule:
                timeout = _bounded_number(rule["timeout"], 0, 0, 60000, True)
                if timeout <= 0:
                    rule.pop("timeout", None)
                else:
                    rule["timeout"] = max(1000, timeout)
            if rule:
                clean_rules[app_id] = rule
    result["applicationRules"] = clean_rules
    return result


class Config(QObject):
    """Live configuration object, exposed to QML as ``Cfg``."""

    changed = Signal()

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._data: dict[str, Any] = dict(DEFAULTS)
        self.load()

        # The file is also edited by hand and by the applet's settings pages,
        # so it is watched rather than read once. The directory is watched too:
        # a write replaces the file, and the inode the watcher was holding is
        # gone the moment it does.
        self._watcher = QFileSystemWatcher(self)
        # On a first run neither the directory nor the file is there yet, and
        # addPath on a path that does not exist quietly registers nothing —
        # with no directory watch, nothing ever fires to re-arm it either, so
        # the whole session would ignore hand edits. Make the directory first;
        # save() would create it moments later anyway.
        try:
            os.makedirs(CONFIG_DIR, exist_ok=True)
        except OSError as failure:
            print(f"[dynamic-island] cannot make {CONFIG_DIR}: {failure}")
        if os.path.isdir(CONFIG_DIR):
            self._watcher.addPath(CONFIG_DIR)
        if os.path.exists(CONFIG_PATH):
            self._watcher.addPath(CONFIG_PATH)
        # A save is several file events in a row; one reload is enough.
        self._settle = QTimer(self)
        self._settle.setSingleShot(True)
        self._settle.setInterval(150)
        self._settle.timeout.connect(self._reread)
        self._watcher.fileChanged.connect(lambda _: self._settle.start())
        self._watcher.directoryChanged.connect(lambda _: self._settle.start())

    def _reread(self) -> None:
        """Pick up a change somebody else made to the file."""
        if os.path.exists(CONFIG_PATH) and CONFIG_PATH not in self._watcher.files():
            self._watcher.addPath(CONFIG_PATH)
        self.load()

    # ------------------------------------------------------------------
    def load(self) -> None:
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as fh:
                stored = json.load(fh)
            if isinstance(stored, dict):
                self._data = normalise_config({**DEFAULTS, **stored})
        except FileNotFoundError:
            pass
        except (OSError, ValueError) as exc:
            print(f"[dynamic-island] ignoring broken config: {exc}")
        self.changed.emit()

    def save(self) -> None:
        # Reached from the settings dialog over D-Bus and from QML, neither of
        # which is a place for an exception about a full disk to surface: a
        # setting that cannot be written is worth a line on stderr, not a dead
        # notification service.
        tmp = CONFIG_PATH + ".tmp"
        try:
            os.makedirs(CONFIG_DIR, exist_ok=True)
            # A webhook token may be in here, and ~/.config is world-readable
            # on most systems. The file is written for its owner and nobody
            # else — set before anything is in it, not after.
            handle = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
            with os.fdopen(handle, "w", encoding="utf-8") as fh:
                json.dump(self._data, fh, indent=2, sort_keys=True)
                fh.write("\n")
            os.replace(tmp, CONFIG_PATH)
        except (OSError, TypeError, ValueError) as failure:
            print(f"[dynamic-island] cannot write {CONFIG_PATH}: {failure}")
            try:
                os.unlink(tmp)
            except OSError:
                pass
            return
        try:
            os.chmod(CONFIG_PATH, 0o600)  # for files written before this rule
        except OSError:
            pass

    # ------------------------------------------------------------------
    @Slot(str, result="QVariant")
    def get(self, key: str) -> Any:
        return self._data.get(key, DEFAULTS.get(key))

    @Slot(str, "QVariant")
    def set(self, key: str, value: Any) -> None:
        updated = normalise_config({**self._data, key: value})
        if updated == self._data:
            return
        self._data = updated
        self.save()
        self.changed.emit()

    def merge(self, values: dict[str, Any]) -> bool:
        """Take a whole batch of keys at once.

        This is what the panel applet's settings pages call over D-Bus: they
        edit the island's configuration, not the widget's, and the island is
        the one process that owns the file.
        """
        updated = normalise_config({**self._data, **values})
        changes = {
            key: value for key, value in updated.items()
            if self._data.get(key) != value
        }
        if not changes:
            return False
        self._data = updated
        self.save()
        self.changed.emit()
        return True

    def as_json(self) -> str:
        return json.dumps(self._data, indent=2, sort_keys=True)

    def _values(self) -> dict[str, Any]:
        return dict(self._data)

    # A single map property keeps the QML side declarative: Cfg.values.topMargin
    values = Property("QVariantMap", _values, notify=changed)
