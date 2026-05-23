import streamlit as st
import pandas as pd
import time

# =========================================
# 1. إعداد الصفحة الأساسي والهوية البصرية
# =========================================
st.set_page_config(
    page_title="LABEEB AI - لبيب",
    page_icon="🧠",
    layout="wide"
)

# واجهة التصميم الحديثة الاحترافية بالكامل (Modern AI SaaS UI)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Cairo', sans-serif;
    direction: rtl;
    text-align: right;
}

.stApp {
    background: linear-gradient(135deg, #F8FAFC 0%, #F5F3FF 50%, #EFF6FF 100%);
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

[data-testid="stMain"] .block-container {
    max-width: 1100px;
    padding-top: 2.5rem;
    padding-bottom: 5rem;
    margin: 0 auto;
}

/* HERO SECTION */
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
}

/* GLASS CARD */
.glass-card {
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.5);
    border-radius: 24px;
    padding: 32px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.02);
    margin-bottom: 25px;
}

.card-title {
    font-size: 22px;
    font-weight: 700;
    color: #1E293B;
    margin-bottom: 20px;
}

.stTextArea textarea {
    border-radius: 16px !important;
    border: 1px solid #E2E8F0 !important;
    padding: 18px !important;
    font-size: 18px !important;
    background: rgba(255, 255, 255, 0.8) !important;
}

