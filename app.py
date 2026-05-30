import streamlit as st
import time
import pandas as pd
from openai import OpenAI

try:
    from tashaphyne.stemming import ArabicLightStemmer
    stemmer = ArabicLightStemmer()
    TASHAPHYNE_OK = True
except Exception:
    stemmer = None
    TASHAPHYNE_OK = False

# =========================================
# إعداد الصفحة
# =========================================
st.set_page_config(
    page_title="LABEEB AI - لبيب",
    page_icon="🧠",
    layout="wide"
)

# =========================================
# OpenRouter AI
# =========================================
client = None
if "OPENROUTER_API_KEY" in st.secrets:
    client = OpenAI(
        api_key=st.secrets["OPENROUTER_API_KEY"],
        base_url="https://openrouter.ai/api/v1"
    )

# =========================================
# CSS
# =========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&family=Poppins:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Cairo', sans-serif;
    direction: rtl;
    text-align: right;
}
.stApp {
    background: linear-gradient(135deg, #F8FAFC 0%, #F5F3FF 50%, #EFF6FF 100%) !important;
}
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stMain"] .block-container {
    max-width: 1140px;
    padding-top: 2rem;
    padding-bottom: 4rem;
    margin: 0 auto;
}
.hero-container {
    background: linear-gradient(135deg, rgba(255,255,255,0.85), rgba(243,232,255,0.7));
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.6);
    border-radius: 28px;
    padding: 45px 35px;
    text-align: center;
    box-shadow: 0 20px 40px rgba(109,40,217,0.03);
    margin-bottom: 30px;
}
.hero-inline {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 35px;
    flex-wrap: wrap;
    margin-bottom: 20px;
}
.brand-main {
    font-size: 52px;
    font-weight: 800;
    color: #4F46E5;
    font-family: 'Poppins', sans-serif;
    letter-spacing: 2px;
    margin-bottom: 6px;
}
.brand-sub {
    font-size: 15px;
    letter-spacing: 4px;
    color: #4338CA;
    font-weight: 700;
    direction: ltr;
    text-align: center;
}
.hero-logo-img {
    width: 160px; height: 160px;
    object-fit: cover; border-radius: 50%;
    box-shadow: 0 0 40px rgba(109,40,217,0.18);
}
.hero-subtitle { font-size: 22px; font-weight: 700; color: #1E293B; margin-bottom: 10px; }
.hero-desc { font-size: 16px; color: #64748B; max-width: 650px; margin: 0 auto 20px auto; line-height: 2; }
.badge-student {
    display: inline-block; background: rgba(255,255,255,0.9);
    border: 1px solid #E9D5FF; padding: 6px 20px;
    border-radius: 999px; font-size: 13px; font-weight: 700; color: #6D28D9;
}
.glass-card {
    background: rgba(255,255,255,0.92);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.5);
    border-radius: 22px; padding: 30px 35px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.04);
    margin-bottom: 25px;
}
.card-title { font-size: 22px; font-weight: 800; color: #4F46E5; margin-bottom: 10px; text-align: center; }
.card-desc { font-size: 16px; color: #64748B; text-align: center; line-height: 2; }
.stTextArea textarea {
    background: white !important;
    border-radius: 18px !important;
    border: 1px solid #E2E8F0 !important;
    padding: 20px !important; font-size: 17px !important;
    line-height: 2 !important; color: #1E293B !important;
    font-family: 'Cairo', sans-serif !important;
    direction: rtl !important; text-align: right !important;
    box-shadow: 0 4px 14px rgba(0,0,0,0.04) !important;
}
.stTextArea textarea:focus {
    border: 1px solid #8B5CF6 !important;
    box-shadow: 0 0 0 4px rgba(139,92,246,0.10) !important;
}
.stButton > button {
    background: linear-gradient(90deg, #4F46E5, #7C3AED) !important;
    color: white !important; border: none !important;
    border-radius: 18px !important; width: 100% !important;
    height: 58px !important; font-size: 17px !important;
    font-weight: 800 !important; font-family: 'Cairo', sans-serif !important;
    transition: 0.3s !important;
    box-shadow: 0 10px 24px rgba(79,70,229,0.25) !important;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 14px 28px rgba(79,70,229,0.35) !important;
}
.result-badge-container { display: flex; gap: 14px; margin-bottom: 20px; flex-wrap: wrap; }
.result-stat-box {
    flex: 1; background: white; border: 1px solid #F3E8FF;
    padding: 14px; border-radius: 14px; text-align: center; min-width: 120px;
}
.result-stat-label { font-size: 13px; color: #64748B; margin-bottom: 4px; }
.result-stat-val { font-size: 18px; font-weight: 700; color: #6D28D9; }
.ai-result-box {
    background: white; border-radius: 22px;
    padding: 30px 35px; margin-top: 20px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 8px 24px rgba(0,0,0,0.05);
    direction: rtl; text-align: right;
}
.ai-result-title { text-align: center; font-size: 24px; font-weight: 800; color: #4F46E5; margin-bottom: 18px; }
.ai-result-content { line-height: 2.8; color: #334155; font-size: 17px; white-space: pre-wrap; direction: rtl; text-align: right; }
.section-main-title { text-align: center; font-size: 26px; font-weight: 800; color: #1E293B; margin: 40px 0 20px 0; }
.step-card {
    background: white; border: 1px solid #F1F5F9;
    border-radius: 18px; padding: 24px; text-align: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.02);
}
.step-icon { font-size: 30px; margin-bottom: 10px; }
.step-title { font-size: 17px; font-weight: 700; color: #1E293B; margin-bottom: 8px; }
.step-desc { font-size: 14px; color: #64748B; line-height: 1.8; }
.researcher-card {
    background: white; border: 1px solid #EEF2F6;
    border-radius: 22px; padding: 28px 32px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.02);
    margin-top: 40px; direction: rtl;
}
.researcher-flex {
    display: flex; align-items: center;
    justify-content: flex-start; gap: 24px;
    direction: rtl; text-align: right; flex-wrap: wrap;
}
.researcher-img {
    width: 110px; height: 110px; border-radius: 50%;
    object-fit: cover; border: 3px solid #F3E8FF; flex-shrink: 0;
}
.researcher-name { font-size: 21px; font-weight: 800; color: #1E293B; margin-bottom: 4px; }
.researcher-title { font-size: 14px; font-weight: 600; color: #6D28D9; margin-bottom: 10px; line-height: 1.8; }
.researcher-bio { font-size: 14px; color: #475569; line-height: 1.9; }
.footer-text {
    text-align: center; color: #94A3B8; font-size: 13px;
    margin-top: 50px; border-top: 1px solid #E2E8F0; padding-top: 20px;
}
.divider { height: 1px; background: #F1F5F9; margin: 22px 0; }
.section-label {
    font-size: 13px; font-weight: 700; color: #94A3B8;
    text-transform: uppercase; letter-spacing: 2px;
    text-align: center; margin-bottom: 14px;
}
/* جدول النتائج — نص وسط + خط فاصل بين الخانتين */
[data-testid="stTable"] table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'Cairo', sans-serif;
    direction: rtl;
}
[data-testid="stTable"] table thead tr th {
    text-align: center !important;
    font-size: 14px;
    font-weight: 700;
    color: #6D28D9;
    padding: 12px 16px;
    background: #F9F5FF;
    border-bottom: 2px solid #E9D5FF;
}
[data-testid="stTable"] table thead tr th:first-child {
    border-left: 2px solid #E9D5FF;
}
[data-testid="stTable"] table tbody tr td {
    text-align: center !important;
    font-size: 15px;
    color: #334155;
    padding: 12px 16px;
    border-bottom: 1px solid #F1F5F9;
}
[data-testid="stTable"] table tbody tr td:first-child {
    border-left: 2px solid #E9D5FF;
    font-weight: 600;
    color: #1E293B;
}
[data-testid="stTable"] table tbody tr:last-child td {
    border-bottom: none;
}
[data-testid="stTable"] table tbody tr:hover td {
    background: #FAF5FF;
}
</style>
""", unsafe_allow_html=True)

# =========================================
# قاعدة البيانات المعجمية
# =========================================
semantic_db = {
    "روح": [
        {"المعنى": "النفس البشرية", "القرائن": {
            "موت": 5, "مات": 5, "توفي": 5, "حياة": 5, "جسد": 4, "جنة": 4,
            "إيمان": 3, "آخرة": 4, "دفن": 5, "فارق": 4, "رحل": 4, "وفاة": 5
        }},
        {"المعنى": "الراحة والطاقة الإيجابية", "القرائن": {
            "هدوء": 5, "راحة": 5, "سعادة": 4, "طمأنينة": 4, "صفاء": 3,
            "بهجة": 4, "انتعاش": 4, "فرح": 3, "نشاط": 3, "حيوية": 4
        }}
    ],
    "باب": [
        {"المعنى": "مدخل مادي", "القرائن": {
            "منزل": 5, "بيت": 5, "غرفة": 4, "قفل": 5, "مفتاح": 5,
            "فتح": 4, "طرق": 5, "دخل": 4, "خرج": 4, "أغلق": 5, "دار": 4
        }},
        {"المعنى": "فصل أو قسم", "القرائن": {
            "كتاب": 5, "فصل": 5, "عنوان": 4, "مبحث": 4, "علم": 3,
            "دراسة": 4, "بحث": 4, "أكاديمي": 3, "مؤلف": 3, "نحو": 3
        }}
    ],
    "كتاب": [
        {"المعنى": "مؤلف مطبوع", "القرائن": {
            "قراءة": 5, "مكتبة": 5, "صفحات": 4, "رواية": 4, "مؤلف": 4,
            "طبع": 4, "اقتنى": 3, "قرأ": 5, "ورق": 3, "فصل": 3
        }},
        {"المعنى": "فرض أو حكم", "القرائن": {
            "شرع": 5, "دين": 4, "واجب": 4, "فرض": 5,
            "الله": 4, "قرآن": 4, "حرام": 4, "حلال": 4
        }}
    ],
    "بحر": [
        {"المعنى": "مسطح مائي", "القرائن": {
            "ماء": 5, "موج": 5, "سفينة": 4, "شاطئ": 4, "غرق": 5,
            "سباحة": 4, "مد": 4, "جزر": 4, "ملاحة": 4, "صيد": 4, "أمواج": 5
        }},
        {"المعنى": "العلم الواسع", "القرائن": {
            "علم": 5, "معرفة": 4, "عبقري": 3, "فهم": 3, "ثقافة": 3,
            "أستاذ": 4, "عالم": 5, "تخصص": 3, "إتقان": 4, "خبرة": 4
        }}
    ],
    "مفتاح": [
        {"المعنى": "أداة فتح", "القرائن": {
            "باب": 5, "قفل": 5, "فتح": 4, "حديد": 3, "منزل": 3,
            "درج": 4, "سيارة": 3, "ثقب": 4, "خزنة": 4, "أغلق": 4
        }},
        {"المعنى": "حل أو وسيلة", "القرائن": {
            "نجاح": 5, "حل": 5, "سر": 4, "فهم": 3, "مشكلة": 4,
            "تقدم": 4, "تميز": 3, "وصول": 4, "هدف": 4, "إنجاز": 4
        }}
    ],
    "عين": [
        {"المعنى": "عضو البصر", "القرائن": {
            "نظر": 5, "رؤية": 5, "يبصر": 5, "دموع": 4, "بصر": 5,
            "عمى": 5, "جندي": 4, "معركة": 4, "جرح": 5, "إصابة": 5,
            "فقد": 4, "أصيب": 5, "طبيب": 3, "ألم": 3, "حرب": 4,
            "شاهد": 4, "رأى": 4, "أبصر": 5, "عدسة": 4, "نظارة": 4
        }},
        {"المعنى": "نبع ماء", "القرائن": {
            "ماء": 5, "نبع": 5, "جارية": 4, "بئر": 4, "تدفقت": 4,
            "وادي": 4, "جبل": 3, "صخر": 3, "ينبوع": 5, "مياه": 4, "شرب": 4
        }},
        {"المعنى": "جاسوس", "القرائن": {
            "عدو": 4, "تجسس": 5, "مخابرات": 5, "سر": 4, "عميل": 5,
            "اختراق": 5, "معلومات": 4, "استخبارات": 5, "رصد": 4, "تقرير": 3
        }}
    ],
    "قلب": [
        {"المعنى": "عضو في جسم الإنسان", "القرائن": {
            "نبض": 5, "دم": 4, "طبيب": 4, "مرض": 5, "جراحة": 5,
            "مستشفى": 5, "ضغط": 4, "شريان": 5, "أزمة": 4, "نوبة": 5,
            "عملية": 5, "صدر": 4, "رئة": 4
        }},
        {"المعنى": "العاطفة والمشاعر", "القرائن": {
            "حب": 5, "اشتياق": 4, "مشاعر": 5, "هيام": 4, "شوق": 5,
            "حزن": 4, "فرح": 3, "وجد": 4, "غرام": 5, "احترق": 5,
            "تألم": 4, "عشق": 5, "لوعة": 5, "هوى": 4
        }},
        {"المعنى": "المركز أو الوسط", "القرائن": {
            "المدينة": 4, "المركز": 5, "وسط": 5, "الحي": 3, "البلاد": 3,
            "العاصمة": 4, "المنطقة": 3, "الحضارة": 3, "موقع": 3
        }}
    ],
    "رأس": [
        {"المعنى": "جزء من جسم الإنسان", "القرائن": {
            "شعر": 4, "صداع": 5, "دماغ": 5, "تفكير": 4, "وجه": 4,
            "رقبة": 4, "خوذة": 5, "جرح": 4, "ضربة": 4, "كسر": 4, "مخ": 5
        }},
        {"المعنى": "قمة أو أعلى شيء", "القرائن": {
            "جبل": 5, "قمة": 5, "مرتفع": 4, "صخور": 3, "تسلق": 4,
            "ارتفاع": 4, "ذروة": 5, "منحدر": 4, "علو": 4
        }}
    ],
    "يد": [
        {"المعنى": "عضو في جسم الإنسان", "القرائن": {
            "أصابع": 5, "كف": 5, "لمس": 4, "ذراع": 4, "كتابة": 3,
            "بطش": 4, "ضرب": 4, "إمساك": 4, "جرح": 4, "بتر": 5, "رسغ": 5
        }},
        {"المعنى": "المساعدة أو الدعم", "القرائن": {
            "مساعدة": 5, "عون": 5, "دعم": 4, "ساند": 4, "خدمة": 3,
            "تعاون": 4, "أسهم": 3, "أسند": 4, "بذل": 4, "قدم": 3
        }}
    ],
    "نور": [
        {"المعنى": "الضوء الحقيقي", "القرائن": {
            "شمس": 5, "ضوء": 5, "مصباح": 4, "ظلام": 4, "إضاءة": 5,
            "قمر": 4, "شعاع": 5, "انبثق": 4, "أنار": 5, "سطع": 5, "نجم": 3
        }},
        {"المعنى": "الهداية أو المعرفة", "القرائن": {
            "هداية": 5, "علم": 4, "معرفة": 5, "إيمان": 4, "حق": 3,
            "دين": 4, "قرآن": 4, "إسلام": 3, "تقوى": 4, "رشد": 4
        }}
    ]
}

# =========================================
# HERO SECTION
# =========================================
st.markdown("""
<div class="hero-container">
    <div class="hero-inline">
        <div>
            <div class="brand-main">✦ LABEEB AI</div>
            <div class="brand-sub">CONTEXTUAL SEMANTIC ANALYZER</div>
        </div>
        <img src="https://raw.githubusercontent.com/hzouaki-ship-it/labeeb-ai/main/logo.png" class="hero-logo-img">
    </div>
    <div class="hero-subtitle">المحلل الدلالي الذكي لفهم المعنى والسياق في اللغة العربية</div>
    <div class="hero-desc">منصة تعتمد على الذكاء الاصطناعي لفهم المعنى والسياق وتحليل الدلالة في اللغة العربية.</div>
    <div class="badge-student">© 2026 — هاجر الزواكي</div>
</div>
""", unsafe_allow_html=True)

# =========================================
# بطاقة الإدخال
# =========================================
st.markdown("""
<div class="glass-card">
    <div class="card-title">🧠 التحليل الدلالي الذكي</div>
    <div class="card-desc">أدخل جملة عربية وسيقوم لبيب بتحليل المعنى والسياق اعتمادًا على الخوارزمية المحلية والذكاء الاصطناعي معاً.</div>
</div>
""", unsafe_allow_html=True)

user_text = st.text_area(
    "",
    placeholder="مثال: فقد الجندي عينه في المعركة...",
    height=180,
    label_visibility="collapsed"
)

submit_btn = st.button("⚡ تشغيل التحليل الذكي")

# =========================================
# التحليل
# =========================================
if submit_btn and user_text.strip():
    with st.spinner("⏳ يجري تحليل المتجهات والروابط السياقية..."):
        time.sleep(0.5)

        # --- المرحلة 1: الخوارزمية المحلية ---
        detected_keyword = None
        for word in semantic_db.keys():
            variants = [word, word + "ه", word + "ها", word + "ي", "ال" + word]
            if any(v in user_text for v in variants):
                detected_keyword = word
                break

        local_result_html = ""
        predicted_meaning = ""
        highest_score = 0.0

        if detected_keyword:
            results_list = []
            meanings = semantic_db[detected_keyword]
            tokens = set(user_text.replace("،","").replace(".","").split())
            raw_scores = []

            for entry in meanings:
                weighted_sum = 0
                for clue, weight in entry["القرائن"].items():
                    found = False
                    # مطابقة مباشرة بالكلمة أو جزء منها
                    if clue in user_text:
                        found = True
                    else:
                        # مطابقة بكل رمز في الجملة
                        for token in tokens:
                            if clue in token or token in clue:
                                found = True
                                break
                        # مطابقة بالجذر إن كان tashaphyne متاحاً
                        if not found and TASHAPHYNE_OK and stemmer:
                            try:
                                stemmer.light_stem(clue)
                                c_stem = stemmer.get_stem()
                                for token in tokens:
                                    stemmer.light_stem(token)
                                    t_stem = stemmer.get_stem()
                                    if c_stem and t_stem and len(c_stem) >= 3 and c_stem == t_stem:
                                        found = True
                                        break
                            except Exception:
                                pass
                    if found:
                        weighted_sum += weight

                raw_scores.append(float(weighted_sum))

            # إذا كانت كل النتائج صفراً، نوزع بالتساوي مع إشارة
            all_zero = all(s == 0 for s in raw_scores)
            if all_zero:
                normalized = [1.0 / len(raw_scores)] * len(raw_scores)
            else:
                # softmax بمعامل حرارة 0.5 لتضخيم الفروق
                import math
                temp = 0.5
                exp_scores = [math.exp(s / temp) for s in raw_scores]
                total_exp = sum(exp_scores)
                normalized = [e / total_exp for e in exp_scores]

            for i, entry in enumerate(meanings):
                score = normalized[i]
                if score > highest_score:
                    highest_score = score
                    predicted_meaning = entry["المعنى"]
                results_list.append({
                    "المعنى المحتمل": entry["المعنى"],
                    "نسبة القرب": f"{score * 100:.1f}%",
                    "_raw": score
                })

            df = pd.DataFrame(results_list).sort_values("_raw", ascending=False).drop(columns=["_raw"])

            local_result_html = f"""
<div class="section-label">① نتيجة الخوارزمية المحلية</div>
<div class="result-badge-container">
    <div class="result-stat-box">
        <div class="result-stat-label">الكلمة المرصودة</div>
        <div class="result-stat-val">{detected_keyword}</div>
    </div>
    <div class="result-stat-box">
        <div class="result-stat-label">المعنى الأقرب</div>
        <div class="result-stat-val">{predicted_meaning}</div>
    </div>
    <div class="result-stat-box">
        <div class="result-stat-label">نسبة القرب الدلالي</div>
        <div class="result-stat-val">{highest_score * 100:.1f}%</div>
    </div>
</div>
"""
        else:
            local_result_html = """
<div class="section-label">① الخوارزمية المحلية</div>
<div style="text-align:center; color:#94A3B8; font-size:15px; padding:16px 0;">
    ⚠️ لم يُرصد لفظ مشترك في قاعدة البيانات — سيعتمد التحليل على الذكاء الاصطناعي فقط.
</div>
"""

        # --- المرحلة 2: الذكاء الاصطناعي ---
        ai_analysis = ""
        if client:
            try:
                context_hint = f"الكلمة المرصودة محلياً: «{detected_keyword}» — المعنى المرجّح: «{predicted_meaning}»\n\n" if detected_keyword else ""
                response = client.chat.completions.create(
                    model="openrouter/auto",
                    messages=[
                        {
                            "role": "system",
                            "content": """أنت محلل دلالي عربي متخصص.
حلل الجملة اعتماداً على السياق الدلالي.
أجب بهذا الشكل الثابت:
• اللفظ المحوري:
• المعنى المقصود:
• نوع الاستعمال: (حقيقي / مجازي)
• التفسير:
• نسبة الثقة:
يجب أن يكون الجواب واضحاً، مختصراً، وأكاديمياً."""
                        },
                        {
                            "role": "user",
                            "content": context_hint + user_text
                        }
                    ]
                )
                ai_analysis = response.choices[0].message.content
            except Exception as e:
                ai_analysis = f"حدث خطأ في الاتصال بالذكاء الاصطناعي: {e}"
        else:
            ai_analysis = "لم يتم العثور على مفتاح OpenRouter.\nتأكدي من إضافة OPENROUTER_API_KEY في إعدادات Streamlit Cloud."

        # --- عرض النتائج ---
        st.markdown(f"""
<div class="ai-result-box">
    {local_result_html}
""", unsafe_allow_html=True)

        if detected_keyword:
            st.table(df.reset_index(drop=True))

        st.markdown(f"""
    <div class="divider"></div>
    <div class="section-label">② تحليل الذكاء الاصطناعي المعمّق</div>
    <div class="ai-result-content">{ai_analysis.replace("**", "")}</div>
</div>
""", unsafe_allow_html=True)

# =========================================
# كيف يعمل لبيب؟
# =========================================
st.markdown('<div class="section-main-title">كيف يعمل لبيب؟</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""<div class="step-card">
    <div class="step-icon">🔎</div>
    <div class="step-title">تحليل السياق</div>
    <div class="step-desc">يفحص النظام البنية التركيبية المحيطة باللفظ ويعزل الكلمات المحورية بدقة عبر الخوارزمية المحلية.</div>
</div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""<div class="step-card">
    <div class="step-icon">✨</div>
    <div class="step-title">اكتشاف المعنى</div>
    <div class="step-desc">تُطابق البيئة السياقية مع الحقول المعجمية ثم يُعمّق الذكاء الاصطناعي التفسير ويرجّح المعنى الأدق.</div>
</div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""<div class="step-card">
    <div class="step-icon">📊</div>
    <div class="step-title">قياس التشابه الدلالي</div>
    <div class="step-desc">يتم حساب أوزان المطابقة الإحصائية وإنتاج جدول يرتب الاحتمالات بحسب النسبة، معززاً بتحليل لغوي أكاديمي.</div>
</div>""", unsafe_allow_html=True)

# =========================================
# بطاقة الباحثة
# =========================================
st.markdown("""
<div class="researcher-card">
    <div class="researcher-flex">
        <img src="https://raw.githubusercontent.com/hzouaki-ship-it/labeeb-ai/main/hajar.jpg"
             class="researcher-img" alt="هاجر الزواكي">
        <div>
            <div class="researcher-name">هاجر الزواكي</div>
            <div class="researcher-title">طالبة ماستر في اللسانيات الرقمية والعربية<br>كلية الآداب والعلوم الإنسانية — جامعة مولاي إسماعيل، مكناس</div>
            <div class="researcher-bio">مهتمة بالذكاء الاصطناعي ومعالجة اللغة العربية وبناء الأنظمة الدلالية الذكية، وأسعى إلى تطوير حلول رقمية حديثة لفهم اللغة العربية وتحليل السياق والمعنى.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================
# التذييل
# =========================================
st.markdown('<div class="footer-text">LABEEB AI © 2026 — جميع الحقوق محفوظة — هاجر الزواكي</div>', unsafe_allow_html=True)
