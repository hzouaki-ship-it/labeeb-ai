import streamlit as st
import pandas as pd
import time
import torch
import torch.nn.functional as F

from transformers import (
    AutoTokenizer,
    AutoModel
)

from tashaphyne.stemming import ArabicLightStemmer
from openai import OpenAI

# =========================================
# 1. إعداد الصفحة
# =========================================

st.set_page_config(
    page_title="LABEEB AI - لبيب",
    page_icon="🧠",
    layout="wide"
)

# =========================================
# 2. أدوات المعالجة
# =========================================

stemmer = ArabicLightStemmer()

# =========================================
# 3. تحميل AraBERT
# =========================================

@st.cache_resource
def load_arabert():

    tokenizer = AutoTokenizer.from_pretrained(
        "aubmindlab/bert-base-arabertv02"
    )

    model = AutoModel.from_pretrained(
        "aubmindlab/bert-base-arabertv02"
    )

    return tokenizer, model

tokenizer, arabert_model = load_arabert()

# =========================================
# 4. OpenRouter
# =========================================

client = None

if "OPENROUTER_API_KEY" in st.secrets:

    client = OpenAI(

        api_key=st.secrets["OPENROUTER_API_KEY"],

        base_url="https://openrouter.ai/api/v1"
    )

# =========================================
# 5. استخراج التمثيل الدلالي
# =========================================

def get_embedding(text):

    inputs = tokenizer(

        text,

        return_tensors="pt",

        truncation=True,

        padding=True,

        max_length=128
    )

    with torch.no_grad():

        outputs = arabert_model(**inputs)

    embedding = outputs.last_hidden_state[:, 0, :]

    return embedding

# =========================================
# 6. حساب التشابه الدلالي
# =========================================

def semantic_similarity(text1, text2):

    emb1 = get_embedding(text1)

    emb2 = get_embedding(text2)

    similarity = F.cosine_similarity(
        emb1,
        emb2
    )

    return similarity.item()

# =========================================
# 7. CSS الجمالي
# =========================================

