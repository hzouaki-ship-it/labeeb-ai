import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import time

# 1. إعدادات الصفحة الأساسية لواجهة المنصة
st.set_page_config(
    page_title="منصة لبيب LABEEB AI",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. تحميل محرك الخوارزمية (AraBERT) ومعالجة المتجهات الدلالية
@st.cache_resource
def load_model():
    # استخدام نسخة خفيفة ومستقرة ومخصصة للسيرفرات السحابية ذات الذاكرة المحدودة
    tokenizer = AutoTokenizer.from_pretrained("aubmindlab/bert-base-arabertv02")
    model = AutoModel.from_pretrained("aubmindlab/bert-base-arabertv02")
    return tokenizer, model

try:
    tokenizer, model = load_model()
except Exception as e:
    st.error("حدث خطأ أثناء تحميل النموذج اللغوي، يرجى إعادة تحديث الصفحة.")

def get_word_vector(sentence, target_word):
    try:
        inputs = tokenizer(sentence, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)
        embeddings = outputs.last_hidden_state[0]
        tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
        for idx, token in enumerate(tokens):
            if target_word in token:
                return embeddings[idx].numpy().reshape(1, -1)
    except Exception:
        return None
    return None

# القاموس الدلالي المرجعي المحاكي لعينات اللفظ المشترك
semantic_dictionary = {
    "عين": {
        "المعنى1": {"النص": "شرب الرجل من عين الماء العذبة", "المعنى": "نبع ماء"},
        "المعنى2": {"النص": "أصيبت عين الطفل و نزلت دموعه", "المعنى": "عضو من الجسم"},
        "المعنى3": {"النص": "كان عينًا للعدو داخل المدينة", "المعنى": "جاسوس"}
    },
    "المغرب": {
        "المعنى1": {"النص": "سافرت إلى المغرب لزيارة الرباط", "المعنى": "دولة المغرب"},
        "المعنى2": {"النص": "ذهبت إلى المسجد لصلاة المغرب", "المعنى": "صلاة المغرب"}
    },
    "رأس": {
        "المعنى1": {"النص": "يشعر بألم في رأسه", "المعنى": "عضو من الجسم"},
        "المعنى2": {"النص": "اجتمع رأس الشركة بالموظفين", "المعنى": "قائد"},
        "المعنى3": {"النص": "وصل المتسلق إلى رأس الجبل", "المعنى": "قمة"}
    }
}

# بناء المتجهات الدلالية المسبقة لعينات معالجة اللفظ المشترك
for word in semantic_dictionary:
    for meaning in semantic_dictionary[word]:
        if "vector" not in semantic_dictionary[word][meaning]:
            semantic_dictionary[word][meaning]["vector"] = get_word_vector(
                semantic_dictionary[word][meaning]["النص"], word
            )

# 3. بناء واجهة المستخدم باستخدام عناصر Streamlit الأصلية 100% (بدون HTML)
st.title("🧠 منصة لبيب | LABEEB AI")
st.subheader("التحليل الدلالي الحواسبّي للنصوص العربية")
st.caption("تطبيق ذكاء اصطناعي لفك اللبس الدلالي وتحليل المشترك اللفظي باستخدام النماذج اللغوية السياقية.")

# صندوق التعريف الأكاديمي والجامعي للباحثة
with st.container(border=True):
    st.markdown("**إعداد الطالبة الباحثة:** هاجر الزواكي")
    st.write("السنة الثانية من سلك الماجستير، تخصص اللسانيات الرقمية والذكاء الاصطناعي")
    st.write("كلية الآداب والعلوم الإنسانية، جامعة مولاي إسماعيل، مكناس")
    st.caption("📌 يندرج هذا المشروع ضمن متطلبات مشروع التخرج (PFE) للعام الجامعي 2025/2026")

st.divider()

# 4. مدخلات فحص العينات اللغوية
st.write("### ✍️ أدخل الجملة العربية المراد فحصها سياقياً:")
user_sentence = st.text_area(
    label="نص الفحص",
    placeholder="مثال: صليت المغرب في المسجد، أو شربت من عين ماء عذبة...",
    height=120,
    label_visibility="collapsed"
)

st.write("")
analysis_triggered = st.button("⚡ إطلاق خوارزمية لبيب للتحليل", use_container_width=True)

st.divider()

# 5. عرض النتائج والقرارات الخوارزمية
st.write("### 📊 نتيجة التحليل والدلالة السياقية:")

if analysis_triggered:
    if user_sentence.strip():
        detected_word = None
        for word in semantic_dictionary:
            if word in user_sentence:
                detected_word = word
                break
        
        if detected_word:
            with st.spinner("⏳ يقوم لبيب بقراءة المؤشرات السياقية عبر نموذج AraBERT اللغوي..."):
                time.sleep(0.4)
                user_vector = get_word_vector(user_sentence, detected_word)
                
                if user_vector is not None:
                    similarities = []
                    for meaning in semantic_dictionary[detected_word]:
                        ref_vector = semantic_dictionary[detected_word][meaning]["vector"]
                        if ref_vector is not None:
                            sim = cosine_similarity(user_vector, ref_vector)[0][0]
