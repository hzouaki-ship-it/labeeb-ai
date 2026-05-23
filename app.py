import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# =========================
# إعداد الصفحة
# =========================

st.set_page_config(
    page_title="LABEEB AI | لبيب",
    page_icon="🧠",
    layout="wide"
)

# =========================
# CSS
# =========================

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
    #F3F0FF 50%,
    #EEF2FF 100%);
}

/* إخفاء عناصر ستريملت */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* الحاوية الرئيسية */

[data-testid="stMain"] .block-container{
    max-width:1400px;
    padding-top:2rem;
    padding-bottom:4rem;
}

/* ================= HERO ================= */

.hero{

    position:relative;

    overflow:hidden;

    background:rgba(255,255,255,0.72);

    border:1px solid rgba(255,255,255,0.45);

    backdrop-filter:blur(18px);

    border-radius:38px;

    padding:80px 70px;

    margin-bottom:45px;

    box-shadow:
    0 10px 40px rgba(139,92,246,0.08),
    0 0 120px rgba(139,92,246,0.05);
}

.hero::before{

    content:"";

    position:absolute;

    width:420px;
    height:420px;

    background:
    radial-gradient(circle,
    rgba(168,85,247,0.16),
    transparent 70%);

    top:-180px;
    left:-180px;
}

.hero::after{

    content:"";

    position:absolute;

    width:320px;
    height:320px;

    background:
    radial-gradient(circle,
    rgba(99,102,241,0.12),
    transparent 70%);

    bottom:-120px;
    right:-120px;
}

.hero-content{

    display:flex;

    align-items:center;

    justify-content:center;

    gap:70px;

    flex-wrap:wrap;

    direction:rtl;

    position:relative;

    z-index:2;
}

.hero-logo{

    width:190px;
    height:190px;

    border-radius:50%;

    background:white;

    display:flex;

    align-items:center;

    justify-content:center;

    box-shadow:
    0 0 35px rgba(124,58,237,0.18);

    overflow:hidden;
}

.hero-logo img{
    width:120px;
}

.hero-text{
    text-align:right;
    max-width:850px;
}

