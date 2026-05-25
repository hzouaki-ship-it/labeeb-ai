import streamlit as st
import google.generativeai as genai
import pandas as pd

# 1. إعداد الصفحة
st.set_page_config(page_title="LABEEB AI - لبيب", page_icon="🧠", layout="wide")

# 2. تهيئة الاتصال بـ Gemini
model = None
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # تعريف النموذج داخل جملة if لضمان أنه لن يُعرف إلا بوجود المفتاح
        model = genai.GenerativeModel('gemini-3.5-flash')
    else:
        st.error("⚠️ لم يتم العثور على GOOGLE_API_KEY في إعدادات التطبيق (Secrets).")
except Exception as e:
    st.error(f"خطأ في تهيئة النموذج: {e}")

# 3. زر تشخيصي لمعرفة النماذج المتاحة
if st.button("عرض النماذج المتاحة"):
    try:
        models_list = genai.list_models()
        for m in models_list:
            if 'generateContent' in m.supported_generation_methods:
                st.write(f"✅ النموذج المتاح: {m.name}")
    except Exception as e:
        st.error(f"خطأ في الاتصال بالخادم: {e}")

# 4. الواجهة والمنطق
st.markdown('<div style="text-align: center;"><h1>✦ LABEEB AI</h1><p>المحلل الدلالي الذكي</p></div>', unsafe_allow_html=True)

user_text = st.text_area("أدخلي الجملة هنا:", placeholder="اكتبي النص الذي تودين تحليله...")

if st.button("⚡ تحليل"):
    if model:
        if user_text.strip():
            with st.spinner("⏳ جاري التحليل بواسطة لبيب..."):
                try:
                    response = model.generate_content(f"حلل الجملة التالية دلالياً: {user_text}")
                    st.success("النتيجة:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {e}")
        else:
            st.warning("الرجاء إدخال نص أولاً!")
    else:
        st.error("لا يمكن التحليل لأن النموذج غير مهيأ.")
