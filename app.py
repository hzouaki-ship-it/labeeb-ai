import streamlit as st
import torch
import torch.nn.functional as F

from transformers import (
    AutoTokenizer,
    AutoModel
)

from tashaphyne.stemming import ArabicLightStemmer
from openai import OpenAI
# =========================================
# 1. إعداد الصفحة الأساسي والهوية البصرية
# =========================================
st.set_page_config(
    page_title="LABEEB AI - لبيب",
    page_icon="🧠",
    layout="wide"
)

# تعيين النمط الجمالي والـ CSS بأمان كامل لتجنب تداخل علامات الاقتباس
st.markdown('<style>'
' @import url("https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&family=Poppins:wght@400;600;700;800&display=swap");'

' html, body, [class*="css"] {'
'     font-family: "Cairo", sans-serif;'
'     direction: rtl;'
'     text-align: right;'
' }'
' .stApp {'
'     background: linear-gradient(135deg, #F8FAFC 0%, #F5F3FF 50%, #EFF6FF 100%) !important;'
' }'
' #MainMenu, footer, header {visibility: hidden;}'
' [data-testid="stMain"] .block-container {'
'     max-width: 1140px;'
'     padding-top: 2rem;'
'     padding-bottom: 4rem;'
'     margin: 0 auto;'
' }'
' /* HERO SECTION */'
' .hero-container {'
'     position: relative;'
'     background: linear-gradient(135deg, rgba(255, 255, 255, 0.85), rgba(243, 232, 255, 0.7));'
'     backdrop-filter: blur(20px);'
'     border: 1px solid rgba(255, 255, 255, 0.6);'
'     border-radius: 28px;'
'     padding: 35px 25px;'
'     text-align: center;'
'     box-shadow: 0 20px 40px rgba(109, 40, 217, 0.03);'
'     margin-bottom: 30px;'
' }'
' .hero-inline {'
'     display: flex;'
'     align-items: center;'
'     justify-content: center;'
'     gap: 35px;'
'     margin-bottom: 25px;'
' }'         
' .hero-brand {'
'     text-align: right;'
'     margin-top: 12px;'
' }'
' .brand-main {'
'     font-size: 42px;'
'     font-weight: 700;'
'     color: #5B21B6;'
'     line-height: 1.2;'
'     font-family: "Poppins", sans-serif;'
'     letter-spacing: 2px;'
'     margin-bottom: 10px;'
' }'
' .brand-ar {'
'     font-size: 38px;'
'     font-weight: 700;'
'     color: #6D28D9;'
'     font-family: "Cairo", sans-serif;'
'     line-height: 1;'
' }'
' .brand-ar span {'
'     font-size: 30px;'
'     color: #6D28D9;'
'     margin-left: 6px;'
'     vertical-align: middle;'
' }'            
' .brand-sub {'
'     font-size: 15px;'
'     letter-spacing: 3px;'
'     color: #4338CA;'
'     font-weight: 600;'
' }'           
' .hero-logo-img {'
'     width: 170px;'
'     height: 170px;'
'     object-fit: cover;'
'     border-radius: 50%;'
'     display: block;'
'     box-shadow: 0 0 40px rgba(109, 40, 217, 0.18);'
' }'
' .hero-title {'
'     font-size: 52px;'
'     margin-top: -5px;'
'     font-weight: 800;'
'     background: linear-gradient(90deg, #6D28D9, #4F46E5);'
'     -webkit-background-clip: text;'
'     -webkit-text-fill-color: transparent;'
'     margin-bottom: 8px;'
' }'
' .hero-subtitle {'
'     font-size: 22px;'
'     font-weight: 700;'
'     color: #1E293B;'
'     margin-bottom: 12px;'
' }'
' .hero-desc {'
'     font-size: 16px;'
'     color: #64748B;'
'     max-width: 650px;'
'     margin: 0 auto 20px auto;'
'     line-height: 1.7;'
' }'
' .badge-student {'
'     display: inline-block;'
'     background: rgba(255, 255, 255, 0.9);'
'     border: 1px solid #E9D5FF;'
'     padding: 6px 18px;'
'     border-radius: 999px;'
'     font-size: 13px;'
'     font-weight: 600;'
'     color: #6D28D9;'
' }'
' /* GLASS CARDS */'
' .glass-card {'
'     background: rgba(255, 255, 255, 0.85);'
'     backdrop-filter: blur(20px);'
'     border: 1px solid rgba(255, 255, 255, 0.5);'
'     border-radius: 22px;'
'     padding: 30px;'
'     box-shadow: 0 10px 30px rgba(0, 0, 0, 0.01);'
'     margin-bottom: 25px;'
' }'
' .card-title {'
'     font-size: 20px;'
'     font-weight: 700;'
'     color: #1E293B;'
'     margin-bottom: 16px;'
'     display: flex;'
'     align-items: center;'
'     gap: 8px;'
' }'
' .stTextArea textarea {'
'     border-radius: 14px !important;'
'     border: 1px solid #E2E8F0 !important;'
'     padding: 16px !important;'
'     font-size: 16px !important;'
'     background: rgba(255, 255, 255, 0.7) !important;'
'     font-family: "Cairo", sans-serif !important;'
' }'
' .stButton > button {'
'     background: linear-gradient(90deg, #4F46E5, #6D28D9) !important;'
'     color: white !important;'
'     border: none !important;'
'     border-radius: 12px !important;'
'     padding: 12px 28px !important;'
'     font-size: 16px !important;'
'     font-weight: 700 !important;'
'     width: 100% !important;'
'     font-family: "Cairo", sans-serif !important;'
'     box-shadow: 0 6px 16px rgba(109, 40, 217, 0.15) !important;'
'     transition: all 0.2s ease;'
' }'
' .stButton > button:hover {'
'     transform: translateY(-1px);'
'     box-shadow: 0 10px 20px rgba(109, 40, 217, 0.25) !important;'
' }'
' /* RESULT COMPONENT */'
' .result-status-empty {'
'     text-align: center;'
'     color: #94A3B8;'
'     font-size: 15px;'
'     padding: 25px 0;'
' }'
' .result-badge-container {'
'     display: flex;'
'     gap: 14px;'
'     margin-bottom: 20px;'
' }'
' .result-stat-box {'
'     flex: 1;'
'     background: white;'
'     border: 1px solid #F3E8FF;'
'     padding: 14px;'
'     border-radius: 14px;'
'     text-align: center;'
' }'
' .result-stat-label {'
'     font-size: 13px;'
'     color: #64748B;'
'     margin-bottom: 2px;'
' }'
' .result-stat-val {'
'     font-size: 18px;'
'     font-weight: 700;'
'     color: #6D28D9;'
' }'
' /* HOW IT WORKS */'
' .section-main-title {'
'     text-align: center;'
'     font-size: 26px;'
'     font-weight: 800;'
'     color: #1E293B;'
'     margin: 40px 0 20px 0;'
' }'
' .step-card {'
'     background: white;'
'     border: 1px solid #F1F5F9;'
'     border-radius: 18px;'
'     padding: 22px;'
'     text-align: center;'
'     box-shadow: 0 4px 12px rgba(0, 0, 0, 0.01);'
' }'
' .step-icon {'
'     font-size: 28px;'
'     margin-bottom: 8px;'
' }'
' .step-title {'
'     font-size: 17px;'
'     font-weight: 700;'
'     color: #1E293B;'
'     margin-bottom: 6px;'
' }'
' .step-desc {'
'     font-size: 14px;'
'     color: #64748B;'
'     line-height: 1.6;'
' }'
' /* RESEARCHER CARD */'
' .researcher-card {'
'     background: white;'
'     border: 1px solid #EEF2F6;'
'     border-radius: 20px;'
'     padding: 24px;'
'     box-shadow: 0 8px 20px rgba(0, 0, 0, 0.01);'
'     margin-top: 40px;'
' }'

' .researcher-img {'
'     width: 110px !important;'
'     height: 110px !important;'
'     min-width: 110px !important;'
'     max-width: 110px !important;'
'     border-radius: 50% !important;'
'     object-fit: cover !important;'
'     border: 3px solid #F3E8FF !important;'
'     display: block !important;'
'     overflow: hidden !important;'
' }'
' .researcher-flex {'
'     display: flex;'
'     align-items: center;'
'     justify-content: flex-start;'
'     gap: 24px;'
'     direction: rtl;'
'     text-align: right;'
' }'
 ' .researcher-name {'
'     font-size: 20px;'
'     font-weight: 800;'
'     color: #1E293B;'
'     margin-bottom: 2px;'
' }'   
' .researcher-title {'
'     font-size: 15px;'
'     font-weight: 600;'
'     color: #6D28D9;'
'     margin-bottom: 8px;'
' }'
' .researcher-bio {'
'     font-size: 14px;'
'     color: #475569;'
'     line-height: 1.7;'
' }'
' .footer-text {'
'     text-align: center;'
'     color: #94A3B8;'
'     font-size: 13px;'
'     margin-top: 50px;'
'     border-top: 1px solid #E2E8F0;'
'     padding-top: 20px;'
' }'
'</style>', unsafe_allow_html=True)


