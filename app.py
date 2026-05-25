if st.button("⚡ تحليل"):
    if model:
        if user_text.strip():
            # استخدام placeholder لعرض النص المكتوب تدريجياً
            st.success("النتيجة:")
            result_placeholder = st.empty()
            full_response = ""
            
            with st.spinner("⏳ جاري التحليل..."):
                try:
                    # تفعيل خاصية الـ stream
                    response = model.generate_content(f"حلل الجملة التالية دلالياً باختصار: {user_text}", stream=True)
                    
                    for chunk in response:
                        full_response += chunk.text
                        result_placeholder.markdown(full_response + "▌")
                    
                    result_placeholder.markdown(full_response) # إزالة المؤشر في النهاية
                except Exception as e:
                    st.error(f"حدث خطأ أثناء الاتصال: {e}")
        else:
            st.warning("الرجاء إدخال نص أولاً!")
    else:
        st.error("لا يمكن التحليل لأن النموذج غير مهيأ.")
