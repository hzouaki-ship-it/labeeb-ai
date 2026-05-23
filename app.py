import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import time

# إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="LABEEB AI | لبيب",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# تنسيقات CSS الاحترافية المدمجة والمطابقة للتصميم الفاخر
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"], .stApp {
    background-color: #F8FAFC !important;
    background-image: radial-gradient(at 50% 0%, rgba(243, 232, 255, 0.4) 0px, transparent 50%) !important;
    direction: rtl !important;
    text-align: right !important;
    font-family: 'Cairo', sans-serif !important;
}

[data-testid="stMain"] .block-container {
    max-width: 900px !important;
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
}

h1, h2, h3, h4, h5, h6, p, span, label {
    font-family: 'Cairo', sans-serif !important;
    direction: rtl !important;
    text-align: right !important;
}

.hero-wrapper {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    padding: 5px 0 15px 0 !important;
}

.top-badge {
    background: white !important;
    color: #6D28D9 !important;
    padding: 6px 18px !important;
    border-radius: 100px !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    margin-bottom: 20px !important;
    box-shadow: 0 2px 10px rgba(109, 40, 217, 0.05) !important;
}

.hero-title {
    font-size: 46px !important;
    font-weight: 800 !important;
    margin-top: 10px !important;
    background: linear-gradient(90deg, #6D28D9, #2563EB) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    text-align: center !important;
}

.hero-subtitle {
    font-size: 20px !important;
    font-weight: 700 !important;
    color: #1E293B !important;
    margin-top: 12px !important;
    text-align: center !important;
}

.hero-description {
    font-size: 15px !important;
    color: #64748B !important;
    max-width: 650px !important;
    line-height: 1.9 !important;
    margin-top: 12px !important;
    text-align: center !important;
}

.author-badge {
    margin-top: 18px !important;
    background: #F3E8FF !important;
    color: #6B21A8 !important;
    padding: 8px 22px !important;
    border-radius: 100px !important;
    font-size: 13px !important;
    font-weight: 700 !important;
}

/* بطاقة احترافية حاضنة مدمجة لمنع تشتت الحاويات */
.section-card {
    background: white !important;
    border-radius: 20px !important;
    padding: 28px 32px !important;
    margin-top: 25px !important;
    border: 1px solid #E2E8F0 !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.02) !important;
}

.card-title-text {
    font-size: 17px !important;
    font-weight: 700 !important;
    color: #1E293B !important;
    margin-bottom: 16px !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
}

.stTextArea textarea {
    border-radius: 14px !important;
    border: 1px solid #CBD5E1 !important;
    padding: 15px !important;
    font-size: 14.5px !important;
    background-color: #FAFAFA !important;
}

.stTextArea textarea:focus {
    border-color: #7C3AED !important;
    background-color: #FFFFFF !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.12) !important;
}

div.stButton > button {
    width: 100% !important;
    background: linear-gradient(90deg, #6D28D9, #7C3AED) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 11px 24px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    transition: 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(109,40,217,0.2) !important;
}

div.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(109,40,217,0.3) !important;
}

.empty-box {
    padding: 20px 0 !important;
    text-align: center !important;
}

.steps-title {
    text-align: center !important;
    font-size: 24px !important;
    font-weight: 800 !important;
    color: #1E293B !important;
    margin-top: 50px !important;
}

.steps-desc {
    text-align: center !important;
    color: #64748B !important;
    font-size: 14px !important;
    margin-bottom: 30px !important;
}

.step-card {
    background: white !important;
    border-radius: 16px !important;
    padding: 22px !important;
    text-align: center !important;
    border: 1px solid #E2E8F0 !important;
    height: 100% !important;
    position: relative !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.01) !important;
}

.step-num {
    position: absolute !important;
    top: 12px;
    left: 12px;
    background: #E0E7FF !important;
    color: #4F46E5 !important;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    font-size: 11px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
}

.footer-container {
    text-align: center !important;
    margin-top: 60px !important;
    padding-top: 20px !important;
    border-top: 1px solid #E2E8F0 !important;
    color: #94A3B8 !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Hero Section - الواجهة العلوية لشعار وهوية لبيب
hero_html = """
<div class="hero-wrapper">
    <div class="top-badge">✦ منصة ذكاء اصطناعي عربية</div>

    <svg width="110" height="110" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="grad" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="#6D28D9"/>
                <stop offset="100%" stop
