import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import time

# 1. إعدادات الصفحة الأساسية لواجهة المنصة والأبعاد
st.set_page_config(
    page_title="منصة لبيب LABEEB AI",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. حقن التنسيقات العربية وتأمين بيئة التصميم الشاملة (RTL) دون تداخل الأسطر البرمجية
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&display=swap');

/* ضبط الخلفية الشاملة وتوحيد خط القاهرة لجميع العناصر بالمنصة */
html, body, [data-testid="stAppViewContainer"], .stApp {
    background-color: #F9FAFB !important;
    direction: rtl !important;
    text-align: right !important;
    font-family: 'Cairo', sans-serif !important;
}

/* تحديد أبعاد وحواف الحاوية الرئيسية للموقع */
[data-testid="stMain"] .block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
    max-width: 850px !important;
}

h1, h2, h3, h4, h5, h6, p, span, label, table, th, td {
    font-family: 'Cairo', sans-serif !important;
    text-align: right !important;
    direction: rtl !important;
}

/* ---------------- ترويسة الصفحة (Hero Section) المحدثة والممركزة ---------------- */
.hero-wrapper {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    padding: 20px 0 10px 0 !important;
    width: 100% !important;
}

.top-badge {
    display: inline-flex !important;
    align-items: center !important;
    background-color: #FFFFFF !important;
    color: #6366F1 !important;
    padding: 4px 16px !important;
    border-radius: 100px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    margin-bottom: 25px !important;
    box-shadow: 0 2px 6px rgba(99, 102, 241, 0.08) !important;
}

.hero-title {
    font-size: 38px !important;
    font-weight: 800 !important;
    color: #4C1D95 !important;
    margin: 20px 0 0 0 !important;
    line-height: 1.2 !important;
    text-align: center !important;
    width: 100% !important;
    display: block !important;
}

.hero-subtitle {
    font-size: 18px !important;
    font-weight: 700 !important;
    color: #1E293B !important;
    margin: 12px 0 !important;
    text-align: center !important;
    width: 100% !important;
}

.hero-description {
    font-size: 15px !important;
    color: #64748B !important;
    max-width: 650px !important;
    margin: 0 auto 20px auto !important;
    line-height: 1.7 !important;
    text-align: center !important;
}

.author-badge {
    display: inline-block !important;
    background: #F3E8FF !important;
    color: #6B21A8 !important;
    padding: 6px 20px !important;
    border-radius: 100px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    border: 1px solid #E9D5FF !important;
    margin-top: 5px !important;
}

/* ---------------- بطاقات الأقسام (Section Cards) ---------------- */
.section-card {
    background: #FFFFFF !important;
    border: 1px solid #F1F5F9 !important;
    border-radius: 24px !important;
    padding: 35px !important;
    box-shadow: 0 4px 25px rgba(0, 0, 0, 0.015) !important;
    margin-top: 30px !important;
    margin-bottom: 25px !important;
    text-align: right !important;
}

.card-title-container {
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    gap: 8px !important;
    margin-bottom: 20px !important;
}

.card-title-text {
    font-size: 16px !important;
    font-weight: 700 !important;
    color: #1E293B !important;
    margin: 0 !important;
}

/* ---------------- مدخلات الكتابة والأزرار التفاعلية ---------------- */
.stTextArea textarea {
    background-color: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 16px !important;
    padding: 18px !important;
    font-family: 'Cairo', sans-serif !important;
    font-size: 14.5px !important;
    color: #334155 !important;
    text-align: right !important;
    direction: rtl !important;
}

div.stButton > button {
    background: #6D28D9 !important;
    color: white !important;
    font-family: 'Cairo', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14.5px !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 10px 24px !important;
    box-shadow: 0 4px 12px rgba(109, 40, 217, 0.25) !important;
    width: 100% !important;
}

/* ---------------- تهيئة وتنسيق حالة ما قبل التحليل ---------------- */
.inner-dashed-box {
    border: 1px dashed #E2E8F0 !important;
    border-radius: 16px !important;
    padding: 40px 20px !important;
    text-align: center !important;
    background: #FAFAFA !important;
}

.empty-icon-box {
    font-size: 36px !important;
    color: #6D28D9 !important;
    background: #F3E8FF !important;
    width: 64px !important;
    height: 64px !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    border-radius: 16px !important;
    margin-bottom: 16px !important;
}

.empty-main-text {
    color: #6D28D9 !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    margin-bottom: 6px !important;
    text-align: center !important;
}

.empty-sub-text {
    color: #94A3B8 !important;
    font-size: 13.5px !important;
    text-align: center !important;
}

/* ---------------- عناوين قسم الخطوات السفلي ---------------- */
.steps-section-title {
    text-align: center !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    color: #1E293B !important;
    margin-top: 40px !important;
    margin-bottom: 6px !important;
}

.steps-section-desc {
    text-align: center !important;
    font-size: 14px !important;
    color: #64748B !important;
    margin-bottom: 25px !important;
}

/* ---------------- التصميم الهندسي الأفقي للخطوات التوضيحية ---------------- */
.step-item-horizontal {
    background: #FFFFFF !important;
    border: 1px solid #F1F5F9 !important;
    border-radius: 20px !important;
    padding: 24px 20px !important;
    text-align: center !important;
    position: relative !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.01) !important;
    height: 100% !important;
}

.step-badge-num-right {
    position: absolute !important;
    top: -12px !important;
    right: 20px !important;
    background: #6D28D9 !important;
    color: white !important;
    width: 24px !important;
    height: 24px !important;
    border-radius: 50% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 12px !important;
    font-weight: 700 !important;
}

.step-icon-wrapper-center {
    font-size: 22px !important;
    margin-bottom: 12px !important;
    background: #F8FAFC !important;
    width: 48px !important;
    height: 48px !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    border-radius: 50% !important;
}

.step-item-title-center {
    font-weight: 700 !important;
    color: #4338CA !important;
    font-size: 14.5px !important;
    margin-bottom: 8px !important;
    text-align: center !important;
}

.step-item-desc-center {
    color: #64748B !important;
    font-size: 13px !important;
    line-height: 1.6 !important;
    text-align: center !important;
}

/* ---------------- تذييل الموقع الأكاديمي ---------------- */
.footer-container {
    text-align: center !important;
    margin-top: 45px !important;
    padding-top: 20px !important;
    color: #94A3B8 !important;
    font-size: 13px !important;
    border-top: 1px solid #E2E8F0 !important;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 3. عرض ترويسة الواجهة (Hero Section) المحدثة بالتراصف العمودي التام للعنوان أسفل الشعار
hero_html = """
<div class="hero-wrapper">
    <div class="top-badge">✦ منصة ذكية عربية</div>
    
    <svg width="135" height="135" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="labeebGrad" x1="40" y1="40" x2="160" y2="160" gradientUnits="userSpaceOnUse">
                <stop offset="0
