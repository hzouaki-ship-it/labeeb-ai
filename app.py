import streamlit as st
import torch
import torch.nn.functional as F
import nltk
from nltk.corpus import wordnet as wn
from tashaphyne.stemming import ArabicLightStemmer
from transformers import AutoTokenizer, AutoModel

# --- 1. الإعدادات ---
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)
stemmer = ArabicLightStemmer()

st.set_page_config(page_title="LABEEB AI - النظام الدلالي", page_icon="🧠", layout="wide")

# --- 2. CSS ---
st.markdown("""
    <style>
    .hero-container { text-align: center; padding: 30px; }
    .glass-card { background: rgba(255,255,255,0.92); backdrop-filter: blur(10px); border-radius: 22px; padding: 25px; margin-top: 20px; border: 1px solid #E2E8F0; box-shadow: 0 8px 20px rgba(0,0,0,0.06); }
    .footer-text { text-align: center; color: #94A3B8; margin-top: 60px; font-size: 13px; }
    .stButton > button { background: linear-gradient(90deg,#4F46E5,#6D28D9) !important; color: white !important; border-radius: 12px !important; width: 100% !important; height: 50px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. محرك AraBERT ---
@st.cache_resource
def load_arabert():
    tokenizer = AutoTokenizer.from_pretrained("aubmindlab/bert-base-arabertv02")
    model = AutoModel.from_pretrained("aubmindlab/bert-base-arabertv02")
    return tokenizer, model

tokenizer, arabert_model = load_arabert()

def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        outputs = arabert_model(**inputs)
    # استخدام [CLS] token للتمثيل الدلالي
    return outputs.last_hidden_state[:, 0, :]

def semantic_similarity(text1, text2):
    emb1 = get_embedding(text1)
    emb2 = get_embedding(text2)
    return F.cosine_similarity(emb1, emb2).item()

# --- 4. قاعدة البيانات الدلالية ---
semantic_db = {
    "عين": ["عضو بصر", "نبع ماء", "جاسوس"],
    "روح": ["نفس بشرية", "جانب معنوي", "عالم الغيب"],
    "نار": ["لهب حقيقي", "حماس عاطفي", "حرب أو فتن"]
}

# --- 5. الواجهة ---
st.markdown('<div class="hero-container"><h1>✦ LABEEB AI</h1><p>المحلل الدلالي الأكاديمي</p></div>', unsafe_allow_html=True)
user_text = st.text_area("أدخلي الجملة:", placeholder="مثال: أشعلت كلماتها نار الحماس...")
submit_btn = st.button("⚡ تحليل دلالي متقدم")

# --- 6. منطق التحليل ---
if submit_btn and user_text.strip():
    with st.spinner("⏳ جاري التحليل الدلالي السياقي..."):
        words = user_text.split()
        found_target = None
        
        # أ) البحث عن اللفظ في DB
        for word in words:
            stemmer.light_stem(word)
            stem = stemmer.get_stem()
            if stem in [stemmer.light_stem(k) for k in semantic_db.keys()]:
                found_target = word
                break
        
        if found_target:
            candidates = semantic_db.get(found_target, ["معنى عام"])
            best_meaning = None
            max_sim = -1
            
            # ب) مقارنة السياق لاختيار المعنى الأفضل
            results = []
            for meaning in candidates:
                sim = semantic_similarity(user_text, f"{found_target} تعني {meaning}")
                results.append((meaning, sim))
                if sim > max_sim:
                    max_sim = sim
                    best_meaning = meaning
            
            # ج) العرض في glass-card
            st.markdown(f"""
                <div class="glass-card">
                    <h3>🔍 التحليل الدلالي المرجح</h3>
                    <p><b>اللفظ المكتشف:</b> {found_target}</p>
                    <p><b>المعنى السياقي الأرجح:</b> {best_meaning}</p>
                    <p><b>نسبة الثقة (Similarity):</b> {max_sim:.2%}</p>
                    <p><b>التفسير:</b> قام لبيب بتحليل المتجهات الدلالية (Embeddings) وقارنها 
                    بالمعاني المحتملة، ووجد أن سياق جملتك يتطابق مع هذا المعنى.</p>
                </div>
            """, unsafe_allow_html=True)
            
            # د) استنتاج المجاز
            if max_sim < 0.6:
                st.info("💡 ملاحظة: قد تحتوي الجملة على استعارة أو معنى مجازي غير مألوف.")
        else:
            st.warning("لم يتم العثور على لفظ محدد في قاعدة البيانات المعجمية.")

st.markdown('<div class="footer-text">LABEEB AI © 2026 — هاجر الزواكي</div>', unsafe_allow_html=True)
