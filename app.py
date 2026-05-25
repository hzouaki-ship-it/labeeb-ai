import streamlit as st
from tashaphyne.stemming import ArabicLightStemmer
import pandas as pd
import time
import google.generativeai as genai

# 1. إعداد الصفحة (يجب أن يكون دائماً في البداية)
st.set_page_config(page_title="LABEEB AI - لبيب", page_icon="🧠", layout="wide")

# 2. تهيئة النموذج
model = None
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')

# 3. هنا ضعي كود الـ CSS الخاص بك (st.markdown('<style>...</style>', ...))
# [ضعي كود الـ CSS الطويل الخاص بكِ هنا]

# 4. إعداد واجهة Hero Section
st.markdown('<div class="hero-container"><h1>✦ LABEEB AI</h1></div>', unsafe_allow_html=True)

# 5. منطقة الإدخال
user_text = st.text_area("أدخلي الجملة هنا:", placeholder="اكتبي النص الذي تودين تحليله...")

# 6. زر التحليل ومنطق العمل (تم دمجهما بشكل صحيح)
if st.button("⚡ تحليل"):
    if not user_text.strip():
        st.warning("الرجاء إدخال نص أولاً!")
    elif not model:
        st.error("مفتاح API غير مهيأ، يرجى التحقق من الإعدادات.")
    else:
        # البدء بالتحليل
        with st.spinner("⏳ جاري التحليل بواسطة لبيب..."):
            try:
                # عرض النتيجة
                st.success("النتيجة:")
                result_placeholder = st.empty()
                full_response = ""
                
                # الاتصال بـ Gemini
                response = model.generate_content(f"حلل الجملة التالية دلالياً باختصار: {user_text}", stream=True)
                
                for chunk in response:
                    full_response += chunk.text
                    result_placeholder.markdown(full_response + "▌")
                
                result_placeholder.markdown(full_response)
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال: {e}")

# 7. التذييل وباقي أقسام الصفحة
st.markdown('<div class="footer-text">LABEEB AI © 2026 — هاجر الزواكي</div>', unsafe_allow_html=True)
