import streamlit as st
import pandas as pd
import time

# =========================================
# 1. إعدادات الصفحة وجعلها بكامل العرض (Wide)
# =========================================
st.set_page_config(
    page_title="LABEEB AI (لبيب)",
    page_icon="🧠",
    layout="wide"
)

# =========================================
# 2. هندسة التصميم الفاخر (CSS) واتجاه اليمين
# =========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Cairo', sans-serif;
    direction: rtl;
    text-align: right;
}

/* خلفية SaaS متدرجة واحترافية */
.stApp {
    background: linear-gradient(135deg, #F8FAFC 0%, #F3F0FF 45%, #EEF2FF 100%);
}

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* الحاوية الرئيسية للمنصة */
[data-testid="stMain"] .block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 4rem;
    margin: 0 auto;
}

/* ================= الهيدر الرئيسي (HERO) ================= */
.hero {
    position: relative;
    overflow: hidden;
    border-radius: 40px;
    padding: 60px 50px;
    margin-bottom: 40px;
    background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(245,243,255,0.90));
    border: 1px solid rgba(255,255,255,0.6);
    box-shadow: 0 20px 40px rgba(139,92,246,0.06);
    backdrop-filter: blur(20px);
    text-align: center;
}

.hero-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 25px;
}

/* اللوغو الممركز المتوهج */
.hero-logo-box {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    background: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 10px 30px rgba(139,92,246,0.25);
    border: 4px solid #E9D5FF;
}

.hero-logo-box img {
    width: 90px;
    height: 90px;
    object-fit: contain;
}

.hero-title {
    font-size: 65px;
    font-weight: 800;
    margin: 10px 0;
    background: linear-gradient(90deg, #4F46E5, #9333EA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 30px;
    font-weight: 700;
    color: #1E1B4B;
    margin-bottom: 10px;
}

.hero-description {
    font-size: 20px;
    color: #64748B;
    max-width: 850px;
    line-height: 1.8;
}

.author-badge {
    background: #FFFFFF;
    padding: 10px 24px;
    border-radius: 999px;
    font-size: 16px;
    color: #4338CA;
    font-weight: 600;
    box-shadow: 0 4px 15px rgba(0,0,0,0.04);
    border: 1px solid #E2E8F0;
}

/* ================= بطاقات الإدخال والنتائج ================= */
.glass-card {
    background: #FFFFFF;
    border-radius: 28px;
    padding: 35px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.02);
    border: 1px solid #E2E8F0;
    margin-bottom: 35px;
}

.section-title {
    font-size: 28px;
    font-weight: 800;
    color: #1E3A8A;
    margin-bottom:
