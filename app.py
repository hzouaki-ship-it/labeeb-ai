import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="منصة لبيب AI - هاجر الزوكي",
    page_icon="🧠",
    layout="centered"
)

# 2. حقن CSS متطور (للثيم الفاتح، الخط العربي Tajawal، والمحاذاة الشاملة)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700&display=swap');

    /* تطبيق الخط والاتجاه والخلفية الفاتحة على كامل التطبيق */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #F8FAFC !important;
        direction: RTL !important;
        text-align: right !important;
        font-family: 'Tajawal', sans-serif !important;
    }

    /* تنسيق كافة العناوين والنصوص */
    h1, h2, h3, h4, p, span, label, .stMarkdown {
        font-family: 'Tajawal', sans-serif !important;
        color: #1E293B !important;
        text-align: right !important;
    }

    /* تنسيق صندوق إدخال النص */
    .stTextArea textarea {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        font-family: 'Tajawal', sans-serif !important;
        font-size: 16px !important;
        color: #0F172A !important;
        direction: RTL !important;
        text-align: right !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }

    /* تنسيق زر التحليل */
    div.stButton > button {
        background-color: #7C3AED !important;
        color: white !important;
        font-family: 'Tajawal', sans-serif !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 0.5rem 2rem !important;
        width: 100% !important;
        transition: 0.3s !important;
    }
    div.stButton > button:hover {
        background-color: #6D28D9 !important;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }

    /* تنسيق الجداول لتناسب الثيم الفاتح */
    .stDataFrame {
        background-color: white !important;
        border-radius: 10px !important;
        padding: 10px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    /* تنسيق صندوق التعريف الشخصي في الأسفل */
    .bio-box {
        background-color: #F1F5F9;
        border-right: 5px solid #7C3AED;
        padding: 20px;
        border-radius: 8px;
        margin-top: 40px;
        font-size: 15px;
        line-height: 1.8;
        color: #334155;
    }
    </style>
""", unsafe_allow_html=True)

# 3. ترويسة المنصة (Header)
st.markdown("""
<div style='text-align: center; direction: RTL;'>
    <h1 style='color:#7C3AED !important; font-size: 45px; margin-bottom: 0;'>🧠 LABEEB AI (لبيب)</h1>
    <h3 style='color:#64748B !important; margin-top: 5px; font-weight: 500;'>المحلل الدلالي الرقمي العربي</h3>
    <p style='color:#7C3AED !important; font-size: 18px; font-weight: 500;'>“منصة ذكية مدعومة بالذكاء الاصطناعي لفهم سياق اللغة العربية”</p>
</div>
""", unsafe_allow_html=True)

st.write("---")

# 4. محرك الذكاء الاصطناعي (AraBERT)
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("aubmindlab/bert-base-arabertv02")
    model = AutoModel.from_pretrained("aubmindlab/bert-base-arabertv02")
    return tokenizer, model

tokenizer, model = load_model()

def get_word_vector(sentence, target_word):
    inputs = tokenizer(sentence, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state[0]
    tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
    for idx, token in enumerate(tokens):
        if target_word in token:
            return embeddings[idx].numpy().reshape(1, -1)
    return None

# القاموس الدلالي المطور
semantic_dictionary = {
    "عين": {
        "المعنى1": {"النص": "شرب الرجل من عين الماء العذبة", "المعنى": "نبع ماء"},
        "المعنى2": {"النص": "أصيبت عين الطفل و نزلت دموعه", "المعنى": "عضو البصر"},
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

# حساب المتجهات المرجعية
for word in semantic_dictionary:
    for meaning in semantic_dictionary[word]:
        if "vector" not in semantic_dictionary[word][meaning]:
            semantic_dictionary[word][meaning]["vector"] = get_word_vector(
                semantic_dictionary[word][meaning]["النص"], word
            )

# 5. منطقة التفاعل
st.markdown("<h4 style='margin-bottom:10px;'>✍️ أدخل الجملة المراد تحليلها:</h4>", unsafe_allow_html=True)
user_sentence = st.text_area("", placeholder="مثال: ذهبت لصلاة المغرب... أو: شربت من عين الماء...", height=100)

if st.button("⚡ إطلاق خوارزمية لبيب للتحليل"):
    if user_sentence:
        detected_word = None
        for word in semantic_dictionary:
            if word in user_sentence:
                detected_word = word
                break
        
        if detected_word:
            st.info(f"✅ **تم اكتشاف الكلمة:** ({detected_word})")
            user_vector = get_word_vector(user_sentence, detected_word)
            
            if user_vector is not None:
                similarities = []
                for meaning in semantic_dictionary[detected_word]:
                    ref_vector = semantic_dictionary[detected_word][meaning]["vector"]
                    if ref_vector is not None:
                        sim = cosine_similarity(user_vector, ref_vector)[0][0]
                        similarities.append({
                            "المعنى الدلالي": semantic_dictionary[detected_word][meaning]["المعنى"],
                            "نسبة القوة السياقية": f"{round(float(sim)*100, 2)}%"
                        })
                
                # عرض النتائج
                st.write("### 📊 نتائج التحليل الدلالي:")
                st.table(pd.DataFrame(similarities))
                
                # القرار النهائي
                best_meaning = max(similarities, key=lambda x: x["نسبة القوة السياقية"])
                st.success(f"🎯 **القرار الدلالي النهائي:** المعنى المقصود في نصّك هو **({best_meaning['المعنى الدلالي']})**")
            else:
                st.error("فشل النموذج في معالجة سياق هذه الجملة.")
        else:
            st.warning("هذه الجملة لا تحتوي على كلمات غامضة مدعومة حالياً.")
    else:
        st.warning("برجاء إدخال نص أولاً.")

# 6. النبذة التعريفية الأكاديمية (الخاتمة)
st.markdown("---")
st.markdown("""
<div class="bio-box">
    <strong>💡 نبذة عن المشروع:</strong><br>
    هذه المنصة هي نتاج عمل بحثي وبرمجي للطالبة: <strong>هاجر الزوكي</strong>، طالبة بالسنة الثانية ماجستير في تخصص <strong>اللسانيات الرقمية والعربية</strong> بجامعة مولاي إسماعيل - كلية الآداب والعلوم الإنسانية، بمكناس.
    <br><br>
    يندرج هذا التطبيق الذكي ضمن متطلبات <strong>مشروع التخرج</strong>، ويهدف إلى تسخير تقنيات التعلم العميق (Deep Learning) لحل مشكلة المشترك اللفظي والغموض الدلالي في النصوص العربية آلياً.
</div>
""", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#94A3B8; font-size: 12px; margin-top:20px;'>حقوق البرمجة محفوظة © 2026 | LABEEB AI - جامعة مولاي إسماعيل</p>", unsafe_allow_html=True)
