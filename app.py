import streamlit as st
import google.generativeai as genai
import pandas as pd
from tashaphyne.stemming import ArabicLightStemmer

# 1. إعداد الصفحة
st.set_page_config(page_title="LABEEB AI - لبيب", page_icon="🧠", layout="wide")

# 2. تهيئة الاتصال بـ Gemini
# سيحاول أولاً استخدام الـ Secrets، إذا فشل، سيستخدم المفتاح المباشر
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    else:
        genai.configure(api_key="AIzaSyA8bG4DU2L815GS-DacoxDSaajRETabM8s")

model = genai.GenerativeModel('models/gemini-1.5-flash')
except Exception as e:
    st.error(f"خطأ في تهيئة النموذج: {e}")

# 3. قاعدة البيانات
semantic_db = {
    "روح": [{"المعنى": "النفس البشرية", "القرائن": ["موت", "حياة", "جسد"]}, {"المعنى": "الراحة", "القرائن": ["هدوء", "راحة"]}],
    "عين": [{"المعنى": "عضو بصر", "القرائن": ["نظر", "رؤية", "بصر"]}, {"المعنى": "نبع", "القرائن": ["ماء", "نبع"]}, {"المعنى": "جاسوس", "القرائن": ["تجسس", "عميل"]}]
}

# 4. الواجهة
st.markdown('<div style="background: #EFF6FF; padding: 20px; border-radius: 15px; text-align: center;"><h1>✦ LABEEB AI</h1><p>المحلل الدلالي الذكي</p></div>', unsafe_allow_html=True)

user_text = st.text_area("أدخلي الجملة هنا:", placeholder="مثال: فقد الجندي عينه في المعركة...")
submit_btn = st.button("⚡ تحليل")

# 5. منطق التحليل
if submit_btn and user_text:
    found = False
    for word, meanings in semantic_db.items():
        if word in user_text:
            found = True
            st.success(f"تم رصد اللفظ في القاموس: {word}")
            results = [{"المعنى": m["المعنى"], "قوة الارتباط": sum(1 for c in m["القرائن"] if c in user_text)} for m in meanings]
            st.table(pd.DataFrame(results))
            break
    
    if not found:
        with st.spinner("⏳ جاري التحليل بواسطة Gemini..."):
            try:
                response = model.generate_content(f"حلل الجملة التالية دلالياً: {user_text}")
                st.write(response.text)
            except Exception as e:
                st.error(f"فشل الاتصال بالذكاء الاصطناعي: {e}")

st.markdown("---")
st.write("تم التطوير بواسطة: هاجر الزواكي | 2026")
