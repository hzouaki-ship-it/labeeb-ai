import streamlit as st
import pandas as pd
import json
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
# Groq
# =========================================
client = None
if "GROQ_API_KEY" in st.secrets:
    client = OpenAI(
        api_key=st.secrets["GROQ_API_KEY"],
        base_url="https://api.groq.com/openai/v1"
    )

GROQ_MODEL = "llama-3.3-70b-versatile"

# =========================================
# Session State
# =========================================
if "history" not in st.session_state:
    st.session_state.history = []
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "page" not in st.session_state:
    st.session_state.page = "التحليل الدلالي"
if "last_results" not in st.session_state:
    st.session_state.last_results = []

# =========================================
# قاعدة البيانات المعجمية
# =========================================
semantic_db = {
    "روح": [
        {"المعنى": "النفس البشرية", "القرائن": {
            "موت": 5, "مات": 5, "حياة": 5, "جسد": 4, "جنة": 4,
            "إيمان": 3, "آخرة": 4, "دفن": 5, "وفاة": 5
        }},
        {"المعنى": "الراحة والطاقة الإيجابية", "القرائن": {
            "هدوء": 5, "راحة": 5, "سعادة": 4, "طمأنينة": 4,
            "بهجة": 4, "انتعاش": 4, "فرح": 3, "حيوية": 4
        }}
    ],
    "عين": [
        {"المعنى": "عضو البصر", "القرائن": {
            "نظر": 5, "رؤية": 5, "بصر": 5, "دموع": 4,
            "جندي": 4, "معركة": 4, "جرح": 5, "إصابة": 5
        }},
        {"المعنى": "نبع ماء", "القرائن": {
            "ماء": 5, "نبع": 5, "جارية": 4, "بئر": 4,
            "وادي": 4, "جبل": 3, "ينبوع": 5, "مياه": 4
        }},
        {"المعنى": "جاسوس ومراقب", "القرائن": {
            "عدو": 4, "تجسس": 5, "مخابرات": 5, "سر": 4,
            "عميل": 5, "اختراق": 5, "استخبارات": 5
        }}
    ],
    "قلب": [
        {"المعنى": "عضو في جسم الإنسان", "القرائن": {
            "نبض": 5, "دم": 4, "طبيب": 4, "مرض": 5,
            "مستشفى": 5, "شريان": 5, "نوبة": 5
        }},
        {"المعنى": "العاطفة والمشاعر", "القرائن": {
            "حب": 5, "مشاعر": 5, "شوق": 5, "حزن": 4,
            "غرام": 5, "عشق": 5, "لوعة": 5
        }},
        {"المعنى": "مركز المدينة", "القرائن": {
            "المدينة": 4, "المركز": 5, "وسط": 5,
            "العاصمة": 4, "المنطقة": 3, "الحي": 3
        }}
    ],
    "رأس": [
        {"المعنى": "جزء من جسم الإنسان", "القرائن": {
            "شعر": 4, "صداع": 5, "دماغ": 5, "وجه": 4,
            "رقبة": 4, "خوذة": 5, "جرح": 4, "مخ": 5
        }},
        {"المعنى": "قمة أو أعلى شيء", "القرائن": {
            "جبل": 5, "قمة": 5, "مرتفع": 4,
            "تسلق": 4, "ذروة": 5, "علو": 4
        }}
    ],
    "بحر": [
        {"المعنى": "مسطح مائي", "القرائن": {
            "ماء": 5, "موج": 5, "سفينة": 4, "شاطئ": 4,
            "غرق": 5, "سباحة": 4, "صيد": 4
        }},
        {"المعنى": "العلم الواسع", "القرائن": {
            "علم": 5, "معرفة": 4, "عبقري": 3,
            "أستاذ": 4, "عالم": 5, "إتقان": 4
        }}
    ],
    "نور": [
        {"المعنى": "الضوء الحقيقي", "القرائن": {
            "شمس": 5, "ضوء": 5, "مصباح": 4, "ظلام": 4,
            "قمر": 4, "شعاع": 5, "أنار": 5
        }},
        {"المعنى": "الهداية أو المعرفة", "القرائن": {
            "هداية": 5, "علم": 4, "إيمان": 4,
            "دين": 4, "قرآن": 4, "تقوى": 4
        }}
    ],
    "أسد": [
        {"المعنى": "حيوان مفترس", "القرائن": {
            "غابة": 5, "فريسة": 5, "زئير": 5, "مخلب": 5,
            "صيد": 4, "ضاري": 4, "افترس": 5
        }},
        {"المعنى": "الشجاعة والبطولة", "القرائن": {
            "شجاعة": 5, "بطولة": 5, "مقاتل": 4,
            "جندي": 4, "قائد": 4, "بسالة": 5
        }}
    ],
}

