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
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center !important;
    padding: 20px 0 10px 0;
    width: 100%;
}

.top-badge {
    display: inline-flex;
    align-items: center;
    background-color: #FFFFFF;
    color: #6366F1;
    padding: 4px 16px;
    border-radius: 100px;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 25px;
    box-shadow: 0 2px 6px rgba(99, 102, 241, 0.08);
}

.hero-title {
    font-size: 38px !important;
    font-weight: 800 !important;
    color: #4C1D95 !important;
    margin: 15px 0 0 0 !important;
    line-height: 1.2 !important;
    text-align: center !important;
    width: 100%;
}

.hero-subtitle {
    font-size: 18px !important;
    font-weight: 700 !important;
    color: #1E293B !important;
    margin: 12px 0 !important;
    text-align: center !important;
    width: 100%;
}

.hero-description {
    font-size: 15px !important;
    color: #64748B !important;
    max-width: 650px;
    margin: 0 auto 20px auto !important;
    line-height: 1.7;
    text-align: center !important;
}

.author-badge {
    display: inline-block;
    background: #F3E8FF;
    color: #6B21A8 !important;
    padding: 6px 20px;
    border-radius: 100px;
    font-size: 13px !important;
    font-weight: 600;
    border: 1px solid #E9D5FF;
    margin-top: 5px;
}

/* ---------------- بطاقات الأقسام (Section Cards) ---------------- */
.section-card {
    background: #FFFFFF;
    border: 1px solid #F1F5F9;
    border-radius: 24px;
    padding: 35px;
    box-shadow: 0 4px 25px rgba(0, 0, 0, 0.015);
    margin-top: 30px;
    margin-bottom: 25px;
    text-align: right !important;
}

.card-title-container {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 8px;
    margin-bottom: 20px;
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
    border: 1px dashed #E2E8F0;
    border-radius: 16px;
    padding: 40px 20px;
    text-align: center !important;
    background: #FAFAFA;
}

.empty-icon-box {
    font-size: 36px;
    color: #6D28D9;
    background: #F3E8FF;
    width: 64px;
    height: 64px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 16px;
    margin-bottom: 16px;
}

.empty-main-text {
    color: #6D28D9;
    font-weight: 700;
    font-size: 16px;
    margin-bottom: 6px;
    text-align: center !important;
}

.empty-sub-text {
    color: #94A3B8;
    font-size: 13.5
