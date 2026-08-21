<div align="center">

# 📜 Arud Skill (`arud-skill`)
### Comprehensive Arabic Prosody, Metric Scansion & Rhyme Analysis for AI Agents and Developers
**مهارة علم العروض وتقطيع الشعر العربي وعلم القافية والروي**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Skills.sh](https://img.shields.io/badge/Skills-Agent%20Standard-purple.svg)](https://skills.sh/)
[![Powered by PyArud](https://img.shields.io/badge/Engine-PyArud%20v1.0-emerald.svg)](https://github.com/cnemri/pyarud)

</div>

---

## 📖 Overview | نبذة عامة

`arud-skill` is a production-grade agent skill and CLI toolkit built on top of [`pyarud`](https://github.com/cnemri/pyarud) — the zero-dependency, high-throughput Farahidian dynamic programming scansion engine for Arabic poetry.

It provides autonomous AI coding assistants and agents (such as **Claude Code**, **Cursor**, **Cline**, **Roo Code**, **GitHub Copilot**, **Codex**, **Windsurf**, **Gemini**, **Antigravity**) and human developers with immediate capabilities to:
- **Scan & Classify Arabic Meters**: Identify all 16 classical meters (البحور الستة عشر) and 29 sub-variations (*Tam, Majzoo, Mashtoor, Manhook, Mukhalla'*).
- **Phonetic & Binary Transcription**: Perform exact Arudi writing (الكتابة العروضية) and generate binary prosodic strings (`1` for Mutaharrik, `0` for Sakin).
- **Diagnose Poetic Defects**: Pinpoint broken feet (`ok`, `broken`, `missing`, `extra_bits`), classify single/double Zihafat (*Idmar, Khaban, Tay, Asab, Qabadh, Kaff, etc.*) and 'Ilal (*Hadhf, Qataf, Qataa, Batr, etc.*).
- **Comprehensive Rhyme Analysis**: Extract the Rawi consonant and vocalization, identify Wasl, Khuruj, Ridf, Ta'sees, and Dakhil, and classify rhyme categories (*Al-Mutawatir, Al-Mutadarak, Al-Mutarakib, Al-Mutakawis, Al-Mutaradif*).

---

## 🤖 Installing the Skill for AI Agents (`npx skills`)

`arud-skill` fully adheres to the universal open Agent Skill standard (`SKILL.md` format) and can be installed into any AI agent or IDE via the [`skills`](https://skills.sh/) CLI package manager.

### 1. Universal One-Command Installation
Install `arud-skill` directly into your workspace or across your system agents:

```bash
# Interactive installation (detects agents and prompts for target)
npx skills add cnemri/arud-skill

# Install globally for all supported agents on your machine
npx skills add cnemri/arud-skill -g

# Install to specific agents (e.g. Claude Code, Cursor, Cline, Roo Code)
npx skills add cnemri/arud-skill --agent claude-code cursor cline roo-code

# Headless / Non-interactive installation (for CI/CD or automated setups)
npx skills add cnemri/arud-skill --all
```

### 2. Ephemeral / One-Shot Usage (Without Installation)
You can pipe the skill's instructions and capabilities directly into a single agent prompt without installing it permanently:

```bash
# Pipe context directly to Claude Code CLI
npx skills use cnemri/arud-skill@arud-skill | claude

# Start an interactive agent session equipped with arud-skill
npx skills use cnemri/arud-skill --skill arud-skill --agent claude-code
```

### 3. Managing & Updating Installed Skills
```bash
# List all installed skills (project or global)
npx skills list
npx skills list -g

# Update arud-skill to the latest release
npx skills update arud-skill -g

# Remove the skill
npx skills remove arud-skill
```

### 4. Supported Agents & Manual Path Locations
If your tool does not use `skills` CLI, you can clone or copy this repository into your agent's standard skill directory:

| Agent / IDE | Global Location | Project / Workspace Location |
| :--- | :--- | :--- |
| **Claude Code** | `~/.claude/skills/arud-skill` | `.claude/skills/arud-skill` |
| **Cursor** | `~/.cursor/skills/arud-skill` | `.cursor/skills/arud-skill` |
| **Cline / Roo Code** | `~/.cline/skills/arud-skill` | `.cline/skills/arud-skill` |
| **GitHub Copilot / Codex** | `~/.config/skills/arud-skill` | `.agents/skills/arud-skill` |
| **Antigravity / Gemini CLI** | `~/.gemini/config/skills/arud-skill` | `.agents/skills/arud-skill` |
| **Hermes / Eve Agent** | `~/.hermes/skills/arud-skill` | `.hermes/skills/arud-skill` |

---

## 📂 Repository Structure | هيكل المهارة

```
arud-skill/
├── SKILL.md                          # Master AI agent instructions with YAML frontmatter
├── README.md                         # Project documentation and usage guide
├── pyproject.toml                    # Package build & dependency definition
├── LICENSE                           # MIT License
├── scripts/
│   └── arud_cli.py                   # Full-featured interactive CLI utility
├── references/
│   ├── buhur_reference.md            # Comprehensive guide to the 16 Buhur & sub-meters
│   ├── zihafs_ilal_reference.md      # Taxonomy of Zihafs, 'Ilal, and cost optimization
│   ├── qafiyah_reference.md          # Treatise on classical rhyme letters & movements
│   └── api_guide.md                  # Python developer integration & API guide
├── examples/
│   ├── basic_scansion.py             # Single verse and hemistich scansion
│   ├── poem_batch_analysis.py        # Multi-verse poem scansion and consensus meter
│   ├── defect_debugger.py            # Granular broken foot localization & diagnosis
│   ├── rhyme_extractor.py            # Detailed Qafiyah & Rawi breakdown
│   └── custom_phonetics.py           # Custom spelling dictionary extensions
└── tests/
    └── test_cli.py                   # Automated test suite for CLI subcommands
```

---

## 🚀 CLI Quick Start & Ephemeral Execution (`uv run`) | البدء السريع

All scripts in `arud-skill` (including [`scripts/arud_cli.py`](scripts/arud_cli.py) and all [`examples/`](examples/)) include **[PEP 723](https://peps.python.org/pep-0723/) Inline Script Metadata**. 

This allows `uv` to automatically provision an ephemeral, isolated virtual environment on the fly with all dependencies (`pyarud>=1.0.0`) without requiring any manual virtualenv setup:

```bash
# 1. Clone the repository
git clone https://github.com/cnemri/arud-skill.git
cd arud-skill

# 2. Run CLI commands ephemerally via uv (zero setup required)
uv run scripts/arud_cli.py --help

# 3. Or run any example directly
uv run examples/basic_scansion.py
uv run examples/poem_batch_analysis.py
```

---

## 🛠️ CLI Usage | استخدام أداة سطر الأوامر

### 1. Scan a Single Verse (تقطيع بيت مفرد)
```bash
uv run python scripts/arud_cli.py scan-verse \
  --sadr "قِفَا نَبْكِ مِنْ ذِكْرَى حَبِيبٍ وَمَنْزِلِ" \
  --ajuz "بِسِقْطِ اللِّوَى بَيْنَ الدَّخُولِ فَحَوْمَلِ"
```

Output:
```
═══ [البيت 1] بحر الطويل (Al-Taweel) ═══
• الصدر: قِفَا نَبْكِ مِنْ ذِكْرَى حَبِيبٍ وَمَنْزِلِ
• العجز: بِسِقْطِ اللِّوَى بَيْنَ الدَّخُولِ فَحَوْمَلِ
• النمط العروضي: 11010 1101010 11010 110110 11010 1101010 1101 110110
• درجة التوافق: 99.9% | الحالة: صحيح موزون

  [تقطيع الصدر]
    ✓ التفعيلة 1: فعولن (11010) - سالمة (صحيحة)
    ✓ التفعيلة 2: مفاعيلن (1101010) - سالمة (صحيحة)
    ✓ التفعيلة 3: فعولن (11010) - سالمة (صحيحة)
    ✓ التفعيلة 4: مفاعيلن (110110) - مقبوضة (القبض)

  [تقطيع العجز]
    ✓ التفعيلة 1: فعولن (11010) - سالمة (صحيحة)
    ✓ التفعيلة 2: مفاعيلن (1101010) - سالمة (صحيحة)
    ✓ التفعيلة 3: فعولن (1101) - مقبوضة (القبض)
    ✓ التفعيلة 4: مفاعيلن (110110) - مقبوضة (القبض)

  [علم القافية]
    • الروي: ل (kasra)
    • نوع القافية: المتدارك (muqayyadah)
    • مقطع القافية: فَحَوْمَلِ [10110]
```

### 2. Scan a Multi-Verse Poem (تحليل قصيدة كاملة)
```bash
uv run python scripts/arud_cli.py scan-poem --file path/to/poem.txt
```

### 3. Phonetic Arudi Transcription & Binary Pattern (الكتابة العروضية والترميز)
```bash
uv run python scripts/arud_cli.py phonetics \
  --text "عَلَى قَدْرِ أَهْلِ العَزْمِ تَأْتِي العَزَائِمُ"
```

### 4. Rhyme & Rawi Extraction (تحليل علم القافية والروي)
```bash
uv run python scripts/arud_cli.py qafiyah \
  --text "فَلَا تَقْنَعْ بِمَا دُونَ النُّجُومِ"
```

### 5. Diagnose Broken Verses (تشخيص الكسور والعلل)
```bash
uv run python scripts/arud_cli.py diagnose \
  --sadr "أَخِي جَاوَزَ الظَّالِمُونَ الْمَدَى" \
  --ajuz "وَهَذَا كَلامٌ ثَقِيلٌ جِدًّا" \
  --meter mutakareb
```

### 6. List All 16 Classical Meters (دليل البحور الستة عشر)
```bash
uv run python scripts/arud_cli.py meters
```

---

## 🐍 Python API Integration | التكامل البرمجي

```python
from pyarud import analyze_verse, analyze_poem, QafiyahAnalyzer, ArudiConverter

# Analyze single verse
verse = analyze_verse(
    "إِذَا غَامَرْتَ فِي شَرَفٍ مَرُومِ",
    "فَلَا تَقْنَعْ بِمَا دُونَ النُّجُومِ"
)
print("Meter:", verse.meter_name_ar)     # بحر الوافر
print("Score:", verse.score)             # 0.995
print("Valid:", verse.is_valid)          # True

# Analyze rhyme
analyzer = QafiyahAnalyzer()
q = analyzer.analyze("فَلَا تَقْنَعْ بِمَا دُونَ النُّجُومِ")
print("Rawi:", q.rawi)                   # م
print("Ridf:", q.ridf)                   # و
print("Rhyme Type:", q.qafiyah_type_ar)  # المتواتر
```

---

## 📄 License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for more information.
