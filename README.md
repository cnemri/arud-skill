<div align="center">

# 📜 Arud Skill (`arud-skill`)
### Comprehensive Arabic Prosody, Metric Scansion & Rhyme Analysis for AI Agents and Developers
**مهارة علم العروض وتقطيع الشعر العربي وعلم القافية والروي**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Powered by PyArud](https://img.shields.io/badge/Engine-PyArud%20v1.0-emerald.svg)](https://github.com/cnemri/pyarud)

</div>

---

## 📖 Overview | نبذة عامة

`arud-skill` is a production-grade agent skill and CLI toolkit built on top of [`pyarud`](https://github.com/cnemri/pyarud) — the zero-dependency, high-throughput Farahidian dynamic programming scansion engine for Arabic poetry.

It provides autonomous AI coding assistants (such as Google Antigravity, Gemini, Claude, Cursor) and human developers with immediate capabilities to:
- **Scan & Classify Arabic Meters**: Identify all 16 classical meters (البحور الستة عشر) and 29 sub-variations (*Tam, Majzoo, Mashtoor, Manhook, Mukhalla'*).
- **Phonetic & Binary Transcription**: Perform exact Arudi writing (الكتابة العروضية) and generate binary prosodic strings (`1` for Mutaharrik, `0` for Sakin).
- **Diagnose Poetic Defects**: Pinpoint broken feet (`ok`, `broken`, `missing`, `extra_bits`), classify single/double Zihafat (*Idmar, Khaban, Tay, Asab, Qabadh, Kaff, etc.*) and 'Ilal (*Hadhf, Qataf, Qataa, Batr, etc.*).
- **Comprehensive Rhyme Analysis**: Extract the Rawi consonant and vocalization, identify Wasl, Khuruj, Ridf, Ta'sees, and Dakhil, and classify rhyme categories (*Al-Mutawatir, Al-Mutadarak, Al-Mutarakib, Al-Mutakawis, Al-Mutaradif*).

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

## 🚀 Quick Start | البدء السريع

### 1. Prerequisites & Installation

Clone the repository and install with `uv` (recommended) or `pip`:

```bash
# Clone the repository
git clone https://github.com/cnemri/arud-skill.git
cd arud-skill

# Run with uv (zero setup required)
uv run python scripts/arud_cli.py --help
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

## 🤖 Antigravity / Agent Skill Installation

To register `arud-skill` into your Antigravity or AI agent environment:

1. Copy or link this folder into `.agents/skills/arud-skill` in your workspace or `~/.gemini/config/skills/arud-skill`.
2. The agent will automatically discover `SKILL.md` and utilize `scripts/arud_cli.py` or the Python API during prosodic tasks.

---

## 📄 License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for more information.
