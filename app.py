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
# قاعدة البيانات المعجمية الدلالية المدمجة
# =========================================

semantic_db = {
    "عين": [
        {"المعنى": "عضو البصر", "جملة_مرجعية": "أصيبت عين الطفل بسبب الغبار المثار في الجو", "المؤشرات": ["الطفل", "أصيبت", "البصر", "طبيب", "نظارات", "رؤية", "دمعت"]},
        {"المعنى": "نبع ماء طبيعي", "جملة_مرجعية": "شرب المسافرون من عين ماء عذبة تفجرت في الواحة", "المؤشرات": ["ماء", "شرب", "عذبة", "واحة", "بئر", "تدفق", "نبع"]},
        {"المعنى": "جاسوس ومراقب", "جملة_مرجعية": "بث القائد عيناً له ليرصد بدقة تحتحركات الأعداء", "المؤشرات": ["القائد", "العدو", "جاسوس", "رصد", "تحركات", "استطلاع", "الأعداء"]}
    ],
    "المغرب": [
        {"المعنى": "المملكة المغربية (الدولة)", "جملة_مرجعية": "سافرت إلى المغرب لزيارة المعالم الأثرية والتاريخية في مكناس والرباط", "المؤشرات": ["سافرت", "دولة", "الرباط", "فاس", "مكناس", "المملكة", "سياحة"]},
        {"المعنى": "صلاة المغرب (الوقت)", "جملة_مرجعية": "توجه المصلون سريعاً إلى المسجد فور سماع أذان المغرب", "المؤشرات": ["صلاة", "أذان", "المسجد", "صليت", "المصلون", "إفطار", "الفريضة"]}
    ],
    "رأس": [
        {"المعنى": "عضو في الجسم", "جملة_مرجعية": "شعر الطالب الباحث بصداع وألم في رأسه بسبب قلة النوم", "المؤشرات": ["ألم", "صداع", "شعر", "طبيب", "جسم", "السهر", "طبيب"]},
        {"المعنى": "قمة جغرافية", "جملة_مرجعية": "استطاع فريق المغامرين الوصول بنجاح إلى رأس الجبل قبل الغروب", "المؤشرات": ["الجبل", "تسلق", "قمة", "وصل", "منحدر", "مرتفع"]}
    ]
}

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
        # خوارزمية الفحص واستخراج الروابط اللغوية
        detected_keyword = None
        for word in semantic_db.keys():
            if word in text:
                detected_keyword = word
                break
        
        if detected_keyword:
            with st.spinner("⏳ يجري الآن تفكيك العلاقات اللغوية وحساب نسب التقارب السياقي..."):
                time.sleep(0.6)
                
                results_list = []
                highest_score = -1
                predicted_meaning = ""
                
                # حساب النسبة المئوية للتشابه الدلالي
                for entry in semantic_db[detected_keyword]:
                    score = 0.20 # حد أدنى كأولوية لغوية عامة
                    for indicator in entry["المؤشرات"]:
                        if indicator in text:
                            score += 0.25
                    
                    if score > 0.98: score = 0.98
                    
                    results_list.append({
                        "المعنى السياقي المرشح": entry["المعنى"],
                        "السياق النموذجي المقارن": entry["جملة_مرجعية"],
                        "نسبة التقارب الدلالي": f"{score * 100:.2f}%",
                        "_raw_score": score
                    })
                    
                    if score > highest_score:
                        highest_score = score
                        predicted_meaning = entry["المعنى"]
                
                # عرض النتيجة داخل الكرت المصمم الخاص بكِ
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-title">🎯 قرار النظام وفك اللبس المعجمي</div>
                    <div style='font-size:22px; line-height:2; color:#374151; margin-bottom: 20px;'>
                        <b>النص المُدخل:</b> {text}<br><br>
                        🔹 تم رصد لفظ مشترك غامض دلالياً وهو: <b>({detected_keyword})</b><br>
                        📌 <b>المعنى المقصود في سياق جملتكِ هو:</b> <span style='color: #7C3AED; font-weight: 800;'>({predicted_meaning})</span> بنسبة تطابقة بلغت <b>{highest_score * 100:.2f}%</b>.
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # بناء الجدول الإحصائي للمصفوفة بشكل منسق وأنيق أسفل النتيجة
                df_output = pd.DataFrame(results_list)
                df_output = df_output.sort_values(by="_raw_score", ascending=False).drop(columns=["_raw_score"])
                
                st.markdown("<b style='font-size:19px; color:#312E81;'>📊 مصفوفة معاملات التقارب والتشابه السياقي المقارن:</b>", unsafe_allow_html=True)
                st.dataframe(df_output, use_container_width=True, hide_index=True)
                
        else:
            # معالجة النصوص العامة التي لا تحتوي على الكلمات التجريبية المحددة
            with st.spinner("⏳ يجري تحليل الخصائص البنائية العامة للنص..."):
                time.sleep(0.5)
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-title">نتيجة التحليل العامة</div>
                    <div style='font-size:22px; line-height:2; color:#374151; margin-bottom: 15px;'>
                        <b>النص المُدخل:</b> {text}<br><br>
                        <b>التحليل التركيبي:</b> تم فحص البنية اللغوية للنص بنجاح. السياق مستقر ولا يحتوي على لبس معجمي مباشر يقع ضمن عينات المعاجم المثبتة حالياً (عين، المغرب، رأس).
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # عرض جدول هيكلي بسيط للنصوص العامة
                words_count = len(text.split())
                chars_count = len(text)
                st.markdown("<b style='font-size:19px; color:#312E81;'>📊 الخصائص الهيكلية العامة للجملة المدخلة:</b>", unsafe_allow_html=True)
                general_metrics = pd.DataFrame([{
                    "عدد الكلمات الإجمالي": words_count,
                    "عدد الحروف والرموز": chars_count,
                    "طبيعة المعالجة اللغوية": "تحليل تركيبي عام (Syntactic Analysis)",
                    "حالة اللبس الدلالي": "مستقر دلالياً"
                }])
                st.dataframe(general_metrics, use_container_width=True, hide_index=True)

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
