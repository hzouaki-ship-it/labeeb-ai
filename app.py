import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# إعدادات الصفحة
st.set_page_config(
    page_title="منصة لبيب AI - للطالبة هاجر الزوكي",
    page_icon="🧠",
    layout="centered"
)

# حقن كود CSS لقلب اتجاه المنصة بالكامل من اليمين إلى اليسار (RTL) وتنسيق الخطوط
st.markdown("""
    <style>
    /* قلب اتجاه الواجهة بالكامل */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        direction: RTL;
        text-align: right;
    }
    
    /* ضبط صناديق الإدخال والمقاييس لتتحاذى لليمين */
    div[data-testid="stTextArea"] textarea {
        direction: RTL;
        text-align: right;
    }
    div[data-testid="stMetricValue"] {
        text-align: right;
    }
    div[data-testid="stMetricLabel"] {
        text-align: right;
    }
    
    /* تنسيق الجداول لتظهر باتجاه عربي صحيح */
    .stDataFrame table {
        direction: RTL;
        text-align: right;
    }
    
    /* محاذاة التنبيهات ونصوص المعلومات */
    div[data-testid="stAlert"] {
        direction: RTL;
        text-align: right;
    }
    </style>
""", unsafe_allow_html=True)

# تصميم الواجهة العلوية
st.markdown("""
<div style='text-align: center;'>
    <h1 style='color:#7C3AED; margin-bottom: 0;'>🧠 LABEEB AI (لبيب)</h1>
    <h3 style='color:#CBD5E1; margin-top: 5px;'>Arabic Semantic Analyzer</h3>
    <p style='color:#94A3B8; font-size:18px; font-weight: bold;'>“منصة ذكية لتحليل المعنى والسياق في اللغة العربية”</p>
    <p style='color:#7C3AED; font-size:16px; font-weight: bold; margin-top: 15px;'>صُممت هذه المنصة بواسطة الطالبة: هاجر الزوكي</p>
</div>
""", unsafe_allow_html=True)

st.write("---")

# تحميل AraBERT
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("aubmindlab/bert-base-arabertv02")
    model = AutoModel.from_pretrained("aubmindlab/bert-base-arabertv02")
    return tokenizer, model

tokenizer, model = load_model()

# استخراج المتجه الدلالي
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

# إنشاء المتجهات المرجعية
for word in semantic_dictionary:
    for meaning in semantic_dictionary[word]:
        if "vector" not in semantic_dictionary[word][meaning]:
            semantic_dictionary[word][meaning]["vector"] = get_word_vector(
                semantic_dictionary[word][meaning]["النص"],
                word
            )

# إدخل المستخدم
st.subheader("✍️ أدخل الجملة العربية للفحص:")
user_sentence = st.text_area(
    "",
    placeholder="مثال: صليت المغرب في المسجد، أو اجتمع رأس الشركة بالموظفين...",
    height=100
)

# زر التحليل
if st.button("⚡ إطلاق خوارزمية لبيب للتحليل"):
    if user_sentence:
        detected_word = None
        for word in semantic_dictionary:
            if word in user_sentence:
                detected_word = word
                break

        if detected_word:
            st.info(f"🔍 **ذكاء لبيب:** تم اكتشاف الكلمة متعددة المعنى تلقائياً: **{detected_word}**")
            user_vector = get_word_vector(user_sentence, detected_word)
            similarities = []

            if user_vector is not None:
                for meaning in semantic_dictionary[detected_word]:
                    reference_vector = semantic_dictionary[detected_word][meaning]["vector"]
                    if reference_vector is not None:
                        similarity = cosine_similarity(user_vector, reference_vector)[0][0]
                        similarities.append({
                            "المعنى الدلالي": semantic_dictionary[detected_word][meaning]["المعنى"],
                            "نسبة التشابه السياقي": round(float(similarity), 4)
                        })

                if similarities:
                    df = pd.DataFrame(similarities)
                    st.write("### 📊 نتائج التحليل الدلالي الرقمي:")
                    st.dataframe(df, use_container_width=True)

                    best_meaning = max(similarities, key=lambda x: x["نسبة التشابه السياقي"])
                    st.write("---")
                    st.write("### 🎯 القرار الدلالي النهائي لمنصة لبيب:")
                    st.success(f"المعنى المقصود والمكتشف في النص هو: **{best_meaning['المعنى الدلالي']}**")

                    confidence = best_meaning["نسبة التشابه السياقي"] * 100
                    st.metric(label="درجة ثقة النموذج في القرار", value=f"{confidence:.2f}%")

                    # التفسير التحليلي
                    st.write("### 🧠 التفسير التحليلي للسياق:")
                    actual_meaning = best_meaning["المعنى الدلالي"]
                    if actual_meaning == "نبع ماء":
                        st.write("💡 تم اختيار هذا المعنى بسبب ارتباط كلمات النص بسياق الطبيعة أو السوائل والتدفق.")
                    elif actual_meaning == "عضو البصر":
                        st.write("💡 تم اختيار هذا المعنى لاعتماد النص على سياق تشريحي مرتبط بالرؤية أو البكاء.")
                    elif actual_meaning == "جاسوس":
                        st.write("💡 تم اختيار هذا المعنى نظراً لورود سياق أمني مرتبط بالخفاء أو الأعداء.")
                    elif actual_meaning == "صلاة المغرب":
                        st.write("💡 تم اختيار هذا المعنى لوجود مؤشرات سياقية دينية مرتبطة بالعبادات.")
                    elif actual_meaning == "دولة المغرب":
                        st.write("💡 تم اختيار هذا المعنى لبروز سياق جغرافي مكاني مرتبط بالسفر والدول.")
                    elif actual_meaning == "عضو من الجسم":
                        st.write("💡 تم اختيار هذا المعنى لارتباط العبارة بسياق جسدي بيولوجي.")
                    elif actual_meaning == "قائد":
                        st.write("💡 تم اختيار هذا المعنى لوجود سياق مهني وإداري يعبر عن المسؤولية.")
                    elif actual_meaning == "قمة":
                        st.write("💡 تم اختيار هذا المعنى لبروز سياق فيزيائي مرتبط بالارتفاعات والتضاريس.")
            else:
                st.error("خطأ فني: فشل النموذج في استخراج متجهات النص الحالية.")
        else:
            st.warning("تنبيه: الجملة المكتوبة لا تحتوي على أي من كلمات القاموس المدعومة حالياً.")
    else:
        st.warning("فضلاً، يرجى إدخال جملة أولاً ليتمكن النظام من معالجتها.")

st.write("---")
st.markdown("<p style='text-align:center; color:gray; font-size: 13px;'>تم التطوير والبرمجة بواسطة الطالبة: هاجر الزوكي © 2026 | LABEEB AI</p>", unsafe_allow_html=True)