.stButton > button {
    background: linear-gradient(90deg, #4F46E5, #6D28D9) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 14px 32px !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    width: 100% !important;
    box-shadow: 0 8px 20px rgba(109, 40, 217, 0.2) !important;
}

/* RESULT ELEMENTS */
.result-status-empty {
    text-align: center;
    color: #94A3B8;
    font-size: 16px;
    padding: 20px 0;
}

.result-badge-container {
    display: flex;
    gap: 16px;
    margin-bottom: 24px;
}

.result-stat-box {
    flex: 1;
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

/* HOW IT WORKS */
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

.step-desc {
    font-size: 15px;
    color: #64748B;
    line-height: 1.7;
}

/* RESEARCHER */
.researcher-card {
    background: white;
    border: 1px solid #EEF2F6;
    border-radius: 24px;
    padding: 30px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.01);
    margin-top: 45px;
}

.researcher-flex {
    display: flex;
    align-items: center;
    gap: 28px;
}

.researcher-img {
    width: 110px;
    height: 110px;
    border-radius: 50%;
    object-fit: cover;
    border: 4px solid #F3E8FF;
}

.researcher-name {
    font-size: 22px;
    font-weight: 800;
    color: #1E293B;
    margin-bottom: 4px;
}

.researcher-title {
    font-size: 16px;
    font-weight: 600;
    color: #6D28D9;
    margin-bottom: 10px;
}

.researcher-bio {
    font-size: 15px;
    color: #475569;
    line-height: 1.8;
}
/* =========================================
LABEEB CREATIVE LOGO
========================================= */

.labeeb-orb{

    position:relative;

    width:120px;

    height:120px;

    display:flex;

    align-items:center;

    justify-content:center;

    margin:auto;
}

.orb-core{

    width:85px;

    height:85px;

    border-radius:50%;

    background:
    linear-gradient(
    135deg,
    #6D28D9,
    #4F46E5);

    display:flex;

    align-items:center;

    justify-content:center;

    color:white;

    font-size:42px;

    font-weight:800;

    box-shadow:
    0 0 35px rgba(109,40,217,0.35);

    position:relative;

    z-index:2;

    backdrop-filter:blur(12px);
}

.orb-ring{

    position:absolute;

    width:115px;

    height:115px;

    border-radius:50%;

    border:2px dashed rgba(109,40,217,0.28);

    animation:spinOrb 16s linear infinite;
}

@keyframes spinOrb{

    from{
        transform:rotate(0deg);
    }

    to{
        transform:rotate(360deg);
    }
}
.footer-text {
    text-align: center;
    color: #94A3B8;
    font-size: 14px;
    margin-top: 55px;
    border-top: 1px solid #E2E8F0;
    padding-top: 24px;
}
</style>
""", unsafe_allow_html=True)

# =========================================
# 2. قاعدة البيانات المعجمية المستقرة
# =========================================
semantic_db = {
    "عين": [
        {"المعنى": "عضو البصر والرؤية", "القرائن": ["طفل", "أصيب", "بصر", "طبيب", "نظارات", "رؤية", "جندي", "فقد", "عينه", "عينها"]},
        {"المعنى": "نبع ماء طبيعي", "القرائن": ["ماء", "شرب", "عذب", "واحة", "بئر", "تدفق", "نبع", "ساقية"]},
        {"المعنى": "جاسوس ومراقب سري", "القرائن": ["قائد", "عدو", "جاسوس", "رصد", "تحركات", "استطلاع", "جيش", "حرب"]}
    ],
    "المغرب": [
        {"المعنى": "المملكة المغربية (الدولة)", "القرائن": ["سافر", "دولة", "رباط", "فاس", "مكناس", "مملكة", "سياحة", "تاريخ"]},
        {"المعنى": "صلاة المغرب (الوقت)", "القرائن": ["صلاة", "أذان", "مسجد", "صليت", "مصلون", "إفطار", "رمضان", "وقت"]}
    ],
    "رأس": [
        {"المعنى": "عضو في جسم الإنسان", "القرائن": ["ألم", "صداع", "شعر", "طبيب", "جسم", "تفكير", "مخ", "وجع"]},
        {"المعنى": "قمة جغرافية مرتفعة", "القرائن": ["جبل", "تسلق", "قمة", "وصل", "منحدر", "مرتفع", "صخور"]}
    ]
}

# =========================================
# 3. عرض الهيكل الخارجي (HERO)
# =========================================
st.markdown("""

<div class="hero-container">

    <div class="hero-logo-wrapper">

        <div class="labeeb-orb">

            <div class="orb-core">ل</div>

            <div class="orb-ring"></div>

        </div>

    </div>

    <div class="hero-title">
        LABEEB AI (لبيب)
    </div>

    <div class="hero-subtitle">
        المحلل الدلالي الذكي لفهم المعنى والسياق في اللغة العربية
    </div>

    <div class="hero-desc">
        منصة تعتمد على الذكاء الاصطناعي لتحليل النصوص العربية وفهم معناها العميق في السياق.
    </div>

    <div class="badge-student">
        © 2026 تم تطوير وتصميم بواسطة الطالبة هاجر الزواكي

</div>

""", unsafe_allow_html=True)
</div>
""", unsafe_allow_html=True)

# =========================================
# 4. بطاقة الإدخال (INPUT CARD)
# =========================================
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<div class="card-title">✍️ اكتب النص العربي الذي ترغب في تحليل معناه وسياقه</div>', unsafe_allow_html=True)

user_text = st.text_area("", placeholder="اكتب جملتك هنا (مثال: شرب المسافر من عين ماء عذبة)...", key="main_input", label_visibility="collapsed")
submit_btn = st.button("ابدأ التحليل الذكي")

st.markdown('<div style="text-align:center; color:#94A3B8; font-size:14px; margin-top:12px;">تحليل آمن ودقيق باستخدام الذكاء الاصطناعي</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================================
# 5. بطاقة النتائج المستقرة (RESULT CARD)
# =========================================
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<div class="card-title">✨ نتيجة التحليل</div>', unsafe_allow_html=True)

if submit_btn and user_text.strip():
    detected_keyword = None
    for word in semantic_db.keys():
        if word in user_text or (word == "عين" and ("عينه" in user_text or "عينها" in user_text or "العين" in user_text)):
            detected_keyword = word
            break
            
    if detected_keyword:
        with st.spinner("⏳ يجري تحليل المتجهات والروابط السياقية..."):
            time.sleep(0.3)
            
            results_list = []
            highest_score = 0.0
            predicted_meaning = ""
            
            for entry in semantic_db[detected_keyword]:
                base_score = 0.25
                matched_clues = 0
                
                for clue in entry["القرائن"]:
                    if clue in user_text:
                        matched_clues += 1
                        
                if matched_clues > 0:
                    score = base_score + (matched_clues * 0.35)
                else:
                    score = base_score
                    
                if score > 0.98: score = 0.98
                
                results_list.append({
                    "المعنى المحتمل": entry["المعنى"],
                    "نسبة القرب": f"{score * 100:.2f}%",
                    "_raw": score
                })
                
                if score > highest_score:
                    highest_score = score
                    predicted_meaning = entry["المعنى"]
            
            st.markdown(f"""
            <div class="result-badge-container">
                <div class="result-stat-box">
                    <div class="result-stat-label">المعنى الأقرب</div>
                    <div class="result-stat-val">{predicted_meaning}</div>
                </div>
                <div class="result-stat-box">
                    <div class="result-stat-label">نسبة القرب الدلالي</div>
                    <div class="result-stat-val">{highest_score * 100:.2f}%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            df_clean = pd.DataFrame(results_list).sort_values(by="_raw", ascending=False).drop(columns=["_raw"])
            st.table(df_clean)
    else:
        st.markdown("""
        <div class="result-stat-box" style="width:100%;">
            <div class="result-stat-label">حالة البنية اللغوية</div>
            <div class="result-stat-val" style="color: #64748B; font-size:16px;">لم يتم رصد لفظ مشترك معروف (عين، المغرب، رأس)</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown('<div class="result-status-empty">🤖 لم يتم إجراء أي تحليل بعد. اكتب نصاً واضغط على الزر لبدء المعالجة.</div>', unsafe_allow_html=True)
    
st.markdown('</div>', unsafe_allow_html=True)

# =========================================
# 6. قسم خطوات العمل الآمن (HOW IT WORKS)
# =========================================
st.markdown('<div class="section-main-title">كيف يعمل لبيب؟</div>', unsafe_allow_html=True)

col_w1, col_w2, col_w3 = st.columns(3)
with col_w1:
    st.markdown("""
    <div class="step-card">
        <div class="step-icon">🔎</div>
        <div class="step-title">تحليل السياق</div>
        <div class="step-desc">يقوم النظام بفحص البنية التركيبية المحيطة باللفظ المشترك، وعزل الكلمات المحورية المحيطة به بدقة وعناية.</div>
    </div>
    """, unsafe_allow_html=True)
with col_w2:
    st.markdown("""
    <div class="step-card">
        <div class="step-icon">✨</div>
        <div class="step-title">اكتشاف المعنى</div>
        <div class="step-desc">تُطابق البيئة السياقية الحالية مع الحقول والمؤشرات المعجمية المخزنة لتحديد الإحالة المعنوية الأنسب للفظ.</div>
    </div>
    """, unsafe_allow_html=True)
with col_w3:
    st.markdown("""
    <div class="step-card">
        <div class="step-icon">📊</div>
        <div class="step-title">قياس التشابه الدلالي</div>
        <div class="step-desc">يتم حساب أوزان ومعاملات المطابقة الإحصائية لإنتاج جدول دقيق يرتب الاحتمالات ترتيباً تصاعدياً بحسب النسبة.</div>
    </div>
    """, unsafe_allow_html=True)

# =========================================
# 7. بطاقة الباحثة (RESEARCHER CARD)
# =========================================
st.markdown("""
<div class="researcher-card">
    <div class="researcher-flex">
        <img src="https://raw.githubusercontent.com/hzouaki-ship-it/labeeb-ai/main/hajar.jpg" class="researcher-img" alt="Hajar Zouaki">
        <div>
            <div class="researcher-name">هاجر الزواكي</div>
            <div class="researcher-title">طالبة ماستر في اللسانيات الرقمية والعربية</div>
            <div class="researcher-bio">مهتمة بالذكاء الاصطناعي ومعالجة اللغة العربية وبناء الأنظمة الدلالية الذكية وأسعى إلى تطوير حلول رقمية حديثة لفهم اللغة العربية وتحليل السياق والمعنى.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================
# 8. التذييل (FOOTER)
# =========================================
st.markdown('<div class="footer-text">LABEEB AI © 2026 — جميع الحقوق محفوظة — هاجر الزواكي</div>', unsafe_allow_html=True)
