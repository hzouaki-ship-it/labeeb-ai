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

# 2. هندسة الـ CSS المتقدمة ومحاكاة التصميم المطلوبة بأمان
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"], .stApp {
    background-color: #F9FAFB !important;
    direction: RTL !important;
    text-align: right !important;
    font-family: 'Cairo', sans-serif !important;
}

[data-testid="stMain"] .block-container {
    padding-top: 0rem !important;
    padding-bottom: 3rem !important;
    max-width: 850px !important;
}

[data-testid="stVerticalBlock"] {
    gap: 0rem !important;
}

h1, h2, h3, h4, h5, h6, p, span, label {
    font-family: 'Cairo', sans-serif !important;
}

/* القسم العلوي */
.hero-outer {
    margin-left: -4rem;
    margin-right: -4rem;
    background: linear-gradient(180deg, #EBF0FF 0%, #F4EFFF 60%, #F9FAFB 100%);
    padding: 50px 40px 60px 40px;
    text-align: center !important;
    position: relative;
    overflow: hidden;
    border-bottom-left-radius: 50px 20px;
    border-bottom-right-radius: 50px 20px;
}

.hero-dots-left {
    position: absolute;
    top: 30px;
    left: 40px;
    width: 60px;
    height: 60px;
    background-image: radial-gradient(#94A3B8 1.5px, transparent 1.5px);
    background-size: 12px 12px;
    opacity: 0.4;
}

.hero-dots-right {
    position: absolute;
    bottom: 40px;
    right: 40px;
    width: 60px;
    height: 60px;
    background-image: radial-gradient(#94A3B8 1.5px, transparent 1.5px);
    background-size: 12px 12px;
    opacity: 0.4;
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
    margin-bottom: 24px;
    box-shadow: 0 2px 6px rgba(99, 102, 241, 0.08);
}

.hero-logo-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 14px;
    margin-bottom: 12px;
}

.hero-logo-icon {
    background: #FFFFFF;
    width: 64px;
    height: 64px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.hero-title {
    font-size: 46px !important;
    font-weight: 800 !important;
    color: #5B21B6 !important;
    margin: 0 !important;
    line-height: 1.2;
}

.hero-subtitle {
    font-size: 18px !important;
    font-weight: 700 !important;
    color: #1E293B !important;
    margin-top: 14px !important;
    margin-bottom: 14px !important;
}

.hero-description {
    font-size: 15px !important;
    color: #64748B !important;
    max-width: 650px;
    margin: 0 auto 24px auto !important;
    line-height: 1.7;
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
}

/* بطاقات الحاوية */
.section-card {
    background: #FFFFFF;
    border: 1px solid #F1F5F9;
    border-radius: 24px;
    padding: 35px;
    box-shadow: 0 4px 25px rgba(0, 0, 0, 0.015);
    margin-top: 30px;
    margin-bottom: 5px;
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

/* المدخلات والزر */
.stTextArea textarea {
    background-color: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 16px !important;
    padding: 18px !important;
    font-family: 'Cairo', sans-serif !important;
    font-size: 14.5px !important;
    color: #334155 !important;
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

/* صندوق الحالة الفارغة */
.inner-dashed-box {
    border: 1px dashed #E2E8F0;
    border-radius: 16px;
    padding: 40px 20px;
    text-align: center;
    background: #FAFAFA;
}

.empty-icon-box {
    font-size: 36px;
    color: #6D28D9;
