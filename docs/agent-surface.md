# Agent surface: AGENTS.md, task guides, quirk lint

Revision 1. Not yet adversarially reviewed.

**Status:** built on branch `claude/agent-surface` (draft PR). **Merge after the
`docs/architecture.md` fix.** Rule Q1 fails on this branch until that page lists
`kgf_m_s`, `tf_m_s` and `dyne_cm_s` (see "Live incidents: merge order").

Scoped 2026-09-25 from `main` @ `c2ffc1f`. It follows the agent-surface
playbook piloted in the Ladruno OpenSees fork (WP-115): `AGENTS.md`, then short
task-triggered guides, then a lint that turns greppable lessons into CI
failures. The method comes from that pilot; every rule here comes from this
repo's own history. This page is excluded from the published MkDocs site
(`exclude_docs` in `mkdocs.yml`).

## Problem

There is no gotchas doc, ledger or ADR folder. The lessons are scattered across
these places:

- `CHANGELOG.md`
- the docstrings of `_factors.py`, `checked/_derived.py` and
  `test/test_exact_factors.py`
- `CONTRIBUTING.md` and the PR template
- the bodies of PRs #1 to #4
- two entries in the owner's agent memory

### Phase 0 baseline (2026-09-25)

A recurrence is a rule or lesson that was already written down and was still
broken afterwards.