# =========================================
# 1. إعداد الصفحة
# =========================================

st.set_page_config(
    page_title="LABEEB AI",
    page_icon="🧠",
    layout="wide"
)

# =========================================
# 2. CSS الجمالي
# =========================================

st.markdown(
    """
    <style>

    .hero-container{
        text-align:center;
        padding:35px;
    }

    .hero-title{
        font-size:58px;
        font-weight:800;
        color:#4F46E5;
    }

    .hero-sub{
        color:#64748B;
        font-size:18px;
        margin-top:10px;
    }

    .glass-card{
        background:rgba(255,255,255,0.93);
        backdrop-filter:blur(12px);
        border-radius:24px;
        padding:28px;
        margin-top:22px;
        border:1px solid #E2E8F0;
        box-shadow:0 8px 24px rgba(0,0,0,0.06);
    }

    .footer-text{
        text-align:center;
        color:#94A3B8;
        margin-top:60px;
        font-size:13px;
    }

    .stButton > button{

        background:linear-gradient(
            90deg,
            #4F46E5,
            #6D28D9
        ) !important;

        color:white !important;

        border:none !important;

        border-radius:14px !important;

        width:100% !important;

        height:54px !important;

        font-size:18px !important;

        font-weight:bold !important;
    }

    textarea{
        direction:rtl !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================
# 3. أدوات المعالجة
# =========================================

stemmer = ArabicLightStemmer()

# =========================================
# 4. تحميل AraBERT
# =========================================

@st.cache_resource
def load_arabert():

    tokenizer = AutoTokenizer.from_pretrained(
        "aubmindlab/bert-base-arabertv02"
    )

    model = AutoModel.from_pretrained(
        "aubmindlab/bert-base-arabertv02"
    )

    return tokenizer, model

tokenizer, arabert_model = load_arabert()

# =========================================
# 5. OpenRouter
# =========================================

client = None

if "OPENROUTER_API_KEY" in st.secrets:

    client = OpenAI(

        api_key=st.secrets["OPENROUTER_API_KEY"],

        base_url="https://openrouter.ai/api/v1"
    )

# =========================================
# 6. استخراج Embedding
# =========================================

def get_embedding(text):

    inputs = tokenizer(

        text,

        return_tensors="pt",

        truncation=True,

        padding=True,

        max_length=128
    )

    with torch.no_grad():

        outputs = arabert_model(**inputs)

    embedding = outputs.last_hidden_state[:, 0, :]

    return embedding

# =========================================
# 7. حساب التشابه الدلالي
# =========================================

def semantic_similarity(text1, text2):

    emb1 = get_embedding(text1)

    emb2 = get_embedding(text2)

    similarity = F.cosine_similarity(
        emb1,
        emb2
    )

    return similarity.item()

# =========================================
# 8. قاعدة البيانات الدلالية
# =========================================

semantic_db = {

    "عين": {

        "عضو البصر":
        "الرؤية والنظر والدموع والبصر",

        "نبع ماء":
        "الماء والينبوع والشرب والطبيعة",

        "جاسوس":
        "التجسس والمراقبة والعدو"
    },

    "نار": {

        "لهب حقيقي":
        "الحريق والحرارة والدخان",

        "حماس عاطفي":
        "المشاعر والحب والحماس",

        "حرب أو فتن":
        "الصراع والقتال"
    },

    "روح": {

        "نفس بشرية":
        "الحياة والإنسان والوفاة",

        "جانب معنوي":
        "المشاعر والطاقة الداخلية",

        "عالم الغيب":
        "الأرواح والميتافيزيقا"
    },

    "قلب": {

        "عضو حيوي":
        "النبض والدم والجسد",

        "العاطفة والمشاعر":
        "الحب والإحساس والمشاعر"
    }
}

# =========================================
# 9. الواجهة
# =========================================

st.markdown(
    """
    <div class="hero-container">

        <div class="hero-title">
            ✦ LABEEB AI
        </div>

        <div class="hero-sub">
            المحلل الدلالي السياقي للغة العربية
        </div>

    </div>
    """,
    unsafe_allow_html=True
)

user_text = st.text_area(
    "أدخلي الجملة:",
    placeholder="مثال: أشعلت كلماتها نار الحماس في قلبه..."
)

submit_btn = st.button(
    "⚡ تحليل دلالي ذكي"
)

# =========================================
# 10. التحليل
# =========================================

if submit_btn and user_text.strip():

    with st.spinner(
        "⏳ جاري تحليل السياق الدلالي..."
    ):

        words = user_text.split()

        found_target = None

        # =====================================
        # الكشف عن اللفظ المشترك
        # =====================================

        for word in words:

            stemmer.light_stem(word)

            word_stem = stemmer.get_stem()

            for key in semantic_db.keys():

                stemmer.light_stem(key)

                key_stem = stemmer.get_stem()

                if word_stem == key_stem:

                    found_target = key
                    break

            if found_target:
                break

        # =====================================
        # التحليل باستخدام AraBERT
        # =====================================

        if found_target:

            meanings = semantic_db[
                found_target
            ]

            best_meaning = ""

            highest_similarity = -1

            all_results = []

            for meaning, context in meanings.items():

                similarity = semantic_similarity(
                    user_text,
                    context
                )

                all_results.append(
                    (meaning, similarity)
                )

                if similarity > highest_similarity:

                    highest_similarity = similarity

                    best_meaning = meaning

            # =================================
            # التحليل الذكي
            # =================================

            ai_analysis = ""

            if client:

                try:

                    response = client.chat.completions.create(

                        model="openrouter/auto",

                        messages=[

                            {
                                "role": "system",
                                "content":
                                """
                                أنت محلل دلالي عربي متخصص.

                                حلل الجملة دلالياً اعتماداً على السياق.

                                أجب بهذا الشكل فقط:

                                - المعنى المقصود
                                - هل الاستعمال حقيقي أم مجازي
                                - تفسير مختصر جداً

                                يجب أن يكون الجواب قصيراً وواضحاً.

                                ممنوع:
                                - الشرح البلاغي الطويل
                                - الإعراب
                                - أنواع الاستعارة
                                - التفصيل الأدبي
                                - التوسع
                                """
                            },

                            {
                                "role": "user",
                                "content": user_text
                            }
                        ]
                    )

                    ai_analysis = (
                        response
                        .choices[0]
                        .message
                        .content
                    )

                except Exception as e:

                    ai_analysis = (
                        f"تعذر تنفيذ التحليل الذكي: {e}"
                    )

            # =================================
            # عرض النتيجة
            # =================================

            st.markdown(
                f"""
                <div class="glass-card">

                    <h3>
                    🔍 التحليل الدلالي المرجح
                    </h3>

                    <p>
                    <b>اللفظ المكتشف:</b>
                    {found_target}
                    </p>

                    <p>
                    <b>المعنى السياقي الأرجح:</b>
                    {best_meaning}
                    </p>

                    <p>
                    <b>نسبة التشابه الدلالي:</b>
                    {highest_similarity:.2%}
                    </p>

                    <p>
                    <b>التفسير الدلالي:</b><br>
                    {ai_analysis}
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )

            # =================================
            # عرض الاحتمالات
            # =================================

            st.markdown(
                """
                <div class="glass-card">

                <h3>
                📊 احتمالات المعنى
                </h3>
                """,
                unsafe_allow_html=True
            )

            for meaning, similarity in all_results:

                st.write(
                    f"• {meaning} → "
                    f"{similarity:.2%}"
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

        else:

            # =================================
            # التحليل الذكي الكامل
            # =================================

            if client:

                try:

                    response = client.chat.completions.create(

                        model="openrouter/auto",

                        messages=[

                            {
                                "role": "system",
                                "content":
                                """
                                أنت محلل دلالي عربي متخصص.

                                حلل الجملة دلالياً اعتماداً على السياق.

                                أجب باختصار شديد.

                                حدد:
                                - المعنى المقصود
                                - هل المعنى مجازي أم حقيقي
                                - تفسير مختصر جداً
                                """
                            },

                            {
                                "role": "user",
                                "content": user_text
                            }
                        ]
                    )

                    ai_result = (
                        response
                        .choices[0]
                        .message
                        .content
                    )

                    st.markdown(
                        f"""
                        <div class="glass-card">

                        <h3>
                        🤖 التحليل الذكي
                        </h3>

                        <p>
                        {ai_result}
                        </p>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                except Exception as e:

                    st.error(
                        f"تعذر الاتصال بالمحرك الذكي: {e}"
                    )

            else:

                st.warning(
                    "لم يتم العثور على مفتاح OpenRouter API."
 =========================================
#10. بطاقة الباحثة (RESEARCHER SECTION)
# =========================================
st.markdown('<div class="researcher-card">'
' <div class="researcher-flex">'
'     <img src="https://raw.githubusercontent.com/hzouaki-ship-it/labeeb-ai/main/hajar.jpg" class="researcher-img" alt="Hajar Zouaki" width="85">'
'     <div style="text-align:right;">'
'         <div class="researcher-name">هاجر الزواكي</div>'
'         <div class="researcher-title">طالبة ماستر في اللسانيات الرقمية والعربية | كلية الآداب والعلوم الإنسانية — جامعة مولاي إسماعيل، مكناس</div>'
'         <div class="researcher-bio">مهتمة بالذكاء الاصطناعي ومعالجة اللغة العربية وبناء الأنظمة الدلالية الذكية وأسعى إلى تطوير حلول رقمية حديثة لفهم اللغة العربية وتحليل السياق والمعنى.</div>'
'     </div>'
' </div>'
'</div>', unsafe_allow_html=True)                )

# =========================================
# 11. التذييل
# =========================================
st.markdown('<div class="footer-text">LABEEB AI © 2026 — جميع الحقوق محفوظة — هاجر الزواكي</div>', unsafe_allow_html=True)
l=True
)
