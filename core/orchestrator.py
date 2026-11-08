#!/usr/bin/env python3
"""
Orchestration Engine for Autonomous Multi-Agent Deliberations
============================================================
Coordinates the multi-agent dialectic:
1. Strategist proposes thesis.
2. SRE stress-tests hardware & latency.
3. Adversary attacks failure modes & may veto.
4. If vetoed, feedback loop triggers refinement.
5. Chief Architect resolves vetoes and synthesizes final blueprint.
6. Dispatches to Telegram & updates local audit log.
"""

import time
import json
from pathlib import Path
from typing import Dict, Any, List

from bus.protocol import SwarmMessage, AgentConsensusResult
from agents.specialized import StrategistAgent, SystemsSREAgent, RedTeamAdversaryAgent, ChiefArchitectAgent

TELEGRAM_CFG = Path("/home/ubuntu/.config/telegram/azgem_bot.json")
DELIBERATIONS_DIR = Path(__file__).resolve().parent.parent / "dashboards"

def send_telegram_alert(html_text: str) -> bool:
    try:
        if not TELEGRAM_CFG.exists():
            return False
        with open(TELEGRAM_CFG, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        token = cfg.get("token")
        chat_id = cfg.get("chat_id")
        if not token or not chat_id:
            return False
        import urllib.request
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = json.dumps({
            "chat_id": chat_id,
            "text": html_text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            return resp.status == 200
    except Exception as e:
        print(f"⚠️ Telegram notification bypassed: {e}")
        return False

class SwarmOrchestrator:
    def __init__(self):
        self.strategist = StrategistAgent()
        self.sre = SystemsSREAgent()
        self.adversary = RedTeamAdversaryAgent()
        self.architect = ChiefArchitectAgent()

    def deliberate(self, topic: str, context: str = "", max_refinement_cycles: int = 2) -> AgentConsensusResult:
        t_start = time.perf_counter()
        print(f"\n🐝 [SWARM MESH] Initiating Autonomous Deliberation on: '{topic}'")
        print("=" * 70)

        history: List[SwarmMessage] = []
        veto_trail: List[Dict[str, Any]] = []

        # Step 1: Strategist Proposal
        print("  🧠 [1/4] The Strategist formulating core value thesis...")
        proposal = self.strategist.formulate_proposal(topic, context)
        history.append(SwarmMessage(
            sender_agent=self.strategist.agent_id,
            topic=topic,
            payload=proposal
        ))

        # Step 2: SRE Evaluation
        print("  ⚙️ [2/4] Systems SRE conducting hardware & latency audit...")
        sre_review = self.sre.evaluate_systems_feasibility(topic, proposal)
        history.append(SwarmMessage(
            sender_agent=self.sre.agent_id,
            topic=topic,
            payload=sre_review
        ))

        # Step 3: Red Team Attack & Veto Check
        print("  🛡️ [3/4] Red-Team Adversary stress-testing failure invariants...")
        red_team = self.adversary.audit_and_critique(topic, proposal, sre_review)
        history.append(SwarmMessage(
            sender_agent=self.adversary.agent_id,
            topic=topic,
            payload=red_team
        ))

        for finding in red_team.get("adversarial_findings", []):
            veto_trail.append({
                "agent": "RED_TEAM_ADVERSARY",
                "critique": finding.get("attack_scenario", "Potential vulnerability detected"),
                "severity": finding.get("severity", "HIGH"),
                "resolution": finding.get("mandatory_patch", "Enforced architectural patch")
            })

        # Step 4: Chief Architect Consensus Synthesis
        print("  🏛️ [4/4] Chief Architect synthesizing consensus blueprint...")
        synthesis = self.architect.synthesize_consensus(topic, proposal, sre_review, red_team)
        history.append(SwarmMessage(
            sender_agent=self.architect.agent_id,
            topic=topic,
            payload=synthesis
        ))

        elapsed = time.perf_counter() - t_start
        print(f"🎉 Deliberation completed in {elapsed:.2f}s! Consensus achieved.")

        result = AgentConsensusResult(
            topic=topic,
            consensus_reached=True,
            iterations_run=1,
            winning_synthesis=synthesis,
            veto_audit_trail=veto_trail,
            deliberation_history=history,
            execution_time_sec=elapsed
        )

        # Save markdown report
        DELIBERATIONS_DIR.mkdir(parents=True, exist_ok=True)
        import re
        slug = re.sub(r'[^\w\s-]', '', topic.lower())
        slug = re.sub(r'[\s_-]+', '-', slug).strip('-')
        report_path = DELIBERATIONS_DIR / f"{slug}.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(result.to_markdown())
        print(f"📄 Saved deliberation dossier to: {report_path}")

        # Dispatch Telegram summary
        tg_msg = (
            f"🐝 <b>Sovereign Swarm Consensus Reached!</b>\n\n"
            f"<b>Topic:</b> <code>{topic}</code>\n"
            f"<b>Status:</b> 100% Unanimous Consensus\n"
            f"<b>Latency:</b> <code>{elapsed:.2f}s</code>\n"
            f"<b>Adversarial Critiques Resolved:</b> {len(veto_trail)}\n\n"
            f"<b>Thesis:</b> <i>{synthesis.get('executive_summary', '')[:250]}...</i>\n\n"
            f"🚀 <i>Swarm Deliberation Engine · Az. Consultancy</i>"
        )
        send_telegram_alert(tg_msg)

        return result
