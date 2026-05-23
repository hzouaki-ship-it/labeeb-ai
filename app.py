import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import time

# 1. إعدادات الصفحة الأساسية وتحميل الخطوط
st.set_page_config(
    page_title="منصة لبيب LABEEB AI - هاجر الزواكي",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. حقن هندسة الـ CSS المتقدمة للواجهة الفاتحة العصرية (RTL)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&display=swap');

    /* تصفير التنسيقات الافتراضية وضبط الخلفية العامة والخط */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #FAFAFA !important;
        direction: RTL !important;
        text-align: right !important;
        font-family: 'Cairo', sans-serif !important;
    }
    
    /* ضبط الحاوية الرئيسية للمنصة لتشابه الأنظمة الذكية */
    [data-testid="stMain"] .block-container {
        padding-top: 3rem !important;
        padding-bottom: 3rem !important;
        max-width: 800px !important;
    }

    /* تخصيص النصوص والعناوين الشاملة */
    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown {
        font-family: 'Cairo', sans-serif !important;
        text-align: right !important;
        color: #1E293B !important;
    }

    /* تصميم قسم الـ Hero بتأثير التدرج اللوني الفاخر (Gradient) */
    .hero-section {
        background: linear-gradient(135deg, #F5F3FF 0%, #EFF6FF 100%);
        border: 1px solid #E4E4E7;
        border-radius: 24px;
        padding: 40px;
        text-align: center !important;
        box-shadow: 0 10px 25px -5px rgba(124, 58, 237, 0.05);
        margin-bottom: 40px;
    }
    .hero-section h1 {
        text-align: center !important;
        font-weight: 800 !important;
        font-size: 42px !important;
        background: linear-gradient(90deg, #7C3AED, #4F46E5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .hero-section h3 {
        text-align: center !important;
        color: #475569 !important;
        font-weight: 600 !important;
        font-size: 20px !important;
        margin-bottom: 15px;
    }
    .hero-section p {
        text-align: center !important;
        color: #64748B !important;
        font-size: 16px !important;
        max-width: 600px;
        margin: 0 auto !important;
    }
    .hero-badge {
        display: inline-block;
        background-color: #7C3AED;
        color: white !important;
        padding: 4px 16px;
        border-radius: 100px;
        font-size: 13px !important;
        font-weight: 600;
        margin-top: 15px;
    }

    /* تحسين وتصميم مربع إدخال النص العريض الاحترافي */
    .stTextArea textarea {
        background-color: #FFFFFF !important;
        border: 1px solid #E4E4E7 !important;
        border-radius: 16px !important;
        padding: 18px !important;
        font-family: 'Cairo', sans-serif !important;
        font-size: 16px !important;
        color: #0F172A !important;
        direction: RTL !important;
        text-align: right !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02) !important;
        transition: all 0.25s ease-in-out !important;
    }
    .stTextArea textarea:focus {
        border-color: #7C3AED !important;
        box-shadow: 0 0 0 4px rgba(124, 58, 237, 0.15) !important;
    }

    /* إعادة صياغة زر إطلاق الخوارزمية (النبض والتأثيرات) */
    div.stButton > button {
        background: linear-gradient(90deg, #7C3AED, #6D28D9) !important;
        color: white !important;
        font-family: 'Cairo', sans-serif !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        border-radius: 14px !important;
        border: none !important;
        padding: 14px 28px !important;
        width: 100% !important;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.25) !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        background: linear-gradient(90deg, #6D28D9, #5B21B6) !important;
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4) !important;
        transform: translateY(-1px);
    }
    div.stButton > button:active {
        transform: translateY(1px);
    }

    /* بطاقة عرض النتائج الذكية (Result Card) */
    .result-card {
        background: #FFFFFF;
        border: 1px solid #E4E4E7;
        border-radius: 20px;
        padding: 25px;
        margin-top: 30px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.02);
    }
    .result-header {
        font-size: 18px;
        font-weight: 700;
        color: #7C3AED;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* تصميم قسم "كيف يعمل لبيب؟" */
    .how-it-works-section {
        background-color: #FFFFFF;
        border: 1px solid #E4E4E7;
        border-radius: 20px;
        padding: 30px;
        margin-top: 40px;
    }
    .how-title {
        font-size: 20px;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 20px;
        border-bottom: 2px solid #F4F4F5;
        padding-bottom: 10px;
    }
    .step-card {
        padding: 15px 0;
        border-bottom: 1px dashed #F4F4F5;
    }
    .step-card:last-child {
        border-bottom: none;
    }
    .step-title {
        font-weight: 600;
        color: #4F46E5;
        font-size: 16px;
        margin-bottom: 5px;
    }
    .step-desc {
        color: #64748B;
        font-size: 14px;
        line-height: 1.6;
    }

    /* تذييل الصفحة الأكاديمي الاحترافي */
    .footer-section {
        text-align: center !important;
        margin-top: 60px;
        padding-top: 20px;
        border-top: 1px solid #E4E4E7;
        color: #94A3B8 !important;
        font-size: 13px !important;
    }
    
    /* تنسيق الجداول لتطابق المظهر العصري */
    .stTable, table {
        direction: RTL !important;
        width: 100% !important;
        border-collapse: collapse;
        margin-top: 15px;
    }
    th {
        background-color: #F8FAFC !important;
        color: #475569 !important;
        font-weight: 600 !important;
        padding: 12px !important;
        border-bottom: 2px solid #E2E8F0 !important;
    }
    td {
        padding: 12px !important;
        border-bottom: 1px solid #E2E8F0 !important;
        color: #334155 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. عرض قسم الـ Hero الاحترافي
st.markdown("""
<div class="hero-section">
    <h1>🧠 LABEEB AI (لبيب)</h1>
    <h3>المحلل الدلالي الرقمي للغة العربية</h3>
    <p>منصة أكاديمية ذكية تعتمد على نماذج التعلم العميق المتقدمة (AraBERT) لتحليل السياقات اللغوية، وتفكيك البنى التركيبية، وحل مشكلات المشترك اللفظي والغموض الدلالي آلياً بدقة متناهية.</p>
    <div class="hero-badge">المطورة: هاجر الزواكي © 2026</div>
</div>
""", unsafe_allow_html=True)

# 4. محرك وحقن خوارزميات الذكاء الاصطناعي (AraBERT)
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

# القاموس الدلالي المرجعي للمنصة
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

# توليد المتجهات الدلالية الثابتة للقاموس
for word in semantic_dictionary:
    for meaning in semantic_dictionary[word]:
        if "vector" not in semantic_dictionary[word][meaning]:
            semantic_dictionary[word][meaning]["vector"] = get_word_vector(
                semantic_dictionary[word][meaning]["النص"], word
            )

# 5. منطقة مدخلات المستخدم (Minimalist Input Area)
st.markdown("<p style='font-weight: 600; font-size: 16px; margin-bottom: 8px;'>✍️ أدخل النص العربي المراد فحص دلالته السياقية:</p>", unsafe_allow_html=True)
user_sentence = st.text_area(
    "",
    placeholder="اكتبي جملة تحتوي على إحدى الكلمات المشتركة (عين، المغرب، رأس)... مثال: صليت المغرب في المسجد الحرام.",
    height=110,
    label_visibility="collapsed"
)

# مساحة تفصل المكونات بشكل ناعم
st.write("")

# 6. زر المعالجة والتحليل الدلالي الرقمي
if st.button("⚡ إطلاق خوارزمية لبيب للتحليل"):
    if user_sentence.strip():
        detected_word = None
        for word in semantic_dictionary:
            if word in user_sentence:
                detected_word = word
                break
        
        if detected_word:
            # إظهار خط التحميل الاحترافي لمحاكاة الأنظمة الذكية
            with st.spinner("⏳ لبيب يقوم بقراءة النص واستخراج المؤشرات السياقية عبر AraBERT..."):
                time.sleep(1.2) # تأخير طفيف لإعطاء جمالية للمنصة
                user_vector = get_word_vector(user_sentence, detected_word)
                
                if user_vector is not None:
                    similarities = []
                    for meaning in semantic_dictionary[detected_word]:
                        ref_vector = semantic_dictionary[detected_word][meaning]["vector"]
                        if ref_vector is not None:
                            sim = cosine_similarity(user_vector, ref_vector)[0][0]
                            similarities.append({
                                "المعنى الدلالي الدقيق": semantic_dictionary[detected_word][meaning]["المعنى"],
                                "نسبة المطابقة السياقية": round(float(sim), 4)
                            })
                    
                    # فرز النتائج التنازلية حسب القوة السياقية
                    similarities = sorted(similarities, key=lambda x: x["نسبة المطابقة السياقية"], reverse=True)
                    
                    # بناء وتجهيز الـ Result Card
                    best_meaning = similarities[0]["المعنى الدلالي الدقيق"]
                    confidence_percentage = round(similarities[0]["نسبة المطابقة السياقية"] * 100, 2)
                    
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="result-header">🎯 القرار الدلالي النهائي لمنصة لبيب</div>
                        <p style="font-size: 16px; color: #334155;">
                            الكلمة التي تم رصدها وتحليلها: <strong style="color:#7C3AED;">{detected_word}</strong>
                        </p>
                        <p style="font-size: 20px; font-weight: 700; color: #16A34A; margin: 15px 0 !important;">
                            🔍 المعنى المقصود والمكتشف في سياقكِ هو: ({best_meaning})
                        </p>
                        <p style="font-size: 15px; color: #475569;">
                            درجة ثقة الخوارزمية في القرار: <strong>{confidence_percentage}%</strong>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # عرض الجدول الإحصائي المقارن أسفل البطاقة
                    st.write("")
                    st.markdown("<p style='font-weight: 600; font-size: 15px; margin-top: 15px;'>📊 جدول معاملات التشابه الجيب تمامي (Cosine Similarity):</p>", unsafe_allow_html=True)
                    
                    # تحويل الأرقام إلى نسب مئوية مفهومة للعرض في الجدول
                    display_df = pd.DataFrame(similarities)
                    display_df["نسبة المطابقة السياقية"] = display_df["نسبة المطابقة السياقية"].apply(lambda x: f"{round(x*100, 2)}%")
                    st.table(display_df)
                else:
                    st.error("عذراً، واجه النموذج مشكلة فنية أثناء استخراج الأوزان السياقية للكلمة.")
        else:
            st.warning("⚠️ لم يتم العثور في النص على أي من الكلمات المشتركة المدعومة حالياً بالقاموس المرجعي (عين، المغرب، رأس).")
    else:
        st.warning("⚠️ فضلاً، يرجى كتابة جملة عربية داخل صندوق الإدخال ليتمكن لبيب من معالجتها.")

# 7. قسم "كيف يعمل لبيب؟" (How it works Section)
st.markdown("""
<div class="how-it-works-section">
    <div class="how-title">🧠 كيف تعمل بنية لبيب الخوارزمية؟</div>
    
    <div class="step-card">
        <div class="step-title">1. استخراج المتجهات السياقية (Contextual Embedding)</div>
        <div class="step-desc">لا يعتمد لبيب على المعاني المعجمية الجامدة، بل يقوم بتمرير الجملة كاملة إلى نموذج AraBERT لإنشاء تمثيل رقمي يراعي الكلمات المحيطة والقرائن اللغوية الحالية.</div>
    </div>
    
    <div class="step-card">
        <div class="step-title">2. اكتشاف مواطن الغموض والمشترك اللفظي</div>
        <div class="step-desc">يتم رصد اللفظة المشتركة آلياً وفصل متجهها الدلالي الخاص بها من الطبقات الخفية الأخيرة (Last Hidden States) للنموذج اللغوي.</div>
    </div>
    
    <div class="step-card">
        <div class="step-title">3. قياس التشابه الدلالي (Cosine Similarity)</div>
        <div class="step-desc">تجري المنصة حسابات رياضية دقيقة لمقارنة زاوية متجه الكلمة المدخلة مع متجهات المعاني المرجعية المخزنة مسبقاً، واختيار النسبة الأعلى لتكون هي المعنى الدقيق والنهائي.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# 8. تذييل المنصة (Academic Footer)
st.markdown("""
<div class="footer-section">
    تم تطوير وتصميم منصة LABEEB AI بواسطة الطالبة الباحثة: <strong>هاجر الزواكي</strong><br>
    سنة ثانية ماستر "اللسانيات الرقمية والعربية" | جامعة مولاي إسماعيل - مكناس © 2026
</div>
""", unsafe_allow_html=True)
