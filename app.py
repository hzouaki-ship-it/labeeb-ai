import streamlit as st
import google.generativeai as genai

# إعداد مفتاح الـ API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# استخدام النموذج المتاح في قائمتك
model_name = 'gemini-3.5-flash'

# إعداد النموذج
try:
    model = genai.GenerativeModel(model_name=model_name)
except Exception as e:
    st.error(f"خطأ في تحميل النموذج: {e}")
    model = None

# --- منطق التحليل ---
if submit_btn and user_text.strip():
    if model:
        with st.spinner("⏳ جاري التحليل..."):
            try:
                # استدعاء مباشر ومبسط
                response = model.generate_content(
                    f"حلل الجملة التالية دلالياً وأجب بالمعنى فقط: {user_text}"
                )
                st.markdown(f'<div class="glass-card"><h3>النتيجة:</h3><p>{response.text}</p></div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"خطأ أثناء استدعاء النموذج: {e}")
    else:
        st.error("النموذج غير مهيأ.")
