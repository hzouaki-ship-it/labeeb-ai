import streamlit as st
from tashaphyne.stemming import ArabicLightStemmer
import pandas as pd
import google.generativeai as genai

# --- إعداد النموذج ---
model = None
if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-3.5-flash')
    except:
        model = None

stemmer = ArabicLightStemmer()

# --- قاعدة البيانات المحلية ---
semantic_db = {
    "روح": [{"المعنى": "النفس البشرية", "القرائن": {"موت": 5, "حياة": 5}}, {"المعنى": "راحة", "القرائن": {"هدوء": 5}}],
    "عين": [{"المعنى": "عضو البصر", "القرائن": {"نظر": 5, "رؤية": 5}}, {"المعنى": "جاسوس", "القرائن": {"تجسس": 5, "عميل": 5}}]
}

# --- إعداد الواجهة ---
st.set_page_config(page_title="LABEEB AI - لبيب", page_icon="🧠", layout="wide")

st.markdown('<style>'
    '.stButton > button { background: linear-gradient(90deg, #4F46E5, #6D28D9) !important; color: white !important; border-radius: 12px !important; width: 100% !important; }'
    '.glass-card { background: rgba(255, 255, 255, 0.9); border-radius: 20px; padding: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 15px 0; }'
    '</style>', unsafe_allow_html=True)

st.markdown('<h1>✦ LABEEB AI</h1>', unsafe_allow_html=True)

# 1. منطقة الإدخال
user_text = st.text_area("أدخلي الجملة هنا:", placeholder="اكتبي النص...")

# 2. تعريف الزر (تم وضع التعريف هنا ليكون معرفاً قبل استخدامه)
submit_btn = st.button("⚡ تشغيل خوارزمية لبيب للتحليل")

# 3. منطق التحليل (يعتمد على الزر المعرف أعلاه)
if submit_btn and user_text.strip():
    with st.spinner("⏳ جاري التحليل..."):
        
        # أ) محاولة البحث المحلي
        detected_keyword = next((word for word in semantic_db if word in user_text), None)
        
        if detected_keyword:
            results = semantic_db[detected_keyword]
            st.markdown('<div class="glass-card"><h3>النتائج المحلية:</h3>' + 
                        "".join([f"<p>✅ {r['المعنى']}</p>" for r in results]) + '</div>', unsafe_allow_html=True)
        
        # ب) التحليل عبر النموذج إذا لم يوجد محلياً
        elif model:
            try:
                response = model.generate_content(f"حلل الجملة التالية دلالياً: {user_text}")
                st.markdown(f'<div class="glass-card"><h3>التحليل الذكي:</h3><p>{response.text}</p></div>', unsafe_allow_html=True)
            except Exception as e:
                st.error("تعذر الاتصال بخادم الذكاء الاصطناعي.")
        else:
            st.warning("لم يتم العثور على مطابقة دلالية في قاعدة البيانات.")

# التذييل
st.markdown('<div style="text-align:center; margin-top:50px; color:#94A3B8;">LABEEB AI © 2026 — هاجر الزواكي</div>', unsafe_allow_html=True)
