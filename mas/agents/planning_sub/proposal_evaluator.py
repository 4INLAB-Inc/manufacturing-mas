from __future__ import annotations

from typing import Any, Dict, Mapping, Optional

from .constraint_evaluator import score_against_constraints
from ...protocol.cnp_comparison import merge_into_proposal, normalize_comparison_metrics

DEFAULT_KPI_WEIGHTS: Mapping[str, float] = {
    "quality": 0.30,
    "delivery": 0.25,
    "cost": 0.25,
    "safety": 0.20,
}


def evaluate_proposal(
    proposal: Dict[str, Any],
    *,
    constraints: Optional[Dict[str, Any]] = None,
    kpi_weights: Optional[Mapping[str, float]] = None,
) -> Dict[str, Any]:
    """Normalize and score one proposal for deterministic manufacturing decisions."""
    out = dict(proposal)
    merge_into_proposal(out)
    weights = dict(kpi_weights or DEFAULT_KPI_WEIGHTS)
    scores = out.get("scores") if isinstance(out.get("scores"), dict) else {}
    comparison = out.get("comparison") or normalize_comparison_metrics(out)

    business_score = sum(float(scores.get(k, 0.0)) * w for k, w in weights.items())

    expected_effect = float(comparison.get("expected_effect") or 0.5)
    expected_cost = float(comparison.get("expected_cost") or 0.5)
    quality_risk = float(comparison.get("quality_risk") or 0.3)
    confidence = float(comparison.get("confidence") or 0.7)
    comparison_score = (
        expected_effect * confidence
        - 0.35 * expected_cost
        - 0.25 * quality_risk
    )

    violation_score = 0.0
    violation_note = "ok"
    if constraints:
        violation_score, violation_note = score_against_constraints(out, constraints)

    final_score = (
        0.40 * business_score
        + 0.60 * comparison_score
        - 0.20 * violation_score
    )

    out["business_score"] = round(business_score, 4)
    out["comparison_score"] = round(comparison_score, 4)
    out["constraint_penalty"] = round(violation_score, 4)
    out["constraint_status"] = violation_note
    out["total_score"] = round(final_score, 4)
    return out
