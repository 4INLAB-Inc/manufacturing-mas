from __future__ import annotations

from typing import Any, Dict, List

from .proposal_evaluator import evaluate_proposal


def rank_proposals_by_comparison(
    proposals: List[Dict[str, Any]],
    *,
    constraints: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    """Rank proposals using deterministic total, comparison, and business scores."""
    enriched: List[Dict[str, Any]] = []
    for p in proposals:
        if not isinstance(p, dict):
            continue
        enriched.append(evaluate_proposal(p, constraints=constraints))
    enriched.sort(
        key=lambda x: (
            x.get("total_score", 0),
            x.get("comparison_score", 0),
            x.get("business_score", 0),
        ),
        reverse=True,
    )
    return enriched
