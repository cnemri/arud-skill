#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyarud>=1.0.0",
# ]
# ///
"""
PyArud CLI Utility (أداة سطر الأوامر لعلم العروض والقافية)
Provides command-line prosodic scansion, meter detection, phonetic transcription,
defect debugging, and rhyme analysis using the PyArud engine.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

# Ensure pyarud package is discoverable
_CURRENT_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _CURRENT_DIR.parent
_CANDIDATE_PATHS = [
    _REPO_ROOT / "pyarud",
    _REPO_ROOT,
    Path("/Users/nemri/Downloads/pyarud/pyarud"),
    Path("/Users/nemri/Downloads/pyarud"),
]
for p in _CANDIDATE_PATHS:
    if (p / "pyarud").is_dir() and str(p) not in sys.path:
        sys.path.insert(0, str(p))
        break

try:
    import pyarud
    from pyarud import (
        ArudhProcessor,
        ArudiConverter,
        QafiyahAnalyzer,
        analyze_poem,
        analyze_verse,
        format_poem_report,
        format_verse_report,
        get_all_meters,
        get_qafiyah,
        normalize_ligatures,
        normalize_orthography,
        scan,
        strip_punctuation,
        strip_tashkeel,
        strip_tatweel,
        to_arudi,
    )
except ImportError as e:
    sys.stderr.write(f"Error importing pyarud: {e}\n")
    sys.stderr.write(f"sys.path: {sys.path}\n")
    sys.exit(1)


def cmd_scan_verse(args: argparse.Namespace) -> int:
    """Scan a single Arabic verse or hemistich."""
    sadr = args.sadr or ""
    ajuz = args.ajuz or ""

    if args.verse:
        # Check standard separators: ' * ', ' ... ', ' - ', ' # ', '\t'
        text = args.verse.strip()
        matched_sep = False
        for sep in [" * ", " ... ", "   ", " # ", " - ", "\t"]:
            if sep in text:
                parts = text.split(sep, 1)
                sadr = parts[0].strip()
                ajuz = parts[1].strip()
                matched_sep = True
                break
        if not matched_sep:
            sadr = text
            ajuz = ""

    if not sadr and not ajuz:
        sys.stderr.write("Error: Please provide a verse using --verse, or --sadr (and optional --ajuz).\n")
        return 1

    processor = ArudhProcessor()
    result = processor.analyze_verse(sadr, ajuz, forced_meter=args.meter)

    if args.json:
        out_data = result.to_dict()
        if args.output:
            Path(args.output).write_text(json.dumps(out_data, ensure_ascii=False, indent=2), encoding="utf-8")
        else:
            print(json.dumps(out_data, ensure_ascii=False, indent=2))
    else:
        report = format_verse_report(result)
        if args.output:
            Path(args.output).write_text(report, encoding="utf-8")
        else:
            print(report)

    return 0 if result.is_valid else 2


def cmd_scan_poem(args: argparse.Namespace) -> int:
    """Scan a multi-verse poem from a file or arguments."""
    verses: list[tuple[str, str]] = []

    if args.file:
        file_path = Path(args.file)
        if not file_path.is_file():
            sys.stderr.write(f"Error: File not found: {args.file}\n")
            return 1
        lines = file_path.read_text(encoding="utf-8").splitlines()
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            matched_sep = False
            for sep in [" * ", " ... ", " | ", " - ", "\t", " # "]:
                if sep in line:
                    parts = line.split(sep, 1)
                    verses.append((parts[0].strip(), parts[1].strip()))
                    matched_sep = True
                    break
            if not matched_sep:
                verses.append((line, ""))
    elif args.text:
        lines = args.text.strip().split("\n")
        for line in lines:
            line = line.strip()
            if not line:
                continue
            matched_sep = False
            for sep in [" * ", " ... ", " | ", " - ", "\t", " # "]:
                if sep in line:
                    parts = line.split(sep, 1)
                    verses.append((parts[0].strip(), parts[1].strip()))
                    matched_sep = True
                    break
            if not matched_sep:
                verses.append((line, ""))
    else:
        sys.stderr.write("Error: Please provide poem content using --file or --text.\n")
        return 1

    if not verses:
        sys.stderr.write("Error: No valid verses found to analyze.\n")
        return 1

    processor = ArudhProcessor()
    poem_res = processor.analyze_poem(verses, meter_name=args.meter)

    if args.json:
        out_data = poem_res.to_dict()
        if args.output:
            Path(args.output).write_text(json.dumps(out_data, ensure_ascii=False, indent=2), encoding="utf-8")
        else:
            print(json.dumps(out_data, ensure_ascii=False, indent=2))
    else:
        report = format_poem_report(poem_res)
        if args.output:
            Path(args.output).write_text(report, encoding="utf-8")
        else:
            print(report)

    return 0 if (poem_res.valid_verses_count == poem_res.total_verses and poem_res.meter_key != "unknown") else 2


def cmd_phonetics(args: argparse.Namespace) -> int:
    """Convert text to phonetic Arudi representation and binary pattern."""
    if not args.text:
        sys.stderr.write("Error: Please provide Arabic text with --text.\n")
        return 1

    converter = ArudiConverter()
    if args.custom_spelling:
        for pair in args.custom_spelling:
            if "=" in pair:
                w, r = pair.split("=", 1)
                converter.register_custom_spelling(w.strip(), r.strip())

    arudi_text, pattern = converter.prepare_text(
        args.text, saturate=not args.no_saturate, muqayyad=args.muqayyad
    )

    if args.json:
        data = {
            "input_text": args.text,
            "arudi_text": arudi_text,
            "pattern": pattern,
            "length": len(pattern),
            "mutaharrik_count": pattern.count("1"),
            "sakin_count": pattern.count("0"),
        }
        if args.output:
            Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        else:
            print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(f"النص الأصلي: {args.text}")
        print(f"الكتابة العروضية: {arudi_text}")
        print(f"الترميز الثنائي: {pattern}")
        print(f"الطول: {len(pattern)} مقاطع (متحرك: {pattern.count('1')} | ساكن: {pattern.count('0')})")

    return 0


def cmd_qafiyah(args: argparse.Namespace) -> int:
    """Analyze the rhyme (Qafiyah & Rawi) of a concluding hemistich or verse."""
    if not args.text:
        sys.stderr.write("Error: Please provide Arabic verse ending or Ajuz with --text.\n")
        return 1

    analyzer = QafiyahAnalyzer()
    q = analyzer.analyze(args.text, is_muqayyad=args.muqayyad)

    if args.json:
        data = q.to_dict()
        if args.output:
            Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        else:
            print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print("════════════════════ [علم القافية والروي] ════════════════════")
        print(f"• النص المحلل: {args.text}")
        print(f"• حرف الروي: {q.rawi or 'غير محدد'} ({q.rawi_haraka or 'ساكن'})")
        print(f"• حرف الوصل: {q.wasl or 'لا يوجد'}")
        print(f"• حرف الخروج: {q.khuruj or 'لا يوجد'}")
        print(f"• حرف الردف: {q.ridf or 'لا يوجد'}")
        print(f"• حرف التأسيس: {q.tasees or 'لا يوجد'}" + (f" (الدخيل: {q.dakhil})" if q.dakhil else ""))
        print(f"• نوع القافية: {q.qafiyah_type_ar} ({q.qafiyah_type_en})")
        print(f"• حركة الروي / الحالة: {q.rhyme_classification}")
        print(f"• مقطع القافية: {q.qafiyah_text} [{q.qafiyah_pattern}]")

    return 0


def cmd_meters(args: argparse.Namespace) -> int:
    """List all 16 classical meters and their variations."""
    meter_classes = get_all_meters()

    if args.key:
        if args.key not in meter_classes:
            sys.stderr.write(f"Error: Unknown meter key '{args.key}'.\n")
            sys.stderr.write(f"Available keys: {', '.join(sorted(meter_classes.keys()))}\n")
            return 1
        b_cls = meter_classes[args.key]
        b_inst = b_cls()
        data = {
            "key": b_cls.key,
            "name_ar": b_cls.name_ar,
            "name_en": b_cls.name_en,
            "bahr_type": b_cls.bahr_type,
            "only_one_shatr": b_cls.only_one_shatr,
            "feet_names": [t().name for t in b_cls.tafeelat],
            "feet_patterns": [str(t()) for t in b_cls.tafeelat],
            "canonical_pattern": " ".join(str(t()) for t in b_cls.tafeelat),
        }
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(f"═══════ [{b_cls.name_ar}] ({b_cls.name_en}) ═══════")
            print(f"• المفتاح / المعرف: {b_cls.key}")
            print(f"• نوع البحر: {b_cls.bahr_type}")
            print(f"• أحادي الشطر: {'نعم' if b_cls.only_one_shatr else 'لا'}")
            print(f"• التفاعيل القياسية: {' '.join(t().name for t in b_cls.tafeelat)}")
            print(f"• النمط الثنائي: {' '.join(str(t()) for t in b_cls.tafeelat)}")
        return 0

    all_data: list[dict[str, Any]] = []
    for key, b_cls in sorted(meter_classes.items()):
        all_data.append({
            "key": key,
            "name_ar": b_cls.name_ar,
            "name_en": b_cls.name_en,
            "bahr_type": b_cls.bahr_type,
            "only_one_shatr": b_cls.only_one_shatr,
            "feet": " ".join(t().name for t in b_cls.tafeelat),
            "pattern": " ".join(str(t()) for t in b_cls.tafeelat),
        })

    if args.json:
        if args.output:
            Path(args.output).write_text(json.dumps(all_data, ensure_ascii=False, indent=2), encoding="utf-8")
        else:
            print(json.dumps(all_data, ensure_ascii=False, indent=2))
    else:
        print(f"═══════════ [بحور الشعر العربي الستة عشر وتفرعاتها ({len(all_data)} بحراً)] ═══════════\n")
        print(f"{'المعرف (Key)':<22} | {'الاسم العربي':<22} | {'النوع':<10} | {'التفاعيل القياسية'}")
        print("─" * 90)
        for m in all_data:
            print(f"{m['key']:<22} | {m['name_ar']:<22} | {m['bahr_type']:<10} | {m['feet']}")

    return 0


def cmd_diagnose(args: argparse.Namespace) -> int:
    """Diagnose metric defects and Zihaf/'Ilal modifications in a verse."""
    sadr = args.sadr or ""
    ajuz = args.ajuz or ""

    if args.verse:
        text = args.verse.strip()
        matched_sep = False
        for sep in [" * ", " ... ", "   ", " # ", " - ", "\t"]:
            if sep in text:
                parts = text.split(sep, 1)
                sadr = parts[0].strip()
                ajuz = parts[1].strip()
                matched_sep = True
                break
        if not matched_sep:
            sadr = text
            ajuz = ""

    if not sadr:
        sys.stderr.write("Error: Please provide a verse to diagnose with --verse or --sadr.\n")
        return 1

    processor = ArudhProcessor()
    res = processor.analyze_verse(sadr, ajuz, forced_meter=args.meter)

    if args.json:
        out_data = {
            "meter": res.meter_key,
            "meter_name_ar": res.meter_name_ar,
            "bahr_type": res.bahr_type,
            "is_valid": res.is_valid,
            "score": res.score,
            "errors": res.errors,
            "sadr_feet": [f.to_dict() for f in res.sadr.feet] if res.sadr else [],
            "ajuz_feet": [f.to_dict() for f in res.ajuz.feet] if res.ajuz else [],
        }
        if args.output:
            Path(args.output).write_text(json.dumps(out_data, ensure_ascii=False, indent=2), encoding="utf-8")
        else:
            print(json.dumps(out_data, ensure_ascii=False, indent=2))
    else:
        print(f"═══ [تشخيص العروض والعلل: {res.meter_name_ar} ({res.meter_name_en})] ═══")
        print(f"• الحالة العامة: {'سليم وموزون ✓' if res.is_valid else 'مكسور أو به علة ✗'}")
        print(f"• درجة التوافق: {res.score * 100:.1f}%")

        if res.errors:
            print("\n  [الملاحظات والعيوب المكتشفة]")
            for err in res.errors:
                print(f"    ⚠️  {err}")

        if res.sadr:
            print("\n  [تشخيص تفاعيل الصدر]")
            for f in res.sadr.feet:
                status_icon = "✅" if f.status == "ok" else ("❌" if f.status == "broken" else "⚠️")
                print(
                    f"    {status_icon} تفعيلة {f.foot_index + 1}: {f.actual_tafeela or f.base_tafeela} "
                    f"[{f.actual_segment}] (المتوقع: {f.expected_pattern}) -> {f.zihaf_name_ar} ({f.zihaf_name_en})"
                )

        if res.ajuz:
            print("\n  [تشخيص تفاعيل العجز]")
            for f in res.ajuz.feet:
                status_icon = "✅" if f.status == "ok" else ("❌" if f.status == "broken" else "⚠️")
                print(
                    f"    {status_icon} تفعيلة {f.foot_index + 1}: {f.actual_tafeela or f.base_tafeela} "
                    f"[{f.actual_segment}] (المتوقع: {f.expected_pattern}) -> {f.zihaf_name_ar} ({f.zihaf_name_en})"
                )

    return 0 if res.is_valid else 2


