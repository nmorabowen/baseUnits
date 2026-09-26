# Agent surface: AGENTS.md, task guides, quirk lint

Revision 2 — adversarial review (Opus): verdict "ship-with-changes". All seven
findings were verified before any change; see "Revision 2: review findings and
dispositions" below.

**Status:** built on branch `claude/agent-surface` (draft PR #5); Q1 is green
on the branch. The `docs/architecture.md` defect is fixed in its own docs-only
draft PR #6, which is independent of #5: either can merge first (see "Live
incidents: merge order").

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
| Add a CHANGELOG entry under `Unreleased` | CONTRIBUTING step 5 and the PR template (`d9b230a`, 2026-05-06) | `49d93d7`, `6a4e4a6`, `47b6682`, `862b7e0` (05-06); `d1a655f` (05-07, edited the `[2.0.0]` section, which was never released; #8 folded it into `Unreleased`); `f5574a1`, `bad8554` (PRs #1 and #2, 05-29); `ab8189a` (PR #3, 06-29) | **8** of the 9 commits that changed `src/` since |
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
3. **`scripts/check_quirk_patterns.py`, rule Q1 (registry).** Every system
   module must appear in each of the four hand-maintained lists:
   - `SYSTEMS` in `test/test_consistency.py`
   - `SYSTEMS` in `docs/scripts/gen_unit_tables.py`
   - the package docstring's "pre-built systems" paragraph
   - the README "## Available systems" bullets

   Only the list itself counts, never a mention elsewhere. A site that is
   missing or cannot be read is a finding. The self-test is
   `test/test_check_quirk_patterns.py`, and the lint is the last step of the
   `test` job in `test.yml` (the job name is unchanged).
   *Accept:* the lint must flag the incident on the pre-fix tree and pass it
   on the fix tree. Q1's scope was set by surveying all 20 commits (16
   non-merge) from `f9f3fe2` to `c2ffc1f` and inspecting every hit.
4. **Housekeeping:**
   - `.gitignore` adds `.claude/*` and `!.claude/skills/`. Before this,
     worktrees under `.claude/worktrees/` showed as untracked in the main
     checkout.
   - `mkdocs.yml` excludes this page from the site.
   - `CHANGELOG.md` gets an `Unreleased` entry.

### Why an unreadable site is a finding here

The playbook says a rule that cannot read a case stays silent, never guesses.
That fits a scan over arbitrary code, where most unreadable shapes are
unrelated. Q1 instead reads four fixed, named sites in this repo's own files.
A silently skipped site switches the rule off without anyone noticing. The
review showed four ways this happened: a BOM, a `pytest.param` row,
`SYSTEMS = _EXTRA + [...]`, and deleted files. So a missing file, a missing
variable, a non-literal list or entry, a list modified after assignment, or a
missing README section or docstring paragraph is reported at its line. The
lint never guesses a value, but it never goes dark either.

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
- **Q1 sites dropped in Revision 2** (review finding 5: the rule was stricter
  than its evidence). Q1 keeps a site only if it had an incident (`readme`,
  `package_doc`), or if it is a hand-maintained list whose omission nothing
  else catches (`consistency`: the system escapes the one rule; `docs_tables`:
  the published Systems page omits it, and `docs/architecture.md` now points
  there). Dropped:
  - **`stub`** (`systems/<name>.pyi`): generated by `gen_stubs.py`; never
    missed. Stays a guide item.
  - **`gen_stubs`** (`scripts/gen_stubs.py` `SYSTEMS`): never missed, and the
    script calls itself "Temporary tooling; safe to delete". A lint that
    fails on deleting it would contradict that. Stays a guide item.
  - **`natural_bases`** (`test/test_consistency.py` `NATURAL_BASES`): already
    enforced. Removing `tf_m_s` from it makes
    `test_natural_derived_bases_are_unity` fail with `KeyError: 'tf_m_s'`
    (verified 2026-09-25).
  - **`architecture`** (`docs/architecture.md`): review finding 6. The right
    fix is a pointer to the generated Systems page, not a fourth
    hand-maintained list, and a lint site would block that pointer. The page
    is fixed in PR #6.
- **`test/test_systems_parity.py` as a Q1 site.** It is not a list: it holds
  per-system tests, so there is nothing to parse. It stays a guide item.
- **Marker comments around each list** (the review's alternative for finding
  1). They would mean editing `src/baseUnits/__init__.py`, which is library
  source and out of scope. Q1 parses each list's own structure instead.
- **Putting the lint in a new `ci/` directory,** as the pilot did. This repo
  keeps its tooling in `scripts/`.
- **Fixing `docs/architecture.md` here.** Live instances get their own PR and
  are never waived. It is fixed in PR #6
  (`docs/architecture-systems-pointer`).
- **Editing CONTRIBUTING's incomplete step lists.** That is a separate change;
  `AGENTS.md` and the guides say where the full lists are. See Open questions.
- **A rule checking the guides' pointers** (Ladruno L3). There is no incident
  here. The pointers were checked once by script instead (Results).
- **Command metadata or generators** (Omarchy). `scripts/` has two files.

## Results (2026-09-25)

**Q1 survey, Revision 2** (the final rule run over all 20 commits, 16
non-merge, from `f9f3fe2` to `c2ffc1f`; every hit inspected):

| Commits | Hits | Verdict |
|---|---|---|
| `f9f3fe2` | `docs_tables` unreadable | Expected: `gen_unit_tables.py` was added later the same day (`8c6a951`). |
| `f9f3fe2` to `5dd136a` | `package_doc` at `__init__.py:7`: `N_mm` | True, but borderline. The docstring listed the *other* systems and described the default by its label; `d1a655f` added `N_mm_s (default)`. |
| `49d93d7` to `862b7e0` | `package_doc` (`__init__.py:7`) and `readme` (`README.md:20`): `cgs`, `mks`, `kgf_m`, `kg_cm_s` | True: modules added, lists not updated. |
| `d1a655f` to `c2ffc1f` | none | Clean. |

Revision 1's hits on `architecture` (live) and its first-draft false positive
on `natural_bases` (a tuple-keyed dict before `47b6682`) are both gone,
because both sites are dropped.

**Mutation acceptance, Revision 2** (lint run on `git archive` trees):

| Run | Tree | Expected | Got |
|---|---|---|---|
| A1 | `862b7e0` (pre-fix) | flags README and the package docstring | **FLAGGED**: 9 findings, `readme` for 4 systems at `README.md:20` and `package_doc` for 5 at `src/baseUnits/__init__.py:7`; exit 1 |
| A1b | `d1a655f` (fix) | clean | **PASSED**: 0 findings, exit 0 |
| A3 | this branch | clean | 0 findings |

**The review's reproductions, re-run on the Revision 2 lint** (scratch copies
of the branch tree):