# =========================================
# CSS الكامل
# =========================================
dark = st.session_state.dark_mode

bg_main    = "#0F0F1A" if dark else "#F4F3FF"
bg_sidebar = "#16162A" if dark else "#FFFFFF"
bg_card    = "#1E1E35" if dark else "#FFFFFF"
bg_input   = "#1E1E35" if dark else "#FFFFFF"
text_main  = "#E8E6FF" if dark else "#1A1A2E"
text_muted = "#8886A8" if dark else "#6B6B8A"
border_col = "#2E2E50" if dark else "#E8E6FF"
accent     = "#7C6FFF"
accent2    = "#A78BFA"
accent_bg  = "#2A2550" if dark else "#EDE9FE"
green      = "#34D399"
orange     = "#FBBF24"
pink       = "#F472B6"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap');

* {{ box-sizing: border-box; margin: 0; padding: 0; }}

html, body, [class*="css"], .stApp {{
    font-family: 'Cairo', sans-serif !important;
    background: {bg_main} !important;
    color: {text_main} !important;
    direction: rtl;
}}

#MainMenu, footer, header {{ visibility: hidden; }}

section[data-testid="stSidebar"] {{
    background: {bg_sidebar} !important;
    border-left: 1px solid {border_col} !important;
    min-width: 220px !important;
    max-width: 220px !important;
}}

section[data-testid="stSidebar"] > div {{
    padding: 0 !important;
}}

[data-testid="stMain"] .block-container {{
    padding: 1.5rem 2rem 3rem 2rem !important;
    max-width: 100% !important;
}}

/* ---- Sidebar Nav ---- */
.sidebar-logo {{
    padding: 28px 20px 20px;
    border-bottom: 1px solid {border_col};
    text-align: center;
}}
.sidebar-logo-icon {{
    width: 56px; height: 56px;
    background: linear-gradient(135deg, {accent}, {accent2});
    border-radius: 16px;
    display: flex; align-items: center; justify-content: center;
    font-size: 26px; margin: 0 auto 10px;
}}
.sidebar-brand {{
    font-size: 17px; font-weight: 900; color: {accent};
    font-family: 'Space Grotesk', sans-serif; letter-spacing: 1px;
}}
.sidebar-tagline {{
    font-size: 10px; color: {text_muted}; margin-top: 2px;
    letter-spacing: 2px; text-transform: uppercase;
}}
.nav-section {{
    padding: 20px 12px 8px;
    font-size: 10px; font-weight: 700; color: {text_muted};
    letter-spacing: 2px; text-transform: uppercase;
}}
.nav-item {{
    display: flex; align-items: center; gap: 10px;
    padding: 10px 16px; border-radius: 12px; margin: 2px 8px;
    font-size: 14px; font-weight: 600; cursor: pointer;
    color: {text_muted}; transition: all 0.2s;
    text-decoration: none;
}}
.nav-item:hover {{ background: {accent_bg}; color: {accent}; }}
.nav-item.active {{ background: {accent_bg}; color: {accent}; }}
.nav-icon {{ font-size: 16px; }}
.sidebar-version {{
    position: absolute; bottom: 16px; right: 0; left: 0;
    text-align: center; font-size: 11px; color: {text_muted};
}}

