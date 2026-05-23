import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import time

# إعدادات الصفحة
st.set_page_config(
    page_title="LABEEB AI | لبيب",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# تنسيقات CSS
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"], .stApp {
    background-color: #F8FAFC !important;
    direction: rtl !important;
    text-align: right !important;
    font-family: 'Cairo', sans-serif !important;
}

[data-testid="stMain"] .block-container {
    max-width: 900px !important;
    padding-top: 1rem !important;
    padding-bottom: 3rem !important;
}

h1, h2, h3, h4, h5, h6, p, span, label {
    font-family: 'Cairo', sans-serif !important;
    direction: rtl !important;
}

.hero-wrapper {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    padding: 5px 0 10px 0 !important;
}

.top-badge {
    background: white !important;
    color: #6D28D9 !important;
    padding: 6px 18px !important;
    border-radius: 100px !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    margin-bottom: 20px !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05) !important;
}

.hero-title {
    font-size: 46px !important;
    font-weight: 800 !important;
    margin-top: 10px !important;
    background: linear-gradient(90deg, #6D28D9, #2563EB) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
}

.hero-subtitle {
    font-size: 20px !important;
    font-weight: 700 !important;
    color: #1E293B !important;
    margin-top: 12px !important;
}

.hero-description {
    font-size: 15px !important;
    color: #64748B !important;
    max-width: 650px !important;
    line-height: 1.9 !important;
    margin-top: 12px !important;
}

.author-badge {
    margin-top: 18px !important;
    background: #F3E8FF !important;
    color: #6B21A8 !important;
    padding: 8px 22px !important;
    border-radius: 100px !important;
    font-size: 13px !important;
    font-weight: 700 !important;
}

.section-card {
    background: white !important;
    border-radius: 24px !important;
    padding: 32px !important;
    margin-top: 25px !important;
    border: 1px solid #E2E8F0 !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.03) !important;
}

.card-title-text {
    font-size: 18px !important;
    font-weight: 700 !important;
    color: #1E293B !important;
    margin-bottom: 15px !important;
}

.stTextArea textarea {
    border-radius: 18px !important;
    border: 1px solid #CBD5E1 !important;
    padding: 18px !important;
    font-size: 15px !important;
    direction: rtl !important;
    text-align: right !important;
}

.stTextArea textarea:focus {
    border: 1px solid #7C3AED !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.15) !important;
}

.stButton > button {
    width: 100% !important;
    background: linear-gradient(90deg, #6D28D9, #7C3AED) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 12px 24px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    transition: 0.3s ease !important;
    box-shadow: 0 6px 18px rgba(109,40,217,0.25) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
}

.empty-box {
    border: 1px dashed #CBD5E1 !important;
    border-radius: 18px !important;
    padding: 40px 20px !important;
    text-align: center !important;
    background: #FAFAFA !important;
}

.steps-title {
    text-align: center !important;
    font-size: 24px !important;
    font-weight: 800 !important;
    color: #1E293B !important;
    margin-top: 50px !important;
}

.steps-desc {
    text-align: center !important;
    color: #64748B !important;
    margin-bottom: 25px !important;
}

.step-card {
    background: white !important;
    border-radius: 22px !important;
    padding: 24px !important;
    text-align: center !important;
    border: 1px solid #E2E8F0 !important;
    height: 100% !important;
}

.footer-container {
    text-align: center !important;
    margin-top: 50px !important;
    padding-top: 20px !important;
    border-top: 1px solid #E2E8F0 !important;
    color: #94A3B8 !important;
    font-size: 13px !important;
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Hero Section
hero_html = """
<div class="hero-wrapper">
    <div class="top-badge">✦ منصة ذكاء اصطناعي عربية</div>

    <svg width="105" height="105" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="grad" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="#6D28D9"/>
                <stop offset="100%" stop-color="#2563EB"/>
            </linearGradient>
        </defs>

        <path d="M115 30V125C115 149.85 94.85 170 70 170C45.15 170 25 149.85 25 125V105"
        stroke="url(#grad)"
        stroke-width="18"
        stroke-linecap="round"/>

        <circle cx="150" cy="45" r="6" fill="#7C3AED" />
        <circle cx="180" cy="70" r="7" fill="#2563EB" />
        <circle cx="155" cy="95" r="6" fill="#7C3AED" />

        <path d="M115 70L150 45M115 70L155 95M150 45L180 70M155 95L180 70"
        stroke="url(#grad)"
        stroke-width="3"/>
    </svg>

    <h1 class="hero-title">لبيب | LABEEB AI</h1>

    <div class="hero-subtitle">
        المحلل الدلالي الذكي لفهم المعنى والسياق في اللغة العربية
    </div>

    <div class="hero-description">
        منصة تعتمد على الذكاء الاصطناعي وتحليل السياق اللغوي لاكتشاف المعنى الصحيح للكلمات العربية متعددة الدلالات باستخدام نماذج لغوية عميقة.
    </div>

    <div class="author-badge">
        تم تطوير وتصميم منصة LABEEB AI بواسطة الطالبة الباحثة هاجر الزواكي © 2026
    </div>
</div>
"""

st.markdown(hero_html, unsafe_allow_html=True)

# تحميل النموذج
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("aubmindlab/bert-base-arabertv02")
    model = AutoModel.from_pretrained("aubmindlab/bert-base-arabertv02")
    return tokenizer, model

tokenizer, model = load_model()

@st.cache_data
def get_word_vector(sentence, target_word):
    inputs = tokenizer(sentence, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    
    embeddings = outputs.last_hidden_state[0]
    tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
    
    # خوارزمية محسنة للبحث عن الكلمة حتى في حالة التقطيع أو الاتصال بضمائر
    for idx, token in enumerate(tokens):
        clean_token = token.replace("##", "")
        if target_word in clean_token or clean_token in target_word:
            return embeddings[idx].numpy().reshape(1, -1)
            
    return None

semantic_dictionary = {
    "عين": {
        "المعنى1": {
            "النص": "شرب الرجل من عين الماء العذبة",
            "المعنى": "نبع ماء"
        },
        "المعنى2": {
            "النص": "أصيبت عين الطفل ونزلت دموعه",
            "المعنى": "عضو البصر"
        },
        "المعنى3": {
            "النص": "كان عيناً للعدو داخل المدينة",
            "المعنى": "جاسوس"
        }
    },
    "المغرب": {
        "المعنى1": {
            "النص": "سافرت إلى المغرب لزيارة الرباط",
            "المعنى": "دولة المغرب"
        },
        "المعنى2": {
            "النص": "ذهبت إلى المسجد لصلاة المغرب",
            "المعنى": "صلاة المغرب"
        }
    },
    "رأس": {
        "المعنى1": {
            "النص": "يشعر بألم في رأسه",
            "المعنى": "عضو من الجسم"
        },
        "المعنى2": {
            "النص": "اجتمع رأس الشركة بالموظفين",
            "المعنى": "قائد"
        },
        "المعنى3": {
            "النص": "وصل المتسلق إلى رأس الجبل",
            "المعنى": "قمة"
        }
    }
}

# حساب المتجهات الدلالية المرجعية مسبقاً
for word in semantic_dictionary:
    for meaning in semantic_dictionary[word]:
        semantic_dictionary[word][meaning]["vector"] = get_word_vector(
            semantic_dictionary[word][meaning]["النص"],
            word
        )

# بطاقة الإدخال والتحليل الموحدة لجمالية التصميم
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<h3 class="card-title-text">✍️ أدخل النص العربي لاكتشاف المعنى الدلالي بدقة:</h3>', unsafe_allow_html=True)

user_sentence = st.text_area(
    "",
    placeholder="اكتب نصاً عربياً يحتوي على كلمة متعددة المعاني (مثل: عين، المغرب، رأس) لتحليل السياق واكتشاف المعنى المقصود...",
    height=120,
    label_visibility="collapsed"
)

st.write("")
analysis_triggered = st.button("✨ ابدأ التحليل الذكي")
st.markdown('</div>', unsafe_allow_html=True)

#
