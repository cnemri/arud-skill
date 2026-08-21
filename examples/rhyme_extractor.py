#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyarud>=1.0.0",
# ]
# ///
"""
Example: Rhyme & Qafiyah Extraction.
Demonstrates extracting Rawi, Wasl, Ridf, Ta'sees, Dakhil, and classical classifications.
"""

import sys
from pathlib import Path

# Add repo to sys.path
repo_root = Path(__file__).resolve().parent.parent.parent.parent
for p in [repo_root / "pyarud", repo_root, Path("/Users/nemri/Downloads/pyarud/pyarud")]:
    if (p / "pyarud").is_dir() and str(p) not in sys.path:
        sys.path.insert(0, str(p))
        break

from pyarud import QafiyahAnalyzer

def main() -> None:
    analyzer = QafiyahAnalyzer()

    samples = [
        ("فَلَا تَقْنَعْ بِمَا دُونَ النُّجُومِ", "Al-Mutanabbi (Al-Wafer)"),
        ("بِسِقْطِ اللِّوَى بَيْنَ الدَّخُولِ فَحَوْمَلِ", "Imru' al-Qais (Al-Taweel)"),
        ("وَكُلُّ الَّذِي فَوْقَ التُّرَابِ تُرَابُ", "Abu al-Atahiya (Al-Saree)"),
    ]

    for ajuz, desc in samples:
        print("=" * 60)
        print(f"Sample: {desc}")
        print(f"Text: {ajuz}")
        print("=" * 60)

        q = analyzer.analyze(ajuz)
        print(f"• Rawi Consonant: {q.rawi} ({q.rawi_haraka or 'sakin'})")
        print(f"• Wasl: {q.wasl or 'None'}")
        print(f"• Khuruj: {q.khuruj or 'None'}")
        print(f"• Ridf: {q.ridf or 'None'}")
        print(f"• Ta'sees: {q.tasees or 'None'}" + (f" (Dakhil: {q.dakhil})" if q.dakhil else ""))
        print(f"• Rhyme Category: {q.qafiyah_type_ar} ({q.qafiyah_type_en})")
        print(f"• Rhyme Form: {q.rhyme_classification}")
        print(f"• Qafiyah Segment: {q.qafiyah_text} [{q.qafiyah_pattern}]")
        print()

if __name__ == "__main__":
    main()