/* ---- Header ---- */
.top-header {{
    background: {bg_card};
    border: 1px solid {border_col};
    border-radius: 20px;
    padding: 24px 32px;
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 24px;
    flex-wrap: wrap; gap: 16px;
}}
.header-left {{
    display: flex; align-items: center; gap: 20px;
}}
.header-logo {{
    width: 70px; height: 70px; border-radius: 18px;
    background: linear-gradient(135deg, {accent}, {accent2});
    display: flex; align-items: center; justify-content: center;
    font-size: 32px; flex-shrink: 0;
}}
.header-title {{
    font-size: 36px; font-weight: 900; color: {accent};
    font-family: 'Space Grotesk', sans-serif; letter-spacing: 1px;
    line-height: 1;
}}
.header-subtitle {{
    font-size: 14px; font-weight: 700; color: {text_main}; margin-top: 4px;
}}
.header-desc {{
    font-size: 12px; color: {text_muted}; margin-top: 2px;
}}
.header-badge {{
    background: {accent_bg}; color: {accent};
    border: 1px solid {accent}33;
    padding: 6px 16px; border-radius: 999px;
    font-size: 12px; font-weight: 700;
    display: flex; align-items: center; gap: 6px;
}}

/* ---- Section title ---- */
.section-title {{
    font-size: 15px; font-weight: 800; color: {accent};
    margin-bottom: 10px; display: flex; align-items: center; gap: 8px;
}}

/* ---- Input card ---- */
.input-card {{
    background: {bg_card};
    border: 1px solid {border_col};
    border-radius: 20px;
    padding: 24px 28px;
    margin-bottom: 20px;
}}

/* ---- Streamlit overrides ---- */
.stTextArea textarea {{
    background: {bg_input} !important;
    border: 1.5px solid {border_col} !important;
    border-radius: 14px !important;
    color: {text_main} !important;
    font-family: 'Cairo', sans-serif !important;
    font-size: 16px !important;
    line-height: 1.9 !important;
    direction: rtl !important; text-align: right !important;
    padding: 16px !important;
}}
.stTextArea textarea:focus {{
    border-color: {accent} !important;
    box-shadow: 0 0 0 3px {accent}22 !important;
}}
.stButton > button {{
    background: linear-gradient(135deg, {accent}, {accent2}) !important;
    color: white !important; border: none !important;
    border-radius: 14px !important; width: 100% !important;
    height: 52px !important; font-size: 16px !important;
    font-weight: 800 !important; font-family: 'Cairo', sans-serif !important;
    box-shadow: 0 8px 20px {accent}44 !important;
    transition: all 0.2s !important;
}}
.stButton > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 28px {accent}66 !important;
}}
.stSelectbox > div > div {{
    background: {bg_input} !important;
    border: 1.5px solid {border_col} !important;
    border-radius: 12px !important;
    color: {text_main} !important;
    font-family: 'Cairo', sans-serif !important;
}}
label, .stSelectbox label {{
    color: {text_muted} !important;
    font-family: 'Cairo', sans-serif !important;
    font-size: 13px !important;
    font-weight: 700 !important;
}}

