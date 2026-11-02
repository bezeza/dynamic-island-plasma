# AI and Human Contribution Guide

This repository is the single source of truth for **Dynamic Island Plasma**. Every human or AI contributor must follow this guide.

## 1. Read before changing code

Before planning, editing, or opening a PR:

1. Read `PROJECT_CONTEXT.md` for product vision, constraints, architecture principles, and roadmap.
2. Read this file.
3. Read `TASKS.md` for task IDs, priorities, ownership, dependencies, and current status.
4. Inspect the live default branch, relevant feature branches, open issues, open PRs, and recent commits. The status files can be stale; GitHub is authoritative.
5. Read the actual source and tests related to the task. Distinguish implemented code from roadmap text.

Do not ask the maintainer to repeat product requirements already documented here.

## 2. Task ownership and coordination

- Every non-trivial change must reference a task ID (for example, `DI-003`) or an issue number.
- Before starting, check whether another open PR or active branch already changes the same feature or files.
- Claim the task in `TASKS.md` by adding contributor/agent name and a short status note. If you cannot safely update the shared task file, state your claim in the issue/PR and notify the maintainer.
- One task should have one implementation owner at a time. Other agents may review or test, but must not independently implement the same scope.
- Split work by clear file/component boundaries when parallel work is necessary.
- Never overwrite, revert, cherry-pick over, or force-push another contributor's work without explicit maintainer approval.
- If dependencies or conflicts are unclear, stop and report the conflict rather than guessing.

## 3. Branch and Pull Request rules

- Create one focused branch per task: `feature/DI-###-short-name`, `fix/DI-###-short-name`, or `docs/DI-###-short-name`.
- Branch from the correct dependency/base branch stated in the issue or agreed with the maintainer. Do not assume every PR targets `main`; the project may use stacked PRs.
- Never commit directly to `main`.
- Never force-push shared branches, rewrite published history, delete branches, merge PRs, or change release/version numbers without explicit approval.
- Keep PRs small and limited to the assigned task.
- Link the task/issue in the PR title or body and explain dependencies on other PRs.
- Mark PRs draft until implementation and required checks are ready for review.
- Do not merge a stacked PR before its base/dependency PR is integrated or explicitly retargeted by the maintainer.

## 4. Engineering requirements

- Inspect and reuse the existing architecture; do not create parallel managers, config stores, or UI systems.
- Preserve existing behaviour and backward compatibility unless the task explicitly authorizes a migration.
- Keep configuration defaults safe. Validate external values and clamp numeric ranges.
- Do not discard unknown config keys. Add migration logic for incompatible schema changes.
- Keep user-visible strings translatable. Update the translation template and all applicable catalogs using the repository's scripts.
- Add or update tests for new behaviour, edge cases, and policy precedence.
- Do not log private notification bodies, tokens, or other sensitive content.
- Keep optional integrations isolated from core notification handling.
- Respect KDE Plasma 6, Qt/KF versions, Wayland limitations, accessibility, reduced motion, and multi-monitor behaviour.
- Never label a visual effect as blur, Genie, Spring, or another effect unless the implementation genuinely provides it.

## 5. Required validation

Run the checks relevant to your changes. The repository's current CI baseline is:

```bash
python -m compileall -q src/dynamicisland tools
python tools/update-translations.py --check
python tools/build-translations.py
QT_QPA_PLATFORM=offscreen python tools/selftest.py --offline
```

For QML/UI, D-Bus, packaging, Wayland, or compositor-facing changes, add the relevant toolchain and manual checks where available. If a check cannot be run, say why. Never claim a test passed unless you ran it and observed success.

For desktop-facing changes, record manual test environment and results, including Plasma/Qt version, Wayland/X11 session, monitor/scaling details when relevant.

## 6. Definition of done

A task is complete only when:

- implementation matches the task and existing architecture;
- relevant automated tests pass;
- manual tests are recorded or explicitly marked not run;
- translations and documentation are updated;
- configuration persistence and upgrade compatibility are considered;
- known limitations and rollback/recovery behaviour are documented;
- a PR is open with reviewable commits and a clear summary.

A pushed branch or opened PR is not, by itself, proof that the feature works.

## 7. Required hand-off in every PR

Include:

1. Task ID and purpose.
2. What changed and why.
3. Files/components affected.
4. Tests run, exact commands, and results.
5. Manual test environment and results, or why not run.
6. Known issues, risks, and remaining work.
7. Base/dependency PRs and any migration/rollback notes.

Update `TASKS.md` when task status, owner, dependency, or next action changes. Update `PROJECT_CONTEXT.md` only when product direction, architecture, priority, supported platforms, or durable implementation status changes.

## 8. Communication style

- Be precise, concise, and factual.
- Separate facts, assumptions, and proposals.
- Report blockers early.
- Do not silently broaden scope.
- Do not tell the maintainer to repeat context already in the repository.
- The maintainer has final authority over product decisions and merges.
