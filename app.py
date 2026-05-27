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
# إعداد الصفحة
# =========================================

st.set_page_config(
    page_title="LABEEB AI - لبيب",
    page_icon="🧠",
    layout="wide"
)

# =========================================
# أدوات المعالجة
# =========================================

stemmer = ArabicLightStemmer()

# =========================================
# تحميل AraBERT
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
# OpenRouter
# =========================================

client = None

if "OPENROUTER_API_KEY" in st.secrets:

    client = OpenAI(

        api_key=st.secrets[
            "OPENROUTER_API_KEY"
        ],

        base_url=
        "https://openrouter.ai/api/v1"
    )

# =========================================
# التمثيل الدلالي
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

    return outputs.last_hidden_state[:, 0, :]

# =========================================
# حساب التشابه الدلالي
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
# CSS
# =========================================

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&display=swap');

    html, body, [class*="css"]{
        font-family:'Cairo', sans-serif;
        direction:rtl;
    }

    .stApp{
        background:
        linear-gradient(
            135deg,
            #F8FAFC,
            #EEF2FF
        );
    }

    .block-container{
        padding-top:2rem;
        max-width:1100px;
    }

    .hero-container{
        text-align:center;
        padding:55px 35px;
        background:rgba(255,255,255,0.82);
        backdrop-filter:blur(16px);
        border-radius:30px;
        margin-bottom:35px;
        border:1px solid #E2E8F0;
        box-shadow:0 10px 30px rgba(0,0,0,0.05);
    }

    .hero-title{
        font-size:72px;
        font-weight:800;
        color:#4F46E5;
        margin-bottom:10px;
        letter-spacing:2px;
    }

    .hero-sub{
        color:#64748B;
        font-size:17px;
        letter-spacing:4px;
        font-weight:700;
    }

    .hero-desc{
        margin-top:22px;
        color:#475569;
        line-height:2;
        font-size:18px;
        max-width:750px;
        margin-left:auto;
        margin-right:auto;
    }

    .glass-card{
        background:rgba(255,255,255,0.95);
        backdrop-filter:blur(12px);
        border-radius:24px;
        padding:28px;
        margin-top:22px;
        border:1px solid #E2E8F0;
        box-shadow:0 8px 24px rgba(0,0,0,0.06);
    }

    .stTextArea textarea{
        background:white !important;
        border-radius:22px !important;
        border:1px solid #E2E8F0 !important;
        padding:20px !important;
        font-size:18px !important;
        line-height:2 !important;
        direction:rtl !important;
    }

    .stButton > button{
        background:
        linear-gradient(
            90deg,
            #4F46E5,
            #6D28D9
        ) !important;

        color:white !important;
        border:none !important;
        border-radius:16px !important;
        width:100% !important;
        height:58px !important;
        font-size:18px !important;
        font-weight:bold !important;
    }

    .result-badge-container{
        display:flex;
        gap:14px;
        margin-bottom:20px;
    }

    .result-stat-box{
        flex:1;
        background:white;
        border:1px solid #F3E8FF;
        padding:14px;
        border-radius:14px;
        text-align:center;
    }

    .result-stat-label{
        font-size:13px;
        color:#64748B;
    }

    .result-stat-val{
        font-size:18px;
        font-weight:700;
        color:#6D28D9;
    }

    .footer-text{
        text-align:center;
        color:#94A3B8;
        margin-top:60px;
        font-size:13px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================
# قاعدة البيانات
# =========================================

semantic_db = {

    "قلب": [

        {
            "المعنى": "عضو حيوي",
            "القرائن": {
                "نبض": 5,
                "دم": 4,
                "عملية": 5,
                "مستشفى": 4
            }
        },

        {
            "المعنى": "العاطفة والمشاعر",
            "القرائن": {
                "حب": 5,
                "اشتياق": 4,
                "مشاعر": 5,
                "حزن": 4,
                "شوق": 4
            }
        }
    ],

    "عين": [

        {
            "المعنى": "عضو البصر",
            "القرائن": {
                "نظر": 5,
                "رؤية": 5,
                "دموع": 4,
                "عدسة": 3
            }
        },

        {
            "المعنى": "نبع ماء",
            "القرائن": {
                "ماء": 5,
                "نبع": 5,
                "وادي": 3
            }
        }
    ],

    "نار": [

        {
            "المعنى": "لهب حقيقي",
            "القرائن": {
                "حريق": 5,
                "دخان": 4,
                "احتراق": 5
            }
        },

        {
            "المعنى": "حماس عاطفي",
            "القرائن": {
                "مشاعر": 5,
                "حب": 4,
                "شغف": 5
            }
        }
    ]
}

# =========================================
# HERO SECTION
# =========================================

st.markdown(
    """
    <div class="hero-container">

        <div class="hero-title">
            ✦ LABEEB AI
        </div>

        <div class="hero-sub">
            CONTEXTUAL SEMANTIC ANALYZER
        </div>

        <div class="hero-desc">

        منصة تعتمد على الذكاء الاصطناعي
        لتحليل المعنى والسياق
        في اللغة العربية.

        </div>

    </div>
    """,
    unsafe_allow_html=True
)

# =========================================
# الإدخال
# =========================================

st.markdown(
    """
    <div class="glass-card">

        <h3 style="text-align:center;">
        🖋️ ابدأ التحليل الدلالي
        </h3>

    </div>
    """,
    unsafe_allow_html=True
)

user_text = st.text_area(
    "",
    placeholder="مثال: احترق قلبي من شدة الشوق...",
    height=180,
    label_visibility="collapsed"
)

submit_btn = st.button(
    "⚡ تشغيل خوارزمية لبيب للتحليل"
)

# =========================================
# التحليل
# =========================================

if submit_btn and user_text.strip():

    with st.spinner("⏳ جاري التحليل..."):

        time.sleep(0.5)

        detected_keyword = None

        for word in semantic_db.keys():

            if word in user_text:
                detected_keyword = word
                break

        if detected_keyword:

            meanings = semantic_db[
                detected_keyword
            ]

            results_list = []

            highest_score = 0
            predicted_meaning = ""

            for entry in meanings:

                context_text = " ".join(
                    entry["القرائن"].keys()
                )

                score = semantic_similarity(
                    user_text,
                    context_text
                )

                if score < 0:
                    score = 0.05

                if score > 1:
                    score = 1.0

                results_list.append({

                    "المعنى المحتمل":
                    entry["المعنى"],

                    "نسبة القرب":
                    f"{score * 100:.2f}%",

                    "_raw":
                    score
                })

                if score > highest_score:

                    highest_score = score

                    predicted_meaning = (
                        entry["المعنى"]
                    )

            st.markdown(
                '<div class="result-badge-container">'
                ' <div class="result-stat-box">'
                '     <div class="result-stat-label">المعنى الأقرب</div>'
                '     <div class="result-stat-val">' + predicted_meaning + '</div>'
                ' </div>'
                ' <div class="result-stat-box">'
                '     <div class="result-stat-label">نسبة القرب الدلالي</div>'
                '     <div class="result-stat-val">' + f"{highest_score * 100:.2f}%" + '</div>'
                ' </div>'
                '</div>',
                unsafe_allow_html=True
            )

            df_clean = pd.DataFrame(
                results_list
            ).sort_values(
                by="_raw",
                ascending=False
            ).drop(
                columns=["_raw"]
            )

            st.table(
                df_clean.reset_index(drop=True)
            )

            # =========================================
            # التحليل الذكي
            # =========================================

            ai_analysis = ""

            if client:

                try:

                    response = client.chat.completions.create(

                        model="openrouter/auto",

                        messages=[

                            {
                                "role": "system",

                                "content":
                                '''
                                أنت محلل دلالي عربي متخصص.

                                حلل الجملة اعتماداً
                                على السياق.

                                أجب باختصار:

                                - المعنى المقصود
                                - هل الاستعمال حقيقي أم مجازي
                                - تفسير مختصر
                                '''
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

                except Exception as e:

                    ai_analysis = (
                        f"تعذر تنفيذ التحليل الذكي: {e}"
                    )

            st.markdown(
                f'''
                <div class="glass-card">

                    <h3>
                    🤖 التحليل الذكي
                    </h3>

                    <div style="
                    line-height:2;
                    color:#334155;
                    font-size:16px;
                    ">

                    {ai_analysis}

                    </div>

                </div>
                ''',
                unsafe_allow_html=True
            )

        else:

            st.warning(
                "⚠️ لم يتم العثور على لفظ داخل قاعدة البيانات."
            )

# =========================================
# FOOTER
# =========================================

st.markdown(
    """
    <div class="footer-text">
        LABEEB AI © 2026 — هاجر الزواكي
    </div>
    """,
    unsafe_allow_html=True
)
