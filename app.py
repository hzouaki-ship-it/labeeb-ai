import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import time

# 1. إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="منصة لبيب LABEEB AI",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. حقن التنسيقات عبر فك ارتباط النصوص المعقدة لتجنب SyntaxError تماماً
st.markdown('<style>@import url("https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&display=swap");</style>', unsafe_allow_html=True)
st.markdown('<style>html, body, [data-testid="stAppViewContainer"], .stApp { background-color: #F9FAFB !important; direction: RTL !important; text-align: right !important; font-family: "Cairo", sans-serif !important; }</style>', unsafe_allow_html=True)
st.markdown('<style>[data-testid="stMain"] .block-container { padding-top: 0rem !important; padding-bottom: 3rem !important; max-width: 850px !important; }</style>', unsafe_allow_html=True)
st.markdown('<style>[data-testid="stVerticalBlock"] { gap: 0rem !important; } h1, h2, h3, h4, h5, h6, p, span, label { font-family: "Cairo", sans-serif !important; }</style>', unsafe_allow_html=True)

# تنسيقات قسم الـ Hero
st.markdown('<style>.hero-outer { margin-left: -4rem; margin-right: -4rem; background: linear-gradient(180deg, #EBF0FF 0%, #F4EFFF 60%, #F9FAFB 100%); padding: 50px 40px 60px 40px; text-align: center !important; position: relative; overflow: hidden; border-bottom-left-radius: 50px 20px; border-bottom-right-radius: 50px 20px; }</style>', unsafe_allow_html=True)
st.markdown('<style>.hero-dots-left { position: absolute; top: 30px; left: 40px; width: 60px; height: 60px; background-image: radial-gradient(#94A3B8 1.5px, transparent 1.5px); background-size: 12px 12px; opacity: 0.4; }</style>', unsafe_allow_html=True)
st.markdown('<style>.hero-dots-right { position: absolute; bottom: 40px; right: 40px; width: 60px; height: 60px; background-image: radial-gradient(#94A3B8 1.5px, transparent 1.5px); background-size: 12px 12px; opacity: 0.4; }</style>', unsafe_allow_html=True)
st.markdown('<style>.top-badge { display: inline-flex; align-items: center; background-color: #FFFFFF; color: #6366F1; padding: 4px 16px; border-radius: 100px; font-size: 13px; font-weight: 600; margin-bottom: 24px; box-shadow: 0 2px 6px rgba(99, 102, 241, 0.08); }</style>', unsafe_allow_html=True)
st.markdown('<style>.hero-logo-container { display: flex; align-items: center; justify-content: center; gap: 14px; margin-bottom: 12px; } .hero-logo-icon { background: #FFFFFF; width: 64px; height: 64px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 32px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }</style>', unsafe_allow_html=True)
st.markdown('<style>.hero-title { font-size: 46px !important; font-weight: 800 !important; color: #5B21B6 !important; margin: 0 !important; line-height: 1.2; } .hero-subtitle { font-size: 18px !important; font-weight: 700 !important; color: #1E293B !important; margin-top: 14px !important; margin-bottom: 14px !important; }</style>', unsafe_allow_html=True)
st.markdown('<style>.hero-description { font-size: 15px !important; color: #64748B !important; max-width: 650px; margin: 0 auto 24px auto !important; line-height: 1.7; } .author-badge { display: inline-block; background: #F3E8FF; color: #6B21A8 !important; padding: 6px 20px; border-radius: 100px; font-size: 13px !important; font-weight: 600; border: 1px solid #E9D5FF; }</style>', unsafe_allow_html=True)

