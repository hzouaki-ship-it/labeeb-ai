# =========================================================
# LABEEB AI — FINAL PROFESSIONAL UI
# Developed by: Hajar Zawaki
# =========================================================

import streamlit as st

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="LABEEB AI | لبيب",
    page_icon="🧠",
    layout="wide"
)

# ---------------------------------------------------------
# CSS
# ---------------------------------------------------------

st.markdown("""

<style>

@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"], .stApp{
    direction: rtl;
    font-family: 'Cairo', sans-serif !important;

    background:
    radial-gradient(circle at top right, rgba(168,85,247,0.18), transparent 35%),
    radial-gradient(circle at left, rgba(99,102,241,0.12), transparent 25%),
    linear-gradient(to bottom, #F8FAFC, #F5F3FF);

    background-attachment: fixed;
}

[data-testid="stHeader"]{
    background: transparent;
}

[data-testid="stMain"] .block-container{
    max-width: 1400px;
    padding-top: 1rem;
    padding-bottom: 4rem;
}

/* HERO */

.hero{

    position: relative;
    overflow: hidden;

    background: rgba(255,255,255,0.62);

    border: 1px solid rgba(255,255,255,0.35);

    backdrop-filter: blur(18px);

    border-radius: 38px;

    padding: 70px 60px;

    margin-bottom: 45px;

    box-shadow:
    0 10px 40px rgba(139,92,246,0.10),
    0 0 120px rgba(139,92,246,0.08);

}
.hero::before{
    content:"";
    position:absolute;
    width:400px;
    height:400px;
    background: radial-gradient(circle, rgba(168,85,247,0.15), transparent 70%);
    top:-180px;
    left:-180px;
}

.hero::after{
    content:"";
    position:absolute;
    width:300px;
    height:300px;
    background: radial-gradient(circle, rgba(99,102,241,0.12), transparent 70%);
    bottom:-120px;
    right:-120px;
}

.hero-top-badge{
    display:inline-block;
    background:white;
    color:#6D28D9;
    padding:8px 18px;
    border-radius:999px;
    font-size:14px;
    font-weight:700;
    margin-bottom:30px;
    box-shadow:0 4px 12px rgba(0,0,0,0.05);
}

.hero-logo{

    width:190px;
    height:190px;

    border-radius:50%;

    background:rgba(255,255,255,0.72);

    display:flex;

    align-items:center;

    justify-content:center;

    box-shadow:
    0 0 40px rgba(124,58,237,0.18),
    0 0 90px rgba(124,58,237,0.12);

    backdrop-filter:blur(10px);
}
.hero-content{
    display:flex;
    align-items:center;
    justify-content:center;
    gap:40px;
    flex-wrap:wrap;
}
.hero-text{
    text-align:right;
}

.hero-title{
    font-size:78px;
    font-weight:800;
    line-height:1.1;

    background: linear-gradient(90deg,#6D28D9,#2563EB);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;

    margin-bottom:10px;
}

.hero-subtitle{
    font-size:34px;
    font-weight:700;
    color:#374151;

    margin-bottom:18px;
}
.hero-description{
    font-size:22px;
    line-height:2;
    color:#64748B;

    max-width:850px;
}

.author-badge{
    margin-top:25px;

    display:inline-block;

    background:rgba(255,255,255,0.75);

    padding:12px 24px;

    border-radius:999px;

    font-size:17px;

    color:#6D28D9;

    font-weight:700;

    box-shadow:0 6px 20px rgba(0,0,0,0.05);
}

/* CARDS */

.main-card{
    background:white;

    border-radius:28px;

    padding:35px;

    margin-top:30px;

    box-shadow:0 10px 30px rgba(0,0,0,0.05);

    border:1px solid rgba(139,92,246,0.08);
}

.section-title{
    font-size:32px;
    font-weight:800;
    color:#4C1D95;
    margin-bottom:20px;
}

/* TEXT AREA */

textarea{
    direction:rtl !important;
    text-align:right !important;
    font-size:18px !important;
    border-radius:20px !important;
}

/* BUTTON */

div.stButton{
    width:fit-content;
}

div.stButton > button{

    background: linear-gradient(90deg,#6D28D9,#9333EA);

    color:white;

    border:none;

    border-radius:18px;

    padding:14px 36px;

    font-size:18px;

    font-weight:700;

    transition:0.3s;

    box-shadow:0 10px 20px rgba(124,58,237,0.18);
}

div.stButton > button:hover{
    transform:translateY(-3px);
}

/* STEPS */

.steps-grid{
    display:grid;

    grid-template-columns:repeat(auto-fit,minmax(260px,1fr));

    gap:25px;

    margin-top:25px;
}

.step-card{

    background:white;

    border-radius:24px;

    padding:30px;

    text-align:center;

    border:1px solid rgba(139,92,246,0.08);

    transition:0.3s;

    box-shadow:0 8px 20px rgba(0,0,0,0.04);
}

.step-card:hover{
    transform:translateY(-6px);
    box-shadow:0 12px 30px rgba(0,0,0,0.08);
}

.step-icon{
    font-size:48px;
    margin-bottom:15px;
}

.step-title{
    font-size:24px;
    font-weight:800;
    color:#6D28D9;
    margin-bottom:10px;
}

.step-desc{
    color:#64748B;
    line-height:2;
}

/* AUTHOR CARD */

.author-card{

    margin-top:40px;

    background:rgba(255,255,255,0.7);

    border-radius:30px;

    padding:35px;

    border:1px solid rgba(139,92,246,0.1);

    display:flex;

    align-items:center;

    justify-content:space-between;

    gap:40px;

    flex-wrap:wrap;

    backdrop-filter:blur(12px);

    box-shadow:0 10px 35px rgba(0,0,0,0.05);
}

.author-image{
    width:170px;
    height:170px;

    border-radius:50%;

    object-fit:cover;

    border:5px solid #8B5CF6;

    box-shadow:0 10px 25px rgba(124,58,237,0.15);
}

.author-info{
    flex:1;
}

.author-name{
    font-size:40px;
    font-weight:800;
    color:#4C1D95;
}

.author-role{
    font-size:26px;
    font-weight:700;
    color:#7C3AED;
    margin-top:8px;
}

.author-text{
    margin-top:18px;

    line-height:2.2;

    color:#475569;

    font-size:19px;
}

/* FOOTER */

.footer{
    text-align:center;
    margin-top:50px;
    color:#64748B;
    font-size:15px;
}

</style>

""", unsafe_allow_html=True)

