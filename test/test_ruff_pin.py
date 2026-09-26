"""ruff is pinned to one exact version, the same in pre-commit and the [dev] extra.

CI installs ``.[dev]``, so the extra's pin is also CI's ruff. Different ruff
versions format this tree differently, so a looser pin, or a pre-commit rev
bumped on its own, makes ``ruff format --check .`` pass in one place and fail
in another.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _precommit_ruff_rev() -> str:
    text = (ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8")
    m = re.search(
        r"repo:\s*https://github\.com/astral-sh/ruff-pre-commit\s*\n\s*rev:\s*v?(\S+)", text
    )
    assert m, "no ruff-pre-commit repo with a rev in .pre-commit-config.yaml"
    return m.group(1)


def _dev_extra_ruff_requirement() -> str:
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    m = re.search(r"^dev\s*=\s*\[([^\]]*)\]", text, re.MULTILINE)
    assert m, "no dev extra in pyproject.toml"
    reqs = re.findall(r"\"(ruff\b[^\"]*)\"", m.group(1))
    assert len(reqs) == 1, f"expected one ruff requirement in the dev extra, got {reqs}"
    return reqs[0].replace(" ", "")


def test_ruff_pinned_once_in_precommit_and_dev_extra():
    rev = _precommit_ruff_rev()
    req = _dev_extra_ruff_requirement()
    assert re.fullmatch(r"\d+\.\d+\.\d+", rev), f"pre-commit ruff rev is {rev!r}"
    assert req == f"ruff=={rev}", (
        f"the dev extra requires {req!r} but .pre-commit-config.yaml pins ruff v{rev}; "
        "pin the same exact version in both"
    )
