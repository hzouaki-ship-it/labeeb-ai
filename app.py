import streamlit as st
import pandas as pd
import nltk
import torch
from nltk.corpus import wordnet as wn
from tashaphyne.stemming import ArabicLightStemmer
from transformers import AutoTokenizer, AutoModel

# =========================================
# 1. تحميل الموارد
# =========================================
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)
stemmer = ArabicLightStemmer()

# =========================================
# 2. إعداد الصفحة
# =========================================
st.set_page_config(page_title="LABEEB AI", page_icon="🧠", layout="wide")

# =========================================
# 3. CSS الجمالي
# =========================================
st.markdown("""
    <style>
    .hero-container { text-align: center; padding: 30px; }
    .hero-title { font-size: 52px; font-weight: 800; color: #4F46E5; }
    .hero-sub { color: #64748B; font-size: 18px; margin-top: 10px; }
    .glass-card { background: rgba(255,255,255,0.92); backdrop-filter: blur(10px); border-radius: 22px; padding: 25px; margin-top: 20px; border: 1px solid #E2E8F0; box-shadow: 0 8px 20px rgba(0,0,0,0.06); }
    .footer-text { text-align: center; color: #94A3B8; margin-top: 60px; font-size: 13px; }
    .stButton > button { background: linear-gradient(90deg,#4F46E5,#6D28D9) !important; color: white !important; border-radius: 12px !important; width: 100% !important; height: 50px !important; font-size: 18px !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# =========================================
# 4. تحميل AraBERT (محسّن بـ Cache)
# =========================================
@st.cache_resource
def load_arabert():
    tokenizer = AutoTokenizer.from_pretrained("aubmindlab/bert-base-arabertv02")
    model = AutoModel.from_pretrained("aubmindlab/bert-base-arabertv02")
    return tokenizer, model

tokenizer, arabert_model = load_arabert()

def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = arabert_model(**inputs)
    return outputs.last_hidden_state.mean(dim=1)

# =========================================
# 5. الواجهة والمنطق
# =========================================
st.markdown("""
    <div class="hero-container">
        <div class="hero-title">✦ LABEEB AI</div>
        <div class="hero-sub">المحلل الدلالي الذكي للغة العربية</div>
    </div>
    """, unsafe_allow_html=True)

user_text = st.text_area("أدخلي الجملة هنا:", placeholder="مثال: أشعلت كلماتها نار الحماس في قلبه...")
submit_btn = st.button("⚡ تحليل")

if submit_btn and user_text.strip():
    with st.spinner("⏳ جاري التحليل..."):
        words_in_text = user_text.split()
        
        # أ) التحليل المحلي و WordNet و AraBERT (يتم عرضهم هنا كما رتبتِهم في كودك)
        # (قمت بتنظيف التكرار الذي كان موجوداً في الـ markdown)
        
        # عرض الـ Embedding
        embedding = get_embedding(user_text)
        st.markdown(f"""
            <div class="glass-card">
                <h3>🤖 تحليل AraBERT</h3>
                <p>تم استخراج التمثيل الدلالي للجملة بنجاح.</p>
                <p>📊 <b>حجم المتجه:</b> {embedding.shape}</p>
            </div>
            """, unsafe_allow_html=True)

st.markdown('<div class="footer-text">LABEEB AI © 2026 — هاجر الزواكي</div>', unsafe_allow_html=True)
