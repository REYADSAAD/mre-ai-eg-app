import streamlit as st
import openai
import sqlite3

# إعداد مفتاح OpenAI API
openai.api_key = "YOUR_OPENAI_API_KEY"

# إنشاء أو الاتصال بقاعدة بيانات SQLite
conn = sqlite3.connect("user_progress.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_input TEXT,
    ai_response TEXT,
    score INTEGER
)
""")
conn.commit()

# واجهة Streamlit
st.set_page_config(page_title="MRE AI EG - معلم اللغة بالذكاء الاصطناعي", layout="centered")
st.title("📚 MRE AI EG - معلم اللغة بالذكاء الاصطناعي")

# اختيار اللغة
language = st.selectbox("🌍 اختر اللغة", ["العربية", "الإنجليزية", "الإسبانية", "الفرنسية"])

# منطقة الدردشة
st.subheader("💬 المحادثة مع المعلم الذكي")
user_input = st.text_input("أدخل رسالتك:")
if st.button("إرسال"):
    if user_input:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أنت معلم لغة ذكي، ساعد المستخدم على تعلم اللغة بطريقة تفاعلية."},
                {"role": "user", "content": user_input}
            ]
        )
        ai_response = response['choices'][0]['message']['content']
        st.success(f"المعلم الذكي: {ai_response}")
        cursor.execute("INSERT INTO progress (user_input, ai_response, score) VALUES (?, ?, ?)", (user_input, ai_response, None))
        conn.commit()

# زر الوضع الداكن
if st.button("🌙 تبديل الوضع الداكن"):
    st.markdown(
        """
        <style>
        body { background-color: #2c3e50; color: white; }
        </style>
        """,
        unsafe_allow_html=True,
    )

# اختبار لغوي بسيط
st.subheader("📝 اختبار لغوي")
question = "ما هو معنى كلمة 'Car' باللغة العربية؟"
options = ["قطار", "سيارة", "دراجة", "طائرة"]
correct_answer = "سيارة"
answer = st.radio(question, options)
if st.button("تحقق من الإجابة"):
    if answer == correct_answer:
        st.success("✅ إجابة صحيحة!")
        cursor.execute("INSERT INTO progress (user_input, ai_response, score) VALUES (?, ?, ?)", (answer, correct_answer, 1))
    else:
        st.error(f"❌ إجابة خاطئة! الإجابة الصحيحة هي: {correct_answer}")
        cursor.execute("INSERT INTO progress (user_input, ai_response, score) VALUES (?, ?, ?)", (answer, correct_answer, 0))
    conn.commit()

# عرض سجل التقدم
st.subheader("📊 تقدمك السابق")
if st.button("🔍 عرض السجل"):
    cursor.execute("SELECT user_input, ai_response, score FROM progress")
    rows = cursor.fetchall()
    for row in rows:
        st.write(f'أنت: {row[0]}')
        st.write(f'المعلم الذكي: {row[1]}')
        st.write(f'📈 الدرجة: {row[2]}')
        st.markdown("---")

# إغلاق الاتصال بقاعدة البيانات
conn.close()