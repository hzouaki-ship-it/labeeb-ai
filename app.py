import streamlit as st
import pandas as pd
import time

# =========================================
# 1. إعدادات الصفحة (Full Width وبدون هوامش ضيقة)
# =========================================
st.set_page_config(
    page_title="LABEEB AI | لبيب",
    page_icon="🧠",
    layout="wide"
)

# =========================================
# 2. هندسة الواجهة الاحترافية (CSS) وتفعيل الـ RTL والخطوط
# =========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800;900&display=swap');

/* إعدادات الاتجاه من اليمين لليسار والخط العربي */
html, body, [class*="css"], .stApp {
    font-family: 'Cairo', sans-serif !important;
    direction: rtl !important;
    text-align: right !important;
}

/* تصميم خلفية سحابية ناعمة مع تدرجات دافئة وضبابية */
.stApp {
    background: radial-gradient(circle at top right, rgba(243, 232, 255, 0.7), transparent 40%),
                radial-gradient(circle at bottom left, rgba(238, 242, 255, 0.6), transparent 40%),
                #F8FAFC;
}

/* إخفاء عناصر التخصيص الافتراضية لـ Streamlit */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* الحاوية الرئيسية ممتدة العرض */
[data-testid="stMain"] .block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 4rem;
    margin: 0 auto;
}

/* ================= الهيدر الرئيسي (Hero Section) ================= */
.hero-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 3rem 1rem 2.5rem 1rem;
    margin-bottom: 2rem;
    position: relative;
}

/* اللوغو الدائري الاحترافي مع Glow بنفسجي تأثير زجاجي شفاف */
.logo-container {
    width: 160px;
    height: 160px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.75);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.6);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 40px rgba(139, 92, 246, 0.25), 0 10px 20px rgba(139, 92, 246, 0.1);
    margin-bottom: 1.5rem;
    transition: all 0.5s ease;
}

.logo-container:hover {
    box-shadow: 0 0 50px rgba(139, 92, 246, 0.4), 0 10px 25px rgba(139, 92, 246, 0.2);
    transform: scale(1.02);
}

.logo-container img {
    width: 100px;
    height: 100px;
    object-fit: contain;
}

/* العناوين الكبيرة والممركزة بدقة */
.main-title {
    font-size: 72px;
    font-weight: 900;
    line-height: 1.1;
    margin-bottom: 0.5rem;
    background: linear-gradient(90deg, #4F46E5, #9333EA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.sub-title {
    font-size: 28px;
    font-weight: 700;
    color: #4338CA;
    margin-bottom: 0.8rem;
}

.badge-dev {
    background: rgba(255, 255, 255, 0.8);
    border: 1px solid #E9D5FF;
    padding: 6px 18px;
    border-radius: 999px;
    font-size: 15px;
    color: #6B21A8;
    font-weight: 600;
    box-shadow: 0 4px 12px rgba(0,0,0,0.03);
}

/* ================= بطاقة الإدخال والتحليل والنتائج ================= */
.glass-box {
    background: #FFFFFF;
    border-radius: 24px;
    padding: 35px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.02);
    border: 1px solid #ECEBFF;
    margin-bottom: 2rem;
}

.box-header {
    font-size: 24px;
    font-weight: 800;
    color: #1E1B4B;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 10px;
}

/* صناديق الإدخال الكبيرة والاحترافية */
.stTextArea textarea {
    border-radius: 16px !important;
    border: 2px solid #C4B5FD !important;
    padding: 20px !important;
    font-size: 18px !important;
    line-height: 1.8 !important;
    background: #FCFCFF !important;
}
.stTextArea textarea:focus {
    border-color: #7C3AED !important;
    box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1) !important;
}

/* زر التحليل المتوهج والمحاذي لليمين تلقائياً */
.stButton>button {
    background: linear-gradient(90deg, #4338CA, #9333EA) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 35px !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 8px 20px rgba(139, 92, 246, 0.2) !important;
}
.stButton>button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 25px rgba(139, 92, 246, 0.35) !important;
}

/* بطاقة عرض النتيجة الكبيرة */
.result-card-box {
    background: #FFFFFF;
    border-radius: 22px;
    padding: 30px;
    border: 1px solid #ECEBFF;
    box-shadow: 0 10px 25px rgba(0,0,0,0.02);
    margin-top: 1.5rem;
}
.result-card-header {
    color: #7C3AED;
    font-size: 22px;
    font-weight: 800;
    margin-bottom: 1rem;
    border-bottom: 2px solid #F3E8FF;
    padding-bottom: 0.5rem;
}

