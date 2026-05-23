import streamlit as st
import pandas as pd
import time

# =========================================
# إعداد الصفحة
# =========================================
st.set_page_config(
    page_title="LABEEB AI",
    page_icon="🧠",
    layout="wide"
)

# =========================================
# CSS - التنسيق البصري المتناسق والأنيق بالكامل
# =========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Cairo', sans-serif;
}

.stApp {
    direction: rtl;
    background: linear-gradient(135deg, #F8FAFC 0%, #F3F0FF 45%, #EEF2FF 100%);
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

[data-testid="stMain"] .block-container {
    max-width: 1450px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}

/* HERO SECTION */
.hero {
    position: relative;
    overflow: hidden;
    border-radius: 40px;
    padding: 60px 70px;
    margin-bottom: 35px;
    background: linear-gradient(135deg, rgba(255,255,255,0.92), rgba(245,243,255,0.88));
    border: 1px solid rgba(255,255,255,0.45);
    box-shadow: 0 10px 35px rgba(139,92,246,0.08);
    backdrop-filter: blur(18px);
}

.hero-content {
    position: relative;
    z-index: 2;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 90px;
    flex-wrap: wrap;
}

.hero-logo {
    width: 180px;
    height: 180px;
    border-radius: 50%;
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 35px rgba(139,92,246,0.20);
    overflow: hidden;
}

.hero-logo img {
    width: 125px;
}

.hero-text {
    text-align: center;
}

.hero-title {
    font-size: 78px;
    font-weight: 700;
    line-height: 1.1;
    margin-bottom: 14px;
    background: linear-gradient(90deg, #4F46E5, #9333EA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 38px;
    font-weight: 700;
    color: #374151;
    margin-bottom: 18px;
}

.hero-description {
    font-size: 24px;
    color: #64748B;
    line-height: 2.2;
    max-width: 900px;
    margin: auto;
}

.author-badge {
    margin-top: 24px;
    display: inline-flex;
    align-items: center;
    background: white;
    padding: 12px 24px;
    border-radius: 999px;
    font-size: 18px;
    color: #4B5563;
    box-shadow: 0 4px 14px rgba(0,0,0,0.05);
}

/* INPUT CARD */
.glass-card {
    background: white;
    border-radius: 28px;
    padding: 28px;
    box-shadow: 0 6px 22px rgba(0,0,0,0.04);
    border: 1px solid #ECEBFF;
    margin-bottom: 25px;
}

.section-title {
    font-size: 34px;
    font-weight: 800;
    color: #312E81;
    margin-bottom: 25px;
    text-align: right;
}

.stTextArea textarea {
    border-radius: 20px !important;
    border: 2px solid #C4B5FD !important;
    padding: 22px !important;
    font-size: 20px !important;
    line-height: 2 !important;
    background: #FCFCFF !important;
    min-height: 160px !important;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(90deg, #4338CA, #9333EA);
    color: white;
    border: none;
    border-radius: 14px;
    padding: 14px 22px;
    font-size: 20px;
    font-weight: 700;
    width: 280px;
    transition: 0.3s ease;
    box-shadow: 0 8px 18px rgba(139,92,246,0.22);
}

.stButton>button:hover {
    transform: translateY(-2px);
}

/* RESULT CARD */
.result-card {
    background: white;
    border-radius: 26px;
    padding: 35px;
    border: 1px solid #ECEBFF;
    box-shadow: 0 6px 20px rgba(0,0,0,0.04);
    margin-bottom: 30px;
}

.result-title {
    color: #7C3AED;
    font-size: 28px;
    font-weight: 800;
    margin-bottom: 22px;
}

/* STEPS SECTION */
.steps-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: #312E81;
    margin-bottom: 8px;
}

.steps-sub {
    text-align: center;
    color: #64748B;
    margin-bottom: 35px;
    font-size: 19px;
}

.step-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
    margin-bottom: 40px;
}

.step-card {
    background: white;
    padding: 32px;
    border-radius: 24px;
    border: 1px solid #ECEBFF;
    box-shadow: 0 6px 20px rgba(0,0,0,0.04);
    text-align: center;
}

.step-icon {
    font-size: 52px;
    margin-bottom: 14px;
}

.step-title {
    font-size: 26px;
    font-weight: 800;
    color: #4F46E5;
    margin-bottom: 10px;
}

.step-desc {
    color: #64748B;
    line-height: 2;
    font-size: 17px;
}

/* BIO CARD */
.bio-card {
    background: white;
    border-radius: 30px;
    padding: 40px;
    border: 1px solid #E9D5FF;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 40px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.04);
    margin-top: 40px;
    text-align: right;
}

.author-image {
    width: 170px;
    height: 170px;
    object-fit: cover;
    border-radius: 50%;
    border: 6px solid #E9D5FF;
    box-shadow: 0 0 28px rgba(139,92,246,0.18);
}

.bio-title {
    font-size: 42px;
    font-weight: 800;
    color: #312E81;
    margin-bottom: 8px;
}

.bio-sub {
    font-size: 24px;
    color: #7C3AED;
    font-weight: 700;
    margin-bottom: 18px;
}

.bio-desc {
    color: #4B5563;
    line-height: 2.2;
    font-size: 19px;
}

/* FOOTER */
.footer {
    text
