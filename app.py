import streamlit as st
from tashaphyne.stemming import ArabicLightStemmer
import pandas as pd
import time
import google.generativeai as genai

# --- إعداد Gemini كمعالج صامت ---
model = None
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction="أنت أداة معالجة خلفية. وظيفتك تحليل الجملة دلالياً واستخراج المعنى الأقرب. أجب بالمعنى فقط دون مقدمات أو شرح."
    )

stemmer = ArabicLightStemmer()

# --- قاعدة البيانات المعجمية ---
semantic_db = {
    "روح": [{"المعنى": "النفس البشرية", "القرائن": {"موت": 5, "حياة": 5, "جسد": 4}},
            {"المعنى": "الراحة والطاقة", "القرائن": {"هدوء": 5, "راحة": 5, "سعادة": 4}}],
    "عين": [{"المعنى": "عضو البصر", "القرائن": {"نظر": 5, "رؤية": 5, "دموع": 4}},
            {"المعنى": "نبع ماء", "القرائن": {"ماء": 5, "نبع": 5, "شرب": 3}},
            {"المعنى": "جاسوس", "القرائن": {"تجسس": 5, "عدو": 4, "عميل": 5}}]
}

st.set_page_config(page_title="LABEEB AI - لبيب", page_icon="🧠", layout="wide")

# --- CSS ---
st.markdown('<style>'
    '.stButton > button { background: linear-gradient(90deg, #4F46E5, #6D28D9) !important; color: white !important; border-radius: 12px !important; width: 100% !important; }'
    '.glass-card { background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(20px); border-radius: 22px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); margin-bottom: 25px; }'
    '.footer-text { text-align: center; color: #94A3B8; font-size: 13px; margin-top: 50px; }'
    '</style>', unsafe_allow_html=True)

# --- الواجهة ---
st.markdown('<div class="hero-container"><h1>✦ LABEEB AI</h1></div>', unsafe_allow_html=True)
user_text = st.text_area("أدخلي الجملة هنا:", placeholder="مثال: فقد الجندي عينه في المعركة...")
submit_btn = st.button("⚡ تشغيل خوارزمية لبيب للتحليل")

# --- منطق التحليل ---
if submit_btn and user_text.strip():
    with st.spinner("⏳ جاري التحليل..."):
        detected_keyword = None
        for word in semantic_db.keys():
            if word in user_text:
                detected_keyword = word
                break
        
        # 1. التحليل المحلي
        if detected_keyword:
            results = []
            for entry in semantic_db[detected_keyword]:
                results.append({"المعنى": entry["المعنى"], "النوع": "قاعدة بيانات محلية"})
            
            st.markdown('<div class="glass-card"><h3>نتائج لبيب (محلي):</h3>' + 
                        "".join([f"<p>✅ {r['المعنى']}</p>" for r in results]) + '</div>', unsafe_allow_html=True)
        
        # 2. التحليل بالذكاء الاصطناعي (خلفي وصامت)
        elif model:
            try:
                response = model.generate_content(f"حلل الجملة التالية دلالياً: {user_text}")
                st.markdown('<div class="glass-card"><h3>التحليل الدلالي:</h3>'
                            f'<p>{response.text.strip()}</p></div>', unsafe_allow_html=True)
            except Exception:
                st.error("تعذر التحليل، يرجى المحاولة لاحقاً.")
        else:
            st.warning("عذراً، لم يتم العثور على المعنى في القاعدة المحلية، والذكاء الاصطناعي غير مفعل حالياً.")

st.markdown('<div class="footer-text">LABEEB AI © 2026 — هاجر الزواكي</div>', unsafe_allow_html=True)
