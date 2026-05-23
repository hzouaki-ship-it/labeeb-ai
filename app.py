import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModel
import pandas as pd

# 1. إعدادات الصفحة (Full Width)
st.set_page_config(page_title="LABEEB AI | لبيب", page_icon="🧠", layout="wide")

# 2. التنسيق الاحترافي (CSS) - تم تنظيف الكود لمنع أي أخطاء عرض
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;700;900&display=swap');
    
    .stApp {
        background: radial-gradient(circle at top right, #EDE9FE, #F8FAFC);
        font-family: 'Cairo', sans-serif;
        direction: rtl;
    }
    .hero-section { text-align: center; padding: 4rem 1rem; }
    .hero-title { font-size: 4rem; font-weight: 900; color: #7C3AED; margin-bottom: 1rem; }
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 25px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    .stButton>button {
        width: 100%; height: 50px; border-radius: 15px; 
        background: linear-gradient(90deg, #7C3AED, #A855F7);
        color: white; font-weight: bold; border: none; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 5px 15px rgba(124, 58, 237, 0.4); }
    .bio-box { padding: 2rem; border-radius: 20px; background: white; border-right: 5px solid #7C3AED; }
</style>
""", unsafe_allow_html=True)

# 3. واجهة الهيدر
st.markdown('<div class="hero-section"><h1 class="hero-title">LABEEB AI</h1><h3>المحلل الدلالي الذكي للغة العربية</h3></div>', unsafe_allow_html=True)

# 4. المدخلات في بطاقة زجاجية
with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    user_input = st.text_area("أدخل الجملة للتحليل:", height=150)
    if st.button("✨ ابدأ التحليل الاحترافي"):
        st.info("جاري المعالجة باستخدام النماذج اللغوية العميقة...")
    st.markdown('</div>', unsafe_allow_html=True)

# 5. بطاقة معلومات الباحثة
st.markdown("<br><br>", unsafe_allow_html=True)
with st.container():
    col_img, col_bio = st.columns([1, 3])
    with col_img:
        # تأكدي من رفع صورة باسم hajar.jpg في المجلد الرئيسي للمشروع
        st.image("hajar.jpg", width=200, caption="هاجر الزواكي")
    with col_bio:
        st.markdown("""
        <div class="bio-box">
            <h2>هاجر الزواكي</h2>
            <p><b>طالبة ماجستير (سنة ثانية) | تخصص اللسانيات الرقمية والعربية</b></p>
            <p>جامعة مولاي إسماعيل بمكناس</p>
            <p><i>هذا المشروع يمثل جزءاً من بحث التخرج الخاص بي لتطوير أدوات فهم السياق في اللغة العربية.</i></p>
        </div>
        """, unsafe_allow_html=True)

# 6. الفوتر
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<center>© 2026 LABEEB AI - جميع الحقوق محفوظة</center>", unsafe_allow_html=True)
