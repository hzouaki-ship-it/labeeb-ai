import streamlit as st
import pandas as pd
import time

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
'     width: 85px !important;'
'     height: 85px !important;'
'     min-width: 85px !important;'
'     max-width: 85px !important;'
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
# 2. قاعدة البيانات المعجمية المستقرة
# =========================================
semantic_db = {
    "عين": [
        {"المعنى": "عضو البصر والرؤية", "القرائن": ["طفل", "أصيب", "بصر", "طبيب", "نظارات", "رؤية", "جندي", "فقد", "عينه", "عينها"]},
        {"المعنى": "نبع ماء طبيعي", "القرائن": ["ماء", "شرب", "عذب", "واحة", "بئر", "تدفق", "نبع", "ساقية"]},
        {"المعنى": "جاسوس ومراقب سري", "القرائن": ["قائد", "عدو", "جاسوس", "رصد", "تحركات", "استطلاع", "جيش", "حرب"]}
    ],
    "المغرب": [
        {"المعنى": "المملكة المغربية (الدولة)", "القرائن": ["سافر", "دولة", "رباط", "فاس", "مكناس", "مملكة", "سياحة", "تاريخ"]},
        {"المعنى": "صلاة المغرب (الوقت)", "القرائن": ["صلاة", "أذان", "مسجد", "صليت", "مصلون", "إفطار", "رمضان", "وقت"]}
    ],
    "رأس": [
        {"المعنى": "عضو في جسم الإنسان", "القرائن": ["ألم", "صداع", "شعر", "طبيب", "جسم", "تفكير", "مخ", "وجع"]},
        {"المعنى": "قمة جغرافية مرتفعة", "القرائن": ["جبل", "تسلق", "قمة", "وصل", "منحدر", "مرتفع", "صخور"]}
    ]
}

# =========================================
# 3. عرض الهيكل البصري (HERO SECTION)
# =========================================
st.markdown('<div class="hero-container">'

' <div class="hero-inline">'

'     <div class="hero-brand">'

'          <div class="brand-main"><span>✦</span> LABEEB AI</div>'

'          <div class="brand-sub">CONTEXTUAL SEMANTIC ANALYZER</div>'

'     </div>'

'     <img src="https://raw.githubusercontent.com/hzouaki-ship-it/labeeb-ai/main/logo.png" class="hero-logo-img">'

' </div>'

' <div class="hero-subtitle">المحلل الدلالي الذكي لفهم المعنى والسياق في اللغة العربية</div>'

' <div class="hero-desc">منصة تعتمد على الذكاء الاصطناعي لتحليل النصوص العربية وفهم معناها العميق في السياق.</div>'

' <div class="badge-student">© 2026 تم تطوير وتصميم بواسطة الطالبة هاجر الزواكي</div>'

'</div>', unsafe_allow_html=True)
# =========================================
# 4. بطاقة الإدخال (INPUT SECTION)
# =========================================
st.markdown('<div class="glass-card">'
' <div class="card-title">🖋️ ابدأ التحليل</div>'
'</div>', unsafe_allow_html=True)

user_text = st.text_area(
    "",
    placeholder="اكتب جملتك هنا (مثال: فقد الجندي عينه في المعركة)...",
    key="main_input",
    label_visibility="collapsed"
)
submit_btn = st.button("⚡تشغيل خوارزمية لبيب للتحليل")

st.markdown('<div style="text-align:center; color:#94A3B8; font-size:13px; margin-top:-10px; margin-bottom:20px;">تحليل آمن ودقيق باستخدام الذكاء الاصطناعي</div>', unsafe_allow_html=True)

# =========================================
# 5. بطاقة النتائج (RESULT SECTION)
# =========================================
st.markdown('<div class="glass-card">'
' <div class="card-title">📊 نتيجة التحليل</div>', unsafe_allow_html=True)

