#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyarud>=1.0.0",
# ]
# ///
"""
Example: Defect Debugger & Broken Verse Diagnosis.
Shows how to localize broken feet (Taf'ilat), missing syllables, or extra words.
"""

import sys
from pathlib import Path

# Add repo to sys.path
repo_root = Path(__file__).resolve().parent.parent.parent.parent
for p in [repo_root / "pyarud", repo_root, Path("/Users/nemri/Downloads/pyarud/pyarud")]:
    if (p / "pyarud").is_dir() and str(p) not in sys.path:
        sys.path.insert(0, str(p))
        break

from pyarud import analyze_verse

def main() -> None:
    print("=" * 60)
    print("Diagnosing a broken Mutakareb verse:")
    print("=" * 60)

    sadr = "أَخِي جَاوَزَ الظَّالِمُونَ الْمَدَى"
    ajuz_broken = "وَهَذَا كَلامٌ ثَقِيلٌ جِدًّا"  # Broken at end

    # Force check against mutakareb
    verse = analyze_verse(sadr, ajuz_broken, forced_meter="mutakareb")

    print(f"Verse Soundness: {'Valid' if verse.is_valid else 'Broken'}")
    print(f"Confidence Score: {verse.score * 100:.1f}%")

    if verse.errors:
        print("\nIdentified Errors:")
        for err in verse.errors:
            print(f"  ❌ {err}")

    print("\nFoot Diagnostics for Ajuz:")
    for f in verse.ajuz.feet:
        status_symbol = "✅" if f.status == "ok" else "❌"
        print(f"  {status_symbol} Foot {f.foot_index + 1}: [{f.actual_segment}] -> Expected: {f.expected_pattern} -> {f.zihaf_name_ar} ({f.zihaf_name_en})")

if __name__ == "__main__":
    main()
