import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import time

# 1. إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="منصة لبيب LABEEB AI - هاجر الزواكي",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. هندسة الـ CSS المتقدمة لمحاكاة التصميم المطلوب بدقة (ألوان، حواف، بطاقات، وتأثيرات)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&display=swap');

    /* الضبط العام للمنصة والخلفية المريحة */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #F8FAFC !important;
        direction: RTL !important;
        text-align: right !important;
        font-family: 'Cairo', sans-serif !important;
    }
    
    /* تحديد أبعاد الحاوية الرئيسية */
    [data-testid="stMain"] .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 850px !important;
    }

    /* إلغاء الفراغات والحدود الافتراضية من ستريمليت */
    [data-testid="stVerticalBlock"] {
        gap: 0rem !important;
    }

    h1, h2, h3, h4, h5, h6, p, span, label {
        font-family: 'Cairo', sans-serif !important;
    }

    /* ---------------- القسم العلوي (Hero Section) ---------------- */
    .hero-container {
        background: white;
        border-radius: 24px;
        padding: 40px 30px;
        text-align: center !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
        border: 1px solid #EEF2F6;
    }
    
    /* محاكاة النقاط الديكورية الجانبية في التصميم */
    .hero-container::before {
        content: "•••\\A•••\\A•••";
        white-space: pre;
        position: absolute;
        top: 20px;
        left: 25px;
        color: #E2E8F0;
        font-size: 14px;
        letter-spacing: 4px;
        line-height: 1.2;
    }
    .hero-container::after {
        content: "•••\\A•••\\A•••";
        white-space: pre;
        position: absolute;
        bottom: 20px;
        right: 25px;
        color: #E2E8F0;
        font-size: 14px;
        letter-spacing: 4px;
        line-height: 1.2;
    }

    /* الشارة العلوية الصغيرة */
    .top-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background-color: #F5F3FF;
        color: #7C3AED;
        padding: 6px 16px;
        border-radius: 100px;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 20px;
        border: 1px solid #E9E3FF;
    }

    .hero-title {
        font-size: 44px !important;
        font-weight: 800 !important;
        color: #5011CE !important;
        margin: 0px 0px 8px 0px !important;
        line-height: 1.2;
    }
    .hero-subtitle {
        font-size: 18px !important;
        font-weight: 700 !important;
        color: #1E293B !important;
        margin-bottom: 16px !important;
    }
    .hero-description {
        font-size: 15px !important;
        color: #64748B !important;
        max-width: 680px;
        margin: 0 auto 24px auto !important;
        line-height: 1.7;
    }
    .author-badge {
        display: inline-block;
        background: linear-gradient(135deg, #F5F3FF 0%, #F0E9FF 100%);
        color: #6D28D9 !important;
        padding: 8px 20px;
        border-radius: 12px;
        font-size: 14px !important;
        font-weight: 600;
        border: 1px solid #E4D9FF;
    }

    /* ---------------- بطاقات الأقسام (Cards) ---------------- */
    .section-card {
        background: #FFFFFF;
        border: 1px solid #EEF2F6;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.015);
        margin-bottom: 24px;
    }
    
    .section-title-container {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 16px;
        border-bottom: 1px solid #F1F5F9;
        padding-bottom: 12px;
    }
    
    .section-title {
        font-size: 18px !important;
        font-weight: 700 !important;
        color: #1E293B !important;
        margin: 0 !important;
    }

    /* ---------------- مدخلات المستخدم والزر ---------------- */
    .stTextArea textarea {
        background-color: #FAFAFA !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 14px !important;
        padding: 16px !important;
        font-family: 'Cairo', sans-serif !important;
        font-size: 15px !important;
        color: #1E293B !important;
        transition: all 0.2s ease;
    }
    .stTextArea textarea:focus {
        border-color: #7C3AED !important;
        background-color: #FFFFFF !important;
        box-shadow: 0 0 0 4px rgba(124, 58, 237, 0.08) !important;
    }
    
    /* تخصيص الزر البنفسجي الأنيق بنبضة خفيفة */
    div.stButton > button {
        background: #7C3AED !important;
        color: white !important;
        font-family: 'Cairo', sans-serif !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 12px 24px !important;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.2) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        background: #6D28D9 !important;
        box-shadow: 0 6px 16px rgba(124, 58, 237, 0.3) !important;
        transform: translateY(-1px);
    }

    /* ---------------- حالة الانتظار والبطاقة الفارغة ---------------- */
    .empty-state {
        text-align: center;
        padding: 40px 20px;
    }
    .empty-icon {
        font-size: 40px;
        color: #7C3AED;
        background: #F5F3FF;
        width: 70px;
        height: 70px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        margin-bottom: 16px;
    }
    .empty-text {
        color: #4F46E5;
        font-weight: 700;
        font-size: 16px;
        margin-bottom: 6px;
    }
    .empty-subtext {
        color: #64748B;
        font-size: 14px;
    }

    /* ---------------- بطاقات قسم "كيف يعمل لبيب؟" الثلاثية ---------------- */
    .steps-grid {
        display: flex;
        gap: 16px;
        margin-top: 15px;
    }
    .step-card {
        flex: 1;
        background: #FAFAFA;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        position: relative;
    }
    .step-number {
        position: absolute;
        top: -12px;
        left: 20px;
        background: #7C3AED;
        color: white;
        width: 26px;
        height: 26px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: 700;
        box-shadow: 0 2px 8px rgba(124, 58, 237, 0.3);
    }
    .step-icon {
        font-size: 24px;
        margin-bottom: 10px;
        background: white;
        width: 50px;
        height: 50px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border-radius: 12px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    }
    .step-title {
        font-weight: 700;
        color: #4F46E5;
        font-size: 15px;
        margin-bottom: 8px;
    }
    .step-desc {
        color: #64748B;
        font-size: 13px;
        line-height: 1.6;
    }

    /* ---------------- جداول استعراض البيانات ---------------- */
    .stTable, table {
        width: 100% !important;
        border-collapse: collapse;
        margin-top: 10px;
    }
    th {
        background-color: #F8FAFC !important;
        color: #475569 !important;
        font-weight: 600 !important;
        padding: 10px !important;
        border-bottom: 2px solid #E2E8F0 !important;
    }
    td {
        padding: 10px !important;
        border-bottom: 1px solid #E2E8F0 !important;
        color: #334155 !important;
    }

    /* ---------------- تذييل الصفحة الأكاديمي ---------------- */
    .footer-text {
        text-align: center !important;
        margin-top: 40px;
        padding: 20px 0;
        color: #94A3B8 !important;
        font-size: 13px !important;
        border-top: 1px solid #E2E8F0;
    }
    
    /* استجابة الشاشات الصغيرة لبطاقات الخطوات */
    @media (max-width: 768px) {
        .steps-grid {
            flex-direction: column;
            gap: 20px;
        }
        .step-number {
            left: auto;
            right: 20px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# 3. عرض قسم الـ Hero الاحترافي بمحاكاة بصرية كاملة للتصميم المستهدف
st.markdown("""
<div class="hero-container">
    <div class="top-badge">✦ منصة ذكية عربية</div>
    <h1 class="hero-title">LABEEB AI (لبيب)</h1>
    <div class="hero-subtitle">المحلل الدلالي الذكي لفهم المعنى والسياق في اللغة العربية</div>
    <p class="hero-description">
        منصة تعتمد على الذكاء الاصطناعي لفهم السياق اللغوي واكتشاف المعنى الصحيح للكلمات من خلال تحليل دلالي عميق ودقيق.
    </p>
    <div class="author-badge">تصميم وتطوير: هاجر الزواكي © 2026</div>
</div>
""", unsafe_allow_html=True)

# 4. محرك وتحميل أوزان نموذج الخوارزمية (AraBERT) في الذاكرة التخزينية المؤقتة
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

# القاموس الدلالي المرجعي الأساسي للمنصة
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

# بناء وبث المتجهات السياقية الثابتة للقاموس
for word in semantic_dictionary:
    for meaning in semantic_dictionary[word]:
        if "vector" not in semantic_dictionary[word][meaning]:
            semantic_dictionary[word][meaning]["vector"] = get_word_vector(
                semantic_dictionary[word][meaning]["النص"], word
            )

# 5. بطاقة منطقة مدخلات فحص الجمل العربية
st.markdown("""
<div class="section-card">
    <div class="section-title-container">
        <span style="font-size: 18px;">✍️</span>
        <h3 class="section-title">أدخل الجملة العربية للتحليل:</h3>
    </div>
""", unsafe_allow_html=True)

user_sentence = st.text_area(
    "",
    placeholder="اكتب جملة عربية واضحة تحتوي على المعنى والسياق...",
    height=100,
    label_visibility="collapsed"
)

st.write("") # فاصل جمالي خفيف
analysis_triggered = st.button("⚡ إطلاق خوارزمية لبيب للتحليل")

st.markdown("</div>", unsafe_allow_html=True) # إغلاق بطاقة الإدخال

# 6. بطاقة ديناميكية موحدة لعرض نتائج التحليل والقرارات
st.markdown("""
<div class="section-card">
    <div class="section-title-container">
        <span style="font-size: 18px;">📊</span>
        <h3 class="section-title">نتيجة التحليل</h3>
    </div>
""", unsafe_allow_html=True)

if analysis_triggered:
    if user_sentence.strip():
        detected_word = None
        for word in semantic_dictionary:
            if word in user_sentence:
                detected_word = word
                break
        
        if detected_word:
            with st.spinner("⏳ يقوم لبيب بقراءة المؤشرات السياقية عبر نموذج AraBERT اللغوي..."):
                time.sleep(1.0)
                user_vector = get_word_vector(user_sentence, detected_word)
                
                if user_vector is not None:
                    similarities = []
                    for meaning in semantic_dictionary[detected_word]:
                        ref_vector = semantic_dictionary[detected_word][meaning]["vector"]
                        if ref_vector is not None:
                            sim = cosine_similarity(user_vector, ref_vector)[0][0]
                            similarities.append({
                                "المعنى الدلالي": semantic_dictionary[detected_word][meaning]["المعنى"],
                                "نسبة التشابه السياقي": round(float(sim), 4)
                            })
                    
                    similarities = sorted(similarities, key=lambda x: x["نسبة التشابه السياقي"], reverse=True)
                    best_meaning = similarities[0]["المعنى الدلالي"]
                    confidence_percentage = round(similarities[0]["نسبة التشابه السياقي"] * 100, 2)
                    
                    # طباعة القرار الدلالي النهائي بشكل منظم وجذاب
                    st.markdown(f"""
                        <p style="font-size: 16px; color: #1E293B; margin-bottom: 8px;">
                            الكلمة التي تم رصدها وتحليلها تلقائياً: <strong style="color:#7C3AED;">{detected_word}</strong>
                        </p>
                        <div style="background-color: #F0FDF4; border: 1px solid #DCFCE7; padding: 16px; border-radius: 12px; margin: 15px 0;">
                            <span style="font-size: 18px; font-weight: 700; color: #15803D;">🎯 القرار النهائي الخوارزمي:</span>
                            <p style="font-size: 18px; font-weight: 700; color: #16A34A; margin: 6px 0 0 0 !important;">
                                المعنى المقصود والمكتشف في النص هو: ({best_meaning})
                            </p>
                        </div>
                        <p style="font-size: 15px; color: #475569; margin-bottom: 20px;">
                            درجة ثقة الخوارزمية في القرار الحالي: <strong style="color: #7C3AED;">{confidence_percentage}%</strong>
                        </p>
                        <p style="font-weight: 700; font-size: 14px; color: #1E293B; margin-bottom: 6px;">📊 جدول معاملات التشابه الجيب تمامي (Cosine Similarity):</p>
                    """, unsafe_allow_html=True)
                    
                    # عرض جدول التشابه
                    display_df = pd.DataFrame(similarities)
                    display_df["نسبة التشابه السياقي"] = display_df["نسبة التشابه السياقي"].apply(lambda x: f"{round(x*100, 2)}%")
                    st.table(display_df)
                else:
                    st.error("عذراً، واجه النظام خطأ غير متوقع أثناء استخراج متجهات الكلمة المستهدفة.")
        else:
            st.warning("⚠️ لم يتم العثور في النص على أي من الكلمات المشتركة المدعومة حالياً بالقاموس المرجعي (عين، المغرب، رأس).")
    else:
        st.warning("⚠️ فضلاً، يرجى كتابة جملة عربية أولاً ليتمكن لبيب من معالجتها وفحص سياقها الدلالي.")
else:
    # شاشة الحالة الافتراضية "لم يتم إجراء أي تحليل بعد" لمطابقة التصميم المستهدف
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">📄</div>
        <div class="empty-text">لم يتم إجراء أي تحليل بعد</div>
        <div class="empty-subtext">اكتب جملة عربية واضغط على زر التحليل للحصول على النتيجة.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True) # إغلاق بطاقة النتائج

# 7. قسم "كيف يعمل لبيب؟" - معالجة كاملة وحقن آمن لشبكة البطاقات الثلاثية المدعومة بالـ CSS
st.markdown("""
<div class="section-card">
    <div class="section-title-container">
        <span style="font-size: 18px;">🧠</span>
        <h3 class="section-title">كيف يعمل لبيب؟</h3>
    </div>
    <p style="font-size: 14px; color: #64748B; margin-bottom: 15px;">يستخدم لبيب الذكاء الاصطناعي لتحليل النصوص العربية وفهم معناها الحقيقي في السياق عبر ثلاث خطوات متكاملة:</p>
    
    <div class="steps-grid">
        <div class="step-card">
            <div class="step-number">1</div>
            <div class="step-icon">🔍</div>
            <div class="step-title">تحليل السياق</div>
            <div class="step-desc">يحلل لبيب الجملة والكلمات المحيطة لفهم السياق اللغوي بدقة متناهية.</div>
        </div>
        
        <div class="step-card">
            <div class="step-number">2</div>
            <div class="step-icon">🎯</div>
            <div class="step-title">اكتشاف المعنى</div>
            <div class="step-desc">يحدد المعنى الأقرب اعتماداً على السياق والدلالة اللغوية المخزنة.</div>
        </div>
        
        <div class="step-card">
            <div class="step-number">3</div>
            <div class="step-icon">📊</div>
            <div class="step-title">قياس التشابه الدلالي</div>
            <div class="step-desc">يستخدم نماذج لغوية متقدمة لقياس التشابه الدلالي وتصنيف النتائج بدقة.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 8. تذييل المنصة (Footer الحماية الأكاديمية)
st.markdown("""
<div class="footer-text">
    تم تطوير وتصميم منصة LABEEB AI بواسطة الطالبة هاجر الزواكي © 2026<br>
    جميع الحقوق محفوظة
</div>
""", unsafe_allow_html=True)
