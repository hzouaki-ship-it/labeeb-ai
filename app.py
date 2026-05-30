import streamlit as st
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
st.set_page_config(page_title="LABEEB AI - لبيب", page_icon="🧠", layout="wide")

# =========================================
# Groq
# =========================================
client = None
if "GROQ_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["GROQ_API_KEY"], base_url="https://api.groq.com/openai/v1")

GROQ_MODEL = "llama-3.3-70b-versatile"

# =========================================
# قائمة الكلمات الوظيفية المحظورة
# =========================================
ARABIC_STOPWORDS = {
    "تلك","هذا","هذه","ذلك","هؤلاء","أولئك","التي","الذي","الذين",
    "اللواتي","ما","من","في","على","إلى","عن","مع","هو","هي","هم",
    "هن","أنا","أنت","أنتِ","نحن","أنتم","كان","كانت","يكون","تكون",
    "لكن","إن","أن","لأن","حتى","إذا","لو","قد","كل","بعض",
    "غير","بين","حول","عبر","خلال","منذ","رغم","بعد","قبل",
    "وهو","وهي","وهم","أو","بل","ثم","إذ","إذن","لا","لم","لن",
    "هناك","هنا","الآن","اليوم","أيضاً","أيضا","فقط","جداً","جدا",
    "كما","مما","عما","فيما","بما","وما","وكان","وكانت","وكانوا",
    "اللذان","اللتان","حيث","كيف","متى","أين","لماذا","ليس","ليست",
    "وقد","وإن","وأن","فإن","فأن","إلا","سوى","عند","لدى","منه","منها"
}

