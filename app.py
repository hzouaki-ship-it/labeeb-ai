import streamlit as st
from tashaphyne.stemming import ArabicLightStemmer
import google.generativeai as genai

# إعداد النموذج مع معالجة الأخطاء
model = None
if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-3.5-flash')
    except Exception:
        model = None

# إعدادات الصفحة
st.set_page_config(page_title="LABEEB AI - لبيب", page_icon="🧠", layout="wide")

# التصميم
st.markdown('<style>'
    '.stButton > button { background: linear-gradient(90deg, #4F46E5, #6D28D9) !important; color: white !important; border-radius: 12px !important; width: 100% !important; }'
    '.glass-card { background: rgba(255, 255, 255, 0.9); border-radius: 20px; padding: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 15px 0; }'
    '</style>', unsafe_allow_html=True)

st.markdown('<h1>✦ LABEEB AI</h1>', unsafe_allow_html=True)

# المدخلات
user_text = st.text_area("أدخلي الجملة هنا:", placeholder="اكتبي النص...")
submit_btn = st.button("⚡ تشغيل خوارزمية لبيب للتحليل")

# المنطق
if submit_btn:
    if not user_text.strip():
        st.warning("يرجى كتابة نص للتحليل.")
    else:
        with st.spinner("⏳ جاري التحليل..."):
            # محاولة الاستدعاء
            if model:
                try:
                    response = model.generate_content(f"حلل الجملة التالية دلالياً وأجب بالمعنى فقط: {user_text}")
                    st.markdown(f'<div class="glass-card"><h3>التحليل:</h3><p>{response.text}</p></div>', unsafe_allow_html=True)
                except Exception:
                    st.info("حدث خطأ في الاتصال بالسيرفر. يرجى التأكد من مفتاح الـ API الخاص بك.")
            else:
                st.error("نظام الذكاء الاصطناعي غير متصل. تأكدي من إعدادات الـ Secrets.")

st.markdown('<div style="text-align:center; margin-top:50px; color:#94A3B8;">LABEEB AI © 2026 — هاجر الزواكي</div>', unsafe_allow_html=True)
