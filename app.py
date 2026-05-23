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

# 2. حقن التنسيقات العربية وتأمين واجهة المستخدم (RTL) دون أي تداخل في الأسطر
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&display=swap');

/* توحيد خط القاهرة وضبط الاتجاه العام للموقع من اليمين إلى اليسار */
html, body, [data-testid="stAppViewContainer"], .stApp {
    background-color: #FAFAFB !important;
    direction: rtl !important;
    text-align: right !important;
    font-family: 'Cairo', sans-serif !important;
}

/* تحديد أبعاد وحواف الحاوية الرئيسية للموقع */
[data-testid="stMain"] .block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
    max-width: 820px !important;
}

/* إلغاء المسافات العمودية العشوائية المفتعلة من محرك ستريمليت تلقائياً */
[data-testid="stVerticalBlock"] {
    gap: 0rem !important;
}

h1, h2, h3, h4, h5, h6, p, span, label, table, th, td {
    font-family: 'Cairo', sans-serif !important;
    text-align: right !important;
    direction: rtl !important;
}

/* ---------------- ترويسة الصفحة (Hero Section) ---------------- */
.hero-white-container {
    background: #FFFFFF;
    border: 1px solid #F1F5F9;
    border-radius: 24px;
    padding: 35px;
    text-align: center !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.01);
    margin-bottom: 25px;
}

.logo-flex-center {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 12px;
}

.main-hero-title {
    font-size: 38px !important;
    font-weight: 800 !important;
    color: #4C1D95 !important;
    margin: 0 0 4px 0 !important;
    text-align: center !important;
}

.main-hero-subtitle {
    font-size: 15px !important;
    font-weight: 400 !important;
    color: #64748B !important;
    margin: 0 0 16px 0 !important;
    text-align: center !important;
    letter-spacing: 0.5px;
}

.main-hero-desc {
    font-size: 15px !important;
    color: #1E293B !important;
    font-weight: 600;
    margin: 0 auto 20px auto !important;
    text-align: center !important;
}

/* صندوق البيو والتعريف الأكاديمي والجامعي للباحثة */
.academic-bio-box {
    background-color: #FAF5FF;
    border: 1px solid #E9D5FF;
    border-radius: 16px;
    padding: 20px;
    margin: 0 auto;
    max-width: 700px;
    text-align: center !important;
}

.academic-bio-text {
    font-size: 14.5px !important;
    color: #3B0764 !important;
    line-height: 1.8 !important;
    margin: 0 !important;
    text-align: center !important;
}

.academic-project-note {
    display: inline-block;
    font-size: 13px !important;
    color: #6B21A8 !important;
    font-weight: 700;
    margin-top: 10px !important;
    background: #F3E8FF;
    padding: 2px 14px;
    border-radius: 100px;
}

/* ---------------- بطاقات الأقسام (Section Cards) ---------------- */
.custom-section-card {
    background: #FFFFFF;
    border: 1px solid #F1F5F9;
    border-radius: 24px;
    padding: 35px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.01);
    margin-top: 25px;
    margin-bottom: 5px;
    text-align: right !important;
}

.card-icon-title-row {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 8px;
    margin-bottom: 18px;
}

.card-title-plain-text {
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
}

/* ---------------- تهيئة وتنسيق حالة ما قبل التحليل ---------------- */
.dashed-waiting-box {
    border: 1px dashed #E2E8F0;
    border-radius: 16px;
    padding: 35px 20px;
    text-align: center !important;
    background: #FAFAFA;
}

.waiting-icon {
    font-size: 34px;
    color: #6D28D9;
    background: #F3E8FF;
    width: 60px;
    height: 60px;
    display: inline-flex;
