import streamlit as st
from tashaphyne.stemming import ArabicLightStemmer
import pandas as pd
import time
import google.generativeai as genai

# إعداد Gemini كمعالج صامت
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel(
        model_name='gemini-3.5-flash',
        system_instruction="أنت أداة معالجة خلفية. وظيفتك تحليل الجملة دلالياً واستخراج المعنى الأقرب. أجب بالمعنى فقط دون مقدمات أو شرح."
    )

stemmer = ArabicLightStemmer()

st.set_page_config(page_title="LABEEB AI - لبيب", page_icon="🧠", layout="wide")

# --- CSS (نفس الستايل الخاص بكِ) ---
st.markdown('<style>'
    '.stButton > button {'
    '   background: linear-gradient(90deg, #4F46E5, #6D28D9) !important;'
    '   color: white !important; border-radius: 12px !important; width: 100% !important;'
    '}'
    '</style>', unsafe_allow_html=True)

# --- الواجهة ---
st.markdown('<div class="hero-container"><h1>✦ LABEEB AI</h1></div>', unsafe_allow_html=True)

user_text = st.text_area("أدخلي الجملة هنا:", placeholder="اكتبي النص...")
submit_btn = st.button("⚡ تشغيل خوارزمية لبيب للتحليل")

# --- المنطق الصامت (Backend) ---
if submit_btn and user_text.strip():
    with st.spinner("⏳ جاري التحليل..."):
        try:
            # استدعاء Gemini كمعالج خلفي فقط
            response = model.generate_content(f"حلل الجملة التالية دلالياً: {user_text}")
            final_meaning = response.text.strip()
            
            # عرض النتيجة
            st.success("النتيجة:")
            st.markdown(f'<div class="glass-card"><h3>{final_meaning}</h3></div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error("حدث خطأ تقني في المعالجة.")

# التذييل
st.markdown('<div class="footer-text">LABEEB AI © 2026 — هاجر الزواكي</div>', unsafe_allow_html=True)
