# الدليل البرمجي الكامل لمكتبة PyArud (Python API Developer Guide)

توفر مكتبة `pyarud` واجهة برمجية عصرية ومرنة مكتوبة بلغة بايثون 3.10+ بدون أي اعتماديات خارجية (Zero-Dependency)، وتدعم بالكامل التلميحات النوعية الصارمة (PEP 561).

---

## 1. التثبيت والاستيراد السريع (Quick Imports)

```python
import pyarud

# الوظائف والمحركات الأساسية
from pyarud import (
    ArudhProcessor,     # المعالج الشامل للعروض والقافية
    ArudiConverter,     # محول الكتابة الصوتية والترميز الثنائي
    QafiyahAnalyzer,    # محلل القافية والروي
    scan,               # دالة الفحص السريع للأبيات
    analyze_verse,      # تحليل بيت واحد
    analyze_poem,       # تحليل قصيدة كاملة
    to_arudi,           # تحويل نص إلى كتابة عروضية
    get_qafiyah,        # استخراج القافية
    get_all_meters,     # قاموس جميع البحور وتفريعاتها
)

# منسقات التقارير
from pyarud import (
    format_verse_report,
    format_poem_report,
)

# نماذج البيانات المكتوبة (Data Classes)
from pyarud.models import (
    VerseAnalysis,
    PoemAnalysis,
    ShatrAnalysis,
    FootAnalysis,
    QafiyahAnalysis,
)
```

---

## 2. تحليل الأبيات الشعرية (Single Verse Analysis)

### استخدام `analyze_verse` أو `ArudhProcessor`

```python
from pyarud import analyze_verse, format_verse_report

# 1. تحليل بيت تام (صدر وعجز)
sadr = "قِفَا نَبْكِ مِنْ ذِكْرَى حَبِيبٍ وَمَنْزِلِ"
ajuz = "بِسِقْطِ اللِّوَى بَيْنَ الدَّخُولِ فَحَوْمَلِ"

res = analyze_verse(sadr, ajuz)

print("البحر:", res.meter_name_ar)         # بحر الطويل
print("المعرف:", res.meter_key)             # taweel
print("الحالة:", res.is_valid)              # True
print("درجة التوافق:", res.score)           # 0.999
print("الصدر عروضياً:", res.sadr.arudi_text)
print("العجز عروضياً:", res.ajuz.arudi_text)

# طباعة التقرير الشامل
print(format_verse_report(res))
```

### تحليل شطر واحد (مشطور أو منهوك أو تفعيلة مفردة)

```python
from pyarud import analyze_verse

# تمرير العجز كسلسلة فارغة
shatr_only = "أَخِي جَاوَزَ الظَّالِمُونَ الْمَدَى"
res = analyze_verse(shatr_only, "")

print("البحر:", res.meter_name_ar)     # بحر المتقارب
print("الصدر:", res.sadr.text)
assert res.ajuz is None
```

### فرض بحر محدد للتشخيص (Forced Meter)

```python
from pyarud import analyze_verse

sadr = "أَخِي جَاوَزَ الظَّالِمُونَ الْمَدَى"
ajuz = "وَهَذَا كَلامٌ ثَقِيلٌ جِدًّا"  # عجز مكسور

# فرض بحر المتقارب لاكتشاف موضع الكسر
res = analyze_verse(sadr, ajuz, forced_meter="mutakareb")

if not res.is_valid:
    print("العيوب المكتشفة:")
    for err in res.errors:
        print(" -", err)
    
    # فحص التفاعيل تفصيلياً
    for foot in res.ajuz.feet:
        if foot.status != "ok":
            print(f"تفعيلة مكسورة رقم {foot.foot_index + 1}: {foot.actual_segment} (المتوقع: {foot.expected_pattern})")
```

---

## 3. تحليل القصائد والمجموعات الشعرية (Poem Analysis)

```python
from pyarud import analyze_poem, format_poem_report

verses = [
    ("إِذَا غَامَرْتَ فِي شَرَفٍ مَرُومِ", "فَلَا تَقْنَعْ بِمَا دُونَ النُّجُومِ"),
    ("فَطَعْمُ الْمَوْتِ فِي أَمْرٍ حَقِيرٍ", "كَطَعْمِ الْمَوْتِ فِي أَمْرٍ عَظِيمِ"),
    ("سَتَبْكِي شَجْوَنَا فَرَسٌ وَمُهْرٌ", "صَفِيحُ الدَّمْعِ يَجْرِي فِي الرُّسُومِ"),
]

poem_res = analyze_poem(verses)

print("البحر المشترك:", poem_res.meter_name_ar)   # بحر الوافر
print("إجمالي الأبيات:", poem_res.total_verses)      # 3
print("الأبيات السليمة:", poem_res.valid_verses_count) # 3
print("متوسط التوافق:", poem_res.average_score)     # ~0.99
print("حرف الروي السائد:", poem_res.dominant_rawi)   # م
print("وحدة البحر:", poem_res.is_homogeneous)       # True

# تحويل القصيدة إلى قاموس JSON كامل
json_dict = poem_res.to_dict()
```

---

## 4. محرك الكتابة العروضية والترميز الصوتي (`ArudiConverter`)

```python
from pyarud import ArudiConverter, to_arudi

converter = ArudiConverter()

# 1. تحويل بسيط
text = "هَذَا بَيْتٌ جَمِيلٌ لِلشِّعْرِ"
arudi_text, pattern = converter.prepare_text(text)

print("الكتابة العروضية:", arudi_text)  # هاذا بيتون جميلن لششعري
print("الترميز الثنائي:", pattern)      # 10101010101101010

# 2. تخصيص قاموس الإملاء الصوتي لكلمات معينة
converter.register_custom_spelling("طاووس", "طاوووس")
converter.register_custom_spelling("داود", "داووود")
```

---

## 5. محرك القافية المستقل (`QafiyahAnalyzer`)

```python
from pyarud import QafiyahAnalyzer, get_qafiyah

# دالة سريعة
q = get_qafiyah("فَلَا تَقْنَعْ بِمَا دُونَ النُّجُومِ")

print("الروي:", q.rawi)                       # م
print("الردف:", q.ridf)                       # و
print("الوصل:", q.wasl)                       # None
print("نوع القافية:", q.qafiyah_type_ar)      # المتواتر
print("مقطع القافية:", q.qafiyah_text)        # النُّجُومِ
```

---

## 6. أدوات معالجة النصوص العربية (`pyarud.core.arabic`)

```python
from pyarud.core.arabic import (
    strip_tashkeel,
    strip_tatweel,
    strip_punctuation,
    normalize_orthography,
    normalize_ligatures,
    is_sun_letter,
    is_moon_letter,
    is_haraka,
    is_sukun,
    is_shadda,
    is_tanween,
)

sample = "قِـــفَا نَبْكِ!"
print(strip_tatweel(sample))       # قِفا نَبْكِ!
print(strip_tashkeel(sample))      # قـــفا نبك!
print(strip_punctuation(sample))   # قِـــفَا نَبْكِ
```
