import streamlit as st
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel
from tashaphyne.stemming import ArabicLightStemmer
from openai import OpenAI

# =========================================
# 1. إعداد الصفحة الأساسي
# =========================================
st.set_page_config(
    page_title="LABEEB AI - لبيب",
    page_icon="🧠",
    layout="wide"
)

# =========================================
# 2. CSS الجمالي (مدمج مرة واحدة)
# =========================================
st.markdown("""
    <style>
    @import url("https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&family=Poppins:wght@400;600;700;800&display=swap");
    
    html, body, [class*="css"] { font-family: "Cairo", sans-serif; direction: rtl; text-align: right; }
    .stApp { background: linear-gradient(135deg, #F8FAFC 0%, #F5F3FF 50%, #EFF6FF 100%) !important; }
    #MainMenu, footer, header { visibility: hidden; }
    
    .hero-container { text-align: center; padding: 35px; }
    .hero-title { font-size: 58px; font-weight: 800; color: #4F46E5; }
    .hero-sub { color: #64748B; font-size: 18px; margin-top: 10px; }
    
    .glass-card { background: rgba(255,255,255,0.93); backdrop-filter: blur(12px); border-radius: 24px; padding: 28px; margin-top: 22px; border: 1px solid #E2E8F0; box-shadow: 0 8px 24px rgba(0,0,0,0.06); }
    
    .stButton > button { background: linear-gradient(90deg, #4F46E5, #6D28D9) !important; color: white !important; border: none !important; border-radius: 14px !important; width: 100% !important; height: 54px !important; font-size: 18px !important; font-weight: bold !important; }
    
    .researcher-card { background: white; border: 1px solid #EEF2F6; border-radius: 20px; padding: 24px; margin-top: 40px; }
    .researcher-flex { display: flex; align-items: center; gap: 24px; }
    .researcher-img { width: 110px; height: 110px; border-radius: 50%; object-fit: cover; border: 3px solid #F3E8FF; }
    .researcher-name { font-size: 20px; font-weight: 800; color: #1E293B; }
    .researcher-title { font-size: 15px; font-weight: 600; color: #6D28D9; margin-bottom: 8px; }
    .researcher-bio { font-size: 14px; color: #475569; line-height: 1.7; }
    
    .footer-text { text-align: center; color: #94A3B8; margin-top: 60px; font-size: 13px; border-top: 1px solid #E2E8F0; padding-top: 20px; }
    </style>
""", unsafe_allow_html=True)

# =========================================
# 3. الأدوات والنماذج
# =========================================
stemmer = ArabicLightStemmer()

@st.cache_resource
def load_arabert():
    tokenizer = AutoTokenizer.from_pretrained("aubmindlab/bert-base-arabertv02")
    model = AutoModel.from_pretrained("aubmindlab/bert-base-arabertv02")
    return tokenizer, model

tokenizer, arabert_model = load_arabert()

# =========================================
# 4. الإعدادات والوظائف
# =========================================
client = None
if "OPENROUTER_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENROUTER_API_KEY"], base_url="https://openrouter.ai/api/v1")

def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        outputs = arabert_model(**inputs)
    return outputs.last_hidden_state[:, 0, :]

def semantic_similarity(text1, text2):
    return F.cosine_similarity(get_embedding(text1), get_embedding(text2)).item()

semantic_db = {
    "عين": {"عضو البصر": "الرؤية والنظر والدموع والبصر", "نبع ماء": "الماء والينبوع والشرب والطبيعة", "جاسوس": "التجسس والمراقبة والعدو"},
    "نار": {"لهب حقيقي": "الحريق والحرارة والدخان", "حماس عاطفي": "المشاعر والحب والحماس", "حرب أو فتن": "الصراع والقتال"},
    "روح": {"نفس بشرية": "الحياة والإنسان والوفاة", "جانب معنوي": "المشاعر والطاقة الداخلية", "عالم الغيب": "الأرواح والميتافيزيقا"},
    "قلب": {"عضو حيوي": "النبض والدم والجسد", "العاطفة والمشاعر": "الحب والإحساس والمشاعر"}
}

# =========================================
# 5. الواجهة الرئيسية
# =========================================
st.markdown('<div class="hero-container"><div class="hero-title">✦ LABEEB AI</div><div class="hero-sub">المحلل الدلالي السياقي للغة العربية</div></div>', unsafe_allow_html=True)

user_text = st.text_area("أدخلي الجملة:", placeholder="مثال: أشعلت كلماتها نار الحماس في قلبه...")
submit_btn = st.button("⚡ تحليل دلالي ذكي")

if submit_btn and user_text.strip():
    with st.spinner("⏳ جاري تحليل السياق الدلالي..."):
        words = user_text.split()
        found_target = None
        for word in words:
            stemmer.light_stem(word)
            word_stem = stemmer.get_stem()
            for key in semantic_db.keys():
                stemmer.light_stem(key)
                if word_stem == stemmer.get_stem():
                    found_target = key
                    break
            if found_target: break

        # عرض النتائج
        if found_target:
            meanings = semantic_db[found_target]
            best_meaning, highest_similarity, all_results = "", -1, []
            for meaning, context in meanings.items():
                sim = semantic_similarity(user_text, context)
                all_results.append((meaning, sim))
                if sim > highest_similarity:
                    highest_similarity, best_meaning = sim, meaning
            
            # استدعاء LLM
            ai_analysis = "تعذر الاتصال بالمحرك الذكي."
            if client:
                try:
                    res = client.chat.completions.create(model="openrouter/auto", messages=[{"role": "system", "content": "أنت محلل دلالي عربي. أجب باختصار: المعنى المقصود، هل هو حقيقي أم مجازي، وتفسير مختصر."}, {"role": "user", "content": user_text}])
                    ai_analysis = res.choices[0].message.content
                except Exception as e: ai_analysis = f"خطأ: {e}"

            st.markdown(f'<div class="glass-card"><h3>🔍 التحليل الدلالي</h3><p><b>اللفظ:</b> {found_target}<br><b>المعنى الأرجح:</b> {best_meaning}<br><b>نسبة التشابه:</b> {highest_similarity:.2%}</p><p><b>التفسير:</b> {ai_analysis}</p></div>', unsafe_allow_html=True)
        else:
            st.warning("لم يتم العثور على لفظ مشترك في قاعدة البيانات.")

# =========================================
# 6. بطاقة الباحثة والتذييل
# =========================================
st.markdown('<div class="researcher-card"><div class="researcher-flex"><img src="https://raw.githubusercontent.com/hzouaki-ship-it/labeeb-ai/main/hajar.jpg" class="researcher-img"><div style="text-align:right;"><div class="researcher-name">هاجر الزواكي</div><div class="researcher-title">طالبة ماستر في اللسانيات الرقمية والعربية</div><div class="researcher-bio">مهتمة بالذكاء الاصطناعي ومعالجة اللغة العربية وبناء الأنظمة الدلالية الذكية.</div></div></div></div>', unsafe_allow_html=True)
st.markdown('<div class="footer-text">LABEEB AI © 2026 — جميع الحقوق محفوظة — هاجر الزواكي</div>', unsafe_allow_html=True)
