"""Stretch Goal #3 — Delete cascade (Luật 91/2025 — Quyền yêu cầu xoá dữ liệu).

Xoá 1 subject khỏi `data/customers.json` theo yêu cầu xoá dữ liệu cá nhân,
đồng thời ghi vết vào ledger mà không phá vỡ hash chain tamper-evident.
"""
from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

from agent import ledger, policy, tools

REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"
DEFAULT_LEDGER_PATH = REPORTS_DIR / "ledger.jsonl"


def delete_customer(
    customer_id: str,
    customers_file: Path | None = None,
    log_dir: Path | None = None,
) -> bool:
    """Xoá thông tin khách hàng khỏi data store và ghi vết audit ledger append-only."""
    customers_file = customers_file or tools.CUSTOMERS_FILE
    ledger_path = (log_dir / "ledger.jsonl") if log_dir else DEFAULT_LEDGER_PATH

    ctx = policy.PolicyContext(
        data_classification="restricted",
        request_purpose="data-subject-deletion-law-91",
        agent_owner="dpo-admin",
        delegation_depth=0,
        egress_enabled=False,
    )
    allow, reason = policy.check(ctx)

    args_hash = hashlib.sha256(
        json.dumps({"customer_id": customer_id}, sort_keys=True).encode("utf-8")
    ).hexdigest()

    ledger.append(
        {
            "ts": datetime.now(timezone.utc).isoformat(),
            "agent_id": "lab24-agent",
            "run_id": f"run-delete-{uuid.uuid4().hex[:6]}",
            "tool": "delete_customer",
            "args_hash": args_hash,
            "classification": "restricted",
            "decision": "allow" if allow else "deny",
            "reason": f"Delete cascade for {customer_id}: {reason}",
        },
        ledger_path,
    )

    if not allow:
        return False

    records = json.loads(customers_file.read_text(encoding="utf-8"))
    filtered = [r for r in records if str(r.get("customer_id")) != str(customer_id)]

    if len(filtered) == len(records):
        return False  # Customer not found

    customers_file.write_text(json.dumps(filtered, indent=2, ensure_ascii=False), encoding="utf-8")
    return True