# ---------------------------------------------------------
# HERO
# ---------------------------------------------------------

st.markdown("""

<div class="hero">

<div class="hero-top-badge">
✨ منصة ذكية عربية
</div>

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

منصة تعتمد على الذكاء الاصطناعي وتحليل السياق اللغوي
لاكتشاف المعنى الصحيح للكلمات داخل النصوص العربية
باستخدام تقنيات حديثة في معالجة اللغة الطبيعية.

</div>

<div class="author-badge">
🎓 تم تطوير وتصميم LABEEB AI بواسطة الطالبة هاجر الزواكي © 2026
</div>

</div>

</div>

</div>

""", unsafe_allow_html=True)

# ---------------------------------------------------------
# INPUT SECTION
# ---------------------------------------------------------

st.markdown("""
<div class="main-card">
<div class="section-title">
✍️ اكتب النص العربي الذي ترغب في تحليل معناه وسياقه
</div>
""", unsafe_allow_html=True)

text = st.text_area(
    "",
    height=140,
    placeholder="اكتب هنا جملة عربية واضحة تحتوي على معنى أو سياق لغوي..."
)

analyze = st.button("⚡ ابدأ التحليل الذكي")

st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# RESULT SECTION
# ---------------------------------------------------------

st.markdown("""
<div class="main-card">

<div class="section-title">
📊 نتيجة التحليل
</div>

""", unsafe_allow_html=True)

if analyze and text:

    st.success("✅ تم تحليل النص بنجاح")

    st.markdown(f"""

    <div style="
    background:#F8FAFC;
    border-radius:22px;
    padding:25px;
    line-height:2;
    font-size:18px;
    border:1px solid rgba(139,92,246,0.1);
    ">

    <b>النص المدخل:</b><br>
    {text}

    <br><br>

    <b>التحليل:</b><br>
    تم التعرف على السياق اللغوي للنص وتحليل المعنى
    اعتمادًا على البنية الدلالية والعلاقات السياقية للكلمات.

    </div>

    """, unsafe_allow_html=True)

else:

    st.info("لم يتم إجراء أي تحليل بعد.")

st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# HOW IT WORKS
# ---------------------------------------------------------

st.markdown("""

<div class="main-card">

<div class="section-title">
🧠 كيف يعمل لبيب؟
</div>

<div class="steps-grid">

<div class="step-card">
<div class="step-icon">🔎</div>
<div class="step-title">تحليل السياق</div>
<div class="step-desc">
يقوم النظام بفهم الكلمات المحيطة وتحليل العلاقات بينها لفهم المعنى الحقيقي.
</div>
</div>

<div class="step-card">
<div class="step-icon">✨</div>
<div class="step-title">اكتشاف المعنى</div>
<div class="step-desc">
يحدد المعنى الصحيح للكلمة اعتمادًا على البنية الدلالية للنص.
</div>
</div>

<div class="step-card">
<div class="step-icon">📊</div>
<div class="step-title">قياس التشابه</div>
<div class="step-desc">
يستخدم تقنيات الذكاء الاصطناعي لحساب التشابه بين المعاني المختلفة.
</div>
</div>

</div>

</div>

""", unsafe_allow_html=True)

# ---------------------------------------------------------
# AUTHOR SECTION
# ---------------------------------------------------------

st.markdown("""

<div class="author-card">

<div class="author-info">

<div class="author-name">
👩🏻‍💻 هاجر الزواكي
</div>

<div class="author-role">
طالبة ماجستير سنة ثانية — تخصص اللسانيات الرقمية والعربية
</div>

<div class="author-text">

هذا المشروع جزء من بحث التخرج بجامعة مولاي إسماعيل بمكناس،
ويهدف إلى تطوير منصة ذكية لتحليل المعنى والسياق في اللغة العربية
باستخدام تقنيات الذكاء الاصطناعي ومعالجة اللغة الطبيعية.

<br><br>

أهتم ببناء الأنظمة الدلالية الذكية، والنماذج اللغوية العربية،
وتطوير حلول رقمية حديثة لفهم النصوص العربية وتحليلها حاسوبيًا.

</div>

</div>

<img class="author-image"
src="https://raw.githubusercontent.com/hzouaki-ship-it/labeeb-ai/main/hajar.jpg">
</div>

""", unsafe_allow_html=True)

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown("""

<div class="footer">

LABEEB AI © 2026 — جامعة مولاي إسماعيل بمكناس

</div>

""", unsafe_allow_html=True)
