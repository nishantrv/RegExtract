"""The pipeline on the synthetic sample document, SAMPLE-01.

This repository ships synthetic data only, so these tests show the pipeline
working end to end without the original evaluation document.
"""

from pathlib import Path

import pytest

from regextract.config import Settings
from regextract.contract import Decision
from regextract.pipeline.graph import run_pipeline
from regextract.publishing.publog import verify_log
from regextract.resolution.retrieval import HybridIndex, load_catalog, resolve

SAMPLE = Path(__file__).resolve().parent.parent / "data" / "sample" / "SAMPLE-01.pdf"


@pytest.fixture(scope="module")
def sample(tmp_path_factory):
    settings = Settings(output_dir=tmp_path_factory.mktemp("sample"))
    state = run_pipeline(pdf_path=str(SAMPLE), issuer="ESA", jurisdiction="EX", settings=settings)
    return state, settings


def test_the_footer_gives_the_document_details(sample):
    document = sample[0]["document"]
    assert (document.id, document.revision, document.review_date) == ("SAMPLE-01", "1", "2025-03-01")
    assert document.title == "Requirements for Registration of Garden Water Pumps"


def test_every_clause_is_found(sample):
    ids = [c.id for c in sample[0]["clauses"]]
    assert len(ids) == 33
    assert {"3.1.1", "3.1.2", "5.5", "9.3", "ANNEX-1"} <= set(ids)


def test_every_fact_is_grounded_and_routed(sample):
    state = sample[0]
    items = state["items"]
    assert items and all(i.evidence.grounded for i in items)
    assert any(i.kind == "obligation" and i.payload.get("modality") == "shall" for i in items)
    assert {i.review.decision for i in items} <= {Decision.AUTO_ACCEPT, Decision.REVIEW}
    assert not [f.code for f in state["flags"]]


def test_the_publication_log_is_intact(sample):
    assert verify_log(sample[1].output_dir / "publish_log.jsonl")["valid"]


def test_references_link_to_the_synthetic_catalogue(tmp_path):
    settings = Settings(output_dir=tmp_path)
    index = HybridIndex(load_catalog(settings.catalog_path, settings.distractors_path), settings)
    assert resolve("Water Safety Law No. 7 of 2020", index, settings).target_document_id == "EX-WSL-7"
    assert resolve("Water Safety Law No. 70 of 2020", index, settings).status == "not_found"