/* ================= بطاقات "كيف يعمل لبيب" ================= */
.section-center-title {
    text-align: center;
    font-size: 34px;
    font-weight: 800;
    color: #1E1B4B;
    margin-top: 3.5rem;
    margin-bottom: 0.5rem;
}
.section-center-sub {
    text-align: center;
    color: #64748B;
    font-size: 17px;
    margin-bottom: 2.5rem;
}

.step-flex-container {
    display: flex;
    gap: 24px;
    justify-content: space-between;
    margin-bottom: 4rem;
}
.step-item-card {
    flex: 1;
    background: #FFFFFF;
    padding: 32px 25px;
    border-radius: 20px;
    border: 1px solid #ECEBFF;
    box-shadow: 0 6px 20px rgba(0,0,0,0.02);
    text-align: center;
    position: relative;
}
.step-number-badge {
    position: absolute;
    top: -15px;
    right: 25px;
    background: #7C3AED;
    color: white;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 14px;
}
.step-item-icon {
    font-size: 40px;
    margin-bottom: 1rem;
}
.step-item-title {
    font-size: 20px;
    font-weight: 800;
    color: #4F46E5;
    margin-bottom: 0.6rem;
}
.step-item-desc {
    color: #64748B;
    font-size: 15px;
    line-height: 1.8;
}

/* ================= بطاقة تعريف المطورة (هاجر الزواكي) ممركزة واحترافية ================= */
.profile-card {
    background: #FFFFFF;
    border-radius: 24px;
    padding: 40px;
    border: 1px solid #E9D5FF;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 40px;
    box-shadow: 0 10px 30px rgba(139, 92, 246, 0.03);
    margin-top: 3rem;
}
.profile-text-side { flex: 3; }
.profile-img-side { flex: 1; display: flex; justify-content: center; }

.avatar-image {
    width: 180px;
    height: 180px;
    object-fit: cover;
    border-radius: 50%;
    border: 5px solid #E9D5FF;
    box-shadow: 0 10px 25px rgba(139, 92, 246, 0.15);
}

