import streamlit as st
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
    page_title="LABEEB AI",
    page_icon="🧠",
    layout="wide"
)

# =========================================
# 2. CSS الجمالي الكامل
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

    .hero-inline{

        display:flex;

        justify-content:center;

        align-items:center;

        gap:25px;

        margin-bottom:20px;
    }

    .hero-brand{
        text-align:center;
    }

    .hero-title {

        font-size:72px;

        font-weight:800;

        color:#4F46E5;

        margin-bottom:10px;

        letter-spacing:2px;

        text-shadow:
        0 6px 18px rgba(
            79,
            70,
            229,
            0.15
        );
    }

    .hero-sub {

        color:#64748B;

        font-size:17px;

        letter-spacing:4px;

        font-weight:700;

        margin-top:10px;
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

    .footer-text{

        text-align:center;

        color:#94A3B8;

        margin-top:60px;

        font-size:13px;
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

    textarea{

        direction:rtl !important;

        font-size:18px !important;

        border-radius:18px !important;

        border:1px solid #E2E8F0 !important;

        padding:18px !important;
    }

    h3{
        color:#1E293B;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================
# 3. أدوات المعالجة
# =========================================

stemmer = ArabicLightStemmer()

# =========================================
# 4. تحميل AraBERT
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
# 5. OpenRouter
# =========================================

client = None

if "OPENROUTER_API_KEY" in st.secrets:

    client = OpenAI(

        api_key=st.secrets["OPENROUTER_API_KEY"],

        base_url="https://openrouter.ai/api/v1"
    )

# =========================================
# 6. استخراج التمثيل الدلالي
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
# 7. حساب التشابه الدلالي
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
# 8. قاعدة البيانات الدلالية
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

    "نار": {

        "لهب حقيقي":
        "الحريق والحرارة والدخان",

        "حماس عاطفي":
        "المشاعر والحب والحماس",

        "حرب أو فتن":
        "الصراع والقتال"
    },

    "روح": {

        "نفس بشرية":
        "الحياة والإنسان والوفاة",

        "جانب معنوي":
        "المشاعر والطاقة الداخلية",

        "عالم الغيب":
        "الأرواح والميتافيزيقا"
    },

    "قلب": {

        "عضو حيوي":
        "النبض والدم والجسد",

        "العاطفة والمشاعر":
        "الحب والإحساس والمشاعر"
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

                <div class="hero-title">
                    ✦ LABEEB AI
                </div>

                <div class="hero-sub">
                    CONTEXTUAL SEMANTIC ANALYZER
                </div>

            </div>

        </div>

        <div style="
        font-size:24px;
        font-weight:700;
        color:#1E293B;
        margin-top:15px;
        ">

        المحلل الدلالي الذكي لفهم
        المعنى والسياق في اللغة العربية

        </div>

        <div class="hero-desc">

        منصة تعتمد على الذكاء الاصطناعي
        وتحليل التمثيلات الدلالية
        لفهم المعنى العميق للنصوص العربية.

        </div>

        <div style="
        margin-top:25px;
        display:inline-block;
        background:white;
        padding:10px 24px;
        border-radius:999px;
        border:1px solid #E9D5FF;
        color:#6D28D9;
        font-size:14px;
        font-weight:700;
        ">

        © 2026 — هاجر الزواكي

        </div>

    </div>
    """,
    unsafe_allow_html=True
)

# =========================================
# 10. بطاقة الإدخال
# =========================================

st.markdown(
    """
    <div class="glass-card">

        <h3 style="
        margin-bottom:18px;
        color:#1E293B;
        ">

        🖋️ ابدأ التحليل

        </h3>

    </div>
    """,
    unsafe_allow_html=True
)

user_text = st.text_area(
    "",
    placeholder=
    "مثال: أشعلت كلماتها نار الحماس في قلبه...",
    label_visibility="collapsed"
)

submit_btn = st.button(
    "⚡ تشغيل خوارزمية لبيب للتحليل"
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

                                حلل الجملة دلالياً اعتماداً
                                على السياق.

                                أجب باختصار شديد.

                                حدد:
                                - المعنى المقصود
                                - هل المعنى مجازي أم حقيقي
                                - تفسير مختصر جداً
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

            st.markdown(
                f"""
                <div class="glass-card">

                    <h3>
                    🔍 التحليل الدلالي المرجح
                    </h3>

                    <p>
                    <b>اللفظ المكتشف:</b>
                    {found_target}
                    </p>

                    <p>
                    <b>المعنى السياقي الأرجح:</b>
                    {best_meaning}
                    </p>

                    <p>
                    <b>نسبة التشابه الدلالي:</b>
                    {highest_similarity:.2%}
                    </p>

                    <p>
                    <b>التفسير الدلالي:</b><br>
                    {ai_analysis}
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <div class="glass-card">

                <h3>
                📊 احتمالات المعنى
                </h3>
                """,
                unsafe_allow_html=True
            )

            for meaning, similarity in all_results:

                st.write(
                    f"• {meaning} → "
                    f"{similarity:.2%}"
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

        else:

            st.warning(
                "⚠️ لم يتم العثور على لفظ داخل قاعدة البيانات."
            )

# =========================================
# 12. التذييل
# =========================================

st.markdown(
    """
    <div class="footer-text">
        LABEEB AI © 2026 — هاجر الزواكي
    </div>
    """,
    unsafe_allow_html=True
)
