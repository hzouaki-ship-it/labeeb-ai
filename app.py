import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import time

# 1. إعدادات الصفحة الأساسية لواجهة المنصة والأبعاد
st.set_page_config(
    page_title="منصة لبيب LABEEB AI",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. حقن التنسيقات العربية وتأمين بيئة التصميم الشاملة (RTL) دون استخدام النصوص البرمجية المتداخلة الحساسة
st.markdown(
    '<style>'
    '@import url("https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&display=swap");'
    'html, body, [data-testid="stAppViewContainer"], .stApp {'
    '    background-color: #F9FAFB !important;'
    '    direction: rtl !important;'
    '    text-align: right !important;'
    '    font-family: "Cairo", sans-serif !important;'
    '}'
    '[data-testid="stMain"] .block-container {'
    '    padding-top: 2rem !important;'
    '    padding-bottom: 3rem !important;'
    '    max-width: 850px !important;'
    '}'
    'h1, h2, h3, h4, h5, h6, p, span, label, table, th, td {'
    '    font-family: "Cairo", sans-serif !important;'
    '    text-align: right !important;'
    '    direction: rtl !important;'
    '}'
    '.hero-wrapper {'
    '    display: flex !important;'
    '    flex-direction: column !important;'
    '    align-items: center !important;'
    '    justify-content: center !important;'
    '    text-align: center !important;'
    '    padding: 10px 0 !important;'
    '    width: 100% !important;'
    '}'
    '.top-badge {'
    '    display: inline-flex !important;'
    '    background-color: #FFFFFF !important;'
    '    color: #6366F1 !important;'
    '    padding: 4px 16px !important;'
    '    border-radius: 100px !important;'
    '    font-size: 13px !important;'
    '    font-weight: 600 !important;'
    '    margin-bottom: 20px !important;'
    '    box-shadow: 0 2px 6px rgba(99, 102, 241, 0.08) !important;'
    '}'
    '.hero-title {'
    '    font-size: 36px !important;'
    '    font-weight: 800 !important;'
    '    color: #4C1D95 !important;'
    '    margin: 15px 0 5px 0 !important;'
    '    line-height: 1.2 !important;'
    '    text-align: center !important;'
    '    width: 100% !important;'
    '}'
    '.hero-subtitle {'
    '    font-size: 18px !important;'
    '    font-weight: 700 !important;'
    '    color: #1E293B !important;'
    '    margin: 10px 0 !important;'
    '    text-align: center !important;'
    '    width: 100% !important;'
    '}'
    '.hero-description {'
    '    font-size: 15px !important;'
    '    color: #64748B !important;'
    '    max-width: 650px !important;'
    '    margin: 0 auto 20px auto !important;'
    '    line-height: 1.7 !important;'
    '    text-align: center !important;'
    '}'
    '.author-badge {'
    '    display: inline-block !important;'
    '    background: #F3E8FF !important;'
    '    color: #6B21A8 !important;'
    '    padding: 6px 20px !important;'
    '    border-radius: 100px !important;'
    '    font-size: 13px !important;'
    '    font-weight: 600 !important;'
    '    border: 1px solid #E9D5FF !important;'
    '    margin-top: 5px !important;'
    '}'
    '.section-card {'
    '    background: #FFFFFF !important;'
    '    border: 1px solid #F1F5F9 !important;'
    '    border-radius: 24px !important;'
    '    padding: 35px !important;'
    '    box-shadow: 0 4px 25px rgba(0, 0, 0, 0.015) !important;'
    '    margin-top: 25px !important;'
    '    margin-bottom: 25px !important;'
    '    text-align: right !important;'
    '}'
    '.card-title-container {'
    '    display: flex !important;'
    '    align-items: center !important;'
    '    justify-content: flex-start !important;'
    '    gap: 8px !important;'
    '    margin-bottom: 20px !important;'
    '}'
    '.card-title-text {'
    '    font-size: 16px !important;'
    '    font-weight: 700 !important;'
    '    color: #1E293B !important;'
    '    margin: 0 !important;'
    '}'
    '.stTextArea textarea {'
    '    background-color: #FFFFFF !important;'
    '    border: 1px solid #E2E8F0 !important;'
    '    border-radius: 16px !important;'
    '    padding: 18px !important;'
    '    font-family: "Cairo", sans-serif !important;'
    '    font-size: 14.5px !important;'
    '    color: #334155 !important;'
    '    text-align: right !important;'
    '    direction: rtl !important;'
    '}'
    'div.stButton > button {'
    '    background: #6D28D9 !important;'
    '    color: white !important;'
    '    font-family: "Cairo", sans-serif !important;'
    '    font-weight: 600 !important;'
    '    font-size: 14.5px !important;'
    '    border-radius: 12px !important;'
    '    border: none !important;'
    '    padding: 10px 24px !important;'
    '    box-shadow: 0 4px 12px rgba(109, 40, 217, 0.25) !important;'
    '    width: 100% !important;'
    '}'
    '.inner-dashed-box {'
    '    border: 1px dashed #E2E8F0 !important;'
    '    border-radius: 16px !important;'
    '    padding: 40px 20px !important;'
    '    text-align: center !important;'
    '    background: #FAFAFA !important;'
    '}'
    '.empty-icon-box {'
    '    font-size: 36px !important;'
    '    color: #6D28D9 !important;'
    '    background: #F3E8FF !important;'
    '    width: 64px !important;'
    '    height: 64px !important;'
    '    display: inline-flex !important;'
    '    align-items: center !important;'
    '    justify-content: center !important;'
    '    border-radius: 16px !important;'
    '    margin-bottom: 16px !important;'
    '}'
    '.empty-main-text {'
    '    color: #6D28D9 !important;'
    '    font-weight: 700 !important;'
    '    font-size: 16px !important;'
    '    margin-bottom: 6px !important;'
    '    text-align: center !important;'
    '}'
    '.empty-sub-text {'
    '    color: #94A3B8 !important;'
    '    font-size: 13.5px !important;'
    '    text-align: center !important;'
    '}'
    '.steps-section-title {'
    '    text-align: center !important;'
    '    font-size: 18px !important;'
    '    font-weight: 700 !important;'
    '    color: #1E293B !important;'
    '    margin-top: 40px !important;'
    '    margin-bottom: 6px !important;'
    '}'
    '.steps-section-desc {'
    '    text-align: center !important;'
    '    font-size: 14px !important;'
    '    color: #64748B !important;'
    '    margin-bottom: 25px !important;'
    '}'
    '.step-item-horizontal {'
    '    background: #FFFFFF !important;'
    '    border: 1px solid #F1F5F9 !important;'
    '    border-radius: 20px !important;'
    '    padding: 24px 20px !important;'
    '    text-align: center !important;'
    '    position: relative !important;'
    '    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.01) !important;'
    '    height: 100% !important;'
    '}'
    '.step-badge-num-right {'
    '    position: absolute !important;'
    '    top: -12px !important;'
    '    right: 20px !important;'
    '    background: #6D28D9 !important;'
    '    color: white !important;'
    '    width: 24px !important;'
    '    height: 24px !important;'
    '    border-radius: 50% !important;'
    '    display: flex !important;'
    '    align-items: center !important;'
    '    justify-content: center !important;'
    '    font-size: 12px !important;'
    '    font-weight: 700 !important;'
    '}'
    '.step-icon-wrapper-center {'
    '    font-size: 22px !important;'
    '    margin-bottom: 12px !important;'
    '    background: #F8FAFC !important;'
    '    width: 48px !important;'
    '    height: 48px !important;'
    '    display: inline-flex !important;'
    '    align-items: center !important;'
    '    justify-content: center !important;'
    '    border-radius: 50% !important;'
    '}'
    '.step-item-title-center {'
    '    font-weight: 700 !important;'
    '    color: #4338CA !important;'
    '    font-size: 14.5px !important;'
    '    margin-bottom: 8px !important;'
    '    text-align: center !important;'
    '}'
    '.step-item-desc-center {'
    '    color: #64748B !important;'
    '    font-size: 13px !important;'
    '    line-height: 1.6 !important;'
    '    text-align: center !important;'
    '}'
    '.footer-container {'
    '    text-align: center !important;'
    '    margin-top: 45px !important;'
    '    padding-top: 20px !important;'
    '    color: #94A3B8 !important;'
    '    font-size: 13px !important;'
    '    border-top: 1px solid #E2E8F0 !important;'
    '}'
    '</style>',
    unsafe_allow_html=True
)

# 3. عرض ترويسة الواجهة (Hero Section) المحدثة بدون علامات اقتباس ثلاثية لمنع الـ SyntaxError نهائياً
st.markdown('<div class="hero-wrapper">', unsafe_allow_html=True)
st.markdown('<div class="top-badge">✦ منصة ذكية عربية</div>', unsafe_allow_html=True)

# حقن كود الـ SVG الخاص بالشعار بأمان كامل داخل أسطر مقتبسة بسيطة ومفردة
svg_code = (
    '<svg width="135" height="135" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg" style="display: block; margin: 0 auto;">'
    '<defs>'
    '<linearGradient id="labeebGrad" x1="40" y1="40" x2="160" y2="160" gradientUnits="userSpaceOnUse">'
    '<stop offset="0%" stop-color="#4C1D95"/>'
    '<stop offset="50%" stop-color="#7C3AED"/>'
    '<stop offset="100%" stop-color="#2563EB"/>'
    '</linearGradient>'
    '</defs>'
    '<path d="M115 70L150 45M115 70L155 95M150 45L185 70M155 95L185 70M115 70L135 120M155 95L135 120M150 45L130 25" stroke="url(#labeebGrad)" stroke-width="3" stroke-linecap="round" opacity="0.85"/>'
    '<circle cx="115" cy="70" r="5.5" fill="#4C1D95" />'
    '<circle cx="150" cy="45" r="5.5" fill="#7C3AED" />'
    '<circle cx="155" cy="95" r="5.5" fill="#7C3AED" />'
    '<circle cx="185" cy="70" r="6.5" fill="#2563EB" />'
    '<circle cx="135" cy="120" r="4.5" fill="#6D28D9" />'
    '<circle cx="130" cy="25" r="4.5" fill="#4C1D95" />'
    '<path d="M115 30V125C115 149.85 94.85 170 70 170C45.15 170 25 149.85 25 125V105" stroke="url(#labeebGrad)" stroke-width="19" stroke-linecap="round" stroke-linejoin="round"/>'
    '<path d="M155 15C155 21 158 24 164 24C158 24 155 27 155 33C155 27 152 24 146 24C152 24 155 21 155 15Z" fill="url(#labeebGrad)"/>'
    '</svg>'
)
st.markdown(svg_code, unsafe_allow_html=True)

# كتابة بقية عناصر الهوية بشكل تسلسلي عمودي منضبط ومضمون الإغلاق
st.markdown('<h1 class="hero-title">LABEEB AI (لبيب)</h1>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">المحلل الدلالي الذكي لفهم المعنى والسياق في اللغة العربية</div>', unsafe_allow_html=True)
st.markdown('<p class="hero-description">منصة تعتمد على الذكاء الاصطناعي لفهم السياق اللغوي واكتشاف المعنى الصحيح للكلمات من خلال تحليل دلالي عميق ودقيق.</p>', unsafe_allow_html=True)
st.markdown('<div class="author-badge">تصميم وتطوير الباحثة: هاجر الزواكي © 2026</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 4. استدعاء وتحميل أوزان نموذج المعالجة العميقة (AraBERT)
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

# القاموس الدلالي المرجعي المحاكي لعينات اللفظ المشترك
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

# بناء المتجهات الدلالية المسبقة لعينات معالجة اللفظ المشترك
for word in semantic_dictionary:
    for meaning in semantic_dictionary[word]:
        if "vector" not in semantic_dictionary[word][meaning]:
            semantic_dictionary[word][meaning]["vector"] = get_word_vector(
                semantic_dictionary[word][meaning]["النص"], word
            )

# 5. بناء بطاقة مدخلات فحص العينات اللغوية
st.markdown('<div class="section-card"><div class="card-title-container"><span>✍️</span><h3 class="card-title-text">أدخل الجملة العربية للتحليل:</h3></div>', unsafe_allow_html=True)

user_sentence = st.text_area(
    "",
    placeholder="اكتب جملة عربية واضحة تحتوي على المعنى والسياق...",
    height=110,
    label_visibility="collapsed"
)

st.write("") 
analysis_triggered = st.button("⚡ إطلاق خوارزمية لبيب للتحليل")
st.markdown("</div>", unsafe_allow_html=True)

# 6. بطاقة موحدة وحاضنة لعرض النتائج وجداول التشابه الجيب تمامي
st.markdown('<div class="section-card"><div class="card-title-container"><span style="color:#6D28D9;">📊</span><h3 class="card-title-text" style="color:#6D28D9 !important;">نتيجة التحليل</h3></div>', unsafe_allow_html=True)

if analysis_triggered:
    if user_sentence.strip():
        detected_word = None
        for word in semantic_dictionary:
            if word in user_sentence:
                detected_word = word
                break
        
        if detected_word:
            with st.spinner("⏳ يقوم لبيب بقراءة المؤشرات السياقية عبر نموذج AraBERT اللغوي..."):
                time.sleep(0.5)
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
                    
                    st.markdown(f'<p style="font-size: 15px; color: #1E293B; margin-bottom: 8px; text-align: right; direction: rtl;">الكلمة التي تم رصدها وتحليلها تلقائياً: <strong style="color:#6D28D9;">{detected_word}</strong></p>', unsafe_allow_html=True)
                    st.markdown(f'<div style="background-color: #F0FDF4; border: 1px solid #DCFCE7; padding: 16px; border-radius: 14px; margin: 15px 0; text-align: right; direction: rtl;"><span style="font-size: 16px; font-weight: 700; color: #16A34A;">🎯 القرار النهائي الخوارزمي:</span><p style="font-size: 16px; font-weight: 700; color: #15803D; margin: 6px 0 0 0 !important;">المعنى المقصود والمكتشف في النص هو: ({best_meaning})</p></div>', unsafe_allow_html=True)
                    st.markdown(f'<p style="font-size: 14.5px; color: #475569; margin-bottom: 20px; text-align: right; direction: rtl;">درجة ثقة الخوارزمية في القرار الحالي: <strong style="color: #6D28D9;">{confidence_percentage}%</strong></p>', unsafe_allow_html=True)
                    st.markdown('<p style="font-weight: 700; font-size: 14px; color: #1E293B; margin-bottom: 8px; text-align: right; direction: rtl;">📊 جدول معاملات التشابه الجيب تمامي (Cosine Similarity):</p>', unsafe_allow_html=True)
                    
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
    st.markdown('<div class="inner-dashed-box"><div class="empty-icon-box">🔍</div><div class="empty-main-text">لم يتم إجراء أي تحليل بعد</div><div class="empty-sub-text">اكتب جملة عربية واضحة واضغط على زر التحليل للحصول على النتيجة هنا.</div></div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# 7. قسم "كيف يعمل لبيب؟" المطور أفقياً عبر أعمدة لضمان التراصف جنباً إلى جنب بشكل مثالي
st.markdown('<div class="steps-section-title">🧠 كيف يعمل لبيب؟</div>', unsafe_allow_html=True)
st.markdown('<div class="steps-section-desc">يستخدم لبيب الذكاء الاصطناعي لتحليل النصوص العربية وفهم معناها الحقيقي في السياق.</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="step-item-horizontal"><div class="step-badge-num-right">1</div><div class="step-icon-wrapper-center" style="color: #6D28D9;">🔍</div><div class="step-item-title-center">تحليل السياق</div><div class="step-item-desc-center">يحلل لبيب الجملة والكلمات المحيطة لفهم السياق اللغوي بدقة.</div></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="step-item-horizontal"><div class="step-badge-num-right">2</div><div class="step-icon-wrapper-center" style="color: #EC4899;">🎯</div><div class="step-item-title-center">اكتشاف المعنى</div><div class="step-item-desc-center">يحدد المعنى الأقرب اعتماداً على السياق والدلالة اللغوية المخزنة.</div></div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="step-item-horizontal"><div class="step-badge-num-right">3</div><div class="step-icon-wrapper-center" style="color: #3B82F6;">📊</div><div class="step-item-title-center">قياس التشابه الدلالي</div><div class="step-item-desc-center">يستخدم نماذج لغوية متقدمة لقياس التشابه الدلالي وتصنيف النتائج.</div></div>', unsafe_allow_html=True)

# 8. تذييل الموقع والتوثيق الأكاديمي الشامل للمشروع
st.markdown('<div class="footer-container">تم تطوير وتصميم منصة LABEEB AI بواسطة هاجر الزواكي 💜 2026<br>جميع الحقوق محفوظة</div>', unsafe_allow_html=True)
