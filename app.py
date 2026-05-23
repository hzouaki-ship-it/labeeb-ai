import streamlit as st
import pandas as pd
import time

# =========================================
# إعداد الصفحة الأساسي
# =========================================
st.set_page_config(
    page_title="LABEEB AI - لبيب",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================
# واجهة التصميم الحديثة (Modern AI SaaS UI)
# =========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&display=swap');

/* تصفير الإعدادات الافتراضية وفرض خط القاهرة والاتجاه */
html, body, [class*="css"] {
    font-family: 'Cairo', sans-serif;
    direction: rtl;
    text-align: right;
}

/* خلفية المنصة الفاتحة مع التموجات البنفسجية الناعمة */
.stApp {
    background: linear-gradient(135deg, #F8FAFC 0%, #F5F3FF 50%, #EFF6FF 100%);
    position: relative;
    overflow-x: hidden;
}

/* إخفاء عناصر سترمليت الافتراضية لتبدو كمنصة مستقلة */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ضبط هوامش الحاوية الرئيسية */
[data-testid="stMain"] .block-container {
    max-width: 1200px;
    padding-top: 3rem;
    padding-bottom: 5rem;
    margin: 0 auto;
}

/* =========================================
1. HERO SECTION
========================================= */
.hero-container {
    position: relative;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.8), rgba(243, 232, 255, 0.6));
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.6);
    border-radius: 32px;
    padding: 60px 40px;
    text-align: center;
    box-shadow: 0 20px 40px rgba(109, 40, 217, 0.05);
    margin-bottom: 40px;
}

/* تأثير التوهج الخلفي المضيء */
.hero-container::before {
    content: "";
    position: absolute;
    top: -10%;
    left: 50%;
    transform: translateX(-50%);
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(168, 85, 247, 0.15) 0%, transparent 70%);
    z-index: -1;
    pointer-events: none;
}

.hero-logo-glow {
    width: 100px;
    height: 100px;
    background: linear-gradient(135deg, #4F46E5, #6D28D9);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 24px auto;
    box-shadow: 0 0 30px rgba(109, 40, 217, 0.4);
    font-size: 42px;
    color: white;
}

.hero-title {
    font-size: 54px;
    font-weight: 800;
    background: linear-gradient(90deg, #6D28D9, #4F46E5);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 12px;
}

.hero-subtitle {
    font-size: 26px;
    font-weight: 700;
    color: #1E293B;
    margin-bottom: 16px;
}

.hero-desc {
    font-size: 18px;
    color: #64748B;
    max-width: 700px;
    margin: 0 auto 28px auto;
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
    background: rgba(255, 255, 255, 0.75);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.5);
    border-radius: 24px;
    padding: 35px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.02);
    margin-bottom: 30px;
}

.card-title {
    font-size: 22px;
    font-weight: 700;
    color: #1E293B;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
}

/* تخصيص صندوق الكتابة */
.stTextArea textarea {
    border-radius: 16px !important;
    border: 1px solid #E2E8F0 !important;
    padding: 18px !important;
    font-size: 18px !important;
    background: rgba(255, 255, 255, 0.8) !important;
    transition: all 0.3s ease !important;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.01) !important;
}

.stTextArea textarea:focus {
    border-color: #6D28D9 !important;
    box-shadow: 0 0 0 3px rgba(109, 40, 217, 0.1) !important;
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
    box-shadow: 0 8px 20px rgba(109, 40, 217, 0.25) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 24px rgba(109, 40, 217, 0.35) !important;
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
    padding: 40px 0;
}

.result-badge-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-bottom: 24px;
}

.result-stat-box {
    background: rgba(255, 255, 255, 0.9);
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
    font-size: 32px;
    font-weight: 800;
    color: #1E293B;
    margin: 50px 0 30px 0;
}

.step-card {
    background: white;
    border: 1px solid #F1F5F9;
    border-radius: 20px;
    padding: 30px 24px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.01);
    transition: all 0.3s ease;
}

.step-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 30px rgba(109, 40, 217, 0.06);
    border-color: #E9D5FF;
}

.step-icon {
    font-size: 36px;
    margin-bottom: 16px;
}

.step-title {
    font-size: 20px;
    font-weight: 700;
    color: #1E293B;
    margin-bottom: 10px;
}

.step-desc {
    font-size: 15px;
    color: #64748B;
    line-height: 1.7;
}

/* =========================================
5. RESEARCHER SECTION
========================================= */
.researcher-card {
    background: white;
    border: 1px solid #EEF2F6;
    border-radius: 24px;
    padding: 32px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.01);
    margin-top: 50px;
}

.researcher-flex {
    display: flex;
    align-items: center;
    gap: 32px;
}

.researcher-img {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    object-fit: cover;
    border: 4px solid #F3E8FF;
    box-shadow: 0 8px 20px rgba(109, 40, 217, 0.1);
    flex-shrink: 0;
}

.researcher-name {
    font-size: 24px;
    font-weight: 800;
    color: #1E293B;
    margin-bottom: 4px;
}

.researcher-title {
    font-size: 16px;
    font-weight: 600;
    color: #6D28D9;
    margin-bottom: 12px;
}

.researcher-bio {
    font-size: 15px;
    color: #475569;
    line-height: 1.8;
}

/* استعلام الاستجابة للهواتف */
@media (max-width: 768px) {
    .researcher-flex {
        flex-direction: column;
        text-align: center;
    }
}

/* =========================================
6. FOOTER
========================================= */
.footer-text {
    text-align: center;
    color: #94A3B8;
    font-size: 14px;
    margin-top: 60px;
    border-top: 1px solid #E2E8F0;
    padding-top: 24px;
}
</style>
""", unsafe_allow_html=True)

# =========================================
# قاعدة البيانات اللغوية لفك اللبس
# =========================================
semantic_db = {
    "عين": [
        {"المعنى": "عضو البصر والرؤية", "القرائن": ["طفل", "أصيب", "بصر", "طبيب", "نظارات", "رؤية", "جندي", "فقد", "عينه", "عينها"]},
        {"المعنى": "نبع ماء طبيعي", "القرائن":
