import streamlit as st
import google.generativeai as genai
import pandas as pd

# 1. إعداد الصفحة
st.set_page_config(page_title="LABEEB AI - لبيب", page_icon="🧠", layout="wide")

# 2. تهيئة الاتصال بـ Gemini
# نضع الإعدادات في مكان منفصل لتجنب أي تعارض في الإزاحة
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    else:
        genai.configure(api_key="AIzaSyA8bG4DU2L815GS-DacoxDSaajRETabM8s")
    
    # تعريف النموذج
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"خطأ في تهيئة النموذج: {e}")

# 3. زر تشخيصي (لمعرفة النماذج المتاحة لمفتاحك)
if st.button("عرض النماذج المتاحة"):
    try:
        models_list = genai.list_models()
        for m in models_list:
            if 'generateContent' in m.supported_generation_methods:
                st.write(f"النموذج المتاح: {m.name}")
    except Exception as e:
        st.error(f"خطأ في الاتصال بالخادم: {e}")

# 4. الواجهة والمنطق
st.markdown('<div style="text-align: center;"><h1>✦ LABEEB AI</h1><p>المحلل الدلالي الذكي</p></div>', unsafe_allow_html=True)

user_text = st.text_area("أدخلي الجملة هنا:")
if st.button("⚡ تحليل"):
    try:
        # التأكد من تعريف model قبل استخدامه
        if 'model' in globals():
            with st.spinner("جاري التحليل..."):
                response = model.generate_content(f"حلل الجملة التالية دلالياً: {user_text}")
                st.write(response.text)
        else:
            st.error("النموذج غير مهيأ، يرجى التأكد من مفتاح API.")
    except Exception as e:
        st.error(f"حدث خطأ أثناء التحليل: {e}")