st.markdown(
    """
    <style>

    @import url("https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&family=Poppins:wght@400;600;700;800&display=swap");

    html, body, [class*="css"] {
        font-family: "Cairo", sans-serif;
        direction: rtl;
        text-align: right;
    }

    .stApp {
        background: linear-gradient(
            135deg,
            #F8FAFC 0%,
            #F5F3FF 50%,
            #EFF6FF 100%
        ) !important;
    }

    #MainMenu,
    footer,
    header {
        visibility: hidden;
    }

    [data-testid="stMain"] .block-container {
        max-width: 1140px;
        padding-top: 2rem;
        padding-bottom: 4rem;
        margin: 0 auto;
    }

    .hero-container {
        position: relative;
        background: linear-gradient(
            135deg,
            rgba(255,255,255,0.85),
            rgba(243,232,255,0.7)
        );

        backdrop-filter: blur(20px);

        border: 1px solid rgba(
            255,
            255,
            255,
            0.6
        );

        border-radius: 28px;

        padding: 35px 25px;

        text-align: center;

        box-shadow:
        0 20px 40px rgba(
            109,
            40,
            217,
            0.03
        );

        margin-bottom: 30px;
    }

    .hero-inline {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 35px;
        margin-bottom: 25px;
    }

    .hero-brand {
        text-align: right;
        margin-top: 12px;
    }

    .brand-main {
        font-size: 42px;
        font-weight: 700;
        color: #5B21B6;
        line-height: 1.2;
        font-family: "Poppins", sans-serif;
        letter-spacing: 2px;
        margin-bottom: 10px;
    }

    .brand-sub {
        font-size: 15px;
        letter-spacing: 3px;
        color: #4338CA;
        font-weight: 600;
    }

    .hero-logo-img {
        width: 170px;
        height: 170px;
        object-fit: cover;
        border-radius: 50%;
        display: block;
        box-shadow:
        0 0 40px rgba(
            109,
            40,
            217,
            0.18
        );
    }

    .hero-subtitle {
        font-size: 22px;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 12px;
    }

    .hero-desc {
        font-size: 16px;
        color: #64748B;
        max-width: 650px;
        margin: 0 auto 20px auto;
        line-height: 1.7;
    }

    .badge-student {
        display: inline-block;
        background: rgba(
            255,
            255,
            255,
            0.9
        );

        border: 1px solid #E9D5FF;

        padding: 6px 18px;

        border-radius: 999px;

        font-size: 13px;

        font-weight: 600;

        color: #6D28D9;
    }

    .glass-card {

        background: rgba(
            255,
            255,
            255,
            0.88
        );

        backdrop-filter: blur(20px);

        border: 1px solid rgba(
            255,
            255,
            255,
            0.5
        );

        border-radius: 22px;

        padding: 30px;

        box-shadow:
        0 10px 30px rgba(
            0,
            0,
            0,
            0.02
        );

        margin-bottom: 25px;
    }

    .card-title {
        font-size: 20px;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 16px;
    }

    .stTextArea textarea {

        border-radius: 14px !important;

        border: 1px solid #E2E8F0 !important;

        padding: 16px !important;

        font-size: 16px !important;

        background: rgba(
            255,
            255,
            255,
            0.7
        ) !important;

        font-family:
        "Cairo",
        sans-serif !important;
    }

    .stButton > button {

        background: linear-gradient(
            90deg,
            #4F46E5,
            #6D28D9
        ) !important;

        color: white !important;

        border: none !important;

        border-radius: 12px !important;

        padding: 12px 28px !important;

        font-size: 16px !important;

        font-weight: 700 !important;

        width: 100% !important;

        font-family:
        "Cairo",
        sans-serif !important;

        box-shadow:
        0 6px 16px rgba(
            109,
            40,
            217,
            0.15
        ) !important;
    }

    .result-badge-container {
        display: flex;
        gap: 14px;
        margin-bottom: 20px;
    }

    .result-stat-box {
        flex: 1;
        background: white;
        border: 1px solid #F3E8FF;
        padding: 14px;
        border-radius: 14px;
        text-align: center;
    }

    .result-stat-label {
        font-size: 13px;
        color: #64748B;
        margin-bottom: 2px;
    }

    .result-stat-val {
        font-size: 18px;
        font-weight: 700;
        color: #6D28D9;
    }

    .step-card {
        background: white;
        border: 1px solid #F1F5F9;
        border-radius: 18px;
        padding: 22px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.01);
    }

    .step-icon {
        font-size: 28px;
        margin-bottom: 8px;
    }

    .step-title {
        font-size: 17px;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 6px;
    }

    .step-desc {
        font-size: 14px;
        color: #64748B;
        line-height: 1.6;
    }

    .researcher-card {
        background: white;
        border: 1px solid #EEF2F6;
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.01);
        margin-top: 40px;
    }

    .researcher-flex {
        display: flex;
        align-items: center;
        gap: 24px;
    }

    .researcher-img {
        width: 110px;
        height: 110px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #F3E8FF;
    }

    .researcher-name {
        font-size: 20px;
        font-weight: 800;
        color: #1E293B;
    }

    .researcher-title {
        font-size: 15px;
        font-weight: 600;
        color: #6D28D9;
        margin: 8px 0;
    }

    .researcher-bio {
        font-size: 14px;
        color: #475569;
        line-height: 1.7;
    }

    .footer-text {
        text-align: center;
        color: #94A3B8;
        font-size: 13px;
        margin-top: 50px;
        border-top: 1px solid #E2E8F0;
        padding-top: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================
# 8. قاعدة البيانات
# =========================================

semantic_db = {

    "عين": {

        "عضو البصر":
        "الرؤية والنظر والدموع والبصر",

        "نبع ماء":
        "الماء والينبوع والشرب والطبيعة",

        "جاسوس":
        "التجسس والمراقبة والعدو"
    },

    "قلب": {

        "عضو حيوي":
        "النبض والدم والجسد",

        "العاطفة والمشاعر":
        "الحب والإحساس والمشاعر"
    },

    "نار": {

        "لهب حقيقي":
        "الحريق والحرارة والدخان",

        "حماس عاطفي":
        "المشاعر والحب والحماس"
    },

    "روح": {

        "نفس بشرية":
        "الحياة والإنسان والوفاة",

        "جانب معنوي":
        "المشاعر والطاقة الداخلية"
    }
}

# =========================================
# 9. HERO SECTION
# =========================================

st.markdown(
    """
    <div class="hero-container">

        <div class="hero-inline">

            <div class="hero-brand">

                <div class="brand-main">
                    ✦ LABEEB AI
                </div>

                <div class="brand-sub">
                    CONTEXTUAL SEMANTIC ANALYZER
                </div>

            </div>

            <img
            src="https://raw.githubusercontent.com/hzouaki-ship-it/labeeb-ai/main/logo.png"
            class="hero-logo-img">

        </div>

        <div class="hero-subtitle">
            المحلل الدلالي الذكي لفهم
            المعنى والسياق في اللغة العربية
        </div>

        <div class="hero-desc">
            منصة تعتمد على الذكاء الاصطناعي
            لتحليل النصوص العربية وفهم
            معناها العميق في السياق.
        </div>

        <div class="badge-student">
            © 2026 تم تطوير وتصميم
            بواسطة الطالبة هاجر الزواكي
        </div>

    </div>
    """,
    unsafe_allow_html=True
)

# =========================================
# 10. الإدخال
# =========================================

st.markdown(
    """
    <div class="glass-card">
        <div class="card-title">
        🖋️ ابدأ التحليل
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

user_text = st.text_area(
    "",
    placeholder=
    "اكتب جملتك هنا...",
    key="main_input",
    label_visibility="collapsed"
)

submit_btn = st.button(
    "⚡ تشغيل خوارزمية لبيب"
)

# =========================================
# 11. التحليل
# =========================================

if submit_btn and user_text.strip():

    with st.spinner(
        "⏳ جاري تحليل السياق الدلالي..."
    ):

        words = user_text.split()

        found_target = None

        for word in words:

            stemmer.light_stem(word)

            word_stem = stemmer.get_stem()

            for key in semantic_db.keys():

                stemmer.light_stem(key)

                key_stem = stemmer.get_stem()

                if word_stem == key_stem:

                    found_target = key
                    break

            if found_target:
                break

        if found_target:

            meanings = semantic_db[
                found_target
            ]

            best_meaning = ""

            highest_similarity = -1

            all_results = []

            for meaning, context in meanings.items():

                similarity = semantic_similarity(
                    user_text,
                    context
                )

                all_results.append(
                    (meaning, similarity)
                )

                if similarity > highest_similarity:

                    highest_similarity = similarity

                    best_meaning = meaning

            ai_analysis = ""

            if client:

                try:

                    response = client.chat.completions.create(

                        model="openrouter/auto",

                        messages=[

                            {
                                "role": "system",

                                "content":
                                """
                                أنت محلل دلالي عربي متخصص.

                                حلل الجملة دلالياً
                                اعتماداً على السياق.

                                أجب بهذا الشكل فقط:

                                - المعنى المقصود
                                - هل الاستعمال
                                  حقيقي أم مجازي
                                - تفسير مختصر جداً

                                يجب أن يكون الجواب
                                قصيراً وواضحاً.
                                """
                            },

                            {
                                "role": "user",
                                "content": user_text
                            }
                        ]
                    )

                    ai_analysis = (
                        response
                        .choices[0]
                        .message
                        .content
                    )

                except Exception:

                    ai_analysis = (
                        "تعذر تنفيذ التحليل "
                        "الذكي حالياً."
                    )

            st.markdown(
                '<div class="glass-card">',
                unsafe_allow_html=True
            )

            st.markdown(

                '<div class="result-badge-container">'

                ' <div class="result-stat-box">'

                '     <div class="result-stat-label">'
                '     المعنى الأقرب'
                '     </div>'

                '     <div class="result-stat-val">'
                + best_meaning +
                '</div>'

                ' </div>'

                ' <div class="result-stat-box">'

                '     <div class="result-stat-label">'
                '     نسبة القرب الدلالي'
                '     </div>'

                '     <div class="result-stat-val">'
                + f"{highest_similarity * 100:.2f}%"
                + '</div>'

                ' </div>'

                '</div>',

                unsafe_allow_html=True
            )

            results_df = pd.DataFrame(

                {
                    "المعنى المحتمل":
                    [x[0] for x in all_results],

                    "نسبة القرب":
                    [
                        f"{x[1] * 100:.2f}%"
                        for x in all_results
                    ]
                }

            ).sort_values(
                by="نسبة القرب",
                ascending=False
            )

            st.table(results_df)

            st.markdown(
                f'''
                <div class="glass-card">

                    <div class="card-title">
                    🤖 التفسير الدلالي الذكي
                    </div>

                    <p style="
                    line-height:2;
                    color:#334155;
                    font-size:16px;
                    ">
                    {ai_analysis}
                    </p>

                </div>
                ''',
                unsafe_allow_html=True
            )

        else:

            st.warning(
                "⚠️ لم يتم العثور "
                "على لفظ مشترك "
                "داخل قاعدة البيانات."
            )

# =========================================
# 12. كيف يعمل لبيب
# =========================================

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(
        """
        <div class="step-card">
            <div class="step-icon">🔎</div>
            <div class="step-title">
            تحليل السياق
            </div>
            <div class="step-desc">
            فحص البنية المحيطة
            بالكلمة داخل الجملة.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        """
        <div class="step-card">
            <div class="step-icon">✨</div>
            <div class="step-title">
            فهم المعنى
            </div>
            <div class="step-desc">
            مقارنة السياق بالمعاني
            المحتملة باستخدام AraBERT.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:

    st.markdown(
        """
        <div class="step-card">
            <div class="step-icon">📊</div>
            <div class="step-title">
            قياس التشابه
            </div>
            <div class="step-desc">
            حساب التشابه الدلالي
            لاختيار المعنى الأقرب.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================
# 13. بطاقة الباحثة
# =========================================

st.markdown(
    """
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
                مهتمة بالذكاء الاصطناعي
                ومعالجة اللغة العربية
                وبناء الأنظمة الدلالية الذكية.
                </div>

            </div>

        </div>

    </div>
    """,
    unsafe_allow_html=True
)

# =========================================
# 14. التذييل
# =========================================

st.markdown(
    """
    <div class="footer-text">

        LABEEB AI © 2026
        — جميع الحقوق محفوظة —
        هاجر الزواكي

    </div>
    """,
    unsafe_allow_html=True
)
