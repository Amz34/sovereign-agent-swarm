#!/usr/bin/env python3
"""
Specialized Swarm Agent Personas
================================
1. The Strategist: High-altitude vision, ROI, market positioning, moat.
2. The Systems SRE: Memory, concurrency, throughput, sub-millisecond SLOs.
3. The Red-Team Adversary: Exploit paths, edge failures, Byzantine states, veto authority.
4. The Chief Architect: Cross-agent synthesis, invariant enforcement, consensus finalizer.
"""

from typing import Dict, Any, List
from agents.base import BaseSwarmAgent
from bus.protocol import SwarmMessage

class StrategistAgent(BaseSwarmAgent):
    def __init__(self):
        super().__init__(
            agent_id="THE_STRATEGIST",
            role_title="Principal Product & Ecosystem Strategist",
            system_mission="Maximize business moat, product leverage, non-linear scalability, and zero-token deterministic enterprise advantages."
        )

    def formulate_proposal(self, topic: str, context: str = "") -> Dict[str, Any]:
        prompt = f"""Brainstorm an ambitious, high-impact enterprise architecture proposal for topic: '{topic}'.
Additional Context: {context}

Focus on:
1. Core value hypothesis & strategic advantage.
2. Non-obvious architectural angle.
3. 3 core pillars of the solution."""

        schema = """{
  "strategic_thesis": "...",
  "high_level_approach": "...",
  "core_pillars": ["Pillar 1", "Pillar 2", "Pillar 3"],
  "target_enterprise_metrics": {"token_reduction": "...", "throughput_gain": "...", "cost_savings": "..."}
}"""
        return self.generate_json_response(prompt, schema)

class SystemsSREAgent(BaseSwarmAgent):
    def __init__(self):
        super().__init__(
            agent_id="THE_SYSTEMS_SRE",
            role_title="Staff Systems & Infrastructure SRE",
            system_mission="Enforce sub-millisecond latencies, minimal RAM/VRAM footprints, crash-proof POSIX sandboxes, and zero-egress invariants."
        )

    def evaluate_systems_feasibility(self, topic: str, proposal: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"""Critique the systems infrastructure feasibility of the following proposal:
Topic: {topic}
Proposal: {proposal}

Provide:
1. Required memory, CPU, and network topology.
2. Concrete latency SLOs and hardware limits.
3. 2 severe low-level production risks (e.g., OOM, thread starvation, cache invalidation, disk thrashing).
4. Concrete systems mitigation."""

        schema = """{
  "feasibility_verdict": "APPROVED_WITH_CONSTRAINTS",
  "hardware_requirements": {"ram_budget": "...", "cpu_cores": "...", "network": "..."},
  "latency_slo_target": "...",
  "low_level_risks": [
    {"risk": "...", "impact": "...", "sre_mitigation": "..."}
  ],
  "recommended_data_structures": ["...", "..."]
}"""
        return self.generate_json_response(prompt, schema)

class RedTeamAdversaryAgent(BaseSwarmAgent):
    def __init__(self):
        super().__init__(
            agent_id="RED_TEAM_ADVERSARY",
            role_title="Principal Red-Team Security & Failure Architect",
            system_mission="Aggressively break the system. Uncover race conditions, silent data corruption, prompt injections, Byzantine loops, and supply-chain exploits. Has VETO capability."
        )

    def audit_and_critique(self, topic: str, proposal: Dict[str, Any], systems_review: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"""Rigorously attack this proposed system architecture.
Topic: {topic}
Proposal: {proposal}
Systems SRE Review: {systems_review}

Formulate 3 critical failure modes or adversarial attack vectors:
1. Byzantine / Agent State Corruption
2. Network partition or silent drift
3. Security boundary or injection vulnerability

State whether you exercise a VETO or CONDITIONAL APPROVAL."""

        schema = """{
  "veto_exercised": false,
  "adversarial_findings": [
    {
      "vector_title": "...",
      "severity": "CRITICAL / HIGH / MEDIUM",
      "attack_scenario": "...",
      "mandatory_patch": "..."
    }
  ],
  "unmitigated_concerns": ["..."]
}"""
        return self.generate_json_response(prompt, schema)

class ChiefArchitectAgent(BaseSwarmAgent):
    def __init__(self):
        super().__init__(
            agent_id="CHIEF_ARCHITECT",
            role_title="Fellow & Chief AI Systems Architect",
            system_mission="Synthesize multi-agent deliberations into an authoritative, airtight production architecture. Enforce consensus, resolve vetoes, and output formal Mermaid topology and executable specifications."
        )

    def synthesize_consensus(self, topic: str, proposal: Dict[str, Any], systems_review: Dict[str, Any], red_team: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"""Synthesize the complete multi-agent deliberation into a production-grade enterprise blueprint.
Topic: {topic}

Deliberation Inputs:
- Strategist: {proposal}
- Systems SRE: {systems_review}
- Red-Team Adversary: {red_team}

Resolve all critiques, integrate all SRE constraints, address every Red-Team finding, and construct a robust Mermaid topology diagram.
Output an authoritative production synthesis."""

        schema = """{
  "executive_summary": "High-density synthesis...",
  "mermaid_topology": "graph TD;\\n  A[Input] --> B[Engine];",
  "system_specs": {
    "latency_guarantee": "...",
    "storage_invariants": "...",
    "sovereignty_compliance": "..."
  },
  "red_team_mitigations": [
    "Patched X via Y...",
    "Enforced Z invariant..."
  ],
  "consensus_score": 0.98
}"""
        return self.generate_json_response(prompt, schema)