# تنسيقات المكونات والبطاقات والخطوات
st.markdown('<style>.section-card { background: #FFFFFF; border: 1px solid #F1F5F9; border-radius: 24px; padding: 35px; box-shadow: 0 4px 25px rgba(0, 0, 0, 0.015); margin-top: 30px; margin-bottom: 5px; }</style>', unsafe_allow_html=True)
st.markdown('<style>.card-title-container { display: flex; align-items: center; justify-content: flex-start; gap: 8px; margin-bottom: 20px; } .card-title-text { font-size: 16px !important; font-weight: 700 !important; color: #1E293B !important; margin: 0 !important; }</style>', unsafe_allow_html=True)
st.markdown('<style>.stTextArea textarea { background-color: #FFFFFF !important; border: 1px solid #E2E8F0 !important; border-radius: 16px !important; padding: 18px !important; font-family: "Cairo", sans-serif !important; font-size: 14.5px !important; color: #334155 !important; }</style>', unsafe_allow_html=True)
st.markdown('<style>div.stButton > button { background: #6D28D9 !important; color: white !important; font-family: "Cairo", sans-serif !important; font-weight: 600 !important; font-size: 14.5px !important; border-radius: 12px !important; border: none !important; padding: 10px 24px !important; box-shadow: 0 4px 12px rgba(109, 40, 217, 0.25) !important; }</style>', unsafe_allow_html=True)
st.markdown('<style>.inner-dashed-box { border: 1px dashed #E2E8F0; border-radius: 16px; padding: 40px 20px; text-align: center; background: #FAFAFA; }</style>', unsafe_allow_html=True)
st.markdown('<style>.empty-icon-box { font-size: 36px; color: #6D28D9; background: #F3E8FF; width: 64px; height: 64px; display: inline-flex; align-items: center; justify-content: center; border-radius: 16px; margin-bottom: 16px; } .empty-main-text { color: #6D28D9; font-weight: 700; font-size: 16px; margin-bottom: 6px; } .empty-sub-text { color: #94A3B8; font-size: 13.5px; }</style>', unsafe_allow_html=True)
st.markdown('<style>.steps-section-title { text-align: center !important; font-size: 18px !important; font-weight: 700 !important; color: #1E293B !important; margin-top: 40px !important; margin-bottom: 6px !important; } .steps-section-desc { text-align: center !important; font-size: 14px !important; color: #64748B !important; margin-bottom: 25px !important; }</style>', unsafe_allow_html=True)
st.markdown('<style>.steps-container { display: flex; gap: 16px; } .step-item { flex: 1; background: #FFFFFF; border: 1px solid #F1F5F9; border-radius: 20px; padding: 24px 20px; text-align: center; position: relative; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.01); }</style>', unsafe_allow_html=True)
st.markdown('<style>.step-badge-num { position: absolute; top: -12px; left: 20px; background: #6D28D9; color: white; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; }</style>', unsafe_allow_html=True)
st.markdown('<style>.step-icon-wrapper { font-size: 22px; margin-bottom: 12px; background: #F8FAFC; width: 48px; height: 48px; display: inline-flex; align-items: center; justify-content: center; border-radius: 50%; } .step-item-title { font-weight: 700; color: #4338CA; font-size: 14.5px; margin-bottom: 8px; } .step-item-desc { color: #64748B; font-size: 13px; line-height: 1.6; }</style>', unsafe_allow_html=True)
st.markdown('<style>.footer-container { text-align: center !important; margin-top: 45px; padding-top: 20px; color: #94A3B8 !important; font-size: 13px !important; border-top: 1px solid #E2E8F0; }</style>', unsafe_allow_html=True)
st.markdown('<style>@media (max-width: 768px) { .steps-container { flex-direction: column; gap: 20px; } .step-badge-num { left: auto; right: 20px; } }</style>', unsafe_allow_html=True)

# 3. عرض ترويسة الصفحة (Hero Section) مجزأة بشكل آمن
st.markdown('<div class="hero-outer"><div class="hero-dots-left"></div><div class="hero-dots-right"></div><div class="top-badge">✦ منصة ذكية عربية</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-logo-container"><div class="hero-logo-icon">🧠</div><h1 class="hero-title">LABEEB AI (لبيب)</h1></div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">المحلل الدلالي الذكي لفهم المعنى والسياق في اللغة العربية</div>', unsafe_allow_html=True)
st.markdown('<p class="hero-description">منصة تعتمد على الذكاء الاصطناعي لفهم السياق اللغوي واكتشاف المعنى الصحيح للكلمات من خلال تحليل دلالي عميق ودقيق.</p>', unsafe_allow_html=True)
st.markdown('<div class="author-badge">تصميم وتطوير: هاجر الزواكي © 2026</div></div>', unsafe_allow_html=True)

# 4. تحميل أوزان نموذج الخوارزمية (AraBERT) وتأمين الكاش
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

# بناء القاموس الدلالي المرجعي الأساسي
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

