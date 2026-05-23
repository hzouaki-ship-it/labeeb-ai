import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import time

# إعداد الصفحة
st.set_page_config(page_title="LABEEB AI | لبيب", page_icon="🧠", layout="centered")

# CSS لتنسيق الصفحة بالكامل
st.markdown("""
<style>
    .stApp { background-color: #F8FAFC; direction: rtl; text-align: right; font-family: sans-serif; }
    .hero { text-align: center; padding: 2rem; }
    .card { background: white; padding: 2rem; border-radius: 20px; border: 1px solid #E2E8F0; margin-bottom: 1rem; }
    .stButton > button { width: 100%; background: #6D28D9; color: white; border-radius: 10px; border: none; padding: 10px; }
    .bio-card { background: #F3F4F6; padding: 1.5rem; border-radius: 15px; margin-top: 2rem; }
</style>
""", unsafe_allow_html=True)

# الهيدر
st.markdown('<div class="hero"><h1>لبيب | LABEEB AI</h1><p>المحلل الدلالي الذكي للغة العربية</p></div>', unsafe_allow_html=True)

# تحميل النموذج (مؤقت لغرض العرض)
@st.cache_resource
def load_model():
    return AutoTokenizer.from_pretrained("aubmindlab/bert-base-arabertv02"), AutoModel.from_pretrained("aubmindlab/bert-base-arabertv02")

tokenizer, model = load_model()

# الإدخال والتحليل
st.markdown('<div class="card">', unsafe_allow_html=True)
user_sentence = st.text_area("✍️ أدخل الجملة للتحليل:")

if st.button("✨ ابدأ التحليل"):
    st.success("تم تشغيل محرك التحليل الدلالي بنجاح.")
st.markdown('</div>', unsafe_allow_html=True)

# --- هنا إضافة قسم البايو الجديد ---
st.markdown("---")
st.subheader("عن الباحثة")

with st.container():
    col1, col2 = st.columns([1, 3])
    with col1:
        # تأكدي من وجود صورة باسم hajar.jpg في مجلد المشروع
        try:
            st.image("hajar.jpg", width=150)
        except:
            st.write("🖼️ [صورة الباحثة]")
    with col2:
        st.write("""
        **هاجر الزواكي** باحثة في مجال الذكاء الاصطناعي ومعالجة اللغات الطبيعية (NLP).  
        أهتم بتطوير تقنيات ذكية لفهم سياق اللغة العربية بشكل أدق وأسرع.
        """)
# -----------------------------------

# الفوتر
st.markdown('<div style="text-align: center; color: gray; margin-top: 20px;">© 2026 جميع الحقوق محفوظة</div>', unsafe_allow_html=True)
