#!/usr/bin/env /home/ubuntu/.venvs/antigravity/bin/python
"""
Sovereign Agent Swarm CLI
=========================
Command line interface to dispatch autonomous multi-agent deliberations,
brainstorms, and automated architectural synthesis.

Author: Amz34 / Antigravity
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_DIR))

from core.orchestrator import SwarmOrchestrator, DELIBERATIONS_DIR

def update_readme_index():
    dossiers = []
    if DELIBERATIONS_DIR.exists():
        for f in sorted(DELIBERATIONS_DIR.glob("*.md"), reverse=True):
            title = f.stem.replace("-", " ").title()
            with open(f, "r", encoding="utf-8") as fl:
                for line in fl:
                    if line.startswith("# "):
                        title = line.replace("# ", "").replace("🐝 Autonomous Swarm Deliberation: ", "").strip()
                        break
            dossiers.append({"title": title, "file": f.name})

    rows = []
    for d in dossiers:
        rows.append(f"| [{d['title']}](./dashboards/{d['file']}) | `Consensus Reached` | [`Read Deliberation Blueprint →`](./dashboards/{d['file']}) |")

    readme_content = f"""# 🐝 Sovereign Agent Swarm (Dialectic Deliberation Mesh)

[![Autonomous Swarm](https://img.shields.io/badge/Agent_Mesh-Dialectic%20Consensus-blue?style=flat-square&logo=google)](https://github.com/Amz34/sovereign-agent-swarm)
[![Sovereign Architecture](https://img.shields.io/badge/Architecture-KSA%20%7C%20GCC%20Enterprise-FFC01E?style=flat-square)](https://github.com/Amz34)
[![Zero-Token AST](https://img.shields.io/badge/Security-Red--Team%20Veto%20Authority-FF375F?style=flat-square)](https://github.com/Amz34)
[![Consensus Completed](https://img.shields.io/badge/Deliberations_Indexed-{len(dossiers)}-00B8A3?style=flat-square)](https://github.com/Amz34/sovereign-agent-swarm)

Autonomous, multi-persona AI agent deliberation mesh executing adversarial debates, SRE hardware feasibility audits, and formal architectural consensus without human token burn.

Architected by **[Aamir Zameer (@Amz34)](https://github.com/Amz34)** (Principal AI Systems Architect, Az. Consultancy).

---

## 🏛️ Swarm Dialectic Architecture

```mermaid
flowchart TD
    Task["Target Complex Task / Architectural Prompt"] --> A1["The Strategist Agent\\n(ROI, Value Thesis & Advantage)"]
    A1 --> A2["The Systems SRE Agent\\n(Hardware, Latency & Invariants)"]
    A2 --> A3["The Red-Team Adversary Agent\\n(Byzantine Attacks & Veto Authority)"]
    A3 -->|Veto / Challenge| A2
    A3 --> A4["The Chief Architect Agent\\n(Resolution, Consensus & Blueprint)"]
    A4 --> Out["Production Blueprint & Telegram Executive Dispatch"]
```

---

## 👥 The 4 Deliberating Agent Personas

1. **The Strategist (`THE_STRATEGIST`)**: Formulates the core value proposition, market differentiation, and non-linear leverage.
2. **The Systems SRE (`THE_SYSTEMS_SRE`)**: Enforces memory budgets, sub-millisecond latency SLOs, and thread/hardware bounds.
3. **The Red-Team Adversary (`RED_TEAM_ADVERSARY`)**: Possesses absolute **VETO power**; stress-tests edge failure modes, prompt injection, and state drift.
4. **The Chief Architect (`CHIEF_ARCHITECT`)**: Unifies the debate, patches adversarial findings, and authors formal Mermaid topologies.

---

## 📂 Autonomous Deliberation Blueprints

| Topic | Consensus Status | Dossier Access |
|:---|:---:|:---:|
{chr(10).join(rows) if rows else "| *Pending Initial Deliberation* | - | - |"}

---

## 🛠️ CLI Operations

```bash
# Dispatch autonomous brainstorming & consensus deliberation:
./swarm_cli.py deliberate "Autonomous Micro-VM Sandboxing for AI Code Execution"

# Run deliberation with auto-commit and GitHub push:
./swarm_cli.py deliberate "Autonomous Micro-VM Sandboxing" --push

# View all deliberations:
./swarm_cli.py list
```

---

*Architected & Maintained by [Aamir Zameer (@Amz34)](https://github.com/Amz34) · Az. Consultancy Systems Lab.*
"""
    with open(REPO_DIR / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"📊 Dashboard updated with {len(dossiers)} deliberation dossiers.")

def main():
    parser = argparse.ArgumentParser(description="Sovereign Agent Swarm CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_delib = subparsers.add_parser("deliberate", help="Run multi-agent dialectic deliberation on a topic")
    p_delib.add_argument("topic", help="Topic or problem to brainstorm and design")
    p_delib.add_argument("--context", default="", help="Optional background context")
    p_delib.add_argument("--push", action="store_true", help="Auto git commit and push to GitHub")

    p_list = subparsers.add_parser("list", help="List all generated deliberation dossiers")

    args = parser.parse_args()
    orchestrator = SwarmOrchestrator()

    if args.command == "deliberate":
        result = orchestrator.deliberate(args.topic, args.context)
        update_readme_index()
        if args.push:
            print("📦 Auto-committing and pushing to GitHub...")
            os.chdir(REPO_DIR)
            subprocess.run(["git", "add", "."], check=False)
            msg = f"feat(swarm): publish multi-agent consensus blueprint on '{args.topic}'"
            subprocess.run(["git", "commit", "-m", msg], check=False)
            subprocess.run(["git", "push", "-u", "origin", "main"], check=False)
            print("✅ Pushed to GitHub!")

    elif args.command == "list":
        if not DELIBERATIONS_DIR.exists():
            print("No dossiers found.")
            return
        for f in sorted(DELIBERATIONS_DIR.glob("*.md")):
            print(f"  - {f.name}")

if __name__ == "__main__":
    main()