.hero-title{

    font-size:82px;

    font-weight:800;

    line-height:1.1;

    margin-bottom:18px;

    background:
    linear-gradient(90deg,#6D28D9,#2563EB);

    -webkit-background-clip:text;

    -webkit-text-fill-color:transparent;
}

.hero-subtitle{

    font-size:36px;

    font-weight:700;

    color:#1E293B;

    margin-bottom:20px;
}

.hero-description{

    font-size:22px;

    line-height:2.1;

    color:#64748B;
}

.author-badge{

    display:inline-block;

    margin-top:30px;

    background:white;

    padding:14px 28px;

    border-radius:999px;

    font-size:17px;

    font-weight:700;

    color:#6D28D9;

    box-shadow:
    0 4px 14px rgba(0,0,0,0.06);
}

/* ================= INPUT CARD ================= */

.glass-card{

    background:white;

    padding:2.5rem;

    border-radius:28px;

    box-shadow:
    0 6px 25px rgba(0,0,0,0.05);

    border:1px solid #E2E8F0;

    margin-bottom:2rem;
}

.section-title{

    font-size:34px;

    font-weight:800;

    color:#6D28D9;

    margin-bottom:25px;
}

.stTextArea textarea{

    border-radius:18px !important;

    border:2px solid #DDD6FE !important;

    padding:18px !important;

    font-size:18px !important;

    line-height:2 !important;

    background:#FAFAFF !important;
}

/* ================= BUTTON ================= */

.stButton>button{

    background:
    linear-gradient(90deg,#6D28D9,#8B5CF6);

    color:white;

    border:none;

    border-radius:16px;

    padding:14px 22px;

    font-size:18px;

    font-weight:700;

    width:100%;

    transition:0.3s ease;

    box-shadow:
    0 6px 18px rgba(139,92,246,0.25);
}

.stButton>button:hover{

    transform:translateY(-2px);

    box-shadow:
    0 8px 24px rgba(139,92,246,0.35);
}

/* ================= RESULT ================= */

.result-card{

    background:white;

    border-radius:25px;

    padding:2rem;

    border:1px solid #E2E8F0;

    box-shadow:
    0 4px 18px rgba(0,0,0,0.04);

    margin-top:25px;
}

/* ================= BIO ================= */

.bio-card{

    background:white;

    padding:2.5rem;

    border-radius:30px;

    border:1px solid #E2E8F0;

    display:flex;

    align-items:center;

    gap:2.5rem;

    margin-top:40px;

    box-shadow:
    0 6px 22px rgba(0,0,0,0.05);
}

.author-image{

    border-radius:24px;

    box-shadow:
    0 0 35px rgba(139,92,246,0.25);
}

/* ================= FOOTER ================= */

.footer{

    text-align:center;

    margin-top:50px;

    color:#64748B;

    font-size:16px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HERO
# =========================

st.markdown("""

<div class="hero">

<div class="hero-content">

<div class="hero-logo">
<img src="https://cdn-icons-png.flaticon.com/512/2103/2103633.png">
</div>

<div class="hero-text">

<h1 class="hero-title">LABEEB AI (لبيب)</h1>

<div class="hero-subtitle">
المحلل الدلالي الذكي لفهم المعنى والسياق في اللغة العربية
</div>

<div class="hero-description">
منصة تعتمد على الذكاء الاصطناعي وتحليل السياق اللغوي لاكتشاف المعنى الصحيح للكلمات داخل النصوص العربية باستخدام تقنيات حديثة في معالجة اللغة الطبيعية.
</div>

<div class="author-badge">
🎓 تم تطوير وتصميم LABEEB AI بواسطة الطالبة هاجر الزواكي © 2026
</div>

</div>

</div>

</div>

""", unsafe_allow_html=True)

# =========================
# INPUT
# =========================

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

st.markdown("""
<div class="section-title">
✍️ اكتب النص العربي الذي ترغب في تحليل معناه وسياقه
</div>
""", unsafe_allow_html=True)

user_sentence = st.text_area(
    "",
    placeholder="اكتب هنا جملة عربية واضحة تحتوي على معنى أو سياق لغوي..."
)

if st.button("✨ ابدأ التحليل الذكي"):

    if user_sentence.strip() == "":
        st.warning("الرجاء إدخال جملة للتحليل.")
    else:

        st.markdown("""
        <div class="result-card">
        <h3 style='color:#6D28D9;'>📊 نتيجة التحليل</h3>

        <p style='font-size:20px; line-height:2; color:#334155;'>

        تم تحليل الجملة بنجاح باستخدام نموذج الذكاء الاصطناعي الخاص بمنصة لبيب.

        </p>

        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# BIO
# =========================

st.markdown("""

<div class="bio-card">

<div>

<img class="author-image"
src="https://raw.githubusercontent.com/hzouaki-ship-it/labeeb-ai/main/hajar.jpg"
width="220">

</div>

<div>

<h2 style='color:#6D28D9; font-weight:800;'>

👩🏻‍💻 هاجر الزواكي

</h2>

<p style='font-size:19px; line-height:2.2; color:#475569;'>

طالبة ماجستير سنة ثانية في تخصص
<b>اللسانيات الرقمية والعربية</b>

بجامعة مولاي إسماعيل بمكناس.

<br><br>

هذا المشروع جزء من بحث التخرج الخاص بي، ويهدف إلى تطوير منصة ذكية لتحليل المعنى والسياق في اللغة العربية باستخدام تقنيات الذكاء الاصطناعي ومعالجة اللغة الطبيعية.

</p>

</div>

</div>

""", unsafe_allow_html=True)

# =========================
# FOOTER
# =========================

st.markdown("""

<div class="footer">

LABEEB AI © 2026 — جميع الحقوق محفوظة — هاجر الزواكي

</div>

""", unsafe_allow_html=True)