# =========================================
# CSS
# =========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&family=Poppins:wght@400;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
.stApp { background: linear-gradient(135deg, #F8FAFC 0%, #F5F3FF 50%, #EFF6FF 100%) !important; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stMain"] .block-container { max-width: 1140px; padding-top: 2rem; padding-bottom: 4rem; margin: 0 auto; }
.hero-container {
    background: linear-gradient(135deg, rgba(255,255,255,0.85), rgba(243,232,255,0.7));
    backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.6);
    border-radius: 28px; padding: 45px 35px; text-align: center;
    box-shadow: 0 20px 40px rgba(109,40,217,0.03); margin-bottom: 30px;
}
.hero-inline { display: flex; align-items: center; justify-content: center; gap: 35px; flex-wrap: wrap; margin-bottom: 20px; }
.brand-main { font-size: 52px; font-weight: 800; color: #4F46E5; font-family: 'Poppins', sans-serif; letter-spacing: 2px; margin-bottom: 6px; }
.brand-sub { font-size: 15px; letter-spacing: 4px; color: #4338CA; font-weight: 700; direction: ltr; text-align: center; }
.hero-logo-img { width: 160px; height: 160px; object-fit: cover; border-radius: 50%; box-shadow: 0 0 40px rgba(109,40,217,0.18); }
.hero-subtitle { font-size: 22px; font-weight: 700; color: #1E293B; margin-bottom: 10px; }
.hero-desc { font-size: 16px; color: #64748B; max-width: 650px; margin: 0 auto 20px auto; line-height: 2; }
.badge-student { display: inline-block; background: rgba(255,255,255,0.9); border: 1px solid #E9D5FF; padding: 6px 20px; border-radius: 999px; font-size: 13px; font-weight: 700; color: #6D28D9; }
.glass-card { background: rgba(255,255,255,0.92); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.5); border-radius: 22px; padding: 30px 35px; box-shadow: 0 10px 30px rgba(0,0,0,0.04); margin-bottom: 25px; }
.card-title { font-size: 22px; font-weight: 800; color: #4F46E5; margin-bottom: 10px; text-align: center; }
.card-desc { font-size: 16px; color: #64748B; text-align: center; line-height: 2; }
.stTextArea textarea { background: white !important; border-radius: 18px !important; border: 1px solid #E2E8F0 !important; padding: 20px !important; font-size: 17px !important; line-height: 2 !important; color: #1E293B !important; font-family: 'Cairo', sans-serif !important; direction: rtl !important; text-align: right !important; box-shadow: 0 4px 14px rgba(0,0,0,0.04) !important; }
.stTextArea textarea:focus { border: 1px solid #8B5CF6 !important; box-shadow: 0 0 0 4px rgba(139,92,246,0.10) !important; }
.stButton > button { background: linear-gradient(90deg, #4F46E5, #7C3AED) !important; color: white !important; border: none !important; border-radius: 18px !important; width: 100% !important; height: 58px !important; font-size: 17px !important; font-weight: 800 !important; font-family: 'Cairo', sans-serif !important; transition: 0.3s !important; box-shadow: 0 10px 24px rgba(79,70,229,0.25) !important; }
.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 14px 28px rgba(79,70,229,0.35) !important; }
.multi-banner { background: linear-gradient(90deg,#EDE9FE,#F5F3FF); border: 1px solid #C4B5FD; border-radius: 14px; padding: 12px 20px; margin-bottom: 22px; font-size: 15px; color: #4C1D95; font-weight: 700; text-align: center; }
.result-card { background: linear-gradient(135deg, #FAFAFA 0%, #F5F3FF 100%); border: 1px solid #E9D5FF; border-radius: 26px; padding: 36px 40px; margin-top: 24px; box-shadow: 0 12px 40px rgba(109,40,217,0.07); direction: rtl; }
.result-header { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; margin-bottom: 28px; gap: 12px; }
.result-title { font-size: 20px; font-weight: 800; color: #4F46E5; }
.result-word-title { font-size: 16px; font-weight: 800; color: #6D28D9; margin: 18px 0 14px 0; padding-bottom: 6px; border-bottom: 2px dashed #E9D5FF; }
.result-source-pill { font-size: 12px; font-weight: 700; padding: 5px 16px; border-radius: 999px; display: inline-block; }
.pill-local { background: #EDE9FE; color: #6D28D9; }
.pill-ai    { background: #F0FDF4; color: #16A34A; }
.pill-learn { background: #FEF3C7; color: #D97706; }
.result-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 14px; margin-bottom: 26px; }
.result-cell { background: white; border: 1px solid #F3E8FF; border-radius: 16px; padding: 16px 18px; text-align: center; }
.result-cell-icon { font-size: 22px; margin-bottom: 6px; }
.result-cell-label { font-size: 11px; color: #94A3B8; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }
.result-cell-val { font-size: 17px; font-weight: 800; color: #1E293B; }
.result-divider { height: 1px; background: linear-gradient(90deg,transparent,#E9D5FF,transparent); margin: 22px 0; }
.result-interp { background: white; border-right: 4px solid #7C3AED; border-radius: 0 14px 14px 0; padding: 16px 20px; font-size: 15px; color: #334155; line-height: 2; margin-bottom: 18px; }
.result-confidence { display: flex; align-items: center; gap: 12px; direction: rtl; }
.conf-label { font-size: 13px; color: #64748B; font-weight: 700; white-space: nowrap; }
.conf-bar-wrap { flex: 1; background: #F1F5F9; border-radius: 999px; height: 10px; overflow: hidden; }
.conf-bar { height: 10px; border-radius: 999px; background: linear-gradient(90deg, #7C3AED, #4F46E5); }
.conf-pct { font-size: 14px; font-weight: 800; color: #4F46E5; white-space: nowrap; }
.learn-banner { background: linear-gradient(90deg, #FFFBEB, #FEF3C7); border: 1px solid #FDE68A; border-radius: 14px; padding: 12px 18px; margin-bottom: 20px; font-size: 14px; color: #92400E; font-weight: 600; display: flex; align-items: center; gap: 10px; }
.word-separator { height: 2px; background: linear-gradient(90deg,transparent,#C4B5FD,transparent); margin: 30px 0; }
.section-main-title { text-align: center; font-size: 26px; font-weight: 800; color: #1E293B; margin: 40px 0 20px 0; }
.step-card { background: white; border: 1px solid #F1F5F9; border-radius: 18px; padding: 24px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.02); }
.step-icon { font-size: 30px; margin-bottom: 10px; }
.step-title { font-size: 17px; font-weight: 700; color: #1E293B; margin-bottom: 8px; }
.step-desc { font-size: 14px; color: #64748B; line-height: 1.8; }
.researcher-card { background: white; border: 1px solid #EEF2F6; border-radius: 22px; padding: 28px 32px; box-shadow: 0 8px 20px rgba(0,0,0,0.02); margin-top: 40px; direction: rtl; }
.researcher-flex { display: flex; align-items: center; justify-content: flex-start; gap: 24px; direction: rtl; text-align: right; flex-wrap: wrap; }
.researcher-img { width: 110px; height: 110px; border-radius: 50%; object-fit: cover; border: 3px solid #F3E8FF; flex-shrink: 0; }
.researcher-name { font-size: 21px; font-weight: 800; color: #1E293B; margin-bottom: 4px; }
.researcher-title { font-size: 14px; font-weight: 600; color: #6D28D9; margin-bottom: 10px; line-height: 1.8; }
.researcher-bio { font-size: 14px; color: #475569; line-height: 1.9; }
.footer-text { text-align: center; color: #94A3B8; font-size: 13px; margin-top: 50px; border-top: 1px solid #E2E8F0; padding-top: 20px; }
[data-testid="stTable"] table { width: 100%; border-collapse: collapse; font-family: 'Cairo', sans-serif; direction: rtl; }
[data-testid="stTable"] table thead tr th { text-align: center !important; font-size: 14px; font-weight: 700; color: #6D28D9; padding: 12px 16px; background: #F9F5FF; border-bottom: 2px solid #E9D5FF; }
[data-testid="stTable"] table tbody tr td { text-align: center !important; font-size: 15px; color: #334155; padding: 12px 16px; border-bottom: 1px solid #F1F5F9; }
[data-testid="stTable"] table tbody tr:hover td { background: #FAF5FF; }
</style>
""", unsafe_allow_html=True)

# =========================================
# قاعدة البيانات المعجمية
# =========================================
semantic_db = {
    "روح": [
        {"المعنى": "النفس البشرية", "القرائن": {"موت": 5, "مات": 5, "توفي": 5, "حياة": 5, "جسد": 4, "جنة": 4, "إيمان": 3, "آخرة": 4, "دفن": 5, "فارق": 4, "رحل": 4, "وفاة": 5}},
        {"المعنى": "الراحة والطاقة الإيجابية", "القرائن": {"هدوء": 5, "راحة": 5, "سعادة": 4, "طمأنينة": 4, "صفاء": 3, "بهجة": 4, "انتعاش": 4, "فرح": 3, "نشاط": 3, "حيوية": 4}}
    ],
    "باب": [
        {"المعنى": "مدخل مادي", "القرائن": {"منزل": 5, "بيت": 5, "غرفة": 4, "قفل": 5, "مفتاح": 5, "فتح": 4, "طرق": 5, "دخل": 4, "خرج": 4, "أغلق": 5, "دار": 4}},
        {"المعنى": "فصل أو قسم", "القرائن": {"كتاب": 5, "فصل": 5, "عنوان": 4, "مبحث": 4, "علم": 3, "دراسة": 4, "بحث": 4, "أكاديمي": 3, "مؤلف": 3, "نحو": 3}}
    ],
    "كتاب": [
        {"المعنى": "مؤلف مطبوع", "القرائن": {"قراءة": 5, "مكتبة": 5, "صفحات": 4, "رواية": 4, "مؤلف": 4, "طبع": 4, "اقتنى": 3, "قرأ": 5, "ورق": 3, "فصل": 3}},
        {"المعنى": "فرض أو حكم", "القرائن": {"شرع": 5, "دين": 4, "واجب": 4, "فرض": 5, "الله": 4, "قرآن": 4, "حرام": 4, "حلال": 4}}
    ],
    "بحر": [
        {"المعنى": "مسطح مائي", "القرائن": {"ماء": 5, "موج": 5, "سفينة": 4, "شاطئ": 4, "غرق": 5, "سباحة": 4, "مد": 4, "جزر": 4, "ملاحة": 4, "صيد": 4, "أمواج": 5}},
        {"المعنى": "العلم الواسع", "القرائن": {"علم": 5, "معرفة": 4, "عبقري": 3, "فهم": 3, "ثقافة": 3, "أستاذ": 4, "عالم": 5, "تخصص": 3, "إتقان": 4, "خبرة": 4}}
    ],
    "مفتاح": [
        {"المعنى": "أداة فتح", "القرائن": {"باب": 5, "قفل": 5, "فتح": 4, "حديد": 3, "منزل": 3, "درج": 4, "سيارة": 3, "ثقب": 4, "خزنة": 4, "أغلق": 4}},
        {"المعنى": "حل أو وسيلة", "القرائن": {"نجاح": 5, "حل": 5, "سر": 4, "فهم": 3, "مشكلة": 4, "تقدم": 4, "تميز": 3, "وصول": 4, "هدف": 4, "إنجاز": 4}}
    ],
    "عين": [
        {"المعنى": "عضو البصر", "القرائن": {"نظر": 5, "رؤية": 5, "يبصر": 5, "دموع": 4, "بصر": 5, "عمى": 5, "جندي": 5, "معركة": 5, "جرح": 5, "إصابة": 5, "فقد": 5, "أصيب": 5, "طبيب": 3, "ألم": 3, "حرب": 5, "شاهد": 4, "رأى": 4, "أبصر": 5, "عدسة": 4, "نظارة": 4}},
        {"المعنى": "نبع ماء", "القرائن": {"ماء": 5, "نبع": 5, "جارية": 4, "بئر": 4, "تدفقت": 4, "وادي": 4, "جبل": 3, "صخر": 3, "ينبوع": 5, "مياه": 4, "شرب": 4}},
        {"المعنى": "جاسوس", "القرائن": {"عدو": 4, "تجسس": 5, "مخابرات": 5, "سر": 4, "عميل": 5, "اختراق": 5, "معلومات": 4, "استخبارات": 5, "رصد": 4, "تقرير": 3}}
    ],
    "قلب": [
        {"المعنى": "عضو في جسم الإنسان", "القرائن": {"نبض": 5, "دم": 4, "طبيب": 4, "مرض": 5, "جراحة": 5, "مستشفى": 5, "ضغط": 4, "شريان": 5, "أزمة": 4, "نوبة": 5, "عملية": 5, "صدر": 4, "رئة": 4}},
        {"المعنى": "العاطفة والمشاعر", "القرائن": {"حب": 5, "اشتياق": 4, "مشاعر": 5, "هيام": 4, "شوق": 5, "حزن": 4, "فرح": 3, "وجد": 4, "غرام": 5, "احترق": 5, "تألم": 4, "عشق": 5, "لوعة": 5, "هوى": 4}},
        {"المعنى": "المركز أو الوسط", "القرائن": {"المدينة": 4, "المركز": 5, "وسط": 5, "الحي": 3, "البلاد": 3, "العاصمة": 4, "المنطقة": 3, "الحضارة": 3, "موقع": 3}}
    ],
    "رأس": [
        {"المعنى": "جزء من جسم الإنسان", "القرائن": {"شعر": 4, "صداع": 5, "دماغ": 5, "تفكير": 4, "وجه": 4, "رقبة": 4, "خوذة": 5, "جرح": 4, "ضربة": 4, "كسر": 4, "مخ": 5}},
        {"المعنى": "قمة أو أعلى شيء", "القرائن": {"جبل": 5, "قمة": 5, "مرتفع": 4, "صخور": 3, "تسلق": 4, "ارتفاع": 4, "ذروة": 5, "منحدر": 4, "علو": 4}}
    ],
    "يد": [
        {"المعنى": "عضو في جسم الإنسان", "القرائن": {"أصابع": 5, "كف": 5, "لمس": 4, "ذراع": 4, "كتابة": 3, "بطش": 4, "ضرب": 4, "إمساك": 4, "جرح": 4, "بتر": 5, "رسغ": 5}},
        {"المعنى": "المساعدة أو الدعم", "القرائن": {"مساعدة": 5, "عون": 5, "دعم": 4, "ساند": 4, "خدمة": 3, "تعاون": 4, "أسهم": 3, "أسند": 4, "بذل": 4, "قدم": 3}}
    ],
    "نور": [
        {"المعنى": "الضوء الحقيقي", "القرائن": {"شمس": 5, "ضوء": 5, "مصباح": 4, "ظلام": 4, "إضاءة": 5, "قمر": 4, "شعاع": 5, "انبثق": 4, "أنار": 5, "سطع": 5, "نجم": 3}},
        {"المعنى": "الهداية أو المعرفة", "القرائن": {"هداية": 5, "علم": 4, "معرفة": 5, "إيمان": 4, "حق": 3, "دين": 4, "قرآن": 4, "إسلام": 3, "تقوى": 4, "رشد": 4}}
    ],
    "لسان": [
        {"المعنى": "عضو النطق", "القرائن": {"كلام": 5, "نطق": 5, "فم": 5, "صوت": 4, "لغة": 4, "تذوق": 4, "طعم": 4, "أكل": 3, "حلق": 4, "أسنان": 4}},
        {"المعنى": "اللغة أو الأسلوب", "القرائن": {"عربي": 5, "فصيح": 5, "بيان": 4, "أدب": 4, "شعر": 4, "خطابة": 5, "بلاغة": 5, "تعبير": 4, "كتابة": 3, "فقه": 3}}
    ],
    "سيف": [
        {"المعنى": "سلاح حاد", "القرائن": {"معركة": 5, "حرب": 5, "قتال": 5, "ضرب": 4, "جرح": 4, "دم": 4, "غمد": 5, "فارس": 4, "بطل": 3, "حديد": 4}},
        {"المعنى": "القوة أو الحجة القاطعة", "القرائن": {"حجة": 5, "برهان": 4, "رد": 4, "جدل": 4, "دحض": 5, "قاطع": 5, "حسم": 4, "إفحام": 5, "إثبات": 4, "نقاش": 3}}
    ],
    "أسد": [
        {"المعنى": "حيوان مفترس", "القرائن": {"غابة": 5, "فريسة": 5, "زئير": 5, "مخلب": 5, "صيد": 4, "ضاري": 4, "حيوان": 4, "افترس": 5}},
        {"المعنى": "الشجاعة والبطولة", "القرائن": {"شجاعة": 5, "بطولة": 5, "جرأة": 4, "إقدام": 4, "مقاتل": 4, "جندي": 4, "قائد": 4, "بسالة": 5, "فداء": 3, "نضال": 4}}
    ],
    "ظل": [
        {"المعنى": "انعكاس الضوء", "القرائن": {"شمس": 5, "ضوء": 4, "شجرة": 4, "صيف": 4, "حر": 4, "انعكس": 5, "سقط": 4, "جدار": 3, "وقاية": 3}},
        {"المعنى": "الحماية والكنف", "القرائن": {"أب": 5, "وطن": 5, "حماية": 5, "رعاية": 4, "دفء": 4, "أمان": 5, "لجأ": 4, "استظل": 5, "كنف": 5, "عطف": 4}}
    ]
}

# =========================================
# Session State
# =========================================
if "history" not in st.session_state:
    st.session_state.history = []
if "learned_db" not in st.session_state:
    st.session_state.learned_db = {}


# =========================================
# ✅ دالة ترجيح المعاني بالأوزان
# =========================================
def score_meanings(text: str, meanings: list) -> tuple:
    """
    تحسب نقاط كل معنى بناءً على القرائن الموجودة في الجملة.
    تعيد: (اسم المعنى الأرجح، قاموس النقاط الكامل)
    """
    best_meaning = meanings[0]["المعنى"]
    best_score = 0
    scores = {}
    for entry in meanings:
        score = 0
        for clue, weight in entry["القرائن"].items():
            if clue in text:
                score += weight
        scores[entry["المعنى"]] = score
        if score > best_score:
            best_score = score
            best_meaning = entry["المعنى"]
    return best_meaning, scores


# =========================================
# ✅ استخراج جميع الألفاظ المحورية
# =========================================
def extract_all_pivot_words(text: str, db: dict) -> list:
    """
    تستخرج جميع الكلمات المشتركة الموجودة في الجملة (وليس فقط الأولى).
    """
    found = []
    tokens = [t.strip(".,،؟!:؛-") for t in text.split()]
    for token in tokens:
        if len(token) < 3:
            continue
        candidate = None
        if token in db:
            candidate = token
        else:
            stripped = token.lstrip("ال")
            if len(stripped) >= 3 and stripped in db:
                candidate = stripped
            else:
                for suffix in ["ه", "ها", "هم", "هن", "ي", "ك", "نا"]:
                    if token.endswith(suffix):
                        root = token[:-len(suffix)]
                        if root in db:
                            candidate = root
                            break
                        root2 = root.lstrip("ال")
                        if len(root2) >= 3 and root2 in db:
                            candidate = root2
                            break
        if candidate and candidate not in found:
            found.append(candidate)
    return found


# =========================================
# دالة التعلم التلقائي عبر Groq
# =========================================
def auto_learn_word(word: str, sentence: str, groq_client) -> list | None:
    if not groq_client:
        return None
    try:
        prompt = (
            "أنت خبير في علم الدلالة العربية.\n"
            "الكلمة: «" + word + "»\n"
            "الجملة: «" + sentence + "»\n\n"
            "أعطني معاني هذه الكلمة المشتركة (polysemy) بصيغة JSON فقط.\n"
            '{"معاني": [{"المعنى": "اسم المعنى الأول", "القرائن": {"كلمة1": 5, "كلمة2": 4}}, '
            '{"المعنى": "اسم المعنى الثاني", "القرائن": {"كلمة1": 5, "كلمة2": 4}}]}\n'
            "اذكر على الأقل معنيين وأعطِ 6-10 قرائن لكل معنى.\n"
            "أجب بـ JSON صالح فقط، بدون markdown أو backticks."
        )
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600, temperature=0.2
        )
        raw = response.choices[0].message.content.strip().replace("```json","").replace("```","").strip()
        import json
        data = json.loads(raw)
        meanings = data.get("معاني", [])
        if len(meanings) >= 2:
            return meanings
    except Exception:
        pass
    return None


# =========================================
# دالة تحليل كلمة واحدة عبر Groq
# =========================================
def analyze_single_word(word: str, best_meaning: str, scores: dict, text: str, groq_client) -> dict:
    """
    تحلل كلمة واحدة وتعيد dict بالنتائج.
    """
    result = {"keyword": word, "meaning": best_meaning, "usage": "—", "interp": "—", "conf": 85}
    if not groq_client:
        return result

    scores_text = " | ".join(f"{m}: {s} نقاط" for m, s in scores.items())
    user_prompt = (
        "[معلومة من القاعدة المحلية]\n"
        "الكلمة المحورية: «" + word + "»\n"
        "المعاني المحتملة بأوزانها: " + scores_text + "\n"
        "المعنى الأرجح محلياً: «" + best_meaning + "»\n\n"
        "الجملة: «" + text + "»\n\n"
        "حدد المعنى الدقيق لهذه الكلمة بناءً على السياق وأكد المعنى الأرجح أو صححه."
    )
    try:
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "أنت محلل دلالي عربي متخصص في الاشتراك اللفظي (Polysemy).\n"
                        "مهمتك: تحديد المعنى الدقيق للكلمة المحورية المعطاة بناءً على السياق.\n"
                        "القاعدة المحلية زوّدتك بالمعنى الأرجح بناءً على الأوزان — تحقق منه وأكده أو صححه.\n"
                        "قواعد صارمة:\n"
                        "- اللفظ المحوري يجب أن يكون الكلمة المعطاة لك تحديداً ولا تغيرها.\n"
                        "- لا تختر أسماء إشارة أو ضمائر أو حروف جر.\n\n"
                        "أجب بهذا الشكل الثابت فقط:\n"
                        "• اللفظ المحوري:\n"
                        "• المعنى المقصود:\n"
                        "• نوع الاستعمال: (حقيقي / مجازي)\n"
                        "• التفسير:\n"
                        "• نسبة الثقة:\n"
                    )
                },
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=400, temperature=0.2
        )
        ai_text = response.choices[0].message.content
        for line in ai_text.splitlines():
            line = line.strip().lstrip("•").strip()
            if "اللفظ المحوري" in line and ":" in line:
                extracted = line.split(":",1)[-1].strip().strip("«»").strip()
                if extracted and extracted not in ARABIC_STOPWORDS:
                    result["keyword"] = extracted
            if "المعنى المقصود" in line and ":" in line:
                result["meaning"] = line.split(":",1)[-1].strip()
            if "نوع الاستعمال" in line and ":" in line:
                result["usage"] = line.split(":",1)[-1].strip()
            if "التفسير" in line and ":" in line:
                result["interp"] = line.split(":",1)[-1].strip()
            if "نسبة الثقة" in line and ":" in line:
                raw = line.split(":",1)[-1].strip().replace("%","").strip()
                try:
                    result["conf"] = int(float(raw))
                except Exception:
                    result["conf"] = 85
    except Exception:
        pass
    return result


# =========================================
# دالة بناء HTML بطاقة نتيجة واحدة
# =========================================
def build_result_card_html(r: dict) -> str:
    usage_icon = "🔵" if "حقيقي" in r["usage"] else "🟣"
    conf_w = min(r["conf"], 100)
    return "".join([
        '<div class="result-grid">',
        '<div class="result-cell"><div class="result-cell-icon">📝</div>',
        '<div class="result-cell-label">اللفظ المحوري</div>',
        '<div class="result-cell-val">«' + r["keyword"] + '»</div></div>',
        '<div class="result-cell"><div class="result-cell-icon">💡</div>',
        '<div class="result-cell-label">المعنى المقصود</div>',
        '<div class="result-cell-val">' + r["meaning"] + '</div></div>',
        '<div class="result-cell"><div class="result-cell-icon">' + usage_icon + '</div>',
        '<div class="result-cell-label">نوع الاستعمال</div>',
        '<div class="result-cell-val">' + r["usage"] + '</div></div>',
        '</div>',
        '<div class="result-divider"></div>',
        '<div style="font-size:13px;font-weight:700;color:#94A3B8;margin-bottom:10px;">التفسير</div>',
        '<div class="result-interp">' + r["interp"] + '</div>',
        '<div class="result-confidence">',
        '<span class="conf-label">نسبة الثقة</span>',
        '<div class="conf-bar-wrap"><div class="conf-bar" style="width:' + str(conf_w) + '%"></div></div>',
        '<span class="conf-pct">' + str(r["conf"]) + '%</span>',
        '</div>',
    ])


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
    <div class="card-title">🧠 التحليل الدلالي الذكي</div>
    <div class="card-desc">أدخل جملة عربية وسيقوم لبيب بتحليل جميع الألفاظ المشتركة فيها، كلٍّ على حدة، بدقة أكاديمية.</div>
</div>
""", unsafe_allow_html=True)

user_text = st.text_area("", placeholder="مثال: فتح الجندي عينه على بحر من الدم...", height=180, label_visibility="collapsed")
submit_btn = st.button("⚡ تشغيل التحليل الذكي")

# =========================================
# التحليل الرئيسي
# =========================================
if submit_btn and user_text.strip():
    with st.spinner("⏳ يجري التحليل الدلالي..."):

        # 1 — استخراج جميع الألفاظ المحورية
        all_pivots = extract_all_pivot_words(user_text, semantic_db)
        just_learned = False
        learned_word = None

        # 2 — تعلم تلقائي إن لم توجد كلمة معروفة
        if not all_pivots and client:
            tokens_raw = [t.strip(".,،؟!") for t in user_text.split() if len(t) >= 3]
            all_known = set(semantic_db.keys()) | set(st.session_state.learned_db.keys())
            candidates = [
                t.lstrip("ال") for t in tokens_raw
                if t.lstrip("ال") not in all_known
                and t.lstrip("ال") not in ARABIC_STOPWORDS
                and len(t.lstrip("ال")) >= 3
            ]
            if candidates:
                new_word = candidates[0]
                learned = auto_learn_word(new_word, user_text, client)
                if learned:
                    st.session_state.learned_db[new_word] = learned
                    semantic_db[new_word] = learned
                    all_pivots = [new_word]
                    just_learned = True
                    learned_word = new_word

        # 3 — تحليل كل كلمة بالأوزان ثم Groq
        results = []
        for word in all_pivots:
            best_meaning, scores = score_meanings(user_text, semantic_db[word])
            if client:
                r = analyze_single_word(word, best_meaning, scores, user_text, client)
            else:
                r = {"keyword": word, "meaning": best_meaning, "usage": "حقيقي", "interp": "التحليل المحلي فقط (لا يوجد مفتاح Groq)", "conf": 70}
            results.append(r)
            # حفظ في السجل
            st.session_state.history.append({
                "الجملة": user_text[:50] + ("..." if len(user_text) > 50 else ""),
                "اللفظ المحوري": r["keyword"],
                "المعنى": r["meaning"],
                "الوقت": pd.Timestamp.now().strftime("%H:%M:%S")
            })

        # 4 — عرض النتائج
        n = len(results)

        # بانر التعلم
        if just_learned:
            st.markdown(
                '<div class="learn-banner">✨ لبيب تعلّم كلمة جديدة: <strong>«' + (learned_word or "") + '»</strong> — ستُحلَّل محلياً في الجلسة القادمة!</div>',
                unsafe_allow_html=True
            )

        # بانر التعدد
        if n > 1:
            st.markdown(
                f'<div class="multi-banner">🔍 تم اكتشاف {n} ألفاظ مشتركة في الجملة — يعرض لبيب تحليلاً مستقلاً لكل لفظ</div>',
                unsafe_allow_html=True
            )

        if n == 0:
            st.warning("لم يتم اكتشاف ألفاظ مشتركة معروفة في الجملة. جرّبي جملة أخرى أو تأكدي من الاتصال بـ Groq للتعلم التلقائي.")
        elif n == 1:
            # كلمة واحدة — العرض الكلاسيكي
            pill_cls = "pill-learn" if just_learned else "pill-local"
            pill_txt = "🧠 تعلّم تلقائي جديد" if just_learned else "📚 قاعدة محلية + ذكاء اصطناعي"
            html = (
                '<div class="result-card">'
                '<div class="result-header">'
                '<div class="result-title">🔍 نتيجة التحليل الدلالي</div>'
                '<span class="result-source-pill ' + pill_cls + '">' + pill_txt + '</span>'
                '</div>'
                + build_result_card_html(results[0]) +
                '</div>'
            )
            st.markdown(html, unsafe_allow_html=True)
        else:
            # كلمات متعددة — بطاقة موحدة بفواصل
            pill_txt = "📚 تحليل متعدد الألفاظ"
            html_parts = [
                '<div class="result-card">',
                '<div class="result-header">',
                '<div class="result-title">🔍 نتيجة التحليل الدلالي المتعدد</div>',
                '<span class="result-source-pill pill-local">' + pill_txt + '</span>',
                '</div>',
            ]
            for i, r in enumerate(results):
                if i > 0:
                    html_parts.append('<div class="word-separator"></div>')
                html_parts.append(
                    '<div class="result-word-title">📌 اللفظ ' + str(i+1) + ': «' + r["keyword"] + '»</div>'
                )
                html_parts.append(build_result_card_html(r))
            html_parts.append('</div>')
            st.markdown("".join(html_parts), unsafe_allow_html=True)

        # رسالة عدم وجود Groq
        if not client:
            st.info("⚠️ أضيفي GROQ_API_KEY في Secrets للحصول على التفسير الكامل.")

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
# الكلمات المتعلَّمة
# =========================================
if st.session_state.learned_db:
    st.markdown('<div class="section-main-title">🧬 كلمات تعلّمها لبيب في هذه الجلسة</div>', unsafe_allow_html=True)
    with st.expander(f"عرض الكلمات المتعلَّمة ({len(st.session_state.learned_db)} كلمة)"):
        for word, meanings in st.session_state.learned_db.items():
            st.markdown(f"**• {word}** — المعاني المكتشفة: {', '.join([m['المعنى'] for m in meanings])}")
        st.info("💡 هذه الكلمات ستُستخدم تلقائياً بالخوارزمية المحلية في باقي الجلسة.")

# =========================================
# كيف يعمل لبيب؟
# =========================================
st.markdown('<div class="section-main-title">كيف يعمل لبيب؟</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""<div class="step-card"><div class="step-icon">🔎</div><div class="step-title">تحليل السياق</div><div class="step-desc">يفحص النظام البنية التركيبية ويستخرج جميع الألفاظ المشتركة بدقة عبر الخوارزمية المحلية المعززة بالأوزان.</div></div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""<div class="step-card"><div class="step-icon">✨</div><div class="step-title">ترجيح المعاني</div><div class="step-desc">تُحسب نقاط كل معنى بناءً على القرائن الموجودة في الجملة، ثم يؤكد Groq AI المعنى الأرجح أو يصححه.</div></div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""<div class="step-card"><div class="step-icon">📊</div><div class="step-title">تحليل متعدد الألفاظ</div><div class="step-desc">عند وجود أكثر من لفظ مشترك في الجملة، يحلّل لبيب كل واحد منفردة ويعرض نتائج مستقلة لكل لفظ.</div></div>""", unsafe_allow_html=True)

# =========================================
# بطاقة الباحثة
# =========================================
st.markdown("""
<div class="researcher-card">
    <div class="researcher-flex">
        <img src="https://raw.githubusercontent.com/hzouaki-ship-it/labeeb-ai/main/hajar.jpg" class="researcher-img" alt="هاجر الزواكي">
        <div>
            <div class="researcher-name">هاجر الزواكي</div>
            <div class="researcher-title">طالبة ماستر في اللسانيات الرقمية والعربية<br>كلية الآداب والعلوم الإنسانية — جامعة مولاي إسماعيل، مكناس</div>
            <div class="researcher-bio">مهتمة بالذكاء الاصطناعي ومعالجة اللغة العربية وبناء الأنظمة الدلالية الذكية، وأسعى إلى تطوير حلول رقمية حديثة لفهم اللغة العربية وتحليل السياق والمعنى.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="footer-text">LABEEB AI © 2026 — هاجر الزواكي</div>', unsafe_allow_html=True)
