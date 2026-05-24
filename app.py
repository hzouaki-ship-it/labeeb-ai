import streamlit as st
import google.generativeai as genai
from tashaphyne.stemming import ArabicLightStemmer
import pandas as pd
import time

# 1. إعداد الصفحة والتهيئة
st.set_page_config(page_title="LABEEB AI - لبيب", page_icon="🧠", layout="wide")

try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    pass

stemmer = ArabicLightStemmer()

# 2. التنسيق (CSS) - تم تجميعه في كتلة واحدة
st.markdown("""
<style>
    @import url("https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&family=Poppins:wght@400;600;700;800&display=swap");
    html, body, [class*="css"] { font-family: "Cairo", sans-serif; direction: rtl; text-align: right; }
    .stApp { background: linear-gradient(135deg, #F8FAFC 0%, #F5F3FF 50%, #EFF6FF 100%) !important; }
    .hero-container { background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.6); border-radius: 28px; padding: 35px 25px; text-align: center; box-shadow: 0 20px 40px rgba(109, 40, 217, 0.03); margin-bottom: 30px; }
    .glass-card { background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.5); border-radius: 22px; padding: 30px; margin-bottom: 25px; }
    .card-title { font-size: 20px; font-weight: 700; color: #1E293B; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
    .stButton > button { background: linear-gradient(90deg, #4F46E5, #6D28D9) !important; color: white !important; border-radius: 12px !important; padding: 12px 28px !important; width: 100% !important; font-weight: 700 !important; }
    .result-stat-box { flex: 1; background: white; border: 1px solid #F3E8FF; padding: 14px; border-radius: 14px; text-align: center; }
    .result-stat-val { font-size: 18px; font-weight: 700; color: #6D28D9; }
    .step-card { background: white; border: 1px solid #F1F5F9; border-radius: 18px; padding: 22px; text-align: center; }
    .researcher-img { width: 110px; height: 110px; border-radius: 50%; object-fit: cover; border: 3px solid #F3E8FF; }
</style>
""", unsafe_allow_html=True)

# 3. قاعدة البيانات (semantic_db)
semantic_db = {
    "روح": [{"المعنى": "النفس البشرية", "القرائن": {"موت": 5, "حياة": 5, "جسد": 4}}, {"المعنى": "الراحة", "القرائن": {"هدوء": 5, "راحة": 5}}],
    "باب": [{"المعنى": "مدخل مادي", "القرائن": {"منزل": 5, "قفل": 5}}, {"المعنى": "فصل", "القرائن": {"كتاب": 5, "فصل": 5}}],
    "كتاب": [{"المعنى": "مؤلف مطبوع", "القرائن": {"قراءة": 5, "مكتبة": 5}}, {"المعنى": "فرض أو حكم", "القرائن": {"شرع": 5, "واجب": 4}}],
    "بحر": [{"المعنى": "مسطح مائي", "القرائن": {"ماء": 5, "موج": 5}}, {"المعنى": "العلم الواسع", "القرائن": {"علم": 5, "معرفة": 4}}],
    "مفتاح": [{"المعنى": "أداة فتح", "القرائن": {"باب": 5, "قفل": 5}}, {"المعنى": "حل أو وسيلة", "القرائن": {"نجاح": 5, "حل": 5}}],
    "عين": [{"المعنى": "عضو البصر", "القرائن": {"نظر": 5, "رؤية": 5, "بصر": 5}}, {"المعنى": "نبع ماء", "القرائن": {"ماء": 5, "نبع": 5}}, {"المعنى": "جاسوس", "القرائن": {"تجسس": 5, "عميل": 5}}],
    "قلب": [{"المعنى": "عضو في جسم الإنسان", "القرائن": {"نبض": 5, "دم": 4}}, {"المعنى": "العاطفة والمشاعر", "القرائن": {"حب": 5, "مشاعر": 5}}, {"المعنى": "المركز", "القرائن": {"وسط": 5, "مركز": 5}}],
    "رأس": [{"المعنى": "جزء من جسم الإنسان", "القرائن": {"شعر": 4, "دماغ": 5}}, {"المعنى": "قمة أو أعلى شيء", "القرائن": {"جبل": 5, "قمة": 5}}],
    "يد": [{"المعنى": "عضو في جسم الإنسان", "القرائن": {"أصابع": 5, "كف": 5}}, {"المعنى": "المساعدة أو الدعم", "القرائن": {"مساعدة": 5, "دعم": 4}}],
    "نور": [{"المعنى": "الضوء الحقيقي", "القرائن": {"شمس": 5, "ضوء": 5}}, {"المعنى": "الهداية أو المعرفة", "القرائن": {"هداية": 5, "معرفة": 5}}]
}

# 4. الواجهة (Hero)
st.markdown('<div class="hero-container"><h1>✦ LABEEB AI</h1><p>المحلل الدلالي الذكي لفهم المعنى والسياق في اللغة العربية</p><div class="badge-student">© 2026 تم تطوير وتصميم بواسطة الطالبة هاجر الزواكي</div></div>', unsafe_allow_html=True)

# 5. منطقة الإدخال
user_text = st.text_area("", placeholder="اكتب جملتك هنا (مثال: فقد الجندي عينه في المعركة)...", key="main_input")
submit_btn = st.button("⚡تشغيل خوارزمية لبيب للتحليل")

# 6. منطق التحليل
if submit_btn and user_text.strip():
    st.markdown('<div class="glass-card"><div class="card-title">📊 نتيجة التحليل</div>', unsafe_allow_html=True)
    
    detected_keyword = next((word for word in semantic_db.keys() if word in user_text or (word == "عين" and any(k in user_text for k in ["عينه", "عينها", "العين"]))), None)
    
    if detected_keyword:
        with st.spinner("⏳ يجري تحليل المتجهات والروابط السياقية..."):
            results_list = []
            predicted_meaning = ""
            highest_score = 0
            
            for entry in semantic_db[detected_keyword]:
                matched_clues = sum(1 for clue in entry["القرائن"] if stemmer.light_stem(clue) and stemmer.get_stem() in user_text)
                score = min(0.20 + (matched_clues * 0.40), 0.95)
                results_list.append({"المعنى المحتمل": entry["المعنى"], "نسبة القرب": f"{score * 100:.0f}%"})
                if score > highest_score:
                    highest_score, predicted_meaning = score, entry["المعنى"]
            
            st.write(f"**المعنى الأقرب:** {predicted_meaning}")
            st.table(pd.DataFrame(results_list))
    else:
        st.info("لم يتم رصد لفظ مشترك معروف. جاري الاستعانة بالذكاء الاصطناعي...")
        model = genai.GenerativeModel('gemini-1.5-flash')
        st.write(model.generate_content(f"حلل الجملة التالية دلالياً: {user_text}").text)
    
    st.markdown('</div>', unsafe_allow_html=True)

# 7. التذييل
st.markdown('<div class="footer-text">LABEEB AI © 2026 — جميع الحقوق محفوظة — هاجر الزواكي</div>', unsafe_allow_html=True)
