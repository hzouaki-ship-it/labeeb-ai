import streamlit as st
import google.generativeai as genai
from tashaphyne.stemming import ArabicLightStemmer
import pandas as pd
import time

# 1. إعداد الصفحة
st.set_page_config(page_title="LABEEB AI - لبيب", page_icon="🧠", layout="wide")

# 2. إعداد الاتصال بـ Gemini (بأمان)
# ضعي المفتاح في Secrets في Streamlit Cloud كما شرحنا سابقاً
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("خطأ في الاتصال بالذكاء الاصطناعي: تأكدي من إعداد GOOGLE_API_KEY في الـ Secrets")

stemmer = ArabicLightStemmer()

# 3. قاعدة البيانات
semantic_db = {
    "روح": [{"المعنى": "النفس البشرية", "القرائن": ["موت", "حياة", "جسد"]}, {"المعنى": "الراحة", "القرائن": ["هدوء", "راحة"]}],
    "عين": [{"المعنى": "عضو بصر", "القرائن": ["نظر", "رؤية", "بصر"]}, {"المعنى": "نبع", "القرائن": ["ماء", "نبع"]}, {"المعنى": "جاسوس", "القرائن": ["تجسس", "عميل"]}]
}

# 4. الواجهة والتنسيق
st.markdown("""<style>
    .hero-container { background: linear-gradient(135deg, #F8FAFC, #EFF6FF); padding: 30px; border-radius: 20px; text-align: center; }
    .glass-card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
</style>""", unsafe_allow_html=True)

st.markdown('<div class="hero-container"><h1>✦ LABEEB AI</h1><p>المحلل الدلالي الذكي</p></div>', unsafe_allow_html=True)

# 5. الإدخال
user_text = st.text_area("أدخلي الجملة هنا:", placeholder="مثال: فقد الجندي عينه في المعركة...")
submit_btn = st.button("⚡ تحليل")

# 6. منطق التحليل
if submit_btn and user_text:
    found = False
    for word, meanings in semantic_db.items():
        if word in user_text:
            found = True
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.success(f"تم رصد اللفظ: {word}")
            results = []
            for m in meanings:
                score = sum(1 for c in m["القرائن"] if c in user_text)
                results.append({"المعنى": m["المعنى"], "قوة الارتباط": score})
            st.table(pd.DataFrame(results))
            st.markdown('</div>', unsafe_allow_html=True)
            break
    
    if not found:
        with st.spinner("⏳ جاري التحليل بواسطة Gemini..."):
            try:
                response = model.generate_content(f"حلل الجملة التالية دلالياً: {user_text}")
                st.write(response.text)
            except:
                st.error("حدث خطأ في الاتصال بالنموذج.")

# 7. التذييل
st.markdown("---")
st.write("تم التطوير بواسطة: هاجر الزواكي | 2026")
