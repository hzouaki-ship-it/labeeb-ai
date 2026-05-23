import streamlit as st
import pandas as pd
import time

# =========================================
# إعداد الصفحة الأساسي
# =========================================
st.set_page_config(
    page_title="LABEEB AI - لبيب",
    page_icon="🧠",
    layout="wide"
)

# =========================================
# واجهة التصميم الحديثة الاحترافية (Modern AI SaaS UI)
# =========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&display=swap');

/* فرض خط القاهرة والاتجاه */
html, body, [class*="css"] {
    font-family: 'Cairo', sans-serif;
    direction: rtl;
    text-align: right;
}

/* خلفية المنصة الفاتحة مع التموجات البنفسجية الناعمة */
.stApp {
    background: linear-gradient(135deg, #F8FAFC 0%, #F5F3FF 50%, #EFF6FF 100%);
}

/* إخفاء عناصر سترمليت الافتراضية لتبدو كمنصة مستقلة */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ضبط هوامش الحاوية الرئيسية */
[data-testid="stMain"] .block-container {
    max-width: 1000px;
    padding-top: 2.5rem;
    padding-bottom: 5rem;
    margin: 0 auto;
}

/* =========================================
1. HERO SECTION
========================================= */
.hero-container {
    position: relative;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.85), rgba(243, 232, 255, 0.7));
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.6);
    border-radius: 32px;
    padding: 50px 30px;
    text-align: center;
    box-shadow: 0 20px 40px rgba(109, 40, 217, 0.04);
    margin-bottom: 35px;
}

.hero-logo-glow {
    width: 90px;
    height: 90px;
    background: linear-gradient(135deg, #4F46E5, #6D28D9);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 20px auto;
    box-shadow: 0 0 25px rgba(109, 40, 217, 0.35);
    font-size: 38px;
    color: white;
}

.hero-title {
    font-size: 48px;
    font-weight: 800;
    background: linear-gradient(90deg, #6D28D9, #4F46E5);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}

.hero-subtitle {
    font-size: 24px;
    font-weight: 700;
    color: #1E293B;
    margin-bottom: 14px;
}

.hero-desc {
    font-size: 17px;
    color: #64748B;
    max-width: 650px;
    margin: 0 auto 24px auto;
    line-height: 1.8;
}

.badge-student {
    display: inline-block;
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid #E9D5FF;
    padding: 8px 20px;
    border-radius: 999px;
    font-size: 14px;
    font-weight: 600;
    color: #6D28D9;
    box-shadow: 0 4px 12px rgba(109, 40, 217, 0.04);
}

/* =========================================
2. INPUT & RESULT CARDS (Glassmorphism)
========================================= */
.glass-card {
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.5);
    border-radius: 24px;
    padding: 32px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.02);
    margin-bottom: 30px;
}

.card-title {
    font-size: 22px;
    font-weight: 700;
    color: #1E293B;
    margin-bottom: 20px;
}

/* تخصيص صندوق الكتابة */
.stTextArea textarea {
    border-radius: 16px !important;
    border: 1px solid #E2E8F0 !important;
    padding: 18px !important;
    font-size: 18px !important;
    background: rgba(255, 255, 255, 0.8) !important;
    line-height: 1.8 !important;
}

/* تخصيص زر التحليل الذكي المتدرج */
.stButton > button {
    background: linear-gradient(90deg, #4F46E5, #6D28D9) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 14px 32px !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    width: 100% !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 8px 20px rgba(109, 40, 217, 0.2) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 24px rgba(109, 40, 217, 0.3) !important;
}

.sub-button-text {
    text-align: center;
    color: #94A3B8;
    font-size: 14px;
    margin-top: 12px;
}

/* =========================================
3. RESULT SECTION
========================================= */
.result-status-empty {
    text-align: center;
    color: #94A3B8;
    font-size: 16px;
    padding: 20px 0;
}

.result-badge-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-bottom: 24px;
}

.result-stat-box {
    background: white;
    border: 1px solid #F3E8FF;
    padding: 16px;
    border-radius: 16px;
    text-align: center;
}

.result-stat-label {
    font-size: 14px;
    color: #64748B;
    margin-bottom: 4px;
}

.result-stat-val {
    font-size: 20px;
    font-weight: 700;
    color: #6D28D9;
}

/* =========================================
4. HOW IT WORKS SECTION
========================================= */
.section-main-title {
    text-align: center;
    font-size: 30px;
    font-weight: 800;
    color: #1E293B;
    margin: 45px 0 25px 0;
}

.step-card {
    background: white;
    border: 1px solid #F1F5F9;
    border-radius: 20px;
    padding: 26px;
    text-align: center;
    margin-bottom: 16px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.01);
}

.step-icon {
    font-size: 32px;
    margin-bottom: 12px;
}

.step-title {
    font-size: 19px;
    font-weight: 700;
    color: #1E293B;
    margin-bottom: 8px;
}

.step-desc
