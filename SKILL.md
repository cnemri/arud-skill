---
name: arud-skill
description: >-
  Comprehensive Arabic Prosody (علم العروض), Metric Scansion (التقطيع العروضي),
  and Rhyme Analysis (علم القافية والروي) powered by the deterministic Farahidian
  engine `pyarud`. Use whenever you need to: scan Arabic verses or multi-line
  poems, identify one of the 16 classical meters (البحور الستة عشر) or their
  sub-variations (تام، مجزوء، مشطور، منهوك، مخلع), diagnose poetic defects (الزحافات
  والعلل), detect broken feet (كسر عروضي), perform phonetic Arudi transcription
  (الكتابة العروضية والترميز الثنائي 1/0), or extract comprehensive rhyme features
  (حرف الروي، حركته، الوصل، الخروج، الردف، التأسيس، الدخيل، نوع القافية).
---

# مهام ومهارات علم العروض والقافية (Arud & Arabic Prosody Skill)

تُمكِّن هذه المهارة الوكيل الذكي (AI Agent) والمطوِّر من تسخير كافة قدرات مكتبة `pyarud` (محرك الفراهيدي الحتمي عالي السرعة لتقطيع الشعر العربي).

---

## متى تُستخدم هذه المهارة (When to Use)

يجب تفعيل هذه المهارة فوراً عند مواجهة أي من الحالات التالية:
1. **التقطيع وتحديد البحر (Meter Scansion)**: التحقق من وزن بيت أو قصيدة ومعرفة بحرها الشعري من بين البحور الستة عشر وتفريعاتها (*تام، مجزوء، مشطور، منهوك، مخلع*).
2. **الكتابة العروضية والترميز الثنائي (Phonetic & Binary Transcription)**: تحويل النص المشكول إلى ما يُنطق به صوتياً وإسقاط السواكن والمتحركات (`1` للمتحرك، `0` للساكن).
3. **تشخيص الكسور والعلل (Defect Localization & Debugging)**: تحديد التفعيلة المكسورة تحديداً دقيقاً، أو معرفة الزحافات (*إضمار، خبن، طي، عصب، قبض، كف، خبل، شكل*) والعلل (*حذف، قطف، قطع، بتر، ترفيل، تذييل، تسبيغ، قصر، حذذ، صلم*).
4. **علم القافية والروي (Rhyme & Rawi Extraction)**: استخراج حرف الروي، حركته، الوصل، الخروج، الردف، التأسيس، الدخيل، وتصنيف القافية إيقاعياً (*المتواتر، المتدارك، المتراكب، المتكاوس، المترادف*)، وحالتها (*مطلقة، مقيدة*).
5. **معالجة وتنظيف النصوص الشعرية (Arabic Text Normalization)**: إزالة التشكيل أو التطويل أو علامات الترقيم وتوحيد الإملاء والهمزات.

---

## 1. أداة سطر الأوامر (CLI Utility: `arud_cli.py`)

يتوفر في مجلد المهارة سكربت تنفيذي كامل وسريع: [`scripts/arud_cli.py`](scripts/arud_cli.py).

### أوامر التقطيع والفحص (Scansion Commands)

#### أ. تقطيع بيت شعر مفرد (Scan Single Verse)
```bash
# تقطيع بيت مشكول (صدر وعجز)
uv run python scripts/arud_cli.py scan-verse \
  --sadr "قِفَا نَبْكِ مِنْ ذِكْرَى حَبِيبٍ وَمَنْزِلِ" \
  --ajuz "بِسِقْطِ اللِّوَى بَيْنَ الدَّخُولِ فَحَوْمَلِ"

# تقطيع بيت في سطر واحد بفاصل قياسي (* أو ...)
uv run python scripts/arud_cli.py scan-verse \
  --verse "إِذَا غَامَرْتَ فِي شَرَفٍ مَرُومِ * فَلَا تَقْنَعْ بِمَا دُونَ النُّجُومِ"

# إخراج النتائج بصيغة JSON
uv run python scripts/arud_cli.py scan-verse \
  --verse "عَلَى قَدْرِ أَهْلِ العَزْمِ تَأْتِي العَزَائِمُ" --json
```

#### ب. تقطيع قصيدة كاملة (Scan Multi-Verse Poem)
```bash
# تحليل ملف نصي يحتوي على أبيات القصيدة
uv run python scripts/arud_cli.py scan-poem --file /path/to/poem.txt

# تحليل نص متعدد الأبيات مباشرة مع تصدير التقرير
uv run python scripts/arud_cli.py scan-poem \
  --text "إِذَا غَامَرْتَ فِي شَرَفٍ مَرُومِ * فَلَا تَقْنَعْ بِمَا دُونَ النُّجُومِ\nفَطَعْمُ الْمَوْتِ فِي أَمْرٍ حَقِيرٍ * كَطَعْمِ الْمَوْتِ فِي أَمْرٍ عَظِيمِ" \
  --output poem_report.txt
```

---

### أوامر الصوتيات والترميز الثنائي (Phonetics & Binary)

```bash
# تحويل نص مشكول إلى كتابة عروضية ونمط ثنائي (1=متحرك، 0=ساكن)
uv run python scripts/arud_cli.py phonetics \
  --text "عَلَى قَدْرِ أَهْلِ العَزْمِ تَأْتِي العَزَائِمُ"

# الإخراج كـ JSON
uv run python scripts/arud_cli.py phonetics \
  --text "هَذَا بَيْتٌ جَمِيلٌ" --json
```

---

### أوامر علم القافية والروي (Qafiyah & Rawi Analysis)

```bash
# تحليل قافية وروي عجز البيت
uv run python scripts/arud_cli.py qafiyah \
  --text "فَلَا تَقْنَعْ بِمَا دُونَ النُّجُومِ"

# فحص روي ساكن (قافية مقيدة)
uv run python scripts/arud_cli.py qafiyah \
  --text "وَكُلُّ الَّذِي فَوْقَ التُّرَابِ تُرَابْ" --muqayyad
```

---

### أوامر تشخيص الكسور والعلل (Defect Diagnosis)

```bash
# تشخيص مواضع الخلل في التفاعيل
uv run python scripts/arud_cli.py diagnose \
  --sadr "أَخِي جَاوَزَ الظَّالِمُونَ الْمَدَى" \
  --ajuz "وَهَذَا كَلامٌ ثَقِيلٌ جِدًّا" \
  --meter mutakareb
```

---

### استعراض البحور وقاموس التفاعيل (Meters Directory)

```bash
# استعراض كافة البحور الستة عشر وتفريعاتها الـ 29
uv run python scripts/arud_cli.py meters

# فحص بحر معين بالتفصيل
uv run python scripts/arud_cli.py meters --key taweel
```

---

## 2. الدليل البرمجي في بايثون (Python Developer Workflows)

### أ. فحص وتقطيع الأبيات (Verse Analysis)

```python
from pyarud import analyze_verse, format_verse_report

sadr = "إِذَا غَامَرْتَ فِي شَرَفٍ مَرُومِ"
ajuz = "فَلَا تَقْنَعْ بِمَا دُونَ النُّجُومِ"

verse = analyze_verse(sadr, ajuz)

print(f"البحر: {verse.meter_name_ar} ({verse.meter_key})")
print(f"الحالة: {'سليم موزون' if verse.is_valid else 'مكسور'}")
print(f"درجة التوافق: {verse.score * 100:.1f}%")

# فحص تفاعيل الصدر
for foot in verse.sadr.feet:
    print(f"  • تفعيلة: {foot.actual_tafeela or foot.base_tafeela} [{foot.actual_segment}] - {foot.zihaf_name_ar}")

# تقرير نصي منسق
print(format_verse_report(verse))
```

---

### ب. تحليل قصيدة متكاملة (Poem Scansion & Consensus)

