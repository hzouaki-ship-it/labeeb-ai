import streamlit as st
import time
import math
import pandas as pd
from openai import OpenAI

# =========================================
# إعداد الصفحة
# =========================================
st.set_page_config(
    page_title="LABEEB AI - لبيب",
    page_icon="🧠",
    layout="wide"
)

# =========================================
# ✅ Groq
# =========================================
client = None
if "GROQ_API_KEY" in st.secrets:
    client = OpenAI(
        api_key=st.secrets["GROQ_API_KEY"],
        base_url="https://api.groq.com/openai/v1"
    )

GROQ_MODEL = "llama-3.3-70b-versatile"

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
    "عين": [
        {"المعنى": "عضو البصر", "القرائن": {
            "نظر": 5, "رؤية": 5, "يبصر": 5, "دموع": 4, "بصر": 5,
            "عمى": 5, "جندي": 4, "معركة": 4, "جرح": 5, "إصابة": 5
        }},
        {"المعنى": "نبع ماء", "القرائن": {
            "ماء": 5, "نبع": 5, "جارية": 4, "بئر": 4, "تدفقت": 4,
            "وادي": 4, "جبل": 3, "ينبوع": 5, "مياه": 4, "شرب": 4
        }},
        {"المعنى": "جاسوس", "القرائن": {
            "عدو": 4, "تجسس": 5, "مخابرات": 5, "سر": 4, "عميل": 5,
            "اختراق": 5, "معلومات": 4, "استخبارات": 5
        }}
    ],
    "قلب": [
        {"المعنى": "عضو في جسم الإنسان", "القرائن": {
            "نبض": 5, "دم": 4, "طبيب": 4, "مرض": 5, "جراحة": 5,
            "مستشفى": 5, "ضغط": 4, "شريان": 5, "أزمة": 4, "نوبة": 5
        }},
        {"المعنى": "العاطفة والمشاعر", "القرائن": {
            "حب": 5, "اشتياق": 4, "مشاعر": 5, "هيام": 4, "شوق": 5,
            "حزن": 4, "غرام": 5, "احترق": 5, "عشق": 5, "لوعة": 5
        }},
        {"المعنى": "المركز أو الوسط", "القرائن": {
            "المدينة": 4, "المركز": 5, "وسط": 5, "البلاد": 3,
            "العاصمة": 4, "المنطقة": 3, "الحضارة": 3
        }}
    ],
    "بحر": [
        {"المعنى": "مسطح مائي", "القرائن": {
            "ماء": 5, "موج": 5, "سفينة": 4, "شاطئ": 4, "غرق": 5,
            "سباحة": 4, "مد": 4, "صيد": 4, "أمواج": 5
        }},
        {"المعنى": "العلم الواسع", "القرائن": {
            "علم": 5, "معرفة": 4, "عبقري": 3, "فهم": 3,
            "أستاذ": 4, "عالم": 5, "إتقان": 4, "خبرة": 4
        }}
    ],
    "نور": [
        {"المعنى": "الضوء الحقيقي", "القرائن": {
            "شمس": 5, "ضوء": 5, "مصباح": 4, "ظلام": 4, "إضاءة": 5,
            "قمر": 4, "شعاع": 5, "أنار": 5, "سطع": 5
        }},
        {"المعنى": "الهداية أو المعرفة", "القرائن": {
            "هداية": 5, "علم": 4, "معرفة": 5, "إيمان": 4,
            "دين": 4, "قرآن": 4, "تقوى": 4, "رشد": 4
        }}
    ],
    "أسد": [
        {"المعنى": "حيوان مفترس", "القرائن": {
            "غابة": 5, "فريسة": 5, "زئير": 5, "مخلب": 5, "صيد": 4,
            "حديقة الحيوان": 4, "ضاري": 4, "افترس": 5
        }},
        {"المعنى": "الشجاعة والبطولة", "القرائن": {
            "شجاعة": 5, "بطولة": 5, "جرأة": 4, "مقاتل": 4,
            "جندي": 4, "قائد": 4, "بسالة": 5, "نضال": 4
        }}
    ],
    "سيف": [
        {"المعنى": "سلاح حاد", "القرائن": {
            "معركة": 5, "حرب": 5, "قتال": 5, "ضرب": 4,
            "دم": 4, "غمد": 5, "فارس": 4, "حديد": 4
        }},
        {"المعنى": "القوة أو الحجة القاطعة", "القرائن": {
            "حجة": 5, "برهان": 4, "رد": 4, "جدل": 4,
            "قاطع": 5, "حسم": 4, "إفحام": 5, "نقاش": 3
        }}
    ],
}

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
.result-card {
    background: linear-gradient(135deg, #FAFAFA 0%, #F5F3FF 100%);
    border: 1px solid #E9D5FF;
    border-radius: 26px;
    padding: 36px 40px;
    margin-top: 24px;
    box-shadow: 0 12px 40px rgba(109,40,217,0.07);
    direction: rtl;
}
.result-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    margin-bottom: 28px;
    gap: 12px;
}
.result-title { font-size: 20px; font-weight: 800; color: #4F46E5; }
.result-source-pill {
    font-size: 12px; font-weight: 700; padding: 5px 16px;
    border-radius: 999px; display: inline-block;
}
.pill-local { background: #EDE9FE; color: #6D28D9; }
.pill-ai    { background: #F0FDF4; color: #16A34A; }
.result-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 14px;
    margin-bottom: 26px;
}
.result-cell {
    background: white;
    border: 1px solid #F3E8FF;
    border-radius: 16px;
    padding: 16px 18px;
    text-align: center;
}
.result-cell-icon { font-size: 22px; margin-bottom: 6px; }
.result-cell-label { font-size: 11px; color: #94A3B8; font-weight: 700;
    text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }
.result-cell-val { font-size: 17px; font-weight: 800; color: #1E293B; }
.result-divider { height: 1px; background: linear-gradient(90deg,transparent,#E9D5FF,transparent); margin: 22px 0; }
.result-interp {
    background: white; border-right: 4px solid #7C3AED;
    border-radius: 0 14px 14px 0; padding: 16px 20px;
    font-size: 15px; color: #334155; line-height: 2; margin-bottom: 18px;
}
.result-confidence {
    display: flex; align-items: center; gap: 12px; direction: rtl;
}
.conf-label { font-size: 13px; color: #64748B; font-weight: 700; white-space: nowrap; }
.conf-bar-wrap { flex: 1; background: #F1F5F9; border-radius: 999px; height: 10px; overflow: hidden; }
.conf-bar { height: 10px; border-radius: 999px;
    background: linear-gradient(90deg, #7C3AED, #4F46E5); }
.conf-pct { font-size: 14px; font-weight: 800; color: #4F46E5; white-space: nowrap; }
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
</style>
""", unsafe_allow_html=True)

# =========================================
# Session State
# =========================================
if "history" not in st.session_state:
    st.session_state.history = []

# =========================================
# ✅ الحل الجذري: استخراج اللفظ المحوري عبر Groq
# =========================================
def extract_pivot_word_via_groq(sentence: str, groq_client) -> str:
    """
    يستخدم Groq لاستخراج اللفظ المحوري (الكلمة المشتركة لفظياً) من أي جملة عربية.
    هذا يضمن التعرف على أي كلمة بغض النظر عن تصريفها أو تنوينها.
    """
    if not groq_client:
        return "—"
    try:
        prompt = (
            "أنت خبير في علم الدلالة العربية وتحليل الاشتراك اللفظي.\n\n"
            "الجملة: «" + sentence + "»\n\n"
            "المطلوب: حدد الكلمة المحورية الواحدة في هذه الجملة التي تحمل اشتراكاً لفظياً "
            "(أي لها أكثر من معنى محتمل بحسب السياق).\n\n"
            "قواعد صارمة:\n"
            "- أرجع الكلمة في صيغتها المجردة أو كما وردت في الجملة.\n"
            "- لا ترجع حروف جر أو ضمائر أو أسماء إشارة أو كلمات وظيفية.\n"
            "- أرجع كلمة واحدة فقط بدون أي شرح أو علامات ترقيم.\n"
            "- إذا لم تجد كلمة مشتركة واضحة، أرجع الاسم أو الفعل الأبرز في الجملة."
        )
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=20,
            temperature=0.1
        )
        result = response.choices[0].message.content.strip()
        result = result.strip("«».,،؟!:؛-\"\' ")
        return result if result else "—"
    except Exception as e:
        return "—"


# =========================================
# دالة التحليل الدلالي الكامل عبر Groq
# =========================================
def analyze_via_groq(sentence: str, pivot_word: str, groq_client) -> dict:
    """
    يحلل الجملة دلالياً بعد معرفة اللفظ المحوري.
    """
    if not groq_client:
        return {
            "keyword": pivot_word,
            "meaning": "—",
            "usage": "—",
            "interp": "تعذّر الاتصال بـ Groq.",
            "conf": 85
        }

    # تحقق إذا كانت الكلمة موجودة في القاعدة المحلية
    db_context = ""
    pivot_in_db = pivot_word in semantic_db
    if pivot_in_db:
        meanings_text = " | ".join(
            e["المعنى"] + ": " + ", ".join(list(e["القرائن"].keys())[:5])
            for e in semantic_db[pivot_word]
        )
        db_context = (
            "[معلومة من القاعدة المحلية] الكلمة «" + pivot_word +
            "» لها المعاني التالية مع قرائنها: " + meanings_text + "\n\n"
        )

    try:
        user_prompt = (
            db_context +
            "اللفظ المحوري: «" + pivot_word + "»\n"
            "الجملة: «" + sentence + "»\n\n"
            "حدد المعنى الدقيق لهذا اللفظ في هذا السياق."
        )

        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "أنت محلل دلالي عربي متخصص في علم الاشتراك اللفظي (Polysemy).\n"
                        "مهمتك: تحديد المعنى الدقيق للكلمة المحورية المعطاة في الجملة بناءً على السياق.\n\n"
                        "أجب دائماً بهذا الشكل الثابت فقط:\n"
                        "• اللفظ المحوري:\n"
                        "• المعنى المقصود:\n"
                        "• نوع الاستعمال: (حقيقي / مجازي)\n"
                        "• التفسير:\n"
                        "• نسبة الثقة:\n"
                        "الجواب يجب أن يكون واضحاً، مختصراً، وأكاديمياً."
                    )
                },
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=500,
            temperature=0.2
        )
        ai_text = response.choices[0].message.content

        # استخراج الحقول
        result = {
            "keyword": pivot_word,
            "meaning": "—",
            "usage": "—",
            "interp": "—",
            "conf": 85
        }

        for line in ai_text.splitlines():
            line = line.strip().lstrip("•").strip()
            if "المعنى المقصود" in line and ":" in line:
                result["meaning"] = line.split(":", 1)[-1].strip()
            elif "نوع الاستعمال" in line and ":" in line:
                result["usage"] = line.split(":", 1)[-1].strip()
            elif "التفسير" in line and ":" in line:
                result["interp"] = line.split(":", 1)[-1].strip()
            elif "نسبة الثقة" in line and ":" in line:
                raw_conf = line.split(":", 1)[-1].strip().replace("%", "").strip()
                try:
                    result["conf"] = int(float(raw_conf))
                except Exception:
                    result["conf"] = 85

        return result

    except Exception as e:
        return {
            "keyword": pivot_word,
            "meaning": "—",
            "usage": "—",
            "interp": "حدث خطأ: " + str(e),
            "conf": 0
        }


# =========================================
# HERO
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
    <div class="card-title">✦ التحليل الدلالي الذكي</div>
    <div class="card-desc">أدخل جملة عربية وسيقوم لبيب بتحليل المعنى والسياق اعتمادًا على الذكاء الاصطناعي.</div>
</div>
""", unsafe_allow_html=True)

user_text = st.text_area(
    "",
    placeholder="مثال: تدفقت عين بين الجبال...",
    height=180,
    label_visibility="collapsed"
)

submit_btn = st.button("⚡ تشغيل التحليل الذكي")

# =========================================
# التحليل
# =========================================
if submit_btn and user_text.strip():

    if not client:
        st.error("⚠️ لم يتم العثور على مفتاح Groq. أضيفي GROQ_API_KEY في Streamlit Secrets.")
    else:
        with st.spinner("⏳ يجري استخراج اللفظ المحوري..."):
            # ✅ الخطوة 1: استخراج اللفظ المحوري عبر Groq
            pivot_word = extract_pivot_word_via_groq(user_text, client)

        with st.spinner("🔍 يجري التحليل الدلالي..."):
            # ✅ الخطوة 2: التحليل الدلالي الكامل
            result = analyze_via_groq(user_text, pivot_word, client)

        # حفظ في السجل
        st.session_state.history.append({
            "الجملة": user_text[:60] + ("..." if len(user_text) > 60 else ""),
            "اللفظ المحوري": result["keyword"],
            "المعنى": result["meaning"],
            "الوقت": pd.Timestamp.now().strftime("%H:%M:%S")
        })

        # عرض النتيجة
        pivot_in_db = result["keyword"] in semantic_db
        pill_cls = "pill-local" if pivot_in_db else "pill-ai"
        pill_txt = "📚 قاعدة محلية + ذكاء اصطناعي" if pivot_in_db else "🤖 تحليل بالذكاء الاصطناعي"

        usage_icon = "🔵" if "حقيقي" in result["usage"] else "🟣"
        conf_bar_w = min(result["conf"], 100)

        html_parts = [
            '<div class="result-card">',
            '<div class="result-header">',
            '<div class="result-title">🔍 نتيجة التحليل الدلالي</div>',
            '<span class="result-source-pill ' + pill_cls + '">' + pill_txt + '</span>',
            '</div>',
            '<div class="result-grid">',
            '<div class="result-cell">',
            '<div class="result-cell-icon">📝</div>',
            '<div class="result-cell-label">اللفظ المحوري</div>',
            '<div class="result-cell-val">' + result["keyword"] + '</div>',
            '</div>',
            '<div class="result-cell">',
            '<div class="result-cell-icon">💡</div>',
            '<div class="result-cell-label">المعنى المقصود</div>',
            '<div class="result-cell-val">' + result["meaning"] + '</div>',
            '</div>',
            '<div class="result-cell">',
            '<div class="result-cell-icon">' + usage_icon + '</div>',
            '<div class="result-cell-label">نوع الاستعمال</div>',
            '<div class="result-cell-val">' + result["usage"] + '</div>',
            '</div>',
            '</div>',
            '<div class="result-divider"></div>',
            '<div style="font-size:13px;font-weight:700;color:#94A3B8;margin-bottom:10px;">التفسير</div>',
            '<div class="result-interp">' + result["interp"] + '</div>',
            '<div class="result-confidence">',
            '<span class="conf-label">نسبة الثقة</span>',
            '<div class="conf-bar-wrap"><div class="conf-bar" style="width:' + str(conf_bar_w) + '%"></div></div>',
            '<span class="conf-pct">' + str(result["conf"]) + '%</span>',
            '</div>',
            '</div>',
        ]

        st.markdown("".join(html_parts), unsafe_allow_html=True)

# =========================================
# سجل التحليلات
# =========================================
if st.session_state.history:
    st.markdown('<div class="section-main-title">📋 سجل التحليلات</div>', unsafe_allow_html=True)
    with st.expander("عرض السجل الكامل لهذه الجلسة"):
        df_history = pd.DataFrame(st.session_state.history)
        st.dataframe(df_history, use_container_width=True)
        word_counts = df_history["اللفظ المحوري"].value_counts()
        if len(word_counts) > 1:
            st.markdown("**أكثر الكلمات تحليلاً:**")
            st.bar_chart(word_counts)

# =========================================
# كيف يعمل لبيب؟
# =========================================
st.markdown('<div class="section-main-title">كيف يعمل لبيب؟</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""<div class="step-card">
    <div class="step-icon">🔎</div>
    <div class="step-title">استخراج اللفظ المحوري</div>
    <div class="step-desc">يستخدم Groq AI لتحديد الكلمة الأكثر ثراءً دلالياً في الجملة بدقة تامة، بغض النظر عن أي تصريف.</div>
</div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""<div class="step-card">
    <div class="step-icon">✨</div>
    <div class="step-title">اكتشاف المعنى</div>
    <div class="step-desc">تُطابق البيئة السياقية مع الحقول المعجمية في القاعدة المحلية إن وُجدت، ثم يُعمّق Groq التفسير.</div>
</div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""<div class="step-card">
    <div class="step-icon">📊</div>
    <div class="step-title">قياس الثقة</div>
    <div class="step-desc">يُنتج النظام تفسيراً أكاديمياً دقيقاً مع نسبة ثقة تعكس مدى وضوح الدلالة في السياق.</div>
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

st.markdown('<div class="footer-text">LABEEB AI © 2026 — هاجر الزواكي</div>', unsafe_allow_html=True)
