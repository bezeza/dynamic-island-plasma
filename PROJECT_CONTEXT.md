# Dynamic Island Plasma — Project Context & Roadmap

> **This file is the canonical hand-off brief for maintainers and AI coding agents.**
> Read it before proposing changes, editing code, opening issues, or asking the maintainer to repeat project requirements.
> Keep it up to date whenever scope, architecture, priorities, or implementation status changes.

- Repository: https://github.com/bezeza/dynamic-island-plasma
- Product name: **Dynamic Island Plasma**
- Target desktop: KDE Plasma 6
- Primary platform: Linux, Wayland (Fedora KDE is the maintainer's current test environment)
- Current project direction: a customizable notification surface and notification-control centre for KDE Plasma, inspired by the interaction quality of macOS Dynamic Island / Liquid Glass, while remaining native to KDE.

## 1. Product vision

Build a polished, reliable, configurable notification experience for KDE Plasma 6. This is not just a translated fork, a theme, or a decorative animation. It should become a complete user-facing product that lets people control how notifications from each application are received, filtered, grouped, presented, sounded, and dismissed.

The central UI is the Dynamic Island surface: a compact capsule that expands into notification cards and contextual controls. A companion settings interface should expose the important behaviours without requiring users to edit JSON or restart the desktop.

The product must:
- feel smooth, responsive, accessible, and visually coherent;
- integrate with KDE/Wayland rather than imitate macOS at the cost of Linux desktop conventions;
- let users control notifications **per application** as well as globally;
- provide meaningful animation and appearance choices;
- be safe and reversible, especially because it may own the desktop notification D-Bus service;
- be maintainable, tested, documented, and packageable for multiple distributions.

## 2. Non-negotiable requirements

1. **Per-application control is a core feature, not a nice-to-have.**
2. Global settings and per-app overrides must coexist. A per-app override must not silently change global settings.
3. The user must be able to restore normal Plasma notifications and recover if Dynamic Island crashes or is uninstalled.
4. Do not claim an animation, blur effect, or setting works until it is implemented and tested on a real Plasma 6 Wayland session.
5. Do not break existing features while adding settings: file-operation progress, OSD, media controls, sounds, history, sources, Telegram filtering, DND, and localization.
6. Preserve user configuration across upgrades. New settings need safe defaults and old/unknown config keys should not be discarded.
7. All user-visible strings must be translatable. Do not hard-code English UI labels in QML or Python except for proper names and language self-names.
8. Do not merge experimental changes into `main` until automated checks and manual smoke tests pass.

## 3. User experience and feature requirements

### 3.1 Application manager — highest priority

Add a dedicated **Applications** page in the settings UI. Discover applications from installed desktop entries and/or applications that have sent notifications. Show a searchable list with each application's icon, display name, desktop-entry ID / notification app name, and current policy.

For each application, support:
- Notifications: Allow / Mute / Block.
- Presentation: Show in Dynamic Island / use standard Plasma notification if supported / hide banner but keep in history.
- Sound: inherit global / on / off; optionally choose a sound.
- Urgency or priority: inherit / low / normal / high, without overriding genuinely critical system messages.
- Display duration: inherit global / custom duration.
- Grouping: inherit / group repeated notifications / show separately.
- Quiet hours: inherit global / custom schedule or mute during DND.
- Appearance: inherit / application accent colour / custom accent (only if technically practical).
- Privacy: hide message body or sensitive preview on lock screen where the platform exposes reliable lock-state information.
- Reset this application's settings to global defaults.

Also provide:
- Search and filters (all, allowed, muted, blocked, recently active).
- Bulk actions: allow all, mute selected, block selected, reset overrides.
- A clear indicator showing whether a value is inherited or explicitly overridden.
- A safe default for unknown/new applications.
- A way to add an app manually by desktop-entry ID when discovery is incomplete.

**Policy precedence must be documented and deterministic.** Recommended order:
1. Critical/system safety handling and hard platform constraints.
2. Explicit global Do Not Disturb rules, with user-configured exceptions.
3. Explicit per-app block/mute/allow policy.
4. Per-app presentation/sound/duration/grouping overrides.
5. Global defaults.

Do not silently swallow critical notifications. Make exceptions understandable and user-configurable where safe.

### 3.2 Global notification controls

Provide global controls for:
- Enable/disable Dynamic Island handling.
- Default notification policy and fallback behaviour.
- Do Not Disturb toggle and schedules.
- Exceptions for selected applications and critical notifications.
- Default sound behaviour and volume where the notification protocol permits it.
- Default display duration, low-urgency duration, critical-notification behaviour.
- Pause countdown on hover, stack depth, dismiss gesture and dismissal timeout.
- History length, clear history, search and application filters.
- Whether notification bodies are stored in history; provide privacy-conscious defaults.

### 3.3 Animation Studio

Provide an isolated animation settings page that affects Dynamic Island notifications only, not KWin window animations or unrelated desktop effects.

Initial styles:
- Slide — move in/out from the selected screen edge/anchor.
- Fade — opacity transition.
- Zoom — scale and opacity transition.
- Spring — restrained spring/overshoot transition.

Controls:
- Entry and exit style (allow separate choices if architecture permits).
- Duration/speed.
- Distance/offset for slide.
- Starting scale for zoom.
- Spring damping/overshoot only if stable and understandable.
- Reduced-motion option; disable or simplify motion.
- Live preview / test notification button.
- Reset to defaults.

Future/experimental:
- Genie / Magic Lamp-like morph. Treat as a separate advanced effect; do not label a basic scale animation as Genie.
- Per-notification-type animation only if it remains understandable and performant.

### 3.4 Appearance / Liquid Glass Studio

Offer presets such as:
- Liquid Glass / macOS-inspired translucent surface.
- Dark.
- Light.
- AMOLED.
- Follow system.

Expose supported controls:
- Opacity/transparency.
- Background blur only where the Wayland compositor / Qt layer-shell path actually supports it.
- Corner radius.
- Border/stroke opacity.
- Shadow/glow intensity and accent colour.
- Typography and compact/expanded dimensions.
- High-contrast mode and readable text contrast.

Important: translucent colour is not the same as true background blur. Label controls accurately and show a fallback when blur is unavailable.

### 3.5 Notification surface and interaction

- Compact capsule and expanded notification cards.
- Stacking and grouping of repeated notifications.
- Clear, predictable dismissal and timeout behaviour.
- Notification actions and inline replies where the sender supports them.
- Progress cards for file operations with pause/resume/cancel where the underlying operation supports those actions.
- Media card with album art and play/pause/previous/next using standard Linux media interfaces.
- Volume/brightness and other OSD integrations must be optional and reversible.
- Multi-monitor placement: active screen, selected screen, and sensible behaviour when displays are added/removed.
- Respect screen edges, panels, reserved areas, scaling, and HiDPI.
- Keyboard navigation, screen-reader labels, focus handling, and reduced-motion support.

### 3.6 Notification centre and history

- Search notifications.
- Filter by application and time.
- Group repeated messages.
- Mark read/unread if supported by the data model.
- Clear one, clear selected, clear all.
- Configurable history retention and privacy.
- Avoid storing more sensitive notification content than necessary.

### 3.7 Other integrations

Keep these optional and independently configurable:
- File-operation progress.
- Media playback controls.
- Volume/brightness/OSD.
- RSS/Atom feeds, JSON sources, and webhooks.
- Telegram smart filtering and duplicate merging.

Do not let optional integrations destabilize core desktop notifications.

## 4. Localization

The application must support:
- Ukrainian (`uk`)
- Russian (`ru`)
- English (`en`)
- Existing project languages where they are already supported (inspect current catalogs before changing them).
- Automatic language selection from the desktop/session, with a manual override.

Requirements:
- Translate the main application UI, settings, applet, tooltips, accessibility labels, errors, and notifications generated by Dynamic Island.
- Keep language names in their native form (Українська, Русский, English, etc.).
- Maintain the translation template and extraction/build scripts.
- Do not overwrite an existing translation with machine-translated or unrelated text without review.
- Add a short translator guide and document how to regenerate catalogs.
- Verify plural forms and UTF-8 encoding.

## 5. Architecture and engineering principles

Before implementing a feature, inspect the actual current code and reuse existing abstractions. Avoid parallel settings stores or duplicate notification managers.

Recommended separation:
- Notification D-Bus service / protocol handling.
- Notification model, IDs, actions, urgency and lifecycle.
- Per-application policy resolver.
- Global and per-app configuration persistence/migration.
- Presentation layer (QML).
- Animation controller.
- Appearance/theme controller.
- History store.
- Optional integrations (media, OSD, file jobs, external sources).
- Settings UI and preview/test harness.

Configuration:
- Preserve the existing config location and compatibility unless a migration is justified.
- Add a schema/version and migration path before making incompatible changes.
- Validate all values and clamp numeric settings to safe ranges.
- Use atomic writes and restrictive permissions for files containing tokens or notification content.
- Preserve unknown keys where possible.
- Avoid shelling out for settings that have a supported API.

D-Bus / desktop integration:
- Follow freedesktop notification specifications and KDE-specific behaviour where applicable.
- Handle ownership conflicts, service restart, sender disappearance, action callbacks, replacement IDs, hints, urgency, timeout semantics and sound hints.
- Do not lose notifications during startup/restart if there is a safe fallback.
- Keep an explicit, documented rollback/uninstall path to restore Plasma's standard notification service and any OSD settings changed by installation.

Wayland:
- Do not assume X11 APIs or global window positioning are available.
- Test layer-shell positioning and multi-monitor behaviour under Plasma Wayland.
- Handle compositor limitations gracefully.
- Do not promise arbitrary blur if the relevant Wayland protocol/compositor path does not provide it.

Performance and reliability:
- Avoid busy loops and unnecessary polling.
- Bound history and image/cache sizes.
- Handle malformed notification payloads.
- Ensure one misbehaving app cannot crash the notification service.
- Log useful diagnostics without logging private notification bodies by default.

## 6. Accessibility, privacy and safety

- Reduced-motion option and respect system accessibility preferences where possible.
- Keyboard-operable settings and notification actions.
- Readable contrast in every theme.
- Do not expose notification bodies in debug logs.
- Store as little notification content as possible and make retention configurable.
- Protect webhook/source tokens and config files with restrictive permissions.
- Do not create a network listener by default; webhook functionality must be opt-in, authenticated, and documented.
- Make notification capture/ownership clear to the user.
- Provide an emergency switch to return to standard Plasma notifications.

## 7. Packaging and distribution

Target:
1. Fedora KDE (maintainer's current environment).
2. Arch Linux.
3. openSUSE.
4. Other Plasma 6 distributions where dependencies are available.

Deliverables:
- Reproducible install/uninstall scripts.
- Fedora RPM spec/package and repository guidance.
- Arch PKGBUILD.
- openSUSE packaging guidance.
- KDE Discover integration through appropriate package metadata/repositories; do not imply Discover can install arbitrary GitHub source directly.
- Dependency/version matrix for Plasma, Qt, KDE Frameworks and layer-shell components.
- Upgrade and rollback instructions.
- Optional Flatpak only if the D-Bus notification ownership and required desktop integration can work within its permissions model.

## 8. Testing and release gates

Automated checks:
- Python lint/type/syntax checks.
- QML lint/compile checks using the project's supported Qt/KDE toolchain.
- Translation catalog validation and placeholder consistency.
- Config schema/default/migration tests.
- Unit tests for app policy precedence, DND, timeout, grouping and notification replacement.
- D-Bus protocol tests with fake notification senders.
- Packaging/install/uninstall checks.

Manual test matrix:
- Fedora KDE Plasma 6 Wayland (primary).
- At least one other Plasma 6 distribution.
- Single and multiple monitors.
- Mixed scaling / HiDPI.
- Light and dark themes.
- High notification volume.
- Sender with actions and inline replies.
- Sender requesting sound and custom timeout.
- Critical and low-urgency notifications.
- DND and per-app exceptions.
- Service crash/restart and rollback to stock Plasma.
- Accessibility/reduced-motion.

A feature is **Done** only when:
- settings persist and survive restart;
- UI and behaviour match;
- translations are present;
- automated tests pass;
- manual test notes are recorded;
- documentation is updated;
- rollback remains possible.

## 9. Prioritized roadmap

### P0 — Stabilize the current foundation
- Review the current feature branch and open PRs.
- Run CI, Python checks, QML checks and translation validation.
- Fix regressions before adding more features.
- Confirm current supported Plasma/Qt/KF versions and dependencies.
- Document install, uninstall and recovery steps.

### P1 — Per-application notification manager
- Discover and list applications.
- Build searchable application settings page.
- Implement allow/mute/block and presentation modes.
- Add per-app sound, duration, grouping and priority overrides.
- Implement deterministic policy precedence and tests.
- Add bulk actions and reset-to-inherit.

### P2 — Localization and configuration foundation
- Complete Ukrainian and Russian catalogs.
- Confirm English fallback and auto language selection.
- Add config schema versioning and migrations.
- Ensure every settings label and error is translated.

### P3 — Animation Studio
- Finish Slide/Fade/Zoom/Spring semantics.
- Add duration/speed and reduced motion.
- Add live preview/test notification.
- Add screen-edge/anchor-aware movement.
- Research Genie as a genuinely distinct effect.

### P4 — Appearance Studio
- Liquid Glass preset and opacity controls.
- Blur capability detection/fallback.
- Radius, border, shadow/glow, accent and typography controls.
- High contrast and readability checks.

### P5 — Notification centre and integrations
- History search/filter/retention.
- Grouping and bulk clear.
- Improve media, OSD and file-operation cards.
- Keep external feeds/webhooks optional and secure.

### P6 — Multi-monitor, accessibility and robustness
- Multi-display and HiDPI testing.
- Keyboard/screen-reader support.
- Reduced motion.
- Stress, restart, crash recovery and D-Bus edge cases.

### P7 — Distribution and release
- Fedora RPM first.
- Arch and openSUSE packages.
- Discover distribution path.
- Versioning, changelog, release notes and support policy.

## 10. Current implementation notes (verify before relying on them)

The codebase has previously included configuration keys/features for:
- global Do Not Disturb;
- a global application blacklist;
- Telegram-specific smart filtering, keyword filters and deduplication;
- default/low-urgency/OSD/media timeouts;
- pause-on-hover and critical-notification timeout behaviour;
- history length and stack depth;
- file-operation progress, OSD, media and sound toggles;
- external sources.

These are not equivalent to a full per-application manager. The current UI has a global blacklist text area, not the requested per-app policy editor.

An experimental branch has been used for notification animation, placement, Liquid Glass palette, and localization work:
- Branch: `feature/notification-animation-studio`
- Draft PR: https://github.com/bezeza/dynamic-island-plasma/pull/4

Treat that work as **experimental and unverified** until CI and manual Fedora KDE Wayland testing pass. Inspect the live branch and PR before continuing; do not assume the description here proves code correctness or that the PR is merged.

## 11. Instructions for any AI assistant or contributor

When continuing this project:

1. Read this file first, then read `CONTRIBUTING_AI.md` and `TASKS.md`, followed by the current README, open issues/PRs, and relevant source files.
2. Inspect the current default branch and working branch heads. Never assume branch names or commit SHAs in this document are still current.
3. Identify what is already implemented in code versus merely planned here.
4. Do not ask the maintainer to repeat the product vision, target platform, language goals, or per-app control requirement; they are recorded above.
5. Ask a question only if a genuinely blocking product decision is missing. Otherwise make a conservative, documented choice.
6. Work in a feature branch; do not force-push or rewrite user history.
7. Keep changes small and coherent. Run relevant tests and report exactly what passed, failed, or could not be run.
8. Update this file when priorities, status, architecture or supported platforms change.
9. Never claim that a PR is merged, tests pass, a package installs, or a feature works unless verified.
10. In the final hand-off, list changed files, branch/PR, tests run, known limitations, and the next recommended task.

## 12. Current coordination documents

- `CONTRIBUTING_AI.md` — mandatory workflow and engineering rules for every human and AI contributor.
- `TASKS.md` — task IDs, priorities, owners, dependencies, and the live PR dependency chain. Always verify it against GitHub before starting work.
- `.github/pull_request_template.md` — required implementation and test hand-off.
- `.github/ISSUE_TEMPLATE/` — feature and bug-report templates.

The first per-application manager implementation is in draft PR #5. Do not recreate its existing application discovery, allow/mute/block, sound, timeout, or settings-page work. First review and validate that implementation, then continue with the remaining per-app presentation, priority, grouping, filters, bulk actions, and manual-entry requirements listed in `TASKS.md` and section 3.1 above.
