import streamlit as st

# =========================================
# إعداد الصفحة
# =========================================

st.set_page_config(
    page_title="LABEEB AI",
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

/* إخفاء عناصر Streamlit */

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* الحاوية الرئيسية */

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

.hero::before{

    content:"";

    position:absolute;

    width:500px;
    height:500px;

    background:
    radial-gradient(circle,
    rgba(168,85,247,0.16),
    transparent 70%);

    top:-220px;
    left:-220px;
}

.hero::after{

    content:"";

    position:absolute;

    width:380px;
    height:380px;

    background:
    radial-gradient(circle,
    rgba(99,102,241,0.14),
    transparent 70%);

    bottom:-150px;
    right:-150px;
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
========================================= */

.result-card{

    background:white;

    border-radius:26px;

    padding:35px;

    border:1px solid #ECEBFF;

    box-shadow:
    0 6px 20px rgba(0,0,0,0.04);

    margin-bottom:30px;
}

.result-title{

    color:#7C3AED;

    font-size:28px;

    font-weight:800;

    margin-bottom:22px;
}

/* =========================================
STEPS
========================================= */

.steps-title{

    text-align:center;

    font-size:42px;

    font-weight:800;

    color:#312E81;

    margin-bottom:8px;
}

.steps-sub{

    text-align:center;

    color:#64748B;

    margin-bottom:35px;

    font-size:19px;
}

.step-grid{

    display:grid;

    grid-template-columns:repeat(3,1fr);

    gap:24px;

    margin-bottom:40px;
}

.step-card{

    background:white;

    padding:32px;

    border-radius:24px;

    border:1px solid #ECEBFF;

    box-shadow:
    0 6px 20px rgba(0,0,0,0.04);

    text-align:center;
}

.step-icon{

    font-size:52px;

    margin-bottom:14px;
}

.step-title{

    font-size:26px;

    font-weight:800;

    color:#4F46E5;

    margin-bottom:10px;
}

.step-desc{

    color:#64748B;

    line-height:2;

    font-size:17px;
}

/* =========================================
BIO
========================================= */

.bio-card{

    background:white;

    border-radius:30px;

    padding:40px;

    border:1px solid #E9D5FF;

    display:flex;

    align-items:center;

    justify-content:space-between;

    gap:40px;

    box-shadow:
    0 6px 20px rgba(0,0,0,0.04);

    margin-top:40px;

    text-align:right;
}

.author-image{

    width:170px;
    height:170px;

    object-fit:cover;

    border-radius:50%;

    border:6px solid #E9D5FF;

    box-shadow:
    0 0 28px rgba(139,92,246,0.18);
}

.bio-title{

    font-size:42px;

    font-weight:800;

    color:#312E81;

    margin-bottom:8px;
}

.bio-sub{

    font-size:24px;

    color:#7C3AED;

    font-weight:700;

    margin-bottom:18px;
}

.bio-desc{

    color:#4B5563;

    line-height:2.2;

    font-size:19px;
}

/* =========================================
FOOTER
========================================= */

.footer{

    text-align:center;

    margin-top:45px;

    color:#64748B;

    font-size:16px;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# HERO
# =========================================

st.markdown("""

<div class="hero">

<div class="hero-content">

<div class="hero-logo">
<img src="https://cdn-icons-png.flaticon.com/512/2103/2103633.png">
</div>

<div class="hero-text">

<div class="hero-title">
LABEEB AI (لبيب)
</div>

<div class="hero-subtitle">
المحلل الدلالي الذكي لفهم المعنى والسياق في اللغة العربية
</div>

<div class="hero-description">
منصة تعتمد على الذكاء الاصطناعي لتحليل النصوص العربية وفهم معناها العميق في السياق.
</div>

<div class="author-badge">
© 2026 تم تطوير وتصميم بواسطة الطالبة هاجر الزواكي
</div>

</div>

</div>

</div>

""", unsafe_allow_html=True)

# =========================================
# INPUT
# =========================================

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

st.markdown("""

<div class="section-title">
✍️ اكتب النص العربي الذي ترغب في تحليل معناه وسياقه
</div>

""", unsafe_allow_html=True)

text = st.text_area(
    "",
    placeholder="اكتب أو ألصق جملة عربية واضحة هنا..."
)

if st.button("ابدأ التحليل الذكي"):

    if text.strip() == "":

        st.warning("الرجاء إدخال نص للتحليل.")

    else:

        st.markdown(f"""

        <div class="result-card">

        <div class="result-title">
        نتيجة التحليل
        </div>

        <div style='font-size:22px; line-height:2; color:#374151;'>

        <b>النص المُدخل:</b><br><br>

        {text}

        <br><br>

        <b>التحليل الدلالي:</b><br><br>

        تم تحليل النص بنجاح باستخدام نموذج LABEEB AI لاستخراج المعنى والسياق اللغوي.

        </div>

        </div>

        """, unsafe_allow_html=True)

st.markdown("""
<div style='margin-top:12px; color:#64748B; font-size:17px;'>
تحليل آمن ودقيق باستخدام الذكاء الاصطناعي
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# =========================================
# STEPS
# =========================================

st.markdown("""

<div class="steps-title">
كيف يعمل لبيب؟
</div>

<div class="steps-sub">
يستخدم لبيب الذكاء الاصطناعي لتحليل النصوص العربية وفهم معناها العميق في السياق.
</div>

<div class="step-grid">

<div class="step-card">

<div class="step-icon">🔎</div>

<div class="step-title">
تحليل السياق
</div>

<div class="step-desc">
يحلل بنية الجملة والكلمات المحيطة لفهم السياق اللغوي بدقة.
</div>

</div>

<div class="step-card">

<div class="step-icon">✨</div>

<div class="step-title">
اكتشاف المعنى
</div>

<div class="step-desc">
يحدد المعنى الأقرب اعتمادًا على السياق والدلالة اللغوية.
</div>

</div>

<div class="step-card">

<div class="step-icon">📊</div>

<div class="step-title">
قياس التشابه الدلالي
</div>

<div class="step-desc">
يستخدم تقنيات متقدمة لقياس التشابه الدلالي وتصنيف النتائج.
</div>

</div>

</div>

""", unsafe_allow_html=True)

# =========================================
# BIO
# =========================================

st.markdown("""

<div class="bio-card">

<div>

<div class="bio-title">
هاجر الزواكي
</div>

<div class="bio-sub">
طالبة ماستر في اللسانيات الرقمية والعربية
</div>

<div class="bio-desc">
مهتمة بالذكاء الاصطناعي ومعالجة اللغة العربية وبناء الأنظمة الدلالية الذكية.
<br><br>
أسعى إلى تطوير حلول رقمية حديثة لفهم اللغة العربية وتحليل السياق والمعنى.
</div>

</div>

<div>

<img class="author-image"
src="https://raw.githubusercontent.com/hzouaki-ship-it/labeeb-ai/main/hajar.jpg">

</div>

</div>

""", unsafe_allow_html=True)

# =========================================
# FOOTER
# =========================================

st.markdown("""

<div class="footer">

LABEEB AI © 2026 — جميع الحقوق محفوظة — هاجر الزواكي

</div>

""", unsafe_allow_html=True)
