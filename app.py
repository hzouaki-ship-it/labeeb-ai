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
        model = genai.GenerativeModel('gemini-3.5-flash')
    else:
        st.error("⚠️ لم يتم العثور على GOOGLE_API_KEY في إعدادات التطبيق.")
except Exception as e:
    st.error(f"خطأ في تهيئة النموذج: {e}")

# 3. الواجهة
st.markdown('<div style="text-align: center;"><h1>✦ LABEEB AI</h1><p>المحلل الدلالي الذكي</p></div>', unsafe_allow_html=True)

user_text = st.text_area("أدخلي الجملة هنا:", placeholder="اكتبي النص الذي تودين تحليله...")

# 4. منطق التحليل مع خاصية الـ Streaming للسرعة
if st.button("⚡ تحليل"):
    if model:
        if user_text.strip():
            st.success("النتيجة:")
            # مكان مخصص لعرض النص تدريجياً
            result_placeholder = st.empty()
            full_response = ""
            
            try:
                # تفعيل الـ stream للحصول على النص فوراً
                response = model.generate_content(f"حلل الجملة التالية دلالياً باختصار: {user_text}", stream=True)
                
                for chunk in response:
                    full_response += chunk.text
                    result_placeholder.markdown(full_response + "▌")
                
                # تحديث نهائي لإزالة المؤشر
                result_placeholder.markdown(full_response)
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {e}")
        else:
            st.warning("الرجاء إدخال نص أولاً!")
    else:
        st.error("لا يمكن التحليل، تأكدي من إعدادات المفتاح.")

# زر اختياري للتشخيص (مخفي في الأسفل لجمالية الواجهة)
with st.expander("خيارات متقدمة"):
    if st.button("عرض النماذج المتاحة"):
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    st.write(f"✅ {m.name}")
        except Exception as e:
            st.error(e)
