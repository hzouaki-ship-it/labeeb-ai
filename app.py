import streamlit as st
import pandas as pd
import time
import google.generativeai as genai
import nltk
from nltk.corpus import wordnet as wn
from tashaphyne.stemming import ArabicLightStemmer

# --- 1. الإعدادات والتحميلات ---
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)
stemmer = ArabicLightStemmer()

# قاعدة البيانات المحلية
semantic_db = {
    "روح": {"المعنى": "النفس البشرية", "السياق": "عالم الغيب أو الحياة"},
    "عين": {"المعنى": "عضو البصر أو نبع أو جاسوس", "السياق": "يعتمد على الألفاظ المحيطة"},
    "كتاب": {"المعنى": "مؤلف مطبوع", "السياق": "قراءة أو تشريع"}
}

st.set_page_config(page_title="LABEEB AI - لبيب", page_icon="🧠", layout="wide")

# --- 2. CSS ---
st.markdown('<style>'
    '.hero-container { text-align: center; padding: 20px; }'
    '.glass-card { background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px); border-radius: 20px; padding: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 15px 0; border: 1px solid #E2E8F0; }'
    '.footer-text { text-align: center; color: #94A3B8; font-size: 13px; margin-top: 50px; }'
    '.stButton > button { background: linear-gradient(90deg, #4F46E5, #6D28D9) !important; color: white !important; border-radius: 12px !important; width: 100% !important; }'
    '</style>', unsafe_allow_html=True)

# --- 3. تهيئة Gemini ---
model = None
if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-3.5-flash')
    except Exception:
        model = None

# --- 4. الواجهة ---
st.markdown('<div class="hero-container"><h1>✦ LABEEB AI</h1></div>', unsafe_allow_html=True)
user_text = st.text_area("أدخلي الجملة هنا:", placeholder="اكتبي النص الذي تودين تحليله...")
submit_btn = st.button("⚡ تحليل")

# --- 5. منطق التحليل ---
if submit_btn and user_text.strip():
    with st.spinner("⏳ جاري تحليل البنية الدلالية..."):
        
        # أ) التحليل المحلي
        found_local = False
        words_in_text = user_text.split()
        for word, data in semantic_db.items():
            for token in words_in_text:
                stemmer.light_stem(token)
                if stemmer.get_stem() == stemmer.light_stem(word):
                    st.markdown(f'''<div class="glass-card"><h3>🔍 تحليل لبيب (محلي):</h3>
                                <p><b>اللفظ المكتشف:</b> {word}</p>
                                <p><b>المعنى:</b> {data["المعنى"]}</p>
                                </div>''', unsafe_allow_html=True)
                    found_local = True
                    break

        # ب) البحث في الشبكة الدلالية (WordNet)
        synsets = []
        for w in words_in_text:
            if len(w) > 2:
                results = wn.synsets(w, lang='arb')
                if results:
                    synsets.extend(results[:1])

        if synsets and not found_local:
            st.markdown('<div class="glass-card"><h3>🧠 نتائج الشبكة الدلالية</h3>', unsafe_allow_html=True)
            for syn in synsets[:2]:
                st.write(f"📌 المعنى: {syn.definition()}")
                arabic_words = [lemma.name() for lemma in syn.lemmas(lang='arb')]
                if arabic_words:
                    st.write(f"🔹 المرادفات: {', '.join(arabic_words[:3])}")
            st.markdown('</div>', unsafe_allow_html=True)

        # ج) التحليل الذكي (Gemini) - تم تصحيح المسافات هنا
        if model and not found_local:
            try:
                response = model.generate_content(f"حلل هذه الجملة دلالياً واشرح المجاز إن وجد: {user_text}")
                st.markdown(f'<div class="glass-card"><h3>🤖 التحليل الدلالي الذكي:</h3><p>{response.text}</p></div>', unsafe_allow_html=True)
            except Exception:
                st.info("نظام لبيب: التحليل الذكي مشغول حالياً.")
        elif not model:
            st.warning("نظام التحليل الذكي غير مهيأ.")

# --- 6. التذييل ---
st.markdown('<div class="footer-text">LABEEB AI © 2026 — هاجر الزواكي</div>', unsafe_allow_html=True)
