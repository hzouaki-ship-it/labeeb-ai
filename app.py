import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import time

# إعداد الصفحة
st.set_page_config(page_title="LABEEB AI | لبيب", page_icon="🧠", layout="centered")

# تنسيق CSS - تم تنظيفه ليعمل دون أخطاء
st.markdown("""
<style>
    .stApp { background-color: #F8FAFC; direction: rtl; text-align: right; font-family: 'Cairo', sans-serif; }
    .hero { text-align: center; padding: 2rem; }
    .card { background: white; padding: 2rem; border-radius: 20px; border: 1px solid #E2E8F0; margin-bottom: 1rem; }
    .stButton>button { width: 100%; background: #6D28D9; color: white; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# الهيدر
st.markdown('<div class="hero"><h1>لبيب | LABEEB AI</h1><p>المحلل الدلالي الذكي</p></div>', unsafe_allow_html=True)

# تحميل النموذج
@st.cache_resource
def load_model():
    return AutoTokenizer.from_pretrained("aubmindlab/bert-base-arabertv02"), AutoModel.from_pretrained("aubmindlab/bert-base-arabertv02")

tokenizer, model = load_model()

def get_word_vector(sentence, target_word):
    inputs = tokenizer(sentence, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
    for idx, token in enumerate(tokens):
        if target_word in token.replace("##", ""):
            return outputs.last_hidden_state[0][idx].numpy().reshape(1, -1)
    return None

# القاموس
semantic_dictionary = {
    "عين": {"نبع": "شرب الرجل من عين الماء", "بصر": "أصيبت عين الطفل", "جاسوس": "كان عيناً للعدو"},
    "رأس": {"جسم": "ألم في رأسه", "قائد": "رأس الشركة", "قمة": "رأس الجبل"}
}

# الواجهة
user_sentence = st.text_area("أدخل الجملة العربية للتحليل:")

if st.button("تحليل"):
    found = False
    for word, meanings in semantic_dictionary.items():
        if word in user_sentence:
            found = True
            vec = get_word_vector(user_sentence, word)
            st.write(f"تم تحليل كلمة: {word}")
            # هنا يمكنك إضافة كود حساب التشابه cosine_similarity كما في السابق
            break
    if not found:
        st.warning("الكلمة غير مدعومة في القاموس الحالي.")