| Written rule / lesson | Written where (when) | Broken again by | Recurrences |
|---|---|---|---|
| Add a CHANGELOG entry under `Unreleased` | CONTRIBUTING step 5 and the PR template (`d9b230a`, 2026-05-06) | `49d93d7`, `6a4e4a6`, `47b6682`, `862b7e0` (05-06); `d1a655f` (05-07, edited the released `[2.0.0]` section); `f5574a1`, `bad8554` (PRs #1 and #2, 05-29); `ab8189a` (PR #3, 06-29) | **8** of the 9 commits that changed `src/` since |
| Keep `ruff format .` clean | CONTRIBUTING "Style" and the PR template (`d9b230a`) | PR #2 left `scripts/gen_stubs.py` unformatted (it still is); PR #4 needed the fix-up `b87f29d` | **2** (probably ruff version skew; see Rejected approaches) |
| Every system listed everywhere | `d1a655f` message: "All references in tests, docs, README ... updated"; PR #3: "Registered in every place existing systems are listed" | `docs/architecture.md` was missed by `49d93d7`, `6a4e4a6`, `47b6682` and `ab8189a`; README and the package docstring were missed by the first three (fixed in `d1a655f`) | **4** system additions |
| `_factors.py` is the single source of truth | `_factors.py` docstring and `docs/architecture.md` (`f9f3fe2`, 2026-05-06) | the checked layer's own four-significant-figure copies, which date from the same commit and were fixed in `a74e3ac` (2026-08-03) | 1 incident; it has not recurred since the lesson was recorded |

**Gate: pass.** Written rules recur. They are process rules, though: the
changelog, formatting and the registration lists. The one lesson that came from
a real incident, factor drift, already has a mechanical guard in the form of a
test.

**Kinds of recurring work** (non-merge commits since the rewrite `f9f3fe2`):

- **Adding or renaming a system:** 6 of 16 commits (`49d93d7`, `6a4e4a6`,
  `47b6682`, `862b7e0`, `d1a655f`, `ab8189a`).
- **Factor or unit correctness:** 2 commits (`f9f3fe2`, `a74e3ac`), and it is
  CONTRIBUTING's headline workflow ("Adding a new unit").

## Shape

1. **`AGENTS.md`** (new; the repo had no `CLAUDE.md`), plus a one-line
   `CLAUDE.md` containing `@AGENTS.md`. It holds:
   - a map of the repo
   - the exact commands and their traps
   - five rules
   - the cross-repo contract, read from the consumers
   - a Lessons section, which is the archive the guides point into

   *Accept:* every lesson has an incident reference, and both memory lessons
   are moved in (the density pitfall; the Python 3.10 cluster install).
2. **Two task guides**, one per recurring kind of work:
   `.claude/skills/baseunits-new-system/` and
   `.claude/skills/baseunits-change-factors/`.
   *Accept:* each is at most 100 lines and opens with "Read this before". Every
   pointer resolves to an `AGENTS.md` heading or rule, and no lesson is copied
   into a guide.
3. **`scripts/check_quirk_patterns.py`, rule Q1 (registry).** The self-test is
   `test/test_check_quirk_patterns.py`, and the lint is the last step of the
   `test` job in `test.yml` (the job name is unchanged).
   *Accept:* the lint must flag the incident on the pre-fix tree and pass it
   on the fix tree. Q1's scope was set by surveying all 21 commits since the
   rewrite and inspecting every hit.
4. **Housekeeping:**
   - `.gitignore` adds `.claude/*` and `!.claude/skills/`. Before this,
     worktrees under `.claude/worktrees/` showed as untracked in the main
     checkout.
   - `mkdocs.yml` excludes this page from the site.
   - `CHANGELOG.md` gets an `Unreleased` entry.

### Where the self-test lives, and why

`test/test_check_quirk_patterns.py` sits in `test/` on purpose:

- The repo's single test command (`pytest -q`, and CI on 3.9/3.11/3.12) runs it.
- pyright's `include = ["src", "test"]` covers it.
- It imports the script by file path (`importlib`), so no path configuration
  changes.

The lint on the real tree is a separate, last CI step. Inside `pytest -q`, a
live finding would fail the "Run tests" step and skip `ruff check .` after it.

## Rejected approaches

- **A lint for literal factors in the checked layer** (the `a74e3ac`
  incident). It would be redundant. `test_checked_layer_matches_float_layer`,
  added by the fix, already fails 6 of its 11 dimensions on the pre-fix tree
  `9b869e7` and passes on `a74e3ac`. The checked layer has no units outside
  `_factors` (both sets were compared on 2026-09-25 and are identical), so a
  lint would guard nothing the test does not.
- **`ruff format --check .` as a CI gate.** The result depends on the ruff
  version, and the repo has three:
  - `.pre-commit-config.yaml` pins `v0.7.4`.
  - The `[dev]` extra allows `ruff>=0.6`.
  - CI installs the latest.

  On `main`, ruff 0.15.10 flags `scripts/gen_stubs.py`. Ruff 0.16.8 also flags
  `README.md`, because it formats Python blocks inside Markdown. An unpinned
  gate would fail on some future ruff release. The mutation evidence is still
  recorded: on `a74e3ac`, 0.15.10 and 0.16.8 both flag
  `test/test_exact_factors.py`, and on `b87f29d` that file passes. Both
  format misses may be skew with the 0.7.4 pin; that is *not verified*, since
  0.7.4 is not installed here.
- **A gate requiring a CHANGELOG entry** (`src/` changed, so `Unreleased` must
  change). None of the eight misses was ever fixed, so no fix commit exists to
  pass mutation acceptance. It would also need base-ref plumbing and has
  legitimate exceptions (stub regeneration, tooling). It stays a checklist item.
- **A check that the stubs match the runtime surface.** There is no incident.
  Regenerating the stubs into a scratch copy of `main` gives byte-identical
  `.pyi` files.
- **Checking the other direction** (a site lists a system that has no module,
  e.g. after a rename). There is no incident; `d1a655f` renamed cleanly. This
  is a known hole (see Open questions).
- **`test/test_systems_parity.py` as a Q1 site.** There is no incident; it
  stays a guide item.
- **Putting the lint in a new `ci/` directory,** as the pilot did. This repo
  keeps its tooling in `scripts/`.
- **Fixing `docs/architecture.md` here.** Live instances get their own PR and
  are never waived.
- **Editing CONTRIBUTING's incomplete step lists.** That is a separate change;
  `AGENTS.md` and the guides say where the full lists are. See Open questions.
- **A rule checking the guides' pointers** (Ladruno L3). There is no incident
  here. The pointers were checked once by script instead (Results).
- **Command metadata or generators** (Omarchy). `scripts/` has two files.

## Results (2026-09-25)

**Q1 survey** (the final rule run over every commit from `f9f3fe2` to
`c2ffc1f`; every hit inspected):

| Commits | Hits | Verdict |
|---|---|---|
| `f9f3fe2` to `5dd136a` | `package_doc`: `N_mm` | True, but borderline. The docstring listed the *other* systems and described the default by its label; `d1a655f` added `N_mm_s (default)`. |
| `49d93d7` to `862b7e0` | `package_doc`, `readme` and `architecture`: `cgs`, `mks`, `kgf_m`, `kg_cm_s` (13 at `862b7e0`) | True: modules added, lists not updated. |
| `d1a655f` to `c2ffc1f` | `architecture`: `kgf_m_s`, `dyne_cm_s`; plus `tf_m_s` from `ab8189a` | True and **live**. |
| first draft only | `natural_bases`: every system, `f9f3fe2` to `6a4e4a6` | **False positive,** since fixed. Before `47b6682`, `NATURAL_BASES` was keyed by `(force, length)` tuples. A dict or list with any entry of another shape now counts as unreadable and is skipped. |

The `stub`, `gen_stubs`, `consistency` and `docs_tables` sites have never
missed a system.

**Mutation acceptance** (lint run on `git archive` trees):

| Run | Tree | Expected | Got |
|---|---|---|---|
| A1 | `862b7e0` (pre-fix) | flags README and the package docstring | flagged `readme` for 4 systems and `package_doc` for 5 (13 findings in total, with `architecture`) |
| A1b | `d1a655f` (fix) | README and package docstring clean | clean; only `architecture` flagged (2 findings, live) |
| A2 | `ab8189a` (PR #3, a recurrence) | flags the missed `architecture` site | `tf_m_s` flagged (3 findings); **no fix commit exists** → live incident |
| A3 | this branch | only the live incident | 3 findings, all `docs/architecture.md` |

**Self-test:** 20 cases, one per site, covering:

- the bug shape (`862b7e0`) and the live shape
- whole-word matching (`kN_m_s` does not satisfy `N_m_s`)
- a commented-out entry
- a docstring site versus the code
- skipping an unreadable shape or a missing site
- the stub gate, before and after stubs exist
- waivers: valid, short reason, unknown site, stale
- CLI exit codes

**Self-test against mutations of the lint.** Each one-line mutation below is
caught by exactly one self-test case (all run 2026-09-25):

- plain substring match instead of whole-word
- reading the package site as the whole file instead of its docstring
- no stale-waiver check
- guessing on an unreadable dict
- no stub gate
- no minimum waiver-reason length

**Gates on the new files:**

| Gate | Result |
|---|---|
| Full suite, `PYTHONPATH=src python -m pytest -q` | 109 passed (89 before + 20 new) |
| `ruff check .` (0.15.10; also 0.16.8 on the new files) | clean |
| `ruff format --check` on the new `.py` files (0.15.10 and 0.16.8) | clean. `scripts/gen_stubs.py` and `README.md` are unformatted, as they already were before this branch |
| `pyright` (repo config), plus the lint script | 0 errors |
| `PYTHONPATH=src mkdocs build --strict` | passes; this page is not in the built site |
| Lint runtime on the tree | about 1 s wall time on Windows, mostly interpreter start-up |

**CI on the draft branch** (run 36194144605, Python 3.9, 3.11 and 3.12):

- "Run tests" passed 109 on all three versions.
- "Lint" (`ruff check .` with CI's latest ruff) passed.
- "Quirk-pattern lint" failed, as expected, with exactly the three
  `docs/architecture.md` findings.

**Pointer check:** `new-system` has 4 heading pointers and `change-factors`
has 5, and all of them resolve to `AGENTS.md` headings. The rule references
are to rules 1, 2 and 4. The guides are 86 and 94 lines.

## Live incidents: merge order

- **`docs/architecture.md:46`**, plus the mermaid box at line 8. The page lists
  `N_mm_s`, `N_m_s`, `kN_m_s` and `kip_in_s`, and omits:
  - `kgf_m_s` (missing since `6a4e4a6` added it as `kgf_m`)
  - `dyne_cm_s` (missing since `49d93d7` added it as `cgs`)
  - `tf_m_s` (missing since `ab8189a`)

  This is a real defect because the published Architecture page tells users
  only four systems exist, while `README.md`, the package docstring and the
  Systems page list seven. **Order:** fix it in its own docs PR and merge that
  first. Then merge `main` into this branch; Q1 is then green.

## Findings outside this change (owner's call; nothing changed here)

- **The CHANGELOG is incomplete.** It never records `kgf_m_s`, `dyne_cm_s`,
  `tf_m_s` or the type stubs. The `[2.0.0]` entry lists four systems and is
  dated `2025-05-04`, but its commit is from 2026-05-06.
- **Version mismatch:** `pyproject.toml` says `1.1.0` while the CHANGELOG's
  latest release is `2.0.0`.
- **Three ruff versions** (`v0.7.4` in pre-commit, `ruff>=0.6` in `[dev]`,
  latest in CI). Pin one version, then consider adding `ruff format --check .`.
- **CONTRIBUTING's "Adding a new unit" and "Adding a new system" steps are
  incomplete.** They leave out the checked layer, the stubs, and six of the
  eight system sites.
- **Environment on this machine (not repo content):**
  - The global Python's editable `baseUnits` points at an older clone at
    `9b869e7`, which predates PR #4.
  - `C:\Users\nmora\venv\opensees_venv` has `baseUnits` at `d1a655f`. That
    install has no `tf_m_s`, which apeRevit's docs name, and its float-layer
    `ksi` is `6.894757293168` (truncated).
  - The ape-setup venv lock pins `7bd4c8f`.
- **Name collision:** `APE_Public` ships a legacy top-level package also named
  `baseUnits`, with 4-significant-figure factors and `g = 9.81`. Installing it
  would shadow this one.

## Phase 6: measurement

The baseline is the recurrence table above, as of 2026-09-25. After about 10
PRs, count review and post-merge findings that match an `AGENTS.md` lesson. If
that count does not drop, stop investing in the guides. Keep Q1 either way,
because it is mechanical and cheap.

## Open questions

- Pin ruff (and which version), then gate on `ruff format --check .`?
- Should Q1 also flag a site that lists a system with no module (the stale
  name left after a rename)? A stale name in `gen_unit_tables.py` would break
  the docs deploy only after the merge.
- Text sites accept any whole-word mention, not specifically the list entry. A
  `README.md` code example that names a system therefore satisfies the `readme`
  site. Tighten this if it ever hides a miss.
- Should `CONTRIBUTING.md` point to the two guides instead of carrying partial
  step lists?