/* ---- Result cards ---- */
.results-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
}}
.result-card {{
    background: {bg_card};
    border: 1px solid {border_col};
    border-radius: 20px;
    padding: 22px 20px;
    position: relative;
    overflow: hidden;
}}
.result-card::before {{
    content: '';
    position: absolute; top: 0; right: 0;
    width: 4px; height: 100%;
    background: linear-gradient(180deg, {accent}, {accent2});
    border-radius: 0 20px 20px 0;
}}
.rc-header {{
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 14px;
}}
.rc-label {{
    font-size: 13px; font-weight: 800; color: {accent};
    display: flex; align-items: center; gap: 6px;
}}
.rc-source {{
    font-size: 10px; font-weight: 700; padding: 3px 10px;
    border-radius: 999px;
}}
.src-local {{ background: {accent_bg}; color: {accent}; }}
.src-ai {{ background: {"#0D2A1A" if dark else "#ECFDF5"}; color: {green}; }}
.rc-field {{ margin-bottom: 10px; }}
.rc-field-label {{
    font-size: 10px; color: {text_muted}; font-weight: 700;
    text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;
}}
.rc-field-val {{
    font-size: 14px; font-weight: 800; color: {text_main};
    background: {"#252542" if dark else "#F8F7FF"};
    padding: 6px 12px; border-radius: 8px;
    display: inline-block;
}}
.rc-meaning-val {{
    background: linear-gradient(135deg, {accent}22, {accent2}22);
    color: {accent}; border: 1px solid {accent}33;
    padding: 6px 14px; border-radius: 8px;
    font-size: 14px; font-weight: 800;
    display: inline-block;
}}
.rc-usage-hakiki {{ color: {green}; font-size: 13px; font-weight: 700; }}
.rc-usage-majazi  {{ color: {pink};  font-size: 13px; font-weight: 700; }}

/* ---- Confidence ring ---- */
.conf-row {{
    display: flex; align-items: center; gap: 10px; margin-top: 12px;
}}
.conf-bar-wrap {{
    flex: 1; background: {"#2A2A45" if dark else "#EEF2FF"};
    border-radius: 999px; height: 7px; overflow: hidden;
}}
.conf-bar {{
    height: 7px; border-radius: 999px;
    background: linear-gradient(90deg, {accent}, {accent2});
}}
.conf-pct {{
    font-size: 13px; font-weight: 800; color: {accent};
    white-space: nowrap;
}}

/* ---- Explanation box ---- */
.expl-box {{
    background: {bg_card};
    border: 1px solid {border_col};
    border-right: 4px solid {accent};
    border-radius: 0 16px 16px 0;
    padding: 20px 24px;
    margin-bottom: 24px;
}}
.expl-title {{
    font-size: 14px; font-weight: 800; color: {accent};
    margin-bottom: 10px; display: flex; align-items: center; gap: 6px;
}}
.expl-text {{
    font-size: 14px; color: {text_muted}; line-height: 2;
}}

/* ---- Stats ---- */
.stats-row {{
    display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 20px;
}}
.stat-pill {{
    background: {bg_card}; border: 1px solid {border_col};
    border-radius: 12px; padding: 10px 18px;
    font-size: 13px; color: {text_muted}; font-weight: 600;
}}
.stat-pill span {{ color: {accent}; font-weight: 800; font-size: 16px; }}

/* ---- Char counter ---- */
.char-count {{
    text-align: left; font-size: 11px; color: {text_muted};
    margin-top: 4px;
}}

/* ---- History table ---- */
[data-testid="stDataFrame"] {{
    background: {bg_card} !important;
    border-radius: 14px !important;
    border: 1px solid {border_col} !important;
}}

/* ---- Expander ---- */
.streamlit-expanderHeader {{
    background: {bg_card} !important;
    border: 1px solid {border_col} !important;
    border-radius: 12px !important;
    color: {text_main} !important;
    font-family: 'Cairo', sans-serif !important;
}}

/* ---- Divider ---- */
.fancy-divider {{
    height: 1px;
    background: linear-gradient(90deg, transparent, {accent}44, transparent);
    margin: 20px 0;
}}

/* ---- Info box ---- */
.info-box {{
    background: {accent_bg};
    border: 1px solid {accent}33;
    border-radius: 12px;
    padding: 14px 18px;
    font-size: 13px; color: {text_muted};
    margin-bottom: 16px;
    display: flex; align-items: flex-start; gap: 10px;
}}

