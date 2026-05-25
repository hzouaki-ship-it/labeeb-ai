import streamlit as st
from tashaphyne.stemming import ArabicLightStemmer
import pandas as pd
import time
import google.generativeai as genai

# إعداد Gemini كمعالج صامت
model = None
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel(
        model_name='gemini-3.5-flash',
        system_instruction="أنت أداة معالجة خلفية. وظيفتك تحليل الجملة دلالياً واستخراج المعنى الأقرب. أجب بالمعنى فقط دون مقدمات أو شرح."
    )

stemmer = ArabicLightStemmer()

# --- إعداد الصفحة ---
st.set_page_config(page_title="LABEEB AI - لبيب", page_icon="🧠", layout="wide")

# --- CSS ---
st.markdown('<style>'
    '.stButton > button { background: linear-gradient(90deg, #4F46E5, #6D28D9) !important; color: white !important; border-radius: 12px !important; width: 100% !important; }'
    '.glass-card { background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(20px); border-radius: 22px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); margin-bottom: 25px; }'
    '</style>', unsafe_allow_html=True)

# --- الواجهة ---
st.markdown('<div class="hero-container"><h1>✦ LABEEB AI</h1></div>', unsafe_allow_html=True)
user_text = st.text_area("أدخلي الجملة هنا:", placeholder="مثال: فقد الجندي عينه في المعركة...")
submit_btn = st.button("⚡ تشغيل خوارزمية لبيب للتحليل")

# --- منطق التحليل ---
if submit_btn and user_text.strip():
    with st.spinner("⏳ جاري التحليل..."):
        # 1. محاولة التحليل عبر القاعدة المحلية
        found_local = False
        # (هنا يوضع منطق semantic_db الخاص بك...)
        
        # 2. إذا لم تجد القاعدة المحلية نتيجة، يتم استدعاء Gemini صمتياً
        if not found_local and model:
            try:
                response = model.generate_content(f"حلل الجملة التالية دلالياً واستخرج المعنى المقصود: {user_text}")
                final_meaning = response.text.strip()
                
                st.markdown('<div class="glass-card"><h3>النتيجة:</h3>'
                            f'<p>{final_meaning}</p></div>', unsafe_allow_html=True)
            except Exception as e:
                st.error("تعذر التحليل، يرجى المحاولة لاحقاً.")
        else:
            st.warning("تم العثور على المعنى عبر قاعدة البيانات المحلية.")

# التذييل
st.markdown('<div class="footer-text">LABEEB AI © 2026 — هاجر الزواكي</div>', unsafe_allow_html=True)
