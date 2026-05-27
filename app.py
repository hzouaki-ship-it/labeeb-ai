import streamlit as st
import time
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

        padding-top:2rem;

        max-width:1100px;
    }

    .hero-container{

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

        background:rgba(
            255,
            255,
            255,
            0.95
        );

        backdrop-filter:blur(12px);

        border-radius:24px;

        padding:28px;

        margin-top:22px;

        border:1px solid #E2E8F0;

        box-shadow:
        0 8px 24px rgba(
            0,
            0,
            0,
            0.06
        );
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

        box-shadow:
        0 8px 20px rgba(
            79,
            70,
            229,
            0.25
        ) !important;
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
# HERO SECTION
# =========================================

st.markdown(
    '''
    <div class="hero-container">

        <div style="
        display:flex;
        align-items:center;
        justify-content:center;
        gap:35px;
        flex-wrap:wrap;
        ">

            <div>

                <div class="hero-title">
                    ✦ LABEEB AI
                </div>

                <div class="hero-sub">
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
            box-shadow:0 0 40px rgba(109,40,217,0.18);
            "
            >

        </div>

        <div class="hero-desc">

        منصة تعتمد على الذكاء الاصطناعي
        لفهم المعنى والسياق
        وتحليل الدلالة في اللغة العربية.

        </div>

        <div style="
        margin-top:20px;
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
    """
    <div class="glass-card">

        <h3 style="text-align:center;">
        🖋️ ابدأ التحليل الدلالي
        </h3>

        <p style="
        text-align:center;
        color:#64748B;
        line-height:2;
        ">

        أدخل جملة عربية وسيقوم لبيب
        بتحليل معناها اعتمادًا على
        الذكاء الاصطناعي والسياق.

        </p>

    </div>
    """,
    unsafe_allow_html=True
)

# =========================================
# الإدخال
# =========================================

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
# التحليل الذكي
# =========================================

if submit_btn and user_text.strip():

    with st.spinner("⏳ جاري التحليل الذكي..."):

        time.sleep(1)

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

                            حلل الجملة اعتماداً
                            على السياق الدلالي.

                            أجب بهذا الشكل:

                            - اللفظ المحوري
                            - المعنى المقصود
                            - هل الاستعمال حقيقي أم مجازي
                            - تفسير مختصر
                            - نسبة الثقة التقريبية

                            يجب أن يكون الجواب:
                            أكاديمياً،
                            واضحاً،
                            ومختصراً.
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

            except Exception as e:

                ai_analysis = (
                    f"تعذر تنفيذ التحليل الذكي: {e}"
                )

        else:

            ai_analysis = (
                "لم يتم العثور على مفتاح OpenRouter داخل secrets."
            )

        st.markdown(
            f'''
            <div class="glass-card">

                <h3>
                🤖 التحليل الدلالي الذكي
                </h3>

                <div style="
                line-height:2.2;
                color:#334155;
                font-size:17px;
                ">

                {ai_analysis}

                </div>

            </div>
            ''',
            unsafe_allow_html=True
        )

# =========================================
# بطاقة الباحثة
# =========================================

st.markdown(
    '''
    <div class="glass-card">

        <div style="
        display:flex;
        align-items:center;
        gap:25px;
        flex-wrap:wrap;
        ">

            <img
            src="https://raw.githubusercontent.com/hzouaki-ship-it/labeeb-ai/main/hajar.jpg"

            style="
            width:110px;
            height:110px;
            border-radius:50%;
            object-fit:cover;
            border:3px solid #F3E8FF;
            "
            >

            <div>

                <div style="
                font-size:22px;
                font-weight:800;
                color:#1E293B;
                ">

                هاجر الزواكي

                </div>

                <div style="
                color:#6D28D9;
                font-weight:700;
                margin-top:6px;
                ">

                طالبة ماستر في اللسانيات الرقمية والعربية

                </div>

                <div style="
                color:#475569;
                line-height:2;
                margin-top:10px;
                ">

                مهتمة بالذكاء الاصطناعي
                ومعالجة اللغة العربية
                وبناء الأنظمة الدلالية الذكية.

                </div>

            </div>

        </div>

    </div>
    ''',
    unsafe_allow_html=True
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