| Reproduction | Revision 1 | Revision 2 |
|---|---|---|
| README list minus `kip_in_s` (a code example still names it) | passed | flagged at `README.md:20` |
| Docstring list minus `kip_in_s` (another paragraph names it) | passed | flagged at `__init__.py:7` |
| BOM on `test_consistency.py`, plus the `tf_m_s` row deleted | passed | flagged at `test/test_consistency.py:30` |
| One `pytest.param(...)` row, plus the `dyne_cm_s` row deleted | passed | flagged: `dyne_cm_s` missing |
| `SYSTEMS = _EXTRA + [...]` in `gen_unit_tables.py` | passed | "cannot read site" at line 17 |
| All site files deleted | exit 0 | 4 "cannot read site" findings, exit 1 |
| A comment naming the systems appended to `docs/architecture.md` | passed | not applicable: the site is dropped, and the page is fixed in PR #6 |

**Self-test:** 37 cases (32 test functions, some parametrized) in
`test/test_check_quirk_patterns.py`, covering:

- pass shapes: an annotated assignment, `pytest.param` rows, a UTF-8 BOM, a
  code fence with `#` lines inside the README section
- bug shapes, each asserting the reported `path:line`: README (`862b7e0`), a
  mention outside the list, a list after the next heading, `kN_m_s` versus
  `N_m_s`, the docstring paragraph, a consistency row, a row's first item
  only, a commented-out entry