def cmd_normalize(args: argparse.Namespace) -> int:
    """Normalize Arabic orthography, remove tashkeel, or strip punctuation."""
    if not args.text:
        sys.stderr.write("Error: Please provide text to normalize with --text.\n")
        return 1

    text = args.text
    if args.normalize_ligatures:
        text = normalize_ligatures(text)
    if args.normalize_orthography:
        text = normalize_orthography(text)
    if args.strip_tatweel:
        text = strip_tatweel(text)
    if args.strip_punctuation:
        text = strip_punctuation(text)
    if args.strip_tashkeel:
        text = strip_tashkeel(text, keep_shadda=args.keep_shadda)

    if args.json:
        data = {"original": args.text, "normalized": text}
        if args.output:
            Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        else:
            print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(text)

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="arud_cli.py",
        description="PyArud Arabic Prosody & Metric Analysis CLI Tool (أداة العروض والقافية)",
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="Available subcommands")

    # 1. scan-verse
    p_verse = subparsers.add_parser("scan-verse", aliases=["scan"], help="Scan a single verse or hemistich")
    p_verse.add_argument("--verse", "-v", help="Full verse string (separated by ' * ', ' ... ', etc.)")
    p_verse.add_argument("--sadr", "-s", help="First hemistich (الصدر)")
    p_verse.add_argument("--ajuz", "-a", help="Second hemistich (العجز)")
    p_verse.add_argument("--meter", "-m", help="Force analysis against a specific meter key")
    p_verse.add_argument("--json", action="store_true", help="Output results as JSON")
    p_verse.add_argument("--output", "-o", help="Write output to file")

    # 2. scan-poem
    p_poem = subparsers.add_parser("scan-poem", help="Scan a multi-verse poem")
    p_poem.add_argument("--file", "-f", help="Path to text file containing verses")
    p_poem.add_argument("--text", "-t", help="Poem text with verses separated by newlines")
    p_poem.add_argument("--meter", "-m", help="Force analysis against a specific meter key")
    p_poem.add_argument("--json", action="store_true", help="Output results as JSON")
    p_poem.add_argument("--output", "-o", help="Write output to file")

    # 3. phonetics
    p_phon = subparsers.add_parser("phonetics", aliases=["arudi"], help="Convert text to phonetic Arudi writing")
    p_phon.add_argument("--text", "-t", required=True, help="Diacritized Arabic text")
    p_phon.add_argument("--no-saturate", action="store_true", help="Do not apply rhyme saturation (Ishba')")
    p_phon.add_argument("--muqayyad", action="store_true", help="Analyze as quiescent/restricted rhyme (Muqayyad)")
    p_phon.add_argument("--custom-spelling", action="append", help="Custom word=phonetic mapping (can repeat)")
    p_phon.add_argument("--json", action="store_true", help="Output results as JSON")
    p_phon.add_argument("--output", "-o", help="Write output to file")

    # 4. qafiyah
    p_qaf = subparsers.add_parser("qafiyah", aliases=["rhyme"], help="Analyze poem rhyme, Rawi, and classifications")
    p_qaf.add_argument("--text", "-t", required=True, help="Concluding hemistich (Ajuz)")
    p_qaf.add_argument("--muqayyad", action="store_true", help="Verse has quiescent/sakin Rawi")
    p_qaf.add_argument("--json", action="store_true", help="Output results as JSON")
    p_qaf.add_argument("--output", "-o", help="Write output to file")

    # 5. meters
    p_met = subparsers.add_parser("meters", help="List all 16 classical meters and their variations")
    p_met.add_argument("--key", "-k", help="Inspect a specific meter key in detail")
    p_met.add_argument("--json", action="store_true", help="Output as JSON")
    p_met.add_argument("--output", "-o", help="Write output to file")

    # 6. diagnose
    p_diag = subparsers.add_parser("diagnose", help="Diagnose broken feet and Zihaf/'Ilal modifications")
    p_diag.add_argument("--verse", "-v", help="Full verse string")
    p_diag.add_argument("--sadr", "-s", help="First hemistich")
    p_diag.add_argument("--ajuz", "-a", help="Second hemistich")
    p_diag.add_argument("--meter", "-m", help="Target meter key to check against")
    p_diag.add_argument("--json", action="store_true", help="Output as JSON")
    p_diag.add_argument("--output", "-o", help="Write output to file")

    # 7. normalize
    p_norm = subparsers.add_parser("normalize", help="Normalize Arabic orthography and strip tashkeel")
    p_norm.add_argument("--text", "-t", required=True, help="Input Arabic text")
    p_norm.add_argument("--strip-tashkeel", action="store_true", help="Strip all diacritics")
    p_norm.add_argument("--keep-shadda", action="store_true", help="Preserve Shadda when stripping tashkeel")
    p_norm.add_argument("--strip-tatweel", action="store_true", help="Remove tatweel (kashida)")
    p_norm.add_argument("--strip-punctuation", action="store_true", help="Remove punctuation")
    p_norm.add_argument("--normalize-orthography", action="store_true", help="Normalize wasla, dagger alif, etc.")
    p_norm.add_argument("--normalize-ligatures", action="store_true", help="Decompose ligatures")
    p_norm.add_argument("--json", action="store_true", help="Output as JSON")
    p_norm.add_argument("--output", "-o", help="Write output to file")

    args = parser.parse_args()

    if not args.subcommand:
        parser.print_help()
        return 0

    if args.subcommand in ("scan-verse", "scan"):
        return cmd_scan_verse(args)
    elif args.subcommand == "scan-poem":
        return cmd_scan_poem(args)
    elif args.subcommand in ("phonetics", "arudi"):
        return cmd_phonetics(args)
    elif args.subcommand in ("qafiyah", "rhyme"):
        return cmd_qafiyah(args)
    elif args.subcommand == "meters":
        return cmd_meters(args)
    elif args.subcommand == "diagnose":
        return cmd_diagnose(args)
    elif args.subcommand == "normalize":
        return cmd_normalize(args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
