from dataclasses import dataclass, field
from typing import Any, Dict, List

from mas.agents.planning_agent import PlanningAgent
from mas.domain import Factory
from mas.domain.agent_snapshot import enrich_snapshot_for_agents
from mas.messaging.broker import MessageBroker


@dataclass
class _Responder:
    agent_id: str
    proposal: Dict[str, Any]
    accepted: List[Dict[str, Any]] = field(default_factory=list)

    def handle_cfp(self, cfp_data: Dict[str, Any]) -> Dict[str, Any]:
        return dict(self.proposal)

    def execute_accepted_proposal(self, proposal: Dict[str, Any]) -> None:
        self.accepted.append(dict(proposal))


def test_cnp_golden_rank_and_strategy():
    broker = MessageBroker()
    pa = PlanningAgent(llm_client=None)
    pa.broker = broker

    factory = Factory()
    factory.run_cycle()
    snapshot = enrich_snapshot_for_agents(factory.get_snapshot())

    responders = [
        _Responder(
            "EA",
            {
                "agent": "EA",
                "proposal": "stabilize equipment with moderate slowdown",
                "speed_recommendation": 85,
                "inspection_mode": "enhanced",
                "scores": {"quality": 0.8, "delivery": 0.7, "cost": 0.6, "safety": 0.9},
                "proposal_metrics": {
                    "expected_effect": 0.75,
                    "cost_estimate": 0.35,
                    "quality_risk": 0.15,
                    "constraint_violation_total": 0.05,
                    "confidence": 0.8,
                },
            },
        ),
        _Responder(
            "QA",
            {
                "agent": "QA",
                "proposal": "reduce quality risk and switch to full inspection",
                "speed_recommendation": 78,
                "inspection_mode": "전수",
                "scores": {"quality": 0.95, "delivery": 0.55, "cost": 0.45, "safety": 0.8},
                "proposal_metrics": {
                    "expected_effect": 0.88,
                    "cost_estimate": 0.42,
                    "quality_risk": 0.08,
                    "constraint_violation_total": 0.02,
                    "confidence": 0.92,
                },
            },
        ),
        _Responder(
            "SA",
            {
                "agent": "SA",
                "proposal": "protect material buffer first",
                "speed_recommendation": 92,
                "inspection_mode": "standard",
                "scores": {"quality": 0.6, "delivery": 0.8, "cost": 0.7, "safety": 0.6},
                "proposal_metrics": {
                    "expected_effect": 0.62,
                    "cost_estimate": 0.28,
                    "quality_risk": 0.22,
                    "constraint_violation_total": 0.0,
                    "confidence": 0.75,
                },
            },
        ),
    ]

    strategy = pa.initiate_cnp(responders, snapshot)
    assert strategy is not None

    assert strategy["best_agent"] == "QA"
    assert strategy["target_speed_pct"] == 78
    assert strategy["inspection_mode"] == "전수"
    assert strategy["constraints_applied"] is True
    assert strategy["protocol_version"] == "cnp/1"
    assert strategy["approval_required"] is True
    assert isinstance(strategy.get("conversation_id"), str) and strategy["conversation_id"]

    card = strategy.get("operational_decision_card") or {}
    assert card.get("schema") == "operational_decision_card/v1"
    assert card.get("recommended_actions")

    assert responders[1].accepted, "QA accepted proposal should be executed"