.stSpinner > div {{
    border-top-color: {accent} !important;
}}
</style>
""", unsafe_allow_html=True)


# =========================================
# دوال التحليل
# =========================================
def extract_all_pivot_words(sentence: str, groq_client) -> list:
    """يستخرج كل الألفاظ المحورية من الجملة دفعة واحدة."""
    if not groq_client:
        return []
    try:
        prompt = (
            "أنت خبير في علم الدلالة العربية وتحليل الاشتراك اللفظي.\n\n"
            "الجملة: «" + sentence + "»\n\n"
            "المطلوب: استخرج كل الألفاظ التي تحمل اشتراكاً لفظياً (لها أكثر من معنى محتمل) في هذه الجملة.\n\n"
            "قواعد:\n"
            "- لا تُدرج حروف الجر أو الضمائر أو أسماء الإشارة.\n"
            "- أرجع كل كلمة في صيغتها كما وردت في الجملة أو مجردة.\n"
            "- أرجع JSON صالح فقط بهذا الشكل: {\"الألفاظ\": [\"كلمة1\", \"كلمة2\"]}\n"
            "- إذا لم تجد ألفاظاً مشتركة، أرجع أبرز اسمين في الجملة.\n"
            "- لا تزيد عن 4 ألفاظ."
        )
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=80,
            temperature=0.1
        )
        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        data = json.loads(raw)
        words = data.get("الألفاظ", [])
        return [w.strip("«».,،؟!") for w in words if w.strip()]
    except Exception:
        return []


def analyze_word_in_context(sentence: str, pivot: str, groq_client) -> dict:
    """يحلل لفظاً واحداً في سياق الجملة."""
    db_context = ""
    in_db = pivot in semantic_db
    if in_db:
        meanings_text = " | ".join(
            e["المعنى"] + ": " + ", ".join(list(e["القرائن"].keys())[:5])
            for e in semantic_db[pivot]
        )
        db_context = (
            "[قاعدة محلية] الكلمة «" + pivot + "» معانيها: " + meanings_text + "\n\n"
        )

    if not groq_client:
        return {"keyword": pivot, "meaning": "—", "usage": "—", "interp": "—", "conf": 0, "in_db": in_db}

    try:
        user_prompt = (
            db_context +
            "اللفظ المحوري: «" + pivot + "»\n"
            "الجملة: «" + sentence + "»\n\n"
            "حدد المعنى الدقيق لهذا اللفظ في هذا السياق فقط."
        )
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "أنت محلل دلالي عربي متخصص في الاشتراك اللفظي.\n"
                        "أجب بهذا الشكل الثابت فقط:\n"
                        "• اللفظ المحوري:\n"
                        "• المعنى المقصود:\n"
                        "• نوع الاستعمال: (حقيقي / مجازي)\n"
                        "• التفسير:\n"
                        "• نسبة الثقة:\n"
                        "اجعل الإجابة مختصرة وأكاديمية."
                    )
                },
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=300,
            temperature=0.2
        )
        ai_text = response.choices[0].message.content
        result = {"keyword": pivot, "meaning": "—", "usage": "—", "interp": "—", "conf": 85, "in_db": in_db}
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
        return {"keyword": pivot, "meaning": "—", "usage": "—", "interp": str(e), "conf": 0, "in_db": in_db}


def build_explanation(sentence: str, results: list, groq_client) -> str:
    """يبني شرحاً تفصيلياً مجمّعاً."""
    if not groq_client or not results:
        return ""
    try:
        words_summary = "، ".join(
            f"«{r['keyword']}» بمعنى {r['meaning']}" for r in results
        )
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "أنت محلل لغوي عربي. اكتب شرحاً تفصيلياً أكاديمياً موجزاً."},
                {"role": "user", "content": (
                    "الجملة: «" + sentence + "»\n"
                    "الألفاظ المحورية ومعانيها: " + words_summary + "\n\n"
                    "اكتب فقرة تفصيلية واحدة تشرح كيف حُدّدت هذه المعاني بناءً على السياق. "
                    "لا تزيد عن 3 جمل."
                )}
            ],
            max_tokens=200,
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return ""


# =========================================
# Sidebar
# =========================================
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">🧠</div>
        <div class="sidebar-brand">LABEEB AI</div>
        <div class="sidebar-tagline">Semantic Analyzer</div>
    </div>
    <div class="nav-section">القائمة الرئيسية</div>
    """, unsafe_allow_html=True)

    pages = [
        ("🔍", "التحليل الدلالي"),
        ("🔤", "تحليل متعدد الألفاظ"),
        ("📖", "التعلم التلقائي"),
        ("🗄️", "قاعدة المعرفة"),
        ("📊", "إحصائيات"),
        ("ℹ️", "حول النظام"),
    ]

    for icon, name in pages:
        active_cls = "active" if st.session_state.page == name else ""
        if st.button(f"{icon}  {name}", key=f"nav_{name}", use_container_width=True):
            st.session_state.page = name
            st.rerun()

    st.markdown(f"""
    <div class="sidebar-version">الإصدار 2.0.0</div>
    """, unsafe_allow_html=True)

    # Dark mode toggle
    st.markdown("<br><br>", unsafe_allow_html=True)
    dm_label = "☀️ الوضع الفاتح" if dark else "🌙 الوضع الداكن"
    if st.button(dm_label, use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()


# =========================================
# Header
# =========================================
st.markdown(f"""
<div class="top-header">
    <div class="header-left">
        <div class="header-logo">🧠</div>
        <div>
            <div class="header-title">LABEEB AI - لبيب</div>
            <div class="header-subtitle">نظام ذكي لتحليل الألفاظ متعددة المعاني في اللغة العربية</div>
            <div class="header-desc">يعتمد على الذكاء الاصطناعي والنماذج اللغوية لفهم السياق واستخراج المعنى المقصود بدقة</div>
        </div>
    </div>
    <div class="header-badge">🎓 مشروع تخرج – ماستر 2</div>
</div>
""", unsafe_allow_html=True)


# =========================================
# Pages
# =========================================
page = st.session_state.page

# --------------------------------------------------
if page in ("التحليل الدلالي", "تحليل متعدد الألفاظ"):
    multi_mode = (page == "تحليل متعدد الألفاظ")

    col_main, col_opts = st.columns([2, 1], gap="large")

    with col_main:
        st.markdown(f'<div class="section-title">📝 أدخل الجملة المراد تحليلها</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="input-card">', unsafe_allow_html=True)
        user_text = st.text_area(
            "",
            placeholder="مثال: أرسل القائد عيناً إلى العدو، ثم شرب ماء من عين عند رأس الجبل قبل أن يعود إلى قلب المدينة.",
            height=130,
            max_chars=500,
            label_visibility="collapsed",
            key="input_sentence"
        )
        st.markdown(f'<div class="char-count">{len(user_text)} / 500</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        analyze_btn = st.button(
            "✨  تحليل الجملة" if not multi_mode else "✨  تحليل متعدد الألفاظ",
            use_container_width=True
        )

    with col_opts:
        st.markdown(f'<div class="section-title">⚙️ خيارات التحليل</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="input-card">', unsafe_allow_html=True)
        precision = st.selectbox("دقة التحليل", ["عالية", "متوسطة", "سريعة"], index=0)
        model_choice = st.selectbox("نوع النموذج", ["Llama 3.3 70B (Groq)", "Mixtral 8x7B (Groq)"], index=0)
        st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.last_results:
            words_found = len(st.session_state.last_results)
            avg_conf = int(sum(r["conf"] for r in st.session_state.last_results) / words_found) if words_found else 0
            st.markdown(f"""
            <div class="stats-row">
                <div class="stat-pill">ألفاظ <span>{words_found}</span></div>
                <div class="stat-pill">ثقة <span>{avg_conf}%</span></div>
            </div>
            """, unsafe_allow_html=True)

    # ---- Analysis ----
    if analyze_btn and user_text.strip():
        if not client:
            st.error("⚠️ لم يتم العثور على مفتاح Groq في Secrets.")
        else:
            with st.spinner("⏳ يجري استخراج الألفاظ المحورية..."):
                if multi_mode:
                    pivots = extract_all_pivot_words(user_text, client)
                else:
                    # single: extract one
                    pivots = extract_all_pivot_words(user_text, client)[:1]

            if not pivots:
                st.warning("لم يتم العثور على ألفاظ محورية واضحة. جرّبي جملة أخرى.")
            else:
                results = []
                with st.spinner(f"🔍 يجري تحليل {len(pivots)} لفظ..."):
                    for p in pivots:
                        r = analyze_word_in_context(user_text, p, client)
                        results.append(r)

                st.session_state.last_results = results

                # Save history
                for r in results:
                    st.session_state.history.append({
                        "الجملة": user_text[:50] + ("..." if len(user_text) > 50 else ""),
                        "اللفظ المحوري": r["keyword"],
                        "المعنى": r["meaning"],
                        "الاستعمال": r["usage"],
                        "الثقة": f"{r['conf']}%",
                        "الوقت": pd.Timestamp.now().strftime("%H:%M:%S")
                    })

                # ---- Display results ----
                st.markdown(f"""
                <div class="fancy-divider"></div>
                <div class="section-title">📈 نتائج التحليل الدلالي</div>
                """, unsafe_allow_html=True)

                # Cards
                cards_html = '<div class="results-grid">'
                for i, r in enumerate(results):
                    src_cls = "src-local" if r["in_db"] else "src-ai"
                    src_txt = "قاعدة المعرفة المحلية" if r["in_db"] else "ذكاء اصطناعي"
                    usage_cls = "rc-usage-hakiki" if "حقيقي" in r["usage"] else "rc-usage-majazi"
                    conf_w = min(r["conf"], 100)

                    cards_html += f"""
                    <div class="result-card">
                        <div class="rc-header">
                            <div class="rc-label">🔤 اللفظ: {r['keyword']}</div>
                            <span class="rc-source {src_cls}">المصدر: {src_txt}</span>
                        </div>
                        <div class="rc-field">
                            <div class="rc-field-label">المعنى المقصود</div>
                            <div class="rc-meaning-val">{r['meaning']}</div>
                        </div>
                        <div class="rc-field">
                            <div class="rc-field-label">نوع الاستعمال</div>
                            <div class="{usage_cls}">{'● ' + r['usage']}</div>
                        </div>
                        <div class="conf-row">
                            <div class="conf-bar-wrap">
                                <div class="conf-bar" style="width:{conf_w}%"></div>
                            </div>
                            <span class="conf-pct">{r['conf']}%</span>
                        </div>
                    </div>
                    """
                cards_html += '</div>'
                st.markdown(cards_html, unsafe_allow_html=True)

                # Explanation
                with st.spinner("📝 يجري بناء الشرح التفصيلي..."):
                    explanation = build_explanation(user_text, results, client)

                if explanation:
                    st.markdown(f"""
                    <div class="expl-box">
                        <div class="expl-title">📋 الشرح التفصيلي</div>
                        <div class="expl-text">{explanation}</div>
                    </div>
                    """, unsafe_allow_html=True)

    elif st.session_state.last_results and not analyze_btn:
        # Show previous results
        st.markdown(f'<div class="section-title">📈 آخر نتائج التحليل</div>', unsafe_allow_html=True)
        cards_html = '<div class="results-grid">'
        for r in st.session_state.last_results:
            src_cls = "src-local" if r["in_db"] else "src-ai"
            src_txt = "قاعدة المعرفة المحلية" if r["in_db"] else "ذكاء اصطناعي"
            usage_cls = "rc-usage-hakiki" if "حقيقي" in r["usage"] else "rc-usage-majazi"
            conf_w = min(r["conf"], 100)
            cards_html += f"""
            <div class="result-card">
                <div class="rc-header">
                    <div class="rc-label">🔤 اللفظ: {r['keyword']}</div>
                    <span class="rc-source {src_cls}">المصدر: {src_txt}</span>
                </div>
                <div class="rc-field">
                    <div class="rc-field-label">المعنى المقصود</div>
                    <div class="rc-meaning-val">{r['meaning']}</div>
                </div>
                <div class="rc-field">
                    <div class="rc-field-label">نوع الاستعمال</div>
                    <div class="{usage_cls}">{'● ' + r['usage']}</div>
                </div>
                <div class="conf-row">
                    <div class="conf-bar-wrap">
                        <div class="conf-bar" style="width:{conf_w}%"></div>
                    </div>
                    <span class="conf-pct">{r['conf']}%</span>
                </div>
            </div>
            """
        cards_html += '</div>'
        st.markdown(cards_html, unsafe_allow_html=True)


# --------------------------------------------------
elif page == "قاعدة المعرفة":
    st.markdown(f'<div class="section-title">🗄️ قاعدة المعرفة المحلية</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="info-box">
        💡 تحتوي القاعدة على <strong>{len(semantic_db)}</strong> لفظاً محورياً مع قرائنهم السياقية.
        تُستخدم لتعزيز دقة التحليل عند الكلمات المعروفة.
    </div>
    """, unsafe_allow_html=True)
    for word, meanings in semantic_db.items():
        with st.expander(f"📌 {word} — {len(meanings)} معاني"):
            for m in meanings:
                st.markdown(f"**{m['المعنى']}** — القرائن: {', '.join(list(m['القرائن'].keys()))}")


# --------------------------------------------------
elif page == "إحصائيات":
    st.markdown(f'<div class="section-title">📊 إحصائيات الجلسة</div>', unsafe_allow_html=True)
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        total = len(df)
        unique_words = df["اللفظ المحوري"].nunique()
        st.markdown(f"""
        <div class="stats-row">
            <div class="stat-pill">تحليلات <span>{total}</span></div>
            <div class="stat-pill">ألفاظ فريدة <span>{unique_words}</span></div>
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)
        wc = df["اللفظ المحوري"].value_counts()
        if len(wc) > 1:
            st.bar_chart(wc)
    else:
        st.markdown(f'<div class="info-box">لا توجد إحصائيات بعد. ابدئي بتحليل جملة.</div>', unsafe_allow_html=True)


# --------------------------------------------------
elif page == "حول النظام":
    st.markdown(f"""
    <div class="expl-box">
        <div class="expl-title">🧠 عن لبيب</div>
        <div class="expl-text">
            لبيب هو نظام ذكي متخصص في تحليل الاشتراك اللفظي في اللغة العربية.
            يساعد على تحديد المعنى المقصود للألفاظ متعددة المعاني باستخدام السياق اللغوي والذكاء الاصطناعي.
        </div>
    </div>
    <div class="expl-box" style="margin-top:16px">
        <div class="expl-title">👩‍🎓 الباحثة</div>
        <div class="expl-text">
            <strong>هاجر الزواكي</strong> — طالبة ماستر في اللسانيات الرقمية والعربية<br>
            كلية الآداب والعلوم الإنسانية — جامعة مولاي إسماعيل، مكناس<br><br>
            مهتمة بالذكاء الاصطناعي ومعالجة اللغة العربية وبناء الأنظمة الدلالية الذكية.
        </div>
    </div>
    """, unsafe_allow_html=True)


# --------------------------------------------------
elif page == "التعلم التلقائي":
    st.markdown(f'<div class="section-title">📖 التعلم التلقائي</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="info-box">
        🚧 هذه الميزة قيد التطوير. ستسمح للنظام بإضافة ألفاظ جديدة لقاعدة المعرفة تلقائياً عبر Groq.
    </div>
    """, unsafe_allow_html=True)


# Footer
st.markdown(f"""
<div style="text-align:center; color:{text_muted}; font-size:12px; margin-top:40px; padding-top:16px; border-top:1px solid {border_col};">
    LABEEB AI © 2026 — هاجر الزواكي — الإصدار 2.0.0
</div>
""", unsafe_allow_html=True)
