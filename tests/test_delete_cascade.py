"""Unit test cho Stretch Goal #3 — Delete cascade (Luật 91/2025)."""
from __future__ import annotations

import json
from pathlib import Path

from agent import delete_cascade, ledger


def test_delete_cascade_removes_customer_and_preserves_ledger_integrity(tmp_path):
    # Setup temporary customers file
    customers_file = tmp_path / "customers.json"
    dummy_data = [
        {"customer_id": "KH-000001", "name": "Nguyễn Văn A"},
        {"customer_id": "KH-000002", "name": "Trần Thị B"},
    ]
    customers_file.write_text(json.dumps(dummy_data, ensure_ascii=False), encoding="utf-8")

    ledger_path = tmp_path / "ledger.jsonl"

    # Delete customer KH-000001
    success = delete_cascade.delete_customer(
        "KH-000001",
        customers_file=customers_file,
        log_dir=tmp_path,
    )
    assert success is True

    # Verify customer is removed
    remaining = json.loads(customers_file.read_text(encoding="utf-8"))
    remaining_ids = [c["customer_id"] for c in remaining]
    assert "KH-000001" not in remaining_ids
    assert "KH-000002" in remaining_ids

    # Verify ledger integrity
    assert ledger.verify(ledger_path) is True

    # Verify ledger entry details
    lines = ledger_path.read_text(encoding="utf-8").splitlines()
    entry = json.loads(lines[-1])
    assert entry["tool"] == "delete_customer"
    assert entry["decision"] == "allow"
    assert "KH-000001" in entry["reason"]