- unreadable site as a finding: each missing file, a missing variable, list
  concatenation, a non-literal entry, a list modified after assignment
  (`append`, `+=`, reassignment), a syntax error, invalid UTF-8, a README
  without its section or entries, a docstring without its paragraph
- waivers: valid, short reason, unknown site, stale, duplicate, text inside a
  docstring, a waiver for an unreadable site, a module that cannot be
  tokenized
- CLI exit codes, including all four sites missing (exit 1)

**Self-test against one-line mutations of the lint: 29 of 29 killed**
(2026-09-25; every mutant makes at least one case fail):

- the review's five survivors, adapted to the new code:
  - an unreadable entry skipped (`return None` → `continue`)
  - `except SyntaxError` swapped for another exception
  - `UnicodeDecodeError` dropped
  - a tuple's last or second item read instead of its first (two mutants)
  - the Python-site line number replaced by 1
- Revision 1's mutants that still apply:
  - no stale-waiver check
  - no minimum reason length
  - the docstring read whole instead of by paragraph
  - `pytest.param` not read
  - the README scan not bounded by the next heading
- the new code paths:
  - the BOM not stripped
  - the code fence not tracked
  - list modification after assignment not detected: any, `AugAssign`, or a
    method call (three mutants)
  - an unreadable site skipped, or reported at line 1 (two mutants)
  - a duplicate waiver accepted
  - a waiver matched in any token rather than only in comments
  - an empty README list accepted
  - the docstring paragraph's line lost
  - the README heading's line lost
  - `pytest.param` detection broken
  - a tokenize failure not reported
  - `main` always exiting 0
  - private modules counted as systems
  - a missing variable not reported
  - a missing docstring accepted

**Gates on the new files (Revision 2):**

| Gate | Result |
|---|---|
| Full suite, `PYTHONPATH=src python -m pytest -q` | 126 passed (89 before + 37 new) |
| `ruff check .` (0.15.10; also 0.16.8) | clean |
| `ruff format --check` on the new `.py` files (0.15.10 and 0.16.8) | clean. `scripts/gen_stubs.py` and `README.md` are unformatted, as they already were before this branch |
| `pyright` (repo config), plus the lint script | 0 errors |
| `PYTHONPATH=src mkdocs build --strict` | passes; this page is not in the built site |
| Lint on the tree | 0 findings, about 1 s wall time on Windows (mostly interpreter start-up) |

**CI on the draft branch, Revision 1** (run 36194144605, Python 3.9, 3.11 and
3.12): "Run tests" passed on all three versions, "Lint" passed, and
"Quirk-pattern lint" failed, as expected at that revision, with the three
`docs/architecture.md` findings.

**Pointer check:** `new-system` has 4 heading pointers and `change-factors`
has 5, and all of them resolve to `AGENTS.md` headings. The rule references
are to rules 1, 2 and 4. The guides are 91 and 94 lines.

## Live incidents: merge order

Q1 has **no live incident** since Revision 2: the branch lints clean.

The defect Revision 1 found is still real, and it is fixed separately.
`docs/architecture.md:8` (the mermaid box) and `:46` listed `N_mm_s`,
`N_m_s`, `kN_m_s` and `kip_in_s`, and omitted:
- `kgf_m_s` (missing since `6a4e4a6` added it as `kgf_m`)
- `dyne_cm_s` (missing since `49d93d7` added it as `cgs`)
- `tf_m_s` (missing since `ab8189a`)

