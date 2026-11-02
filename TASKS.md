# Project Tasks

> Live status must be checked against GitHub Issues, branches, PRs, and CI before work starts. This file is a coordination index, not proof that code works or has merged.

Repository: https://github.com/bezeza/dynamic-island-plasma

## Working agreements

- Every substantial task has a stable ID: `DI-###`.
- One implementation owner per task at a time.
- Use a dedicated branch and PR; never commit directly to `main`.
- Check `CONTRIBUTING_AI.md` and `PROJECT_CONTEXT.md` before work.
- Update this file when ownership, status, priority, or dependencies change.
- "Implemented in PR" does not mean merged, tested, or released.

## Task ID allocation

- **Next free ID: DI-013.** Canonical feature numbering was confirmed by the maintainer on 2026-11-02. IDs are reserved in this registry; check it before assigning the next one.
- IDs are permanent and never reused. Cancelled tasks remain listed with status `Cancelled`.
- New PR titles use `[DI-###]`; commit subjects use `DI-###: `. Existing PRs #1–#5 keep their existing names because they predate the convention. PR #6 is the workflow task and uses `[DI-011]`.

## Status definitions

- **Backlog** — not started.
- **Ready** — requirements and dependencies are clear.
- **In progress** — an owner is actively implementing.
- **Review** — PR is open and awaiting review.
- **Blocked** — waiting on a dependency or decision.
- **Done** — merged and required validation completed.

## Current PR dependency chain (verified 2026-11-02)

The following open PRs are stacked. Their base branches matter: do not retarget or merge them independently without checking the dependency chain.

| PR | Scope | Head branch | Base branch | Status |
|---|---|---|---|---|
| — | Russian localization foundation (existing branch; no PR in this stack) | `russian-localization` | `main` | Branch dependency |
| [#1](https://github.com/bezeza/dynamic-island-plasma/pull/1) | Searchable notification history | `feature-searchable-history` | `russian-localization` | Open |
| [#2](https://github.com/bezeza/dynamic-island-plasma/pull/2) | Telegram smart filtering | `feature-telegram-smart-filter` | `feature-searchable-history` | Open |
| [#3](https://github.com/bezeza/dynamic-island-plasma/pull/3) | System-adaptive style | `feature-system-adaptive-style` | `feature-telegram-smart-filter` | Open |
| [#4](https://github.com/bezeza/dynamic-island-plasma/pull/4) | Notification animation and appearance settings | `feature/notification-animation-studio` | `feature-system-adaptive-style` | Draft |
| [#5](https://github.com/bezeza/dynamic-island-plasma/pull/5) | Per-application notification manager | `feature/per-application-manager` | `feature/notification-animation-studio` | Draft |

No PR above is represented as merged by this file. Re-check GitHub for current state before acting.

## Product roadmap

| ID | Priority | Task | Status | Owner | Files / components likely touched | Dependency / next action |
|---|---|---|---|---|---|---|
| DI-001 | P0 | Application Manager — per-app discovery, notification policies, sound and timeout overrides, searchable settings | Review | Maintainer | `src/dynamicisland/apps.py`, `controller.py`, `config.py`, `applet/.../ConfigApplications.qml`, tests | PR #5; validate current implementation, policy precedence, persistence and Fedora Plasma 6 Wayland behaviour |
| DI-002 | P0 | Notification Animation Studio — global animation and appearance controls | Review | Maintainer | presentation/animation code, QML settings, tests | PR #4; validate real transitions, preview, reduced motion, edge-aware Slide and Plasma Wayland |
| DI-003 | P1 | Per-App Animation — choose animation and presentation per application | Backlog | Unassigned | animation controller, `applet/.../ConfigApplications.qml`, animation settings | Depends on PR #4 and PR #5; avoid duplicate config keys and coordinate shared QML files |
| DI-004 | P1 | Notification History — searchable history, filtering, retention and privacy | Review | Maintainer | history model/store, `applet/.../History*`, history settings | PR #1; validate storage, search, retention and privacy |
| DI-005 | P1 | Language Manager — language selector and automatic language detection | Backlog | Unassigned | `applet/.../translate/`, locale/config handling, translation scripts | Audit current catalogs and translation tooling first |
| DI-006 | P1 | Per-App Profiles — named profiles/presets for application notification behaviour | Backlog | Unassigned | `src/dynamicisland/config.py`, application rules, `ConfigApplications.qml`, import/export | Depends on DI-001; define profile schema and precedence before implementation |
| DI-007 | P2 | Appearance / Liquid Glass Studio and compositor capability fallback | Backlog | Unassigned | presentation code, QML theme/components, capability detection | Depends on supported Plasma/Qt/Wayland rendering path |
| DI-008 | P2 | Packaging, install/uninstall, rollback and emergency recovery | Backlog | Unassigned | `tools/install.sh`, `tools/uninstall.sh`, packaging metadata, docs | Fedora first; document restoring standard Plasma notification service |
| DI-009 | P2 | Multi-monitor, HiDPI, accessibility, keyboard and reduced-motion audit | Backlog | Unassigned | QML surfaces, placement, focus/accessibility, tests | Test on real Plasma 6 Wayland session |
| DI-010 | P2 | CI expansion: QML lint/compile, D-Bus protocol tests, config migration tests | Ready | Unassigned | `.github/workflows/check.yml`, `pyproject.toml`, tests | Extend existing workflow after checking available toolchain |
| DI-011 | P0 | Shared AI/human contributor workflow and task tracking | Review | Maintainer | `CONTRIBUTING_AI.md`, `TASKS.md`, `.github/ISSUE_TEMPLATE/`, `.github/pull_request_template.md`, README | PR #6; review and merge workflow docs into main |
| DI-012 | P0 | Stabilize and integrate the existing stacked PR series | Ready | Maintainer | `src/`, `applet/`, `tools/`, `.github/workflows/` | Check PR dependency order; resolve CI, conflicts and runtime validation before merges |

## Agent assignment log

When an agent starts a task, add a row with its name/tool, task ID, branch, date, and scope. Remove or close the assignment when the PR is merged or the task is stopped.

| Agent / contributor | Task ID | Branch / PR | Scope | Started | Status |
|---|---|---|---|---|---|
| Maintainer + ChatGPT | DI-011 | [PR #6](https://github.com/bezeza/dynamic-island-plasma/pull/6) — `docs/ai-contributor-workflow` | Contributor rules, task registry, issue/PR templates | 2026-11-02 | Review |

## How to add a task

1. Open a GitHub Issue using the feature or bug template.
2. Assign the next unused `DI-###` ID in the title/body and add it to this file.
3. Record priority, owner, status, and dependencies.
4. Before implementation, check branches and open PRs for overlap.
5. Close the task only after merge and required validation.
