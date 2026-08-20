#!/usr/bin/env python3
"""
Example: Custom Phonetics and Arudi Extensions.
Demonstrates registering custom spelling replacements and handling special words.
"""

import sys
from pathlib import Path

# Add repo to sys.path
repo_root = Path(__file__).resolve().parent.parent.parent.parent
for p in [repo_root / "pyarud", repo_root, Path("/Users/nemri/Downloads/pyarud/pyarud")]:
    if (p / "pyarud").is_dir() and str(p) not in sys.path:
        sys.path.insert(0, str(p))
        break

from pyarud import ArudiConverter

def main() -> None:
    converter = ArudiConverter()

    text1 = "هَذَا لَيْلٌ طَوِيلٌ جِدًّا"
    arudi1, pat1 = converter.prepare_text(text1)
    print(f"Original: {text1}")
    print(f"Default Arudi: {arudi1}")
    print(f"Pattern: {pat1}")
    print()

    # Register custom orthographic rules
    converter.register_custom_spelling("طاووس", "طاوووس")
    converter.register_custom_spelling("داود", "داووود")

    text2 = "رَأَيْتُ طَاوُوسَ الجَمَالِ وَدَاوُدَ الحِكْمَةِ"
    arudi2, pat2 = converter.prepare_text(text2)
    print(f"Original: {text2}")
    print(f"Custom Arudi: {arudi2}")
    print(f"Pattern: {pat2}")

if __name__ == "__main__":
    main()
