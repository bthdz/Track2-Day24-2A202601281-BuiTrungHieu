"""Stretch Goal #1 — OPA/Rego Policy-as-Code Evaluator.

So sánh việc định nghĩa policy trong Python native (`agent/policy.py`)
với định nghĩa theo chuẩn OPA/Rego declarative policy (`agent/policy.rego`).
"""
from __future__ import annotations

from dataclasses import asdict
from agent.policy import PolicyContext


def check_opa(context: PolicyContext) -> tuple[bool, str]:
    """Mô phỏng OPA Engine đánh giá PolicyContext dựa trên các quy tắc trong policy.rego."""
    input_data = asdict(context)

    # Rego rule: deny if classification == "restricted" and egress_enabled == True
    is_denied = (
        input_data.get("data_classification") == "restricted"
        and input_data.get("egress_enabled") is True
    )

    if is_denied:
        return False, "Restricted data egress is strictly forbidden by policy (OPA rego rule)"

    allow = not is_denied
    reason = (
        f"Policy check passed (OPA rego rule) for "
        f"data_classification={input_data.get('data_classification')!r}, "
        f"egress_enabled={input_data.get('egress_enabled')}"
    )
    return allow, reason
