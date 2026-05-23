import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import time

# 1. إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="منصة لبيب LABEEB AI",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. التنسيقات الشاملة لتطابق الهوية البصرية 100% (CSS)
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&display=swap');

/* تنسيق الخلفية العامة للمنصة */
html, body, [data-testid="stAppViewContainer"], .stApp {
    background-color: #F8FAFC !important;
    background-image: radial-gradient(at 50% 0%, rgba(233, 213, 255, 0.45) 0px, transparent 50%) !important;
    direction: rtl !important;
    text-align: right !important;
    font-family: 'Cairo', sans-serif !important;
}

/* ضبط أبعاد الحاوية الرئيسية */
[data-testid="stMain"] .block-container {
    max-width: 920px !important;
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
}

h1, h2, h3, h4, h5, h6, p, span, label, div {
    font-family: 'Cairo', sans-serif !important;
    direction: rtl !important;
    text-align: right !important;
}

/* الشارات العلوية */
.badge-top-container {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    width: 100% !important;
    margin-bottom: -10px !important;
}
.grid-dots {
    font-size: 22px !important;
    color: #C7D2FE !important;
    letter-spacing: 2px !important;
    line-height: 1 !important;
    font-weight: bold;
}
.floating-badge {
    background: white !important;
    color: #4F46E5 !important;
    padding: 6px 16px !important;
    border-radius: 100px !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 8px rgba(79, 70, 229, 0.08) !important;
    border: 1px solid #E2E8F0 !important;
}

/* قسم الهيدر الرئيسي ممركز بالكامل */
.hero-wrapper {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    padding: 10px 0 30px 0 !important;
    width: 100% !important;
}
.hero-title {
    font-size: 48px !important;
    font-weight: 800 !important;
    color: #6D28D9 !important;
    margin: 15px 0 0 0 !important;
    text-align: center !important;
    width: 100% !important;
}
.hero-subtitle {
    font-size: 20px !important;
    font-weight: 700 !important;
    color: #4338CA !important;
    margin: 8px 0 0 0 !important;
    text-align: center !important;
    width: 100% !important;
}
.hero-description {
    font-size: 14px !important;
    color: #64748B !important;
    margin: 8px 0 0 0 !important;
    text-align: center !important;
    width: 100% !important;
}
.author-badge {
    margin-top: 15px !important;
    background: transparent !important;
    color: #64748B !important;
    font-size: 12.5px !important;
    font-weight: 600 !important;
    display: flex !important;
    align-items: center !important;
    gap: 5px !important;
}

/* تصميم البطاقات الموحدة */
.section-card {
    background: white !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 16px !important;
    padding: 24px 30px !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.01) !important;
    margin-top: 25px !important;
}
.card-header-row {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    margin-bottom: 18px !important;
}
.card-title-text {
    font-size: 16px !important;
    font-weight: 700 !important;
    color: #1E293B !important;
    margin: 0 !important;
}
.card-icon {
    font-size: 18px !important;
    color: #7C3AED !important;
}

/* الحقول والأزرار تتبع ستايل المنصة الفاخر */
.stTextArea textarea {
    border-radius: 10px !important;
    border: 1px solid #CBD5E1 !important;
    padding: 15px !important;
    font-size: 14.5px !important;
    background-color: #FFFFFF !important;
}
.stTextArea textarea:focus {
    border-color: #A78BFA !important;
    box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.15) !important;
}
div.stButton > button {
    background: linear-gradient(90deg, #5B21B6, #7C3AED) !important;
    color: white !important;
    font-family: 'Cairo', sans-serif !important;
    font-weight: 700 !important;
    font-size: 14.5px !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 10px 28px !important;
    box-shadow: 0 4px 15px rgba(91, 33, 182, 0.2) !important;
    transition: all 0.2s ease !important;
}
div.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(91, 33, 182, 0.3) !important;
}
.security-note {
    font-size: 12px !important;
    color: #94A3B8 !important;
    margin-top: 10px !important;
    display: flex !important;
    align-items: center !important;
    gap: 4px !important;
}

/* صندوق الحالة الفارغة الافتراضي */
.empty-box {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    padding: 30px 0 !important;
    border