# توليد المتجهات للقاموس المرجعي
for word in semantic_dictionary:
    for meaning in semantic_dictionary[word]:
        if "vector" not in semantic_dictionary[word][meaning]:
            semantic_dictionary[word][meaning]["vector"] = get_word_vector(
                semantic_dictionary[word][meaning]["النص"], word
            )

# 5. منطقة بطاقة الإدخال
st.markdown('<div class="section-card"><div class="card-title-container"><span>✍️</span><h3 class="card-title-text">أدخل الجملة العربية للتحليل:</h3></div>', unsafe_allow_html=True)
user_sentence = st.text_area("", placeholder="اكتب جملة عربية واضحة تحتوي على المعنى والسياق...", height=110, label_visibility="collapsed")
st.write("") 
analysis_triggered = st.button("⚡ إطلاق خوارزمية لبيب للتحليل")
st.markdown('</div>', unsafe_allow_html=True)

# 6. بطاقة عرض نتائج الفحص
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
                    
                    st.markdown(f'<p style="font-size: 15px; color: #1E293B; margin-bottom: 8px;">الكلمة التي تم رصدها وتحليلها تلقائياً: <strong style="color:#6D28D9;">{detected_word}</strong></p>', unsafe_allow_html=True)
                    st.markdown(f'<div style="background-color: #F0FDF4; border: 1px solid #DCFCE7; padding: 16px; border-radius: 14px; margin: 15px 0;"><span style="font-size: 16px; font-weight: 700; color: #16A34A;">🎯 القرار النهائي الخوارزمي:</span><p style="font-size: 16px; font-weight: 700; color: #15803D; margin: 6px 0 0 0 !important;">المعنى المقصود والمكتشف في النص هو: ({best_meaning})</p></div>', unsafe_allow_html=True)
                    st.markdown(f'<p style="font-size: 14.5px; color: #475569; margin-bottom: 20px;">درجة ثقة الخوارزمية في القرار الحالي: <strong style="color: #6D28D9;">{confidence_percentage}%</strong></p>', unsafe_allow_html=True)
                    st.markdown('<p style="font-weight: 700; font-size: 14px; color: #1E293B; margin-bottom: 8px;">📊 جدول معاملات التشابه الجيب تمامي (Cosine Similarity):</p>', unsafe_allow_html=True)
                    
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

st.markdown('</div>', unsafe_allow_html=True)

# 7. قسم "كيف يعمل لبيب؟" المحمي والمبني بأسطر آمنة
st.markdown('<div class="steps-section-title">🧠 كيف يعمل لبيب؟</div>', unsafe_allow_html=True)
st.markdown('<div class="steps-section-desc">يستخدم لبيب الذكاء الاصطناعي لتحليل النصوص العربية وفهم معناها الحقيقي في السياق.</div>', unsafe_allow_html=True)

st.markdown('<div class="steps-container">', unsafe_allow_html=True)
st.markdown('<div class="step-item"><div class="step-badge-num">1</div><div class="step-icon-wrapper" style="color: #6D28D9;">🔍</div><div class="step-item-title">تحليل السياق</div><div class="step-desc">يحلل لبيب الجملة والكلمات المحيطة لفهم السياق اللغوي بدقة.</div></div>', unsafe_allow_html=True)
st.markdown('<div class="step-item"><div class="step-badge-num">2</div><div class="step-icon-wrapper" style="color: #EC4899;">🎯</div><div class="step-item-title">اكتشاف المعنى</div><div class="step-desc">يحدد المعنى الأقرب اعتماداً على السياق والدلالة اللغوية المخزنة.</div></div>', unsafe_allow_html=True)
st.markdown('<div class="step-item"><div class="step-badge-num">3</div><div class="step-icon-wrapper" style="color: #3B82F6;">📊</div><div class="step-item-title">قياس التشابه الدلالي</div><div class="step-desc">يستخدم نماذج لغوية متقدمة لقياس التشابه الدلالي وتصنيف النتائج.</div></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 8. تذييل المنصة
st.markdown('<div class="footer-container">تم تطوير وتصميم منصة LABEEB AI بواسطة هاجر الزواكي 💜 2026<br>جميع الحقوق محفوظة</div>', unsafe_allow_html=True)