```python
from pyarud import analyze_poem, format_poem_report

verses = [
    ("إِذَا رَأَيْتَ نُيُوبَ اللَّيْثِ بَارِزَةً", "فَلَا تَظُنَّنَّ أَنَّ اللَّيْثَ يَبْتَسِمُ"),
    ("وَمُهْجَةٍ سُقْتُهَا فِي مَفْرِقِ الْخَطَرِ", "مَا نَالَ صَاحِبُهَا مَجْدًا وَلَا كَرَمُ"),
]

poem = analyze_poem(verses)

print(f"البحر السائد: {poem.meter_name_ar}")
print(f"عدد الأبيات السليمة: {poem.valid_verses_count}/{poem.total_verses}")
print(f"الروي السائد: {poem.dominant_rawi}")
print(f"تجانس القصيدة: {poem.is_homogeneous}")
```

---

### ج. تحويل الكتابة الصوتية وتخصيص الكلمات الشاذة

```python
from pyarud import ArudiConverter

converter = ArudiConverter()

# إضافة كلمات ذات كتابة إملائية خاصة
converter.register_custom_spelling("طاووس", "طاوووس")
converter.register_custom_spelling("داود", "داووود")

arudi_text, pattern = converter.prepare_text("رَأَيْتُ طَاوُوسَ الجَمَالِ")
print("العروضي:", arudi_text)
print("الترميز:", pattern)
```

---

### د. تحليل تفصيلي للقافية (Rhyme Breakdown)

```python
from pyarud import QafiyahAnalyzer

analyzer = QafiyahAnalyzer()
q = analyzer.analyze("فَلَا تَقْنَعْ بِمَا دُونَ النُّجُومِ")

print(f"حرف الروي: {q.rawi} (حركته: {q.rawi_haraka})")
print(f"الردف: {q.ridf}")
print(f"التأسيس: {q.tasees} (الدخيل: {q.dakhil})")
print(f"الوصل: {q.wasl} | الخروج: {q.khuruj}")
print(f"نوع القافية: {q.qafiyah_type_ar}")
print(f"التصنيف: {q.rhyme_classification}")
print(f"مقطع القافية: {q.qafiyah_text} [{q.qafiyah_pattern}]")
```

---

## 3. المراجع التفصيلية الملحقة (References)

تتضمن هذه المهارة أدلة مرجعية شاملة يمكن الرجوع إليها عند الحاجة:
- [`references/buhur_reference.md`](references/buhur_reference.md): الدليل الشامل لكافة البحور الستة عشر ومفاتيحها وأنماطها الثنائية وتفريعاتها وقواعد التمييز بين المتشابهات.
- [`references/zihafs_ilal_reference.md`](references/zihafs_ilal_reference.md): معجم الزحافات المفردة والمزدوجة وعلل الزيادة والنقص وجدول التكلفة الحسابية.
- [`references/qafiyah_reference.md`](references/qafiyah_reference.md): الدليل الموسع لعلم القافية وحروفها الستة وحركاتها وتصنيفاتها الإيقاعية.
- [`references/api_guide.md`](references/api_guide.md): دليل المطورين البرمجي لكافة فئات ونماذج ودوال الحزمة.

---

## 4. الأمثلة الجاهزة للتنفيذ (Examples)

- [`examples/basic_scansion.py`](examples/basic_scansion.py): تقطيع بيت معلقة امرئ القيس وتقطيع شطر مفرد.
- [`examples/poem_batch_analysis.py`](examples/poem_batch_analysis.py): تقطيع قصيدة أبي الطيب المتنبي وحساب الروي السائد والتجانس.
- [`examples/defect_debugger.py`](examples/defect_debugger.py): تشخيص بيت مكسور في بحر المتقارب واكتشاف التفعيلة المعيبة.
- [`examples/rhyme_extractor.py`](examples/rhyme_extractor.py): استخراج القافية والروي وحروف المد لنماذج شعرية متعددة.
- [`examples/custom_phonetics.py`](examples/custom_phonetics.py): تخصيص قواعد الإملاء الصوتي للكلمات الشاذة.
