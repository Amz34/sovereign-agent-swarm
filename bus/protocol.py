#!/usr/bin/env python3
"""
Sovereign Swarm Typed Message Protocol
======================================
Strict dataclasses and JSON serialization for inter-agent communication,
veto records, deliberation trails, and deterministic consensus.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import json
import uuid

@dataclass
class SwarmMessage:
    msg_id: str = field(default_factory=lambda: f"msg_{uuid.uuid4().hex[:12]}")
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    sender_agent: str = ""
    target_agent: str = "ALL"  # Broadcast or point-to-point
    message_type: str = "DELIBERATION"  # DELIBERATION, PROPOSAL, CRITIQUE, VETO, CONSENSUS, DISPATCH
    topic: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    confidence_score: float = 1.0  # 0.0 to 1.0
    telemetry_latency_ms: float = 0.0

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> "SwarmMessage":
        data = json.loads(json_str)
        return cls(**data)

@dataclass
class AgentConsensusResult:
    topic: str
    consensus_reached: bool
    iterations_run: int
    winning_synthesis: Dict[str, Any]
    veto_audit_trail: List[Dict[str, Any]]
    deliberation_history: List[SwarmMessage]
    execution_time_sec: float
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_markdown(self) -> str:
        status_badge = "✅ CONSENSUS REACHED" if self.consensus_reached else "⚠️ PARTIAL CONVERGENCE"
        md = [
            f"# 🐝 Autonomous Swarm Deliberation: {self.topic}",
            "",
            f"**Status:** {status_badge}  ",
            f"**Execution Latency:** `{self.execution_time_sec:.2f}s`  ",
            f"**Deliberation Cycles:** `{self.iterations_run}`  ",
            f"**Deliberating Agents:** `The Strategist`, `The Systems SRE`, `The Red-Team Adversary`, `The Chief Architect`  ",
            f"**Timestamp:** `{self.timestamp}`  ",
            "",
            "---",
            "",
            "## 🏆 Executive Consensus & Synthesis",
            "",
            f"### Proposed Strategic Thesis",
            f"> {self.winning_synthesis.get('executive_summary', 'N/A')}",
            "",
            "### Architectural Invariants & Topology",
            "```mermaid",
            self.winning_synthesis.get("mermaid_topology", "graph TD;\nA[Input]-->B[Swarm];"),
            "```",
            "",
            "### Systems Engineering & Invariant Specifications",
        ]

        specs = self.winning_synthesis.get("system_specs", {})
        if isinstance(specs, dict):
            for k, v in specs.items():
                md.append(f"- **{k}:** {v}")
        elif isinstance(specs, list):
            for s in specs:
                md.append(f"- {s}")
        else:
            md.append(str(specs))

        md.extend([
            "",
            "### Hardened Red-Team Mitigations",
        ])
        mitigations = self.winning_synthesis.get("red_team_mitigations", [])
        if isinstance(mitigations, list):
            for m in mitigations:
                md.append(f"- 🛡️ {m}")
        else:
            md.append(f"- 🛡️ {mitigations}")

        md.extend([
            "",
            "---",
            "",
            "## 🛡️ Adversarial Veto & Refinement Trail",
            f"Total critiques evaluated: `{len(self.veto_audit_trail)}`",
            ""
        ])

        for idx, veto in enumerate(self.veto_audit_trail, 1):
            agent = veto.get("agent", "Adversary")
            concern = veto.get("critique", "")
            severity = veto.get("severity", "HIGH")
            mitigation = veto.get("resolution", "")
            md.append(f"#### #{idx} [{severity}] Challenged by `{agent}`")
            md.append(f"- **Vulnerability / Skeptical Challenge:** {concern}")
            md.append(f"- **Enforced Architectural Patch:** {mitigation}")
            md.append("")

        md.append("---")
        md.append("*Generated Autonomously by Sovereign Agent Swarm Engine · Az. Consultancy Systems Lab*")
        return "\n".join(md)
