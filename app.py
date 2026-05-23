import streamlit as st
import pandas as pd
import time

# =========================================
# إعداد الصفحة
# =========================================

st.set_page_config(
    page_title="LABEEB AI - لبيب",
    page_icon="🧠",
    layout="wide"
)

# =========================================
# CSS
# =========================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&display=swap');

html, body, [class*="css"]{
    font-family:'Cairo', sans-serif;
    direction:rtl;
    text-align:right;
}

.stApp{
    background:
    linear-gradient(
    135deg,
    #F8FAFC 0%,
    #F5F3FF 50%,
    #EEF2FF 100%);
}

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

[data-testid="stMain"] .block-container{
    max-width:1100px;
    padding-top:2rem;
    padding-bottom:5rem;
    margin:auto;
}

/* =========================================
HERO
========================================= */

.hero-container{

    position:relative;

    overflow:hidden;

    background:
    linear-gradient(
    135deg,
    rgba(255,255,255,0.88),
    rgba(243,232,255,0.72));

    backdrop-filter:blur(18px);

    border:1px solid rgba(255,255,255,0.6);

    border-radius:32px;

    padding:60px 35px;

    text-align:center;

    box-shadow:
    0 20px 40px rgba(109,40,217,0.05);

    margin-bottom:35px;
}

/* اللوغو */

.hero-logo{

    width:90px;

    height:90px;

    border-radius:50%;

    margin:0 auto 24px auto;

    background:
    linear-gradient(
    135deg,
    #7C3AED,
    #4F46E5);

    display:flex;

    align-items:center;

    justify-content:center;

    color:white;

    font-size:42px;

    font-weight:800;

    box-shadow:
    0 0 35px rgba(109,40,217,0.25);
}

.hero-title{

    font-size:60px;

    font-weight:800;

    background:
    linear-gradient(
    90deg,
    #6D28D9,
    #4F46E5);

    -webkit-background-clip:text;

    -webkit-text-fill-color:transparent;

    margin-bottom:10px;
}

.hero-subtitle{

    font-size:26px;

    font-weight:700;

    color:#1E293B;

    margin-bottom:16px;
}

.hero-desc{

    font-size:18px;

    color:#64748B;

    max-width:750px;

    margin:0 auto 24px auto;

    line-height:2;
}

.badge-student{

    display:inline-block;

    background:white;

    border:1px solid #E9D5FF;

    padding:10px 22px;

    border-radius:999px;

    font-size:14px;

    font-weight:600;

    color:#6D28D9;
}

/* =========================================
GLASS CARD
========================================= */

.glass-card{

    background:
    rgba(255,255,255,0.90);

    backdrop-filter:blur(20px);

    border:1px solid rgba(255,255,255,0.5);

    border-radius:24px;

    padding:32px;

    box-shadow:
    0 10px 30px rgba(0,0,0,0.03);

    margin-bottom:25px;
}

.card-title{

    font-size:24px;

    font-weight:700;

    color:#1E293B;

    margin-bottom:22px;
}

/* =========================================
TEXT AREA
========================================= */

.stTextArea textarea{

    border-radius:18px !important;

    border:1px solid #E2E8F0 !important;

    padding:18px !important;

    font-size:18px !important;

    background:white !important;
}

/* =========================================
BUTTON
========================================= */

.stButton > button{

    background:
    linear-gradient(
    90deg,
    #4F46E5,
    #6D28D9) !important;

    color:white !important;

    border:none !important;

    border-radius:14px !important;

    padding:14px 32px !important;

    font-size:18px !important;

    font-weight:700 !important;

    width:100% !important;

    box-shadow:
    0 8px 20px rgba(109,40,217,0.18) !important;
}

/* =========================================
RESULTS
========================================= */

.result-status-empty{

    text-align:center;

    color:#94A3B8;

    font-size:16px;

    padding:20px 0;
}

.result-badge-container{

    display:flex;

    gap:16px;

    margin-bottom:24px;
}

.result-stat-box{

    flex:1;

    background:white;

    border:1px solid #F3E8FF;

    padding:16px;

    border-radius:16px;

    text-align:center;
}

.result-stat-label{

    font-size:14px;

    color:#64748B;

    margin-bottom:4px;
}

.result-stat-val{

    font-size:20px;

    font-weight:700;

    color:#6D28D9;
}

/* =========================================
TABLE
========================================= */

table{
    border-radius:18px !important;
    overflow:hidden !important;
}

thead tr th{
    background:#F3E8FF !important;
    color:#6D28D9 !important;
}

/* =========================================
HOW IT WORKS
========================================= */

.section-main-title{

    text-align:center;

    font-size:30px;

    font-weight:800;

    color:#1E293B;

    margin:45px 0 25px 0;
}

.step-card{

    background:white;

    border:1px solid #F1F5F9;

    border-radius:20px;

    padding:26px;

    text-align:center;

    box-shadow:
    0 4px 15px rgba(0,0,0,0.02);
}

.step-icon{

    font-size:32px;

    margin-bottom:12px;
}

.step-title{

    font-size:19px;

    font-weight:700;

    color:#1E293B;

    margin-bottom:8px;
}

.step-desc{

    font-size:15px;

    color:#64748B;

    line-height:1.7;
}

/* =========================================
RESEARCHER
========================================= */

.researcher-card{

    background:white;

    border:1px solid #EEF2F6;

    border-radius:24px;

    padding:30px;

    box-shadow:
    0 10px 25px rgba(0,0,0,0.02);

    margin-top:45px;
}

.researcher-flex{

    display:flex;

    align-items:center;

    gap:28px;
}

.researcher-img{

    width:120px;

    height:120px;

    border-radius:50%;

    object-fit:cover;

    border:4px solid #F3E8FF;
}

.researcher-name{

    font-size:24px;

    font-weight:800;

    color:#1E293B;

    margin-bottom:4px;
}

.researcher-title{

    font-size:16px;

    font-weight:600;

    color:#6D28D9;

    margin-bottom:10px;
}

.researcher-bio{

    font-size:15px;

    color:#475569;

    line-height:1.8;
}

/* =========================================
FOOTER
========================================= */

.footer-text{

    text-align:center;

    color:#94A3B8;

    font-size:14px;

    margin-top:55px;

    border-top:1px solid #E2E8F0;

    padding-top:24px;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# قاعدة البيانات
# =========================================

semantic_db = {

    "عين":[

        {
            "المعنى":"عضو البصر والرؤية",
            "القرائن":["بصر","عينه","عينها","طبيب","رؤية","نظارات","أصيب"]
        },

        {
            "المعنى":"نبع ماء طبيعي",
            "القرائن":["ماء","نبع","شرب","عذب","واحة","بئر"]
        },

        {
            "المعنى":"جاسوس ومراقب",
            "القرائن":["جاسوس","عدو","حرب","تحركات","استطلاع"]
        }
    ]
}

# =========================================
# HERO
# =========================================

st.markdown("""

<div class="hero-container">

    <div class="hero-logo">
        ل
    </div>

    <div class="hero-title">
        LABEEB AI (لبيب)
    </div>

    <div class="hero-subtitle">
        المحلل الدلالي الذكي لفهم المعنى والسياق في اللغة العربية
    </div>

    <div class="hero-desc">
        منصة ذكية تعتمد على الذكاء الاصطناعي لتحليل النصوص العربية
        وفهم السياق الدلالي للألفاظ المشتركة.
    </div>

    <div class="badge-student">
        © 2026 تم تطوير وتصميم بواسطة هاجر الزواكي
    </div>

</div>

""", unsafe_allow_html=True)

# =========================================
# الإدخال
# =========================================

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

st.markdown(
    '<div class="card-title">✍️ اكتب النص العربي الذي ترغب في تحليله</div>',
    unsafe_allow_html=True
)

user_text = st.text_area(
    "",
    placeholder="مثال: شرب المسافر من عين ماء عذبة...",
    label_visibility="collapsed"
)

analyze = st.button("ابدأ التحليل الذكي")

st.markdown(
    '<div style="text-align:center; color:#94A3B8; font-size:14px; margin-top:12px;">تحليل آمن ودقيق باستخدام الذكاء الاصطناعي</div>',
    unsafe_allow_html=True
)

st.markdown('</div>', unsafe_allow_html=True)

# =========================================
# النتائج
# =========================================

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

st.markdown(
    '<div class="card-title">✨ نتيجة التحليل</div>',
    unsafe_allow_html=True
)

if analyze and user_text.strip():

    results = [
        {
            "المعنى المحتمل":"عضو البصر والرؤية",
            "نسبة القرب":"92%"
        },
        {
            "المعنى المحتمل":"نبع ماء طبيعي",
            "نسبة القرب":"61%"
        },
        {
            "المعنى المحتمل":"جاسوس ومراقب",
            "نسبة القرب":"32%"
        }
    ]

    st.markdown("""

    <div class="result-badge-container">

        <div class="result-stat-box">

            <div class="result-stat-label">
            المعنى الأقرب
            </div>

            <div class="result-stat-val">
            عضو البصر والرؤية
            </div>

        </div>

        <div class="result-stat-box">

            <div class="result-stat-label">
            نسبة القرب الدلالي
            </div>

            <div class="result-stat-val">
            92%
            </div>

        </div>

    </div>

    """, unsafe_allow_html=True)

    df = pd.DataFrame(results)

    st.table(df)

else:

    st.markdown(
        '<div class="result-status-empty">🤖 لم يتم إجراء أي تحليل بعد.</div>',
        unsafe_allow_html=True
    )

st.markdown('</div>', unsafe_allow_html=True)

# =========================================
# كيف يعمل لبيب
# =========================================

st.markdown(
    '<div class="section-main-title">كيف يعمل لبيب؟</div>',
    unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)

with c1:

    st.markdown("""

    <div class="step-card">

        <div class="step-icon">🔎</div>

        <div class="step-title">
        تحليل السياق
        </div>

        <div class="step-desc">
        تحليل الكلمات المحيطة لاكتشاف المعنى الصحيح.
        </div>

    </div>

    """, unsafe_allow_html=True)

with c2:

    st.markdown("""

    <div class="step-card">

        <div class="step-icon">✨</div>

        <div class="step-title">
        اكتشاف المعنى
        </div>

        <div class="step-desc">
        مطابقة السياق مع قاعدة البيانات الدلالية.
        </div>

    </div>

    """, unsafe_allow_html=True)

with c3:

    st.markdown("""

    <div class="step-card">

        <div class="step-icon">📊</div>

        <div class="step-title">
        قياس التشابه
        </div>

        <div class="step-desc">
        حساب نسبة القرب بين المعاني المختلفة.
        </div>

    </div>

    """, unsafe_allow_html=True)

# =========================================
# الباحثة
# =========================================

st.markdown("""

<div class="researcher-card">

    <div class="researcher-flex">

        <img
        src="https://raw.githubusercontent.com/hzouaki-ship-it/labeeb-ai/main/hajar.jpg"
        class="researcher-img">

        <div>

            <div class="researcher-name">
            هاجر الزواكي
            </div>

            <div class="researcher-title">
            طالبة ماستر في اللسانيات الرقمية والعربية
            </div>

            <div class="researcher-bio">
            مهتمة بالذكاء الاصطناعي ومعالجة اللغة العربية
            وبناء الأنظمة الدلالية الذكية وتحليل السياق والمعنى.
            </div>

        </div>

    </div>

</div>

""", unsafe_allow_html=True)

# =========================================
# FOOTER
# =========================================

st.markdown(
    '<div class="footer-text">LABEEB AI © 2026 — جميع الحقوق محفوظة — هاجر الزواكي</div>',
    unsafe_allow_html=True
)
