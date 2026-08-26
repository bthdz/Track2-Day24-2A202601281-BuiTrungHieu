"""Test so sánh kết quả giữa Python native policy và OPA Rego policy."""
from __future__ import annotations

from agent.policy import PolicyContext, check
from agent.policy_opa import check_opa


def test_opa_and_native_policy_decisions_match():
    contexts = [
        PolicyContext("restricted", "reconcile", "run-b", 1, True),
        PolicyContext("internal", "summarize", "run-a", 0, False),
        PolicyContext("public", "faq", "run-a", 0, True),
    ]

    for ctx in contexts:
        native_allow, native_reason = check(ctx)
        opa_allow, opa_reason = check_opa(ctx)

        assert native_allow == opa_allow
        assert bool(native_reason) == bool(opa_reason)
