#!/usr/bin/env python3
"""Add a lead to the Concrete Motivation CRM pipeline."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from concrete_motivation.crm_pipeline_manager import CRMLead, CRMPipelineManager


def main() -> int:
    parser = argparse.ArgumentParser(description="Add a lead to the Concrete Motivation CRM pipeline.")
    parser.add_argument("--lead-name", required=True, help="Lead name")
    parser.add_argument("--organization", default="", help="Organization")
    parser.add_argument("--contact-name", default="", help="Contact name")
    parser.add_argument("--role", default="", help="Role")
    parser.add_argument("--email", default="", help="Email")
    parser.add_argument("--phone", default="", help="Phone")
    parser.add_argument("--segment", default="", help="Segment")
    parser.add_argument("--offer", default="", help="Offer")
    parser.add_argument("--stage", default="New Lead", help="Pipeline stage")
    parser.add_argument("--next-follow-up-date", default="", help="Next follow-up date")
    parser.add_argument("--source", default="Manual Entry", help="Lead source")
    parser.add_argument("--notes", default="", help="Notes")
    parser.add_argument("--outcome", default="", help="Outcome")
    parser.add_argument(
        "--csv-path",
        default=str(ROOT / "outputs" / "crm" / "concrete_motivation_pipeline.csv"),
        help="Master CRM CSV path",
    )
    args = parser.parse_args()

    manager = CRMPipelineManager(csv_path=Path(args.csv_path))
    manager.add_lead(
        CRMLead(
            lead_name=args.lead_name,
            organization=args.organization,
            contact_name=args.contact_name,
            role=args.role,
            email=args.email,
            phone=args.phone,
            segment=args.segment,
            offer=args.offer,
            stage=args.stage,
            last_contact_date="",
            next_follow_up_date=args.next_follow_up_date,
            source=args.source,
            notes=args.notes,
            outcome=args.outcome,
        )
    )
    print(f"Added lead to {manager.csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