PR #6 (branch `docs/architecture-systems-pointer`, docs-only) replaces both
lists with a pointer to the generated Systems page.

**Order: independent.** #5 no longer lints that page, so either PR can merge
first. Both add an `Unreleased` line to `CHANGELOG.md` in different
subsections (#5 under "Added", #6 under "Changed"); whichever merges second
may need a trivial rebase.

## Revision 2: review findings and dispositions

Adversarial review by Opus, verdict "ship-with-changes". Every finding was
re-checked before any change (1 and 2 on scratch copies of the tree; 3 to 5
by reading the code and running the mutants).

| # | Finding | Disposition |
|---|---|---|
| 1 | MAJOR: text sites accepted any whole-word mention anywhere. A comment turned `architecture` green; fixing only `:46` passed; removing `kip_in_s` from the README list passed because a code example names it. Findings were reported at `:1`. | **Accepted.** README is read as the bullets under "## Available systems" (fence-aware, ends at the next heading); the package site is the docstring paragraph that names "pre-built systems". Findings report the list's real line. |
| 2 | MAJOR: sites went dark silently (a BOM, one `pytest.param` row, `_EXTRA + [...]`, all files deleted → exit 0). | **Accepted.** Files are read as `utf-8-sig`; `pytest.param` is read by its first argument; any missing or unreadable fixed site is a finding (see "Why an unreadable site is a finding here"). |
| 3 | MINOR: a stale waiver escaped when its site was unreadable; duplicate waivers and waivers inside a docstring were accepted. | **Accepted.** An unreadable site now fails on its own, so a waiver cannot hide it. Duplicates are findings, and waivers are read only from real comments (`tokenize`). |
| 4 | MINOR: five one-line mutants survived the 20 self-tests. | **Accepted.** A case was added for each; all 29 mutants of the new lint are killed (Results). |
| 5 | MINOR: the rule was stricter than its evidence (5 of 8 sites never missed), and `natural_bases` duplicated a test. | **Accepted.** `stub`, `gen_stubs`, `natural_bases` and `architecture` were dropped (Rejected approaches). `consistency` and `docs_tables` are kept as hand-maintained lists with no other guard. |
| 6 | MINOR: `docs/architecture.md` should point to the generated page, and the lint would block that fix. | **Accepted.** The site was dropped, and PR #6 makes the pointer fix (separate branch and worktree, docs-only, CHANGELOG entry). |
| 7 | NITS: the commit count, and the known holes. | **Accepted.** 20 commits (16 non-merge); the holes are recorded under Open questions. |

Nothing was rejected.

## Findings outside this change (owner's call; nothing changed here)

- **The CHANGELOG is incomplete.** It never records `kgf_m_s`, `dyne_cm_s`,
  `tf_m_s` or the type stubs. The former `[2.0.0]` entry lists four systems and
  was dated `2025-05-04`, but its commit is from 2026-05-06.
- **Version mismatch (resolved by PR #8):** 2.0.0 was never tagged or published.
  The owner kept `pyproject.toml` at `1.1.0` and folded the `[2.0.0]` section
  into `Unreleased`.
- **Three ruff versions** (`v0.7.4` in pre-commit, `ruff>=0.6` in `[dev]`,
  latest in CI). Pin one version, then consider adding `ruff format --check .`.
- **CONTRIBUTING's "Adding a new unit" and "Adding a new system" steps are
  incomplete.** They leave out the checked layer, the stubs, and most of the
  places a system is listed.
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
- **Known holes** (documented, not linted; there is no incident for any):
  - an orphan `.pyi` with no module
  - a system shipped as a package directory (`systems/<name>/__init__.py`),
    which `system_modules` does not see
  - a list that names a system with no module
- ~~Text sites accept any whole-word mention.~~ Fixed in Revision 2 (finding 1).
- Should `CONTRIBUTING.md` point to the two guides instead of carrying partial
  step lists?
