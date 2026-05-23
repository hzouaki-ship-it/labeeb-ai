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
# CSS (التنسيق البصري المتناسق بالكامل)
# =========================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&display=swap');

html, body, [class*="css"]{
    font-family:'Cairo', sans-serif;
}

.stApp{
    direction:rtl;
    background:
    linear-gradient(
    135deg,
    #F8FAFC 0%,
    #F3F0FF 45%,
    #EEF2FF 100%);
}

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

[data-testid="stMain"] .block-container{
    max-width:1450px;
    padding-top:1.5rem;
    padding-bottom:4rem;
}

/* =========================================
HERO
========================================= */

.hero{
    position:relative;
    overflow:hidden;
    border-radius:40px;
    padding:60px 70px;
    margin-bottom:35px;
    background:
    linear-gradient(
    135deg,
    rgba(255,255,255,0.92),
    rgba(245,243,255,0.88));
    border:1px solid rgba(255,255,255,0.45);
    box-shadow:
    0 10px 35px rgba(139,92,246,0.08);
    backdrop-filter:blur(18px);
}

.hero-content{
    position:relative;
    z-index:2;
    display:flex;
    align-items:center;
    justify-content:center;
    gap:90px;
    flex-wrap:wrap;
}

.hero-logo{
    width:180px;
    height:180px;
    border-radius:50%;
    background:white;
    display:flex;
    align-items:center;
    justify-content:center;
    box-shadow:
    0 0 35px rgba(139,92,246,0.20);
    overflow:hidden;
}

.hero-logo img{
    width:125px;
}

.hero-text{
    text-align:center;
}

.hero-title{
    font-size:78px;
    font-weight:700;
    line-height:1.1;
    margin-bottom:14px;
    background:
    linear-gradient(
    90deg,
    #4F46E5,
    #9333EA);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.hero-subtitle{
    font-size:38px;
    font-weight:700;
    color:#374151;
    margin-bottom:18px;
}

.hero-description{
    font-size:24px;
    color:#64748B;
    line-height:2.2;
    max-width:900px;
    margin:auto;
}

.author-badge{
    margin-top:24px;
    display:inline-flex;
    align-items:center;
    background:white;
    padding:12px 24px;
    border-radius:999px;
    font-size:18px;
    color:#4B5563;
    box-shadow:
    0 4px 14px rgba(0,0,0,0.05);
}

/* =========================================
INPUT CARD
========================================= */

.glass-card{
    background:white;
    border-radius:28px;
    padding:28px;
    box-shadow:
    0 6px 22px rgba(0,0,0,0.04);
    border:1px solid #ECEBFF;
    margin-bottom:25px;
}

.section-title{
    font-size:34px;
    font-weight:800;
    color:#312E81;
    margin-bottom:25px;
    text-align:right;
}

.stTextArea textarea{
    border-radius:20px !important;
    border:2px solid #C4B5FD !important;
    padding:22px !important;
    font-size:20px !important;
    line-height:2 !important;
    background:#FCFCFF !important;
    min-height:160px !important;
}

/* =========================================
BUTTON
========================================= */

.stButton>button{
    background:
    linear-gradient(
    90deg,
    #4338CA,
    #9333EA);
    color:white;
    border:none;
    border-radius:14px;
    padding:14px 22px;
    font-size:20px;
    font-weight:700;
    width:280px;
    transition:0.3s ease;
    box-shadow:
    0 8px 18px rgba(139,92,246,0.22);
}

.stButton>button:hover{
    transform:translateY(-2px);
}

/* =========================================
RESULT
================================