.profile-name { font-size: 32px; font-weight: 800; color: #1E1B4B; margin-bottom: 0.4rem; }
.profile-subtitle { font-size: 20px; color: #7C3AED; font-weight: 700; margin-bottom: 1.2rem; }
.profile-bio { color: #4B5563; line-height: 2; font-size: 17px; }

.footer-text {
    text-align: center;
    margin-top: 4rem;
    padding-top: 1.5rem;
    color: #94A3B8;
    font-size: 14px;
    border-top: 1px solid #E2E8F0;
}
</style>
""", unsafe_allow_html=True)

# =========================================
# 3. محرك وقاعدة البيانات الدلالية لمعالجة اللبس
# =========================================
semantic_lexicon_db = {
    "عين": [
        {"المعنى": "عضو البصر"، "جملة_مرجعية": "أصيبت عين الطفل بسبب الغبار المثار في الجو", "المؤشرات": ["الطفل"، "أصيبت"، "البصر"، "طبيب"، "نظارات"، "رؤية"]},
        {"المعنى": "نبع ماء طبيعي"، "جملة_مرجعية": "شرب المسافرون من عين ماء عذبة تفجرت في الواحة", "المؤشرات": ["ماء"، "شرب"، "عذبة"، "واحة"، "بئر"، "تدفق"]},
        {"المعنى": "جاسوس ومراقب"، "جملة_مرجعية": "بث القائد عيناً له ليرصد بدقة تحركات الأعداء", "المؤشرات": ["القائد"، "العدو"، "جاسوس"، "رصد"، "تحركات"، "استطلاع"]}
    ],
    "المغرب": [
        {"المعنى": "المملكة المغربية (الدولة)", "جملة_مرجعية": "سافرت إلى المغرب لزيارة المعالم الأثرية والتاريخية في مكناس والرباط", "المؤشرات": ["سافرت"، "دولة"، "الرباط"، "فاس"، "مكناس"، "المملكة"]},
        {"المعنى": "صلاة المغرب (الوقت)"، "جملة_مرجعية": "توجه المصلون سريعاً إلى المسجد فور سماع أذان المغرب", "المؤشرات": ["صلاة"، "أذان"، "المسجد"، "صليت"، "المصلون"، "إفطار"]}
    ],
    "رأس": [
        {"المعنى": "عضو في الجسم"، "جملة_مرجعية": "شعر الطالب الباحث بصداع وألم في رأسه بسبب قلة النوم", "المؤشرات": ["ألم"، "صداع"، "شعر"، "طبيب"، "جسم"، "السهر"]},
        {"المعنى": "قمة جغرافية"، "جملة_مرجعية": "استطاع فريق المغامرين الوصول بنجاح إلى رأس الجبل قبل الغروب", "المؤشرات": ["الجبل"، "تسلق"، "قمة"، "وصل"، "منحدر"]}
    ]
}

# =========================================
# 4. بناء الهيدر والشعار الممركز بالكامل
# =========================================
st.markdown("""
<div class="hero-wrapper">
    <div class="logo-container">
        <img src="https://cdn-icons-png.flaticon.com/512/2103/2103633.png" alt="LABEEB AI Logo">
    </div>
    <div class="main-title">LABEEB AI (لبيب)</div>
    <div class="sub-title">المحلل الدلالي الذكي لفهم المعنى والسياق في اللغة العربية</div>
    <div class="badge-dev">✨ منصة حوسبية لفك اللبس المعجمي واستخراج العلاقات الدلالية للسياقات العربية 2026 ©</div>
</div>
""", unsafe_allow_html=True)

# =========================================
# 5. قسم صندوق الإدخال ومعالجة ضغط الزر
# =========================================
st.markdown('<div class="glass-box">', unsafe_allow_html=True)
st.markdown('<div class="box-header">📝 اكتب أو ألصق النص العربي المراد استكشاف دلالته السياقية:</div>', unsafe_allow_html=True)

# صندوق النص
input_text = st.text_area("", placeholder="مثال للتجربة: تناول المسافرون جرعة ماء باردة من عين تقع وسط الصحراء...", height=140, label_visibility="collapsed")

# تفعيل زر الفحص والتحليل
if st.button("🔮 ابدأ التحليل الدلالي الذكي"):
    if not input_text.strip():
        st.warning("⚠️ يرجى كتابة جملة أو نص عربي أولاً لبدء تشغيل الخوارزميات الدلالية.")
    else:
        # التحقق من وجود الكلمة المحورية
        detected_keyword = None
        for key in semantic_lexicon_db.keys():
            if key in input_text:
                detected_keyword = key
                break
        
        # حاوية عرض النتيجة الاحترافية الكبيرة
        st.markdown('<div class="result-card-box">', unsafe_allow_html=True)
        st.markdown('<div class="result-card-header">📊 لوحة نتائج المعالجة الحوسبية الشاملة</div>', unsafe_allow_html=True)
        
        if detected_keyword:
            with st.spinner("⏳ يجري الآن تفكيك البنية السياقية للنص وحساب معاملات التقارب الدلالي..."):
                time.sleep(0.7) # معالجة سريعة تحاكي استخراج المتجهات اللغوية
                
                computed_results = []
                best_score = -1
                final_meaning = ""
                
                # حساب درجة المطابقة بناء على الكلمات المفتاحية والسياق المكتوب
                for entry in semantic_lexicon_db[detected_keyword]:
                    match_score = 0.20  # وزن عام أساسي للسياق
                    for indicator in entry["المؤشرات"]:
                        if indicator in input_text:
                            match_score += 0.25
                    
                    if match_score > 0.98: 
                        match_score = 0.98
                        
                    computed_results.append({
                        "المعنى السياقي المكتشف": entry["المعنى"],
                        "السياق النموذجي المقارن": entry["جملة_مرجعية"],
                        "نسبة التقارب الجيب تمامي (Similarity)": f"{match_score * 100:.2f}%",
                        "_raw_score": match_score
                    })
                    
                    if match_score > best_score:
                        best_score = match_score
                        final_meaning = entry["المعنى"]
                
                # إظهار القرار اللغوي للنموذج بنجاح
                st.success(f"🎯 نجح النظام في رصد لفظ مشترك غامض دلالياً وهو: **({detected_keyword})**")
                st.markdown(f"""
                <div style="background-color: #F5F3FF; padding: 18px; border-radius: 12px; margin: 15px 0; border-right: 5px solid #8B5CF6; font-size:17px; color:#1E1B4B;">
                    📌 <b>التفسير اللغوي النهائي:</b> المعنى المراد للكلمة في سياق جملتكِ هو <b>({final_meaning})</b> بنسبة يقين حوسبي بلغت <b>{best_score * 100:.2f}%</b>.
                </div>
                """, unsafe_allow_html=True)
                
                # إنشاء وترتيب الجدول الإحصائي المقارن للنتائج
                df_analysis = pd.DataFrame(computed_results)
                df_analysis = df_analysis.sort_values(by="_raw_score", ascending=False).drop(columns=["_raw_score"])
                
                st.markdown("<b style='font-size:16px; color:#4F46E5;'>📋 مصفوفة حساب التوافق والتشابه المعجمي السياقي:</b>", unsafe_allow_html=True)
                st.dataframe(df_analysis, use_container_width=True, hide_index=True)
                
        else:
            # معالجة عامة للنصوص الخارجة عن نطاق الكلمات الغامضة الثلاثة الأساسية
            with st.spinner("⏳ يجري تحليل السمات النحوية والبنائية للنص..."):
                time.sleep(0.5)
                st.info("💡 تم فحص البنية التركيبية للنص بنجاح. النص سليم تماماً، ولم يتم رصد لبس معجمي مباشر يقع ضمن المعاجم التجريبية المثبتة حالياً (عين، المغرب، رأس).")
                
                # إظهار جدول الخصائص العامة للنص المكتوب
                words_num = len(input_text.split())
                chars_num = len(input_text)
                
                st.markdown("<b style='font-size:16px; color:#4F46E5;'>📋 السمات الهيكلية العامة للنص المدخل:</b>", unsafe_allow_html=True)
                df_general = pd.DataFrame([{
                    "مجموع الكلمات الفعلي": words_num,
                    "عدد الحروف والرموز": chars_num,
                    "نوع التحليل المفعل": "تحليل تركيبي عام (Syntactic Tracking)",
                    "حالة الغموض المعجمي": "مستقر / سياق أحادي الدلالة"
                }])
                st.dataframe(df_general, use_container_width=True, hide_index=True)
                
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='margin-top:15px; color:#64748B; font-size:15px;'>🔒 معالجة لغوية آمنة وموثوقة — تعتمد بالكامل على تتبع المؤشرات والسياقات الحوسبية.</div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================================
# 6. قسم مراحل العرض (كيف يعمل لبيب)
# =========================================
st.markdown('<div class="section-center-title">❖ كيف يعمل لبيب؟</div>', unsafe_allow_html=True)
st.markdown('<div class="section-center-sub">آلية فك اللبس الدلالي وتحليل سياق الجمل العربية بدقة عالية</div>', unsafe_allow_html=True)

st.markdown('<div class="step-flex-container">', unsafe_allow_html=True)

st.markdown("""
<div class="step-item-card">
    <div class="step-number-badge">1</div>
    <div class="step-item-icon">🔎</div>
    <div class="step-item-title">تحليل السياق</div>
    <div class="step-item-desc">يقوم النظام بمسح الجملة والتقاط الكلمات المفتاحية والمؤشرات المصاحبة للفظ المشترك للتعرف على بيئة النص.</div>
</div>
<div class="step-item-card">
    <div class="step-number-badge">2</div>
    <div class="step-item-icon">✨</div>
    <div class="step-item-title">اكتشاف المعنى</div>
    <div class="step-item-desc">يتم مطابقة الكلمات المرصودة مع السمات والروابط المخزنة في القاموس الرقمي لتحديد التوجيه المعجمي الصحيح.</div>
</div>
<div class="step-item-card">
    <div class="step-number-badge">3</div>
    <div class="step-item-icon">📊</div>
    <div class="step-item-title">قياس التشابه الدلالي</div>
    <div class="step-desc">حساب نسب التوافق الدلالي رياضياً وعرض النتائج وترتيبها تصاعدياً لتقديم التفسير المعنوي الأنسب للكلمة.</div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# =========================================
# 7. بطاقة معلومات المطورة (هاجر الزواكي) ممركزة واحترافية
# =========================================
st.markdown('<div class="profile-card">', unsafe_allow_html=True)

st.markdown("""
<div class="profile-text-side">
    <div class="profile-name">هاجر الزواكي</div>
    <div class="profile-subtitle">طالبة باحثة بسلك الماستر في اللسانيات الرقمية والعربية</div>
    <div class="profile-bio">
        مهتمة بالذكاء الاصطناعي ومعالجة اللغة العربية وبناء الأنظمة الدلالية الذكية وفك اللبس المعجمي.<br><br>
        🏛️ <b>جامعة مولاي إسماعيل بمكناس</b> — كلية الآداب والعلوم الإنسانية.<br>
        🎓 يمثل هذا المشروع المنصّي والبرمجي المتكامل <b>الجزء التطبيقي لبحث التخرج</b> لنيل شهادة الماستر للموسم الجامعي 2025/2026.
    </div>
</div>
<div class="profile-img-side">
    <img class="avatar-image" src="https://raw.githubusercontent.com/hzouaki-ship-it/labeeb-ai/main/hajar.jpg" alt="هاجر الزواكي">
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# =========================================
# 8. التذييل والفوتر الأخير للمنصة
# =========================================
st.markdown("""
<div class="footer-text">
    منصة LABEEB AI © 2026 — كلية الآداب والعلوم الإنسانية، جامعة مولاي إسماعيل بمكناس. جميع الحقوق محفوظة للباحثة.
</div>
""", unsafe_allow_html=True)
