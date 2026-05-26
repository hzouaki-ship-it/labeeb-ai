import streamlit as st
import pandas as pd
import nltk
import torch

from nltk.corpus import wordnet as wn
from tashaphyne.stemming import ArabicLightStemmer

from transformers import (
    AutoTokenizer,
    AutoModel
)

# =========================================
# 1. تحميل الموارد
# =========================================

nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

stemmer = ArabicLightStemmer()

# =========================================
# 2. إعداد الصفحة
# =========================================

st.set_page_config(
    page_title="LABEEB AI",
    page_icon="🧠",
    layout="wide"
)

# =========================================
# 3. CSS
# =========================================

st.markdown(
    """
    <style>

    .hero-container{
        text-align:center;
        padding:30px;
    }

    .hero-title{
        font-size:52px;
        font-weight:800;
        color:#4F46E5;
    }

    .hero-sub{
        color:#64748B;
        font-size:18px;
        margin-top:10px;
    }

    .glass-card{
        background:rgba(255,255,255,0.92);
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
        background:linear-gradient(90deg,#4F46E5,#6D28D9) !important;
        color:white !important;
        border:none !important;
        border-radius:12px !important;
        width:100% !important;
        height:50px !important;
        font-size:18px !important;
        font-weight:bold !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================
# 4. قاعدة البيانات الدلالية
# =========================================

semantic_db = {

    "عين": {
        "المعنى": "عضو البصر أو نبع أو جاسوس",
        "السياق": "يعتمد على الألفاظ المحيطة"
    },

    "روح": {
        "المعنى": "النفس البشرية",
        "السياق": "الحياة أو الجانب المعنوي"
    },

    "نار": {
        "المعنى": "قد تدل على الحماس أو الحرب أو النار الحقيقية",
        "السياق": "يحدد عبر السياق المجازي"
    },

    "كتاب": {
        "المعنى": "مؤلف مطبوع",
        "السياق": "القراءة أو المعرفة"
    }
}

# =========================================
# 5. تحميل AraBERT
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
# 6. دالة استخراج embedding
# =========================================

def get_embedding(text):

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True
    )

    with torch.no_grad():

        outputs = arabert_model(**inputs)

    embedding = outputs.last_hidden_state.mean(dim=1)

    return embedding

# =========================================
# 7. الواجهة
# =========================================

st.markdown(
    """
    <div class="hero-container">

st.markdown(
    """
    <div class="hero-container">

        <div class="hero-title">
            ✦ LABEEB AI
        </div>

        <div class="hero-sub">
            المحلل الدلالي الذكي للغة العربية
        </div>

    </div>
    """,
    unsafe_allow_html=True
)
    </div>
    """,
    unsafe_allow_html=True
)

user_text = st.text_area(
    "أدخلي الجملة هنا:",
    placeholder="مثال: أشعلت كلماتها نار الحماس في قلبه..."
)

submit_btn = st.button("⚡ تحليل")

# =========================================
# 8. التحليل
# =========================================

if submit_btn:

    if not user_text.strip():

        st.warning("الرجاء إدخال نص.")

    else:

        with st.spinner("⏳ جاري التحليل الدلالي..."):

            found_local = False

            words_in_text = user_text.split()

            # =====================================
            # أ) التحليل المحلي
            # =====================================

            for word, data in semantic_db.items():

                for token in words_in_text:

                    stemmer.light_stem(token)
                    token_stem = stemmer.get_stem()

                    stemmer.light_stem(word)
                    word_stem = stemmer.get_stem()

                    if token_stem == word_stem:

                        st.markdown(
                            f"""
                            <div class="glass-card">

                                <h3>🔍 تحليل محلي</h3>

                                <p>
                                <b>اللفظ:</b>
                                {word}
                                </p>

                                <p>
                                <b>المعنى:</b>
                                {data["المعنى"]}
                                </p>

                                <p>
                                <b>السياق:</b>
                                {data["السياق"]}
                                </p>

                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        found_local = True
                        break

            # =====================================
            # ب) WordNet
            # =====================================

            synsets = []

            for w in words_in_text:

                if len(w) > 2:

                    results = wn.synsets(w, lang='arb')

                    if results:

                        synsets.extend(results[:1])

            if synsets:

                st.markdown(
                    """
                    <div class="glass-card">

                    <h3>
                    🧠 الشبكة الدلالية WordNet
                    </h3>
                    """,
                    unsafe_allow_html=True
                )

                for syn in synsets[:2]:

                    st.write(
                        f"📌 المعنى: {syn.definition()}"
                    )

                    arabic_words = [

                        lemma.name()

                        for lemma in syn.lemmas(lang='arb')
                    ]

                    if arabic_words:

                        st.write(
                            f"🔹 المرادفات: {', '.join(arabic_words[:3])}"
                        )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )

            # =====================================
            # ج) AraBERT
            # =====================================

            embedding = get_embedding(user_text)

            st.markdown(
                """
                <div class="glass-card">

                <h3>
                🤖 تحليل AraBERT
                </h3>
                """,
                unsafe_allow_html=True
            )

            st.write(
                "تم استخراج التمثيل الدلالي "
                "للجملة باستخدام AraBERT."
            )

            st.write(
                f"📊 حجم المتجه الدلالي: "
                f"{embedding.shape}"
            )

            if "نار" in user_text:

                st.success(
                    "🔥 تم اكتشاف استعمال مجازي "
                    "مرتبط بالحماس أو العاطفة."
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
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
