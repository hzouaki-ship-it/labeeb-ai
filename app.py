import streamlit as st
import pandas as pd

# إعداد واجهة الصفحة
st.set_page_config(page_title="LABEEB AI", layout="centered")

# عنوان التطبيق
st.title("🧠 LABEEB AI - لبيب")
st.subheader("المحلل الدلالي الذكي")

# صندوق إدخال النص
text = st.text_input("أدخل الجملة المراد تحليلها:", "")

# زر التحليل
if st.button("بدء التحليل"):
    if text:
        # هذه بيانات تجريبية للتمثيل
        data = {
            "المعنى السياقي المرشح": ["عضو البصر", "نبع ماء", "جاسوس"],
            "نسبة التقارب الدلالي": ["60%", "20%", "20%"]
        }
        
        # تحويل البيانات إلى جدول
        df = pd.DataFrame(data)
        
        # عرض النتيجة
        st.write("### 🎯 نتائج التحليل:")
        st.table(df)
    else:
        st.warning("الرجاء كتابة جملة أولاً.")

# تذييل الصفحة
st.markdown("---")
st.write("تصميم الطالبة: هاجر الزواكي © 2026")
