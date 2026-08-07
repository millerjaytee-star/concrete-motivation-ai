import json
from pathlib import Path

from scripts.verify_canonical_product import EXPECTED, validate_config


ROOT = Path(__file__).resolve().parents[1]


def test_canonical_product_configuration_is_valid():
    assert validate_config() == []


def test_canonical_product_is_lovable_and_not_legacy_web():
    data = json.loads((ROOT / "config/canonical-product.json").read_text())
    assert data["sourceOfTruth"] == "lovable"
    assert data["productionUrl"] == EXPECTED["productionUrl"]
    assert data["localProductStatus"] == "reconciliation-blocked-pending-lovable-source-export"


def test_repository_instructions_block_stale_deployment():
    instructions = (ROOT / "AGENTS.md").read_text()
    assert EXPECTED["lovableProjectId"] in instructions
    assert "must not be deployed over the Lovable production project" in instructions
