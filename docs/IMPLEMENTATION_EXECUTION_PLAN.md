# Manufacturing MAS Execution Plan

## Priority Modules To Change First

### P0 Contract and decision integrity

1. `mas/domain/manufacturing_context.py`
2. `mas/domain/agent_snapshot.py`
3. `mas/api/server.py`
4. `mas/agents/planning_agent.py`
5. `mas/agents/planning_sub/proposal_ranker.py`
6. `mas/agents/planning_sub/constraint_evaluator.py`
7. `mas/protocol/cnp_session.py`
8. `tests/test_manufacturing_context.py`
9. `tests/test_cnp_golden.py`
10. `tests/test_monitoring_schema_smoke.py`

### P1 Runtime and orchestration hardening

1. `mas/runtime/factory_runtime.py`
2. `mas/runtime/scenario_runtime.py`
3. `mas/intelligence/operational_decision_card.py`
4. `mas/intelligence/control_matrix.py`

### P2 Integration readiness

1. `mas/adapters/base.py`
2. concrete adapter modules to be added under `mas/integration/`
3. adapter contract tests

## What Each Module Must Do

### `manufacturing_context.py`

- define required contract sections
- provide validation helpers
- expose stable agent-facing views
- keep compatibility with existing snapshots

### `planning_agent.py`

- stop owning all scoring details inline
- delegate alert collection, constraint scoring, proposal evaluation, ranking, and reporting
- keep only orchestration and status aggregation

### `proposal_ranker.py` and evaluator modules

- compute one explicit final decision score
- separate business score, comparison score, and constraint penalty
- preserve explainability fields for audit and tests

### `cnp_session.py`

- validate proposals consistently
- stamp session metadata onto final strategy
- provide an approval-ready decision envelope

## Execution Sequence

1. Strengthen `ManufacturingContext` so monitoring payloads and agents consume a validated contract.
2. Refactor PA into explicit collection, evaluation, ranking, and reporting responsibilities.
3. Fix CNP golden ranking so expected manufacturing priorities remain deterministic.
4. Add focused tests for contract validation and proposal scoring.
5. Run full regression tests before touching runtime behavior further.

## Done Criteria For This Phase

- `ManufacturingContext` has validation helpers and agent-facing role views.
- monitoring payload exposes the validated context contract.
- PA delegates proposal evaluation to submodules.
- CNP golden test passes with deterministic ranking.
- full pytest suite passes.
