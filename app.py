import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="LABEEB AI | لبيب", page_icon="🧠", layout="wide")

# 2. التنسيق (تم تنظيفه لضمان عدم وجود أخطاء في السلسلة النصية)
st.markdown("""
<style>
    .stApp { background-color: #F8FAFC; direction: rtl; text-align: right; font-family: sans-serif; }
    .hero { text-align: center; padding: 2rem; }
    .main-card { background: white; padding: 2rem; border-radius: 20px; border: 1px solid #E2E8F0; margin-bottom: 2rem; }
    .bio-section { background: white; padding: 2rem; border-radius: 20px; border: 1px solid #E2E8F0; margin-top: 2rem; display: flex; align-items: center; gap: 20px; }
    .stButton > button { background: #7C3AED; color: white; border-radius: 10px; width: 100%; border: none; padding: 10px; }
</style>
""", unsafe_allow_html=True)

# 3. الهيدر
st.markdown('<div class="hero"><h1>LABEEB AI (لبيب)</h1><p>المحلل الدلالي الذكي للغة العربية</p></div>', unsafe_allow_html=True)

# 4. قسم الإدخال
st.markdown('<div class="main-card">', unsafe_allow_html=True)
user_sentence = st.text_area("✍️ أدخل الجملة للتحليل:")
if st.button("✨ ابدأ التحليل"):
    st.info("جاري التحليل السياقي...")
st.markdown('</div>', unsafe_allow_html=True)

# 5. قسم معلومات الباحثة (Bio)
st.subheader("عن الباحثة")
with st.container():
    st.markdown('<div class="bio-section">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 4])
    with col1:
        # تأكدي أن اسم الملف هو بالضبط hajar.jpg
        st.image("hajar.jpg", width=150)
    with col2:
        st.write("""
        ### هاجر الزواكي
        **طالبة ماجستير (سنة ثانية) | تخصص اللسانيات الرقمية والعربية** جامعة مولاي إسماعيل بمكناس  
        *هذا المشروع هو جزء من بحث التخرج الخاص بي لتطوير أدوات فهم السياق في اللغة العربية.*
        """)
    st.markdown('</div>', unsafe_allow_html=True)

# 6. الفوتر
st.markdown("<hr><center>© 2026 LABEEB AI - جميع الحقوق محفوظة</center>", unsafe_allow_html=True)
