"""Safe payment link configuration for Concrete Motivation."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "config"
EXAMPLE_CONFIG_PATH = CONFIG_DIR / "payment_links.example.json"
LOCAL_CONFIG_PATH = CONFIG_DIR / "payment_links.local.json"


@dataclass(frozen=True, slots=True)
class PaymentLinkDefinition:
    label: str
    config_key: str
    env_var: str
    placeholder: str


@dataclass(frozen=True, slots=True)
class PaymentLinkRecord:
    label: str
    env_var: str
    config_key: str
    value: str
    source: str

    @property
    def configured(self) -> bool:
        value = self.value.strip()
        if not value:
            return False
        lowered = value.lower()
        if value.startswith("[") and value.endswith("]"):
            return False
        if value.startswith("YOUR_") or "placeholder" in lowered or "example.com" in lowered:
            return False
        return True

    @property
    def display_value(self) -> str:
        if self.configured:
            return self.value
        return self.value or f"[{self.label} payment link placeholder]"


@dataclass(frozen=True, slots=True)
class PaymentLinkStatus:
    records: tuple[PaymentLinkRecord, ...]

    @property
    def configured_count(self) -> int:
        return sum(1 for record in self.records if record.configured)

    @property
    def total_count(self) -> int:
        return len(self.records)

    def as_rows(self) -> tuple[tuple[str, str], ...]:
        return tuple(
            (
                record.label,
                "configured" if record.configured else "missing",
            )
            for record in self.records
        )

    def as_markdown(self) -> str:
        rows = "\n".join(
            f"| {record.label} | {record.source} | {record.display_value} | {'yes' if record.configured else 'no'} |"
            for record in self.records
        )
        return f"""# Payment Link Status

| Link | Source | Value | Configured |
|---|---|---|---|
{rows}

## Summary
- Configured links: {self.configured_count}/{self.total_count}
- Missing links: {self.total_count - self.configured_count}
"""


PAYMENT_LINK_DEFINITIONS: tuple[PaymentLinkDefinition, ...] = (
    PaymentLinkDefinition(
        label="Monthly membership",
        config_key="monthly_payment_link",
        env_var="CONCRETE_MOTIVATION_MONTHLY_PAYMENT_LINK",
        placeholder="[Monthly membership payment link]",
    ),
    PaymentLinkDefinition(
        label="Annual membership",
        config_key="annual_payment_link",
        env_var="CONCRETE_MOTIVATION_ANNUAL_PAYMENT_LINK",
        placeholder="[Annual membership payment link]",
    ),
    PaymentLinkDefinition(
        label="Booking deposit",
        config_key="booking_payment_link",
        env_var="CONCRETE_MOTIVATION_BOOKING_PAYMENT_LINK",
        placeholder="[Booking deposit payment link]",
    ),
    PaymentLinkDefinition(
        label="Sponsor payment",
        config_key="sponsor_payment_link",
        env_var="CONCRETE_MOTIVATION_SPONSOR_PAYMENT_LINK",
        placeholder="[Sponsor payment link]",
    ),
)


def _read_json(path: Path) -> dict[str, str]:
    if not path.is_file():
        return {}
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected object in {path}")
    return {str(key): str(value) for key, value in data.items()}


class PaymentLinkManager:
    """Load and report safe payment link placeholders or configured links."""

    def __init__(self, config_path: Path | str | None = None, example_path: Path | str | None = None) -> None:
        self.config_path = Path(config_path) if config_path is not None else LOCAL_CONFIG_PATH
        self.example_path = Path(example_path) if example_path is not None else EXAMPLE_CONFIG_PATH

    def load(self) -> dict[str, str]:
        """Load resolved link values from environment, local config, or example placeholders."""
        local = _read_json(self.config_path)
        example = _read_json(self.example_path)
        resolved: dict[str, str] = {}
        for definition in PAYMENT_LINK_DEFINITIONS:
            value = os.getenv(definition.env_var, "").strip()
            if not value:
                value = local.get(definition.config_key, "").strip()
            if not value:
                value = example.get(definition.config_key, definition.placeholder).strip()
            resolved[definition.config_key] = value or definition.placeholder
        return resolved

    def status(self) -> PaymentLinkStatus:
        resolved = self.load()
        records = []
        local = _read_json(self.config_path)
        for definition in PAYMENT_LINK_DEFINITIONS:
            env_value = os.getenv(definition.env_var, "").strip()
            if env_value:
                source = f"env:{definition.env_var}"
                value = env_value
            elif definition.config_key in local and local[definition.config_key].strip():
                source = f"config:{self.config_path}"
                value = local[definition.config_key]
            else:
                source = f"example:{self.example_path}"
                value = resolved[definition.config_key]
            records.append(
                PaymentLinkRecord(
                    label=definition.label,
                    env_var=definition.env_var,
                    config_key=definition.config_key,
                    value=value,
                    source=source,
                )
            )
        return PaymentLinkStatus(tuple(records))

    def create_example_config(self, path: Path | str | None = None) -> Path:
        target = Path(path) if path is not None else self.example_path
        target.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            definition.config_key: definition.placeholder
            for definition in PAYMENT_LINK_DEFINITIONS
        }
        target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        return target

    def create_local_template(self) -> Path:
        """Create a local ignored config template with placeholders when missing."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.config_path.exists():
            self.config_path.write_text(self.create_example_config().read_text(encoding="utf-8"), encoding="utf-8")
        return self.config_path
