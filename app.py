import streamlit as st
import time
from openai import OpenAI

# =========================================
# إعداد الصفحة
# =========================================

st.set_page_config(
    page_title="LABEEB AI",
    page_icon="🧠",
    layout="wide"
)

# =========================================
# OpenRouter AI
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

        max-width:1100px;

        padding-top:2rem;
    }

    .stTextArea textarea{

        background:white !important;

        border-radius:24px !important;

        border:1px solid #E2E8F0 !important;

        padding:22px !important;

        font-size:18px !important;

        line-height:2 !important;

        color:#1E293B !important;

        box-shadow:
        0 4px 14px rgba(
            0,
            0,
            0,
            0.04
        ) !important;
    }

    .stTextArea textarea:focus{

        border:1px solid #8B5CF6 !important;

        box-shadow:
        0 0 0 4px rgba(
            139,
            92,
            246,
            0.10
        ) !important;
    }

    .stButton > button{

        background:
        linear-gradient(
            90deg,
            #4F46E5,
            #7C3AED
        ) !important;

        color:white !important;

        border:none !important;

        border-radius:18px !important;

        width:100% !important;

        height:60px !important;

        font-size:18px !important;

        font-weight:800 !important;

        transition:0.3s !important;

        box-shadow:
        0 10px 24px rgba(
            79,
            70,
            229,
            0.25
        ) !important;
    }

    .stButton > button:hover{

        transform:translateY(-2px);

        box-shadow:
        0 14px 28px rgba(
            79,
            70,
            229,
            0.35
        ) !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)
# =========================================
# HERO SECTION
# =========================================

st.markdown(
    '''
    <div style="
    text-align:center;

    padding:55px 35px;

    background:rgba(
        255,
        255,
        255,
        0.82
    );

    backdrop-filter:blur(16px);

    border-radius:30px;

    margin-bottom:35px;

    border:1px solid #E2E8F0;

    box-shadow:
    0 10px 30px rgba(
        0,
        0,
        0,
        0.05
    );
    ">

        <div style="
        display:flex;

        align-items:center;

        justify-content:center;

        gap:35px;

        flex-wrap:wrap;
        ">

            <div>

                <div style="
                font-size:72px;

                font-weight:800;

                color:#4F46E5;

                margin-bottom:10px;

                letter-spacing:2px;
                ">

                ✦ LABEEB AI

                </div>

                <div style="
                color:#64748B;

                font-size:17px;

                letter-spacing:4px;

                font-weight:700;
                ">

                CONTEXTUAL SEMANTIC ANALYZER

                </div>

            </div>

            <img
            src="https://raw.githubusercontent.com/hzouaki-ship-it/labeeb-ai/main/logo.png"

            style="
            width:170px;

            height:170px;

            border-radius:50%;

            object-fit:cover;

            box-shadow:
            0 0 40px rgba(
                109,
                40,
                217,
                0.18
            );
            "
            >

        </div>

        <div style="
        margin-top:25px;

        color:#475569;

        line-height:2.2;

        font-size:18px;

        max-width:750px;

        margin-left:auto;

        margin-right:auto;
        ">

        منصة تعتمد على الذكاء الاصطناعي
        لفهم المعنى والسياق
        وتحليل الدلالة في اللغة العربية.

        </div>

        <div style="
        margin-top:22px;

        display:inline-block;

        background:white;

        padding:8px 20px;

        border-radius:999px;

        border:1px solid #E9D5FF;

        color:#6D28D9;

        font-size:14px;

        font-weight:700;
        ">

        © 2026 — هاجر الزواكي

        </div>

    </div>
    ''',
    unsafe_allow_html=True
)
# =========================================
# بطاقة الإدخال
# =========================================

st.markdown(
    '''
    <div style="
    background:rgba(
        255,
        255,
        255,
        0.92
    );

    backdrop-filter:blur(12px);

    border-radius:28px;

    padding:35px;

    border:1px solid #E2E8F0;

    box-shadow:
    0 8px 24px rgba(
        0,
        0,
        0,
        0.05
    );

    margin-bottom:25px;
    ">

        <div style="
        text-align:center;

        font-size:30px;

        font-weight:800;

        color:#4F46E5;

        margin-bottom:12px;
        ">

        🧠 التحليل الدلالي الذكي

        </div>

        <div style="
        text-align:center;

        color:#64748B;

        line-height:2;

        font-size:17px;
        ">

        أدخل جملة عربية وسيقوم لبيب
        بتحليل المعنى والسياق
        اعتمادًا على الذكاء الاصطناعي.

        </div>

    </div>
    ''',
    unsafe_allow_html=True
)

# =========================================
# مربع الإدخال
# =========================================

user_text = st.text_area(
    "",

    placeholder=
    "مثال: احترق قلبي من شدة الشوق...",

    height=180,

    label_visibility="collapsed"
)

submit_btn = st.button(
    "⚡ تشغيل التحليل الذكي"
)
# =================================

