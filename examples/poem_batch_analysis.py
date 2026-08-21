#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyarud>=1.0.0",
# ]
# ///
"""
Example: Poem Batch Analysis and Consensus Meter Determination.
Analyzes multi-verse poems, computes meter homogeneity, and extracts dominant Rawi.
"""

import sys
from pathlib import Path

# Add repo to sys.path
repo_root = Path(__file__).resolve().parent.parent.parent.parent
for p in [repo_root / "pyarud", repo_root, Path("/Users/nemri/Downloads/pyarud/pyarud")]:
    if (p / "pyarud").is_dir() and str(p) not in sys.path:
        sys.path.insert(0, str(p))
        break

from pyarud import analyze_poem, format_poem_report

def main() -> None:
    # Abu al-Tayyib al-Mutanabbi (Al-Wafer)
    verses = [
        ("إِذَا غَامَرْتَ فِي شَرَفٍ مَرُومِ", "فَلَا تَقْنَعْ بِمَا دُونَ النُّجُومِ"),
        ("فَطَعْمُ الْمَوْتِ فِي أَمْرٍ حَقِيرٍ", "كَطَعْمِ الْمَوْتِ فِي أَمْرٍ عَظِيمِ"),
        ("يَرَى الْجُبَنَاءُ أَنَّ الْعَجْزَ عَقْلٌ", "وَتِلْكَ خَدِيعَةُ الطَّبْعِ اللَّئِيمِ"),
    ]

    poem = analyze_poem(verses)
    print(format_poem_report(poem))

    print(f"\nConsensus Summary:")
    print(f"• Dominant Meter: {poem.meter_name_ar} ({poem.meter_key})")
    print(f"• Dominant Rawi: {poem.dominant_rawi}")
    print(f"• Homogeneous: {'Yes' if poem.is_homogeneous else 'No'}")
    print(f"• Valid Verses: {poem.valid_verses_count}/{poem.total_verses}")

if __name__ == "__main__":
    main()
