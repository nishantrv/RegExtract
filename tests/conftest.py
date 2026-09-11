"""Shared fixtures.

The pipeline runs once per test session, offline, and every test reads that
one result. Offline means deterministic, so tests can assert on exact counts
without being flaky.
"""

import os
import sys
from pathlib import Path

import pytest

# LiteLLM otherwise fetches its model price map over the network on import.
os.environ.setdefault("LITELLM_LOCAL_MODEL_COST_MAP", "True")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

PDF = ROOT / "data" / "CARL-01.pdf"
CARL01_PRESENT = PDF.exists()

# These fixtures run the pipeline on CARL-01. The document and its hand-labelled
# data are not in the public repository, so tests that need them are skipped.
_NEEDS_CARL01 = {"pdf_path", "state", "items", "clauses_by_id"}


def pytest_collection_modifyitems(config, items):
    if CARL01_PRESENT:
        return
    skip = pytest.mark.skip(reason="needs data/CARL-01.pdf and its original data, not in this repository")
    for item in items:
        if _NEEDS_CARL01 & set(getattr(item, "fixturenames", ())) or item.get_closest_marker("carl01"):
            item.add_marker(skip)


@pytest.fixture(scope="session")
def pdf_path():
    return str(PDF)


@pytest.fixture(scope="session")
def settings():
    from regextract.config import get_settings

    return get_settings(reload=True, output_dir=ROOT / "outputs" / "pytest")


@pytest.fixture(scope="session")
def state(settings):
    from regextract.pipeline.graph import run_pipeline

    return run_pipeline(
        pdf_path=str(PDF), issuer="ESMA", jurisdiction="AE", settings=settings
    )


@pytest.fixture(scope="session")
def items(state):
    return state["items"]


@pytest.fixture(scope="session")
def clauses_by_id(state):
    return {c.id: c for c in state["clauses"]}
