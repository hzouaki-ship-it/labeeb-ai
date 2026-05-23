import streamlit as st

# إعداد الصفحة
st.set_page_config(page_title="LABEEB AI", layout="wide")

st.title("🧠 LABEEB AI - لبيب")
text = st.text_input("أدخل النص:")

if st.button("تحليل"):
    # معالجة بسيطة للبيانات
    data = {
        "المعنى السياقي": ["عضو البصر", "نبع ماء"],
        "نسبة التقارب": ["75%", "25%"]
    }
    st.table(data)
