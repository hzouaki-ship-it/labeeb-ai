import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="LABEEB AI | لبيب", page_icon="🧠", layout="wide")

# 2. التنسيق (CSS) - تم تنظيفه لضمان عدم وجود أخطاء Syntax
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;700&display=swap');
    
    .stApp { background-color: #F8FAFC; font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    
    /* تصميم البطاقات الزجاجية */
    .glass-card {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0;
        margin-bottom: 2rem;
    }
    
    /* تنسيق الهيدر */
    .hero-text { text-align: center; margin-bottom: 2rem; }
    .hero-title { color: #6D28D9; font-size: 3rem; font-weight: 800; }
    
    /* تنسيق البايو */
    .bio-card { 
        background: white; padding: 2rem; border-radius: 20px; 
        border: 1px solid #E2E8F0; display: flex; align-items: center; gap: 2rem;
    }
    
    /* الزر */
    .stButton>button { 
        background: linear-gradient(90deg, #6D28D9, #8B5CF6); 
        color: white; border-radius: 12px; width: 100%; border: none; padding: 12px;
    }
</style>
""", unsafe_allow_html=True)

# 3. الهيدر واللوغو
st.markdown('<div class="hero-text"><h1 class="hero-title">LABEEB AI (لبيب)</h1><p>المحلل الدلالي الذكي للغة العربية</p></div>', unsafe_allow_html=True)

# 4. قسم الإدخال
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
user_sentence = st.text_area("✍️ أدخل الجملة العربية للتحليل:", height=100)
if st.button("✨ ابدأ التحليل الذكي"):
    st.write("جاري المعالجة...")
st.markdown('</div>', unsafe_allow_html=True)

# 5. قسم معلومات المطورة (هاجر الزواكي)
st.subheader("تعرفي على الباحثة")
with st.container():
    st.markdown('<div class="bio-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 4])
    with col1:
        # تأكدي من وجود صورة hajar.jpg في المجلد
        try:
            st.image("hajar.jpg", width=200)
        except:
            st.warning("⚠️ الصورة غير موجودة")
    with col2:
        st.write("""
        ### هاجر الزواكي
        **طالبة ماجستير (سنة ثانية) | تخصص اللسانيات الرقمية والعربية** جامعة مولاي إسماعيل بمكناس  
        *هذا المشروع هو جزء من بحث التخرج الخاص بي لتطوير حلول ذكية لفهم السياق في اللغة العربية.*
        """)
    st.markdown('</div>', unsafe_allow_html=True)
