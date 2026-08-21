# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pytest>=8.0.0",
#     "pyarud>=1.0.0",
# ]
# ///
"""
Automated unit tests for arud_cli.py subcommands.
"""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CLI_PATH = REPO_ROOT / "scripts" / "arud_cli.py"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CLI_PATH), *args],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )


def test_cli_help():
    res = run_cli("--help")
    assert res.returncode == 0
    assert "PyArud Arabic Prosody & Metric Analysis CLI Tool" in res.stdout


def test_cli_scan_verse():
    res = run_cli(
        "scan-verse",
        "--sadr",
        "قِفَا نَبْكِ مِنْ ذِكْرَى حَبِيبٍ وَمَنْزِلِ",
        "--ajuz",
        "بِسِقْطِ اللِّوَى بَيْنَ الدَّخُولِ فَحَوْمَلِ",
    )
    assert res.returncode == 0
    assert "بحر الطويل" in res.stdout
    assert "صحيح موزون" in res.stdout


def test_cli_scan_verse_json():
    res = run_cli(
        "scan-verse",
        "--verse",
        "إِذَا غَامَرْتَ فِي شَرَفٍ مَرُومِ * فَلَا تَقْنَعْ بِمَا دُونَ النُّجُومِ",
        "--json",
    )
    assert res.returncode == 0
    assert '"meter_key": "wafer"' in res.stdout
    assert '"is_valid": true' in res.stdout


def test_cli_phonetics():
    res = run_cli(
        "phonetics",
        "--text",
        "عَلَى قَدْرِ أَهْلِ العَزْمِ تَأْتِي العَزَائِمُ",
    )
    assert res.returncode == 0
    assert "11010110101011010110110" in res.stdout


def test_cli_qafiyah():
    res = run_cli(
        "qafiyah",
        "--text",
        "فَلَا تَقْنَعْ بِمَا دُونَ النُّجُومِ",
    )
    assert res.returncode == 0
    assert "حرف الروي: م" in res.stdout
    assert "المتواتر" in res.stdout


def test_cli_meters():
    res = run_cli("meters")
    assert res.returncode == 0
    assert "taweel" in res.stdout
    assert "kamel" in res.stdout
    assert "wafer" in res.stdout


def test_cli_diagnose_broken():
    res = run_cli(
        "diagnose",
        "--sadr",
        "أَخِي جَاوَزَ الظَّالِمُونَ الْمَدَى",
        "--ajuz",
        "وَهَذَا كَلامٌ ثَقِيلٌ جِدًّا",
        "--meter",
        "mutakareb",
    )
    assert res.returncode == 2
    assert "مكسور أو به علة" in res.stdout
    assert "broken" in res.stdout


def test_cli_normalize():
    res = run_cli(
        "normalize",
        "--text",
        "قِـفَا نَبْكِ!",
        "--strip-tashkeel",
        "--strip-tatweel",
        "--strip-punctuation",
    )
    assert res.returncode == 0
    assert "قفا نبك" in res.stdout.strip()
