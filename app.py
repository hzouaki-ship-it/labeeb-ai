import streamlit as st
import pandas as pd

# ======================================
# إعداد الصفحة
# ======================================

st.set_page_config(
    page_title="LABEEB AI",
    page_icon="🧠",
    layout="wide"
)

# ======================================
# CSS
# ======================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&display=swap');

html, body, [class*="css"]{
    font-family:'Cairo', sans-serif;
    direction:rtl;
}

.stApp{
    background:linear-gradient(135deg,#F8FAFC,#F3E8FF);
}

.block-container{
    max-width:1100px;
    margin:auto;
    padding-top:2rem;
}

/* HERO */

.hero-container{

    background:white;

    border-radius:30px;

    padding:55px;

    text-align:center;

    box-shadow:0 10px 30px rgba(0,0,0,0.05);

    margin-bottom:30px;
}

.hero-logo{

    width:90px;

    height:90px;

    border-radius:50%;

    margin:auto;

    margin-bottom:20px;

    background:linear-gradient(135deg,#7C3AED,#4F46E5);

    display:flex;

    align-items:center;

    justify-content:center;

    color:white;

    font-size:42px;

    font-weight:800;
}

.hero-title{

    font-size:58px;

    font-weight:800;

    color:#6D28D9;

    margin-bottom:10px;
}

.hero-subtitle{

    font-size:24px;

    font-weight:700;

    color:#1E293B;

    margin-bottom:14px;
}

.hero-desc{

    font-size:17px;

    color:#64748B;

    line-height:2;

    max-width:700px;

    margin:auto;
}

.badge{

    margin-top:22px;

    display:inline-block;

    background:#F3E8FF;

    color:#6D28D9;

    padding:10px 20px;

    border-radius:999px;

    font-size:14px;

    font-weight:700;
}

/* CARDS */

.card{

    background:white;

    border-radius:24px;

    padding:28px;

    margin-bottom:25px;

    box-shadow:0 6px 20px rgba(0,0,0,0.04);
}

/* BUTTON */

.stButton > button{

    width:100%;

    background:linear-gradient(90deg,#4F46E5,#7C3AED);

    color:white;

    border:none;

    border-radius:14px;

    padding:14px;

    font-size:18px;

    font-weight:700;
}

/* TABLE */

thead tr th{

    background:#F3E8FF !important;

    color:#6D28D9 !important;
}

/* RESEARCHER */

.researcher{

    display:flex;

    align-items:center;

    gap:25px;
}

.researcher img{

    width:120px;

    height:120px;

    border-radius:50%;

    object-fit:cover;

    border:4px solid #E9D5FF;
}

.footer{

    text-align:center;

    margin-top:50px;

    color:#94A3B8;
}

</style>
""", unsafe_allow_html=True)

# ======================================
# HERO
# ======================================

st.markdown("""

<div class="hero-container">

    <div class="hero-logo">
        ل
    </div>

    <div class="hero-title">
        LABEEB AI
    </div>

    <div class="hero-subtitle">
        المحلل الدلالي الذكي للغة العربية
    </div>

    <div class="hero-desc">
        منصة تعتمد على الذكاء الاصطناعي لتحليل المعنى والسياق
        داخل النصوص العربية.
    </div>

    <div class="badge">
        تطوير وتصميم: هاجر الزواكي
    </div>

</div>

""", unsafe_allow_html=True)

# ======================================
# الإدخال
# ======================================

st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("✍️ اكتب النص المراد تحليله")

text = st.text_area(
    "",
    placeholder="مثال: شرب الرجل من عين ماء..."
)

analyze = st.button("ابدأ التحليل")

st.markdown("</div>", unsafe_allow_html=True)

# ======================================
# النتائج
# ======================================

st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("✨ نتيجة التحليل")

if analyze and text:

    results = pd.DataFrame({

        "المعنى المحتمل":[
            "عضو البصر",
            "نبع ماء",
            "جاسوس"
        ],

        "نسبة القرب":[
            "92%",
            "61%",
            "20%"
        ]
    })

    st.success("تم التحليل بنجاح")

    st.table(results)

else:

    st.info("لم يتم إجراء أي تحليل بعد")

st.markdown("</div>", unsafe_allow_html=True)

# ======================================
# الباحثة
# ======================================

st.markdown("""

<div class="card">

<div class="researcher">

<img src="https://raw.githubusercontent.com/hzouaki-ship-it/labeeb-ai/main/hajar.jpg">

<div>

<h2>هاجر الزواكي</h2>

<p style="color:#6D28D9;font-weight:700;">
طالبة ماستر في اللسانيات الرقمية والعربية
</p>

<p style="line-height:2;color:#475569;">
مهتمة بالذكاء الاصطناعي ومعالجة اللغة العربية
وبناء الأنظمة الدلالية الذكية.
</p>

</div>

</div>

</div>

""", unsafe_allow_html=True)

# ======================================
# FOOTER
# ======================================

st.markdown(
    '<div class="footer">LABEEB AI © 2026</div>',
    unsafe_allow_html=True
)
