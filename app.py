for entry in meanings:

    # =========================================
    # تحويل القرائن إلى سياق دلالي
    # =========================================

    context_text = " ".join(
        entry["القرائن"].keys()
    )

    # =========================================
    # حساب التشابه الدلالي الحقيقي
    # =========================================

    score = semantic_similarity(
        user_text,
        context_text
    )

    # ضبط القيم
    if score < 0:
        score = 0.05

    if score > 1:
        score = 1.0

    results_list.append({

        "المعنى المحتمل":
        entry["المعنى"],

        "نسبة القرب":
        f"{score * 100:.2f}%",

        "_raw":
        score
    })

    if score > highest_score:

        highest_score = score

        predicted_meaning = (
            entry["المعنى"]
        )

# =========================================
# عرض الكروت الرقمية
# =========================================

st.markdown(
    '<div class="result-badge-container">'
    ' <div class="result-stat-box">'
    '     <div class="result-stat-label">المعنى الأقرب</div>'
    '     <div class="result-stat-val">' + predicted_meaning + '</div>'
    ' </div>'
    ' <div class="result-stat-box">'
    '     <div class="result-stat-label">نسبة القرب الدلالي</div>'
    '     <div class="result-stat-val">' + f"{highest_score * 100:.2f}%" + '</div>'
    ' </div>'
    '</div>',
    unsafe_allow_html=True
)

# =========================================
# عرض الجدول
# =========================================

df_clean = pd.DataFrame(results_list)\
    .sort_values(
        by="_raw",
        ascending=False
    )\
    .drop(columns=["_raw"])

st.table(
    df_clean.reset_index(drop=True)
)

# =========================================
# التحليل الذكي عبر OpenRouter
# =========================================

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

                    حلل الجملة اعتماداً
                    على السياق.

                    أجب باختصار:

                    - المعنى المقصود
                    - هل الاستعمال حقيقي أم مجازي
                    - تفسير مختصر
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

# =========================================
# عرض التحليل الذكي
# =========================================

st.markdown(
    f'''
    <div class="glass-card">

        <div class="card-title">
        🤖 التحليل الذكي
        </div>

        <div style="
        line-height:2;
        color:#334155;
        font-size:16px;
        ">

        {ai_analysis}

        </div>

    </div>
    ''',
    unsafe_allow_html=True
)