if submit_btn and user_text.strip():
    detected_keyword = None
    for word in semantic_db.keys():
        if word in user_text or (word == "عين" and ("عينه" in user_text or "عينها" in user_text or "العين" in user_text)):
            detected_keyword = word
            break
            
    if detected_keyword:
        with st.spinner("⏳ يجري تحليل المتجهات والروابط السياقية..."):
            time.sleep(0.4)
            
            results_list = []
            highest_score = 0.0
            predicted_meaning = ""
            
            for entry in semantic_db[detected_keyword]:
                base_score = 0.20
                matched_clues = 0
                
                for clue in entry["القرائن"]:
                    if clue in user_text:
                        matched_clues += 1
                        
                if matched_clues > 0:
                    score = base_score + (matched_clues * 0.40)
                else:
                    score = base_score
                    
                if score > 0.95: score = 0.95
                
                results_list.append({
                    "المعنى المحتمل": entry["المعنى"],
                    "نسبة القرب": f"{score * 100:.2f}%",
                    "_raw": score
                })
                
                if score > highest_score:
                    highest_score = score
                    predicted_meaning = entry["المعنى"]
            
            # عرض الكروت الرقمية العلوية
            st.markdown('<div class="result-badge-container">'
            ' <div class="result-stat-box">'
            '     <div class="result-stat-label">المعنى الأقرب</div>'
            '     <div class="result-stat-val">' + predicted_meaning + '</div>'
            ' </div>'
            ' <div class="result-stat-box">'
            '     <div class="result-stat-label">نسبة القرب الدلالي</div>'
            '     <div class="result-stat-val">' + f"{highest_score * 100:.2f}%" + '</div>'
            ' </div>'
            '</div>', unsafe_allow_html=True)
            
            # عرض الجدول بخانتين نظيفتين فقط
            df_clean = pd.DataFrame(results_list).sort_values(by="_raw", ascending=False).drop(columns=["_raw"])
            st.table(df_clean)
    else:
        st.markdown('<div class="result-stat-box" style="width:100%;">'
        ' <div class="result-stat-label">حالة البنية اللغوية</div>'
        ' <div class="result-stat-val" style="color: #64748B; font-size:15px;">لم يتم رصد لفظ مشترك معروف (عين، المغرب، رأس)</div>'
        '</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="result-status-empty">🤖 لم يتم إجراء أي تحليل بعد. اكتب نصاً واضغط على الزر لبدء المعالجة.</div>', unsafe_allow_html=True)
    
st.markdown('</div>', unsafe_allow_html=True)

# =========================================
# 6. قسم خطوات العمل (HOW IT WORKS)
# =========================================
st.markdown('<div class="section-main-title">كيف يعمل لبيب؟</div>', unsafe_allow_html=True)

col_w1, col_w2, col_w3 = st.columns(3)
with col_w1:
    st.markdown('<div class="step-card">'
    ' <div class="step-icon">🔎</div>'
    ' <div class="step-title">تحليل السياق</div>'
    ' <div class="step-desc">يقوم النظام بفحص البنية التركيبية المحيطة باللفظ المشترك، وعزل الكلمات المحورية المحيطة به بدقة وعناية.</div>'
    '</div>', unsafe_allow_html=True)
with col_w2:
    st.markdown('<div class="step-card">'
    ' <div class="step-icon">✨</div>'
    ' <div class="step-title">اكتشاف المعنى</div>'
    ' <div class="step-desc">تُطابق البيئة السياقية الحالية مع الحقول والمؤشرات المعجمية المخزنة لتحديد الإحالة المعنوية الأنسب للفظ.</div>'
    '</div>', unsafe_allow_html=True)
with col_w3:
    st.markdown('<div class="step-card">'
    ' <div class="step-icon">📊</div>'
    ' <div class="step-title">قياس التشافه الدلالي</div>'
    ' <div class="step-desc">يتم حساب أوزان ومعاملات المطابقة الإحصائية لإنتاج جدول دقيق يرتب الاحتمالات ترتيباً تصاعدياً بحسب النسبة.</div>'
    '</div>', unsafe_allow_html=True)

# =========================================
# 7. بطاقة الباحثة (RESEARCHER SECTION)
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
'</div>', unsafe_allow_html=True)
# =========================================
# 8. التذييل (FOOTER)
# =========================================
st.markdown('<div class="footer-text">LABEEB AI © 2026 — جميع الحقوق محفوظة — هاجر الزواكي</div>', unsafe_allow_html=True)
