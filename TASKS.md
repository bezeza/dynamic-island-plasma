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
| [#1](https://github.com/bezeza/dynamic-island-plasma/pull/1) | Searchable notification history | `feature-searchable-history` | `russian-localization` | Open |
| [#2](https://github.com/bezeza/dynamic-island-plasma/pull/2) | Telegram smart filtering | `feature-telegram-smart-filter` | `feature-searchable-history` | Open |
| [#3](https://github.com/bezeza/dynamic-island-plasma/pull/3) | System-adaptive style | `feature-system-adaptive-style` | `feature-telegram-smart-filter` | Open |
| [#4](https://github.com/bezeza/dynamic-island-plasma/pull/4) | Notification animation and appearance settings | `feature/notification-animation-studio` | `feature-system-adaptive-style` | Draft |
| [#5](https://github.com/bezeza/dynamic-island-plasma/pull/5) | Per-application notification manager | `feature/per-application-manager` | `feature/notification-animation-studio` | Draft |

No PR above is represented as merged by this file. Re-check GitHub for current state before acting.

## Product roadmap

| ID | Priority | Task | Status | Owner | Dependency / next action |
|---|---|---|---|---|---|
| DI-001 | P0 | Review and stabilize existing PR stack (history, Telegram filter, system style, animation, app manager) | Review | Maintainer | Inspect each PR diff and CI; preserve stack order; resolve failures before merge |
| DI-002 | P0 | Establish contributor/AI workflow and task tracking | In progress | Maintainer | This documentation PR; review and merge into main |
| DI-003 | P1 | Complete per-application manager: presentation modes, priority, grouping, filters, bulk actions, manual app entry | Review | Maintainer | Builds on PR #5; validate existing implementation first; do not duplicate current allow/mute/block, sound, timeout work |
| DI-004 | P1 | Per-application animation selection | Backlog | Unassigned | Depends on animation foundation PR #4 and app manager PR #5 |
| DI-005 | P1 | Finish Animation Studio: live preview, reduced motion, edge-aware Slide, Fade/Zoom/Spring semantics | Review | Maintainer | PR #4; verify actual QML/runtime behaviour on Plasma Wayland |
| DI-006 | P1 | Localization language selector and automatic language detection | Backlog | Unassigned | Audit current translation tooling/catalogues first |
| DI-007 | P2 | Appearance / Liquid Glass Studio and compositor capability fallback | Backlog | Unassigned | Depends on supported Plasma/Qt/Wayland rendering path |
| DI-008 | P2 | Notification history UX: filters, retention, privacy, grouping | Review | Maintainer | PR #1; check current implementation and tests |
| DI-009 | P2 | Packaging, install/uninstall, rollback and emergency recovery | Backlog | Unassigned | Fedora first; document restoring standard Plasma notification service |
| DI-010 | P2 | Multi-monitor, HiDPI, accessibility, keyboard and reduced-motion audit | Backlog | Unassigned | Test on real Plasma 6 Wayland session |
| DI-011 | P2 | CI expansion: QML lint/compile, D-Bus protocol tests, config migration tests | Ready | Unassigned | Extend existing .github/workflows/check.yml after checking available toolchain |

## Agent assignment log

When an agent starts a task, add a row with its name/tool, task ID, branch, date, and scope. Remove or close the assignment when the PR is merged or the task is stopped.

| Agent / contributor | Task ID | Branch / PR | Scope | Started | Status |
|---|---|---|---|---|---|
| Maintainer + ChatGPT | DI-002 | [PR #6](https://github.com/bezeza/dynamic-island-plasma/pull/6) — `docs/ai-contributor-workflow` | Contributor rules, task registry, issue/PR templates | 2026-11-02 | Review |

## How to add a task

1. Open a GitHub Issue using the feature or bug template.
2. Assign the next unused `DI-###` ID in the title/body and add it to this file.
3. Record priority, owner, status, and dependencies.
4. Before implementation, check branches and open PRs for overlap.
5. Close the task only after merge and required validation.
