# AI Talent Discovery System

**ah-talent-finder** -- An AI-powered deep conversation system that helps you discover your innate talents, inner code, and career direction.

Not a test. Not a questionnaire. Not fortune-telling. It's a conversation -- like talking to a friend who's known you for ten years -- that mines your real experiences for patterns you haven't seen yourself.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-green.svg)](https://claude.ai/code)

---

## Background

The author, A-Hang, was a landscape architecture graduate working at a state-owned enterprise. Three months in, he realized: this isn't it. He didn't know what he could do -- only what he didn't want to do.

Through deep conversations with AI -- about his family, his fears, his proudest moments, his dumbest decisions -- patterns emerged. The AI saw what he couldn't: his real need wasn't "stable employment" but "time autonomy + visible competence + controllable feedback loops." His core talent: making complex things simple.

That insight led to product management, then to content creation, and eventually to full-time freelancing.

This method has been iterated with 10+ friends. One became a creator with 10K+ followers. Another transitioned from architecture to AIGC design at Tencent. Another went freelance and built a sustainable income.

---

## How It Works

### The System

```
Opening (introduction, no files created)
  -> User confirms start
    -> Session check (scripts/session.py)
      -> Resume previous? Continue from checkpoint
      -> New session? Init -> Start Step 1
  -> Step 1: Light Profile Collection (7 conversation nodes, ~30 min, 60% accuracy)
    -> Decision: Enough? -> Step 3 / Go deeper? -> Step 2
  -> Step 2: Deep Profile (past + inner exploration, ~30 min, 90% accuracy)
  -> Step 3: Career Directions + 2-Week Validation Plan
  -> Step 4: Bazi Cross-Validation (optional)
```

### What You Get

1. **Light Profile**: Who you are, what you've done, what energizes you, what drains you
2. **Talent Analysis**: 3-5 talents, each backed by evidence from your stories
3. **Career Directions**: 5 recommended paths with match scores
4. **2-Week Validation Plan**: Concrete steps you can take without quitting your job
5. **Inner Code Report** (deep edition): Why you are who you are, what you truly need
6. **Bazi Cross-Validation** (optional): Classical Chinese metaphysics as an independent verification system

### Privacy

All conversations and archive files are stored locally on your device. Nothing is uploaded anywhere.

---

## Installation

### As a Claude Code Skill

1. Copy this entire folder into `.claude/skills/ah-talent-finder/` in your vault
2. Type `/天赋` in Claude Code to start

### As a Python Package

```bash
pip install -e .
# or
python3 scripts/session.py --help
```

---

## Repository Structure

```
ah-talent-finder/
├── SKILL.md                         # Claude Code skill definition
├── README.md                        # This file
├── LICENSE                          # MIT
├── pyproject.toml                   # Python package config
├── steps/                           # Conversation workflows
│   ├── Step1-轻量画像收集.md         # 8-node light profile collection
│   ├── Step2-深度版画像.md           # Deep edition: past + inner
│   ├── Step3-职业方向与验证方案.md    # Career directions + validation
│   └── Step4-命理交叉验证.md         # Bazi cross-validation
├── scripts/                         # Python utilities
│   ├── __init__.py
│   └── session.py                   # Session state management
├── reference/                       # Background theory
│   ├── 天赋理论框架库.md             # 9 psychological frameworks
│   └── 追问规则库.md                 # Probing rules quick reference
└── examples/                        # Example usage
    └── README.md
```

---

## Session Manager CLI

```bash
# Check if a session exists
python3 scripts/session.py check

# Initialize a new session
python3 scripts/session.py init

# Save a conversation field
echo "自由职业者\n城市：南京" | \
  python3 scripts/session.py save --node "Step1-节点1" \
    --field "基本面" --stdin

# Advance progress
python3 scripts/session.py progress --node "Step1-节点2"

# View current status
python3 scripts/session.py status

# Read saved data
python3 scripts/session.py read-file --file "01-轻量画像.md"
```

---

## Theoretical Frameworks

The analysis draws on 9 established frameworks:

- **Multiple Intelligences** (Gardner)
- **VIA Character Strengths** (Peterson & Seligman)
- **RIASEC Career Types** (Holland)
- **CliftonStrengths** (Gallup)
- **Flow Theory** (Csikszentmihalyi)
- **Shadow & Individuation** (Jung)
- **IKIGAI** (Okinawan concept)
- **Narrative Psychology** (McAdams)
- **Attachment Theory** (Bowlby)

Each framework conclusion must be grounded in specific evidence from the user's stories. No abstract scoring.

---

## Requirements

- Claude Code (for skill usage)
- Python 3.9+ (for session management script)
- 30 minutes of uninterrupted time (60 for deep edition)
- Honesty -- fabricated stories don't reveal real talents

---

## Contact

- WeChat: Zephyr136
- X (Twitter): [@Astronaut_1216](https://x.com/Astronaut_1216)
- GitHub: [ahang008](https://github.com/ahang008)

---

## License

MIT -- see [LICENSE](LICENSE) for details.

---

**Built by A-Hang** -- a product manager turned full-time creator who used this exact method to find his own path.
