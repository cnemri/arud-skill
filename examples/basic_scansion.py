#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyarud>=1.0.0",
# ]
# ///
"""
Example: Basic Arabic Verse and Hemistich Scansion.
Demonstrates analyzing complete verses, single hemistichs, and printing pretty reports.
"""

import sys
from pathlib import Path

# Add repo to sys.path for direct execution
repo_root = Path(__file__).resolve().parent.parent.parent.parent
for p in [repo_root / "pyarud", repo_root, Path("/Users/nemri/Downloads/pyarud/pyarud")]:
    if (p / "pyarud").is_dir() and str(p) not in sys.path:
        sys.path.insert(0, str(p))
        break

from pyarud import analyze_verse, format_verse_report

def main() -> None:
    print("=" * 60)
    print("1. Scansion of a classical Mu'allaqah verse (Imru' al-Qais)")
    print("=" * 60)

    sadr = "قِفَا نَبْكِ مِنْ ذِكْرَى حَبِيبٍ وَمَنْزِلِ"
    ajuz = "بِسِقْطِ اللِّوَى بَيْنَ الدَّخُولِ فَحَوْمَلِ"

    verse = analyze_verse(sadr, ajuz)
    print(format_verse_report(verse))

    print("\n" + "=" * 60)
    print("2. Scansion of a Single Hemistich (Single Shatr)")
    print("=" * 60)

    shatr = "عَلَى قَدْرِ أَهْلِ العَزْمِ تَأْتِي العَزَائِمُ"
    shatr_verse = analyze_verse(shatr, "")
    print(f"Text: {shatr}")
    print(f"Detected Meter: {shatr_verse.meter_name_ar} ({shatr_verse.meter_name_en})")
    print(f"Pattern: {shatr_verse.sadr.pattern}")
    print(f"Score: {shatr_verse.score * 100:.1f}%")

if __name__ == "__main__":
    main()
