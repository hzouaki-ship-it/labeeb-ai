import streamlit as st
import torch
import torch.nn.functional as F

from tashaphyne.stemming import ArabicLightStemmer

from transformers import (
    AutoTokenizer,
    AutoModel
)

# =========================================
# 1. الإعدادات العامة
# =========================================

stemmer = ArabicLightStemmer()

st.set_page_config(
    page_title="LABEEB AI - النظام الدلالي",
    page_icon="🧠",
    layout="wide"
)

# =========================================
# 2. CSS الجمالي
# =========================================

st.markdown(
    """
    <style>

    .hero-container{
        text-align:center;
        padding:35px;
    }

    .hero-title{
        font-size:56px;
        font-weight:800;
        color:#4F46E5;
    }

    .hero-sub{
        color:#64748B;
        font-size:18px;
        margin-top:10px;
    }

    .glass-card{
        background:rgba(255,255,255,0.93);
        backdrop-filter:blur(10px);
        border-radius:22px;
        padding:25px;
        margin-top:20px;
        border:1px solid #E2E8F0;
        box-shadow:0 8px 20px rgba(0,0,0,0.06);
    }

    .footer-text{
        text-align:center;
        color:#94A3B8;
        margin-top:60px;
        font-size:13px;
    }

    .stButton > button{
        background:linear-gradient(
            90deg,
            #4F46E5,
            #6D28D9
        ) !important;

        color:white !important;

        border:none !important;

        border-radius:14px !important;

        width:100% !important;

        height:52px !important;

        font-size:18px !important;

        font-weight:bold !important;
    }

    textarea{
        direction:rtl !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

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
# 4. استخراج التمثيل الدلالي
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

    # استعمال CLS token
    embedding = outputs.last_hidden_state[:, 0, :]

    return embedding

# =========================================
# 5. حساب التشابه الدلالي
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
# 6. قاعدة البيانات الدلالية
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

    "روح": {

        "نفس بشرية":
        "الحياة والإنسان والوفاة",

        "جانب معنوي":
        "المشاعر والطاقة الداخلية",

        "عالم الغيب":
        "الأرواح والميتافيزيقا"
    },

    "نار": {

        "لهب حقيقي":
        "الحريق والحرارة والدخان",

        "حماس عاطفي":
        "المشاعر والحب والحماس",

        "حرب أو فتن":
        "الصراع والقتال"
    },

    "قلب": {

        "عضو حيوي":
        "النبض والدم والجسد",

        "العاطفة والمشاعر":
        "الحب والإحساس والمشاعر"
    }
}

# =========================================
# 7. الواجهة
# =========================================

st.markdown(
    """
    <div class="hero-container">

        <div class="hero-title">
            ✦ LABEEB AI
        </div>

        <div class="hero-sub">
            المحلل الدلالي السياقي للغة العربية
        </div>

    </div>
    """,
    unsafe_allow_html=True
)

user_text = st.text_area(
    "أدخلي الجملة:",
    placeholder="مثال: أشعلت كلماتها نار الحماس في قلبه..."
)

submit_btn = st.button(
    "⚡ تحليل دلالي متقدم"
)

# =========================================
# 8. التحليل الدلالي
# =========================================

if submit_btn and user_text.strip():

    with st.spinner(
        "⏳ جاري تحليل السياق الدلالي..."
    ):

        words = user_text.split()

        found_target = None

        # =====================================
        # الكشف عن اللفظ
        # =====================================

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

        # =====================================
        # التحليل السياقي
        # =====================================

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

            # =================================
            # عرض النتيجة الرئيسية
            # =================================

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
                    <b>التفسير:</b>
                    قام النظام بتحليل السياق
                    باستخدام نموذج AraBERT
                    ثم مقارنة المتجهات
                    الدلالية للمعاني المحتملة
                    واختيار المعنى الأقرب
                    لسياق الجملة.
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )

            # =================================
            # عرض الاحتمالات
            # =================================

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

            # =================================
            # كشف المجاز
            # =================================

            if highest_similarity < 0.60:

                st.info(
                    "💡 قد تحتوي الجملة على "
                    "استعارة أو استعمال مجازي."
                )

        else:

            st.warning(
                "لم يتم العثور على لفظ "
                "مشترك داخل قاعدة البيانات."
            )

# =========================================
# 9. التذييل
# =========================================

st.markdown(
    """
    <div class="footer-text">
        LABEEB AI © 2026 — هاجر الزواكي
    </div>
    """,
    unsafe_allow_html=True
)
