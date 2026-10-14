from google import genai
import streamlit as st
import time

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="Unlock AI - كاتب الإعلانات اللطيف",
    page_icon="🌸",
    layout="centered"
)

# 2. تصميم CSS مخصص (فخم، رايق، وكيوت)
st.markdown("""
    <style>
    /* خلفية هادئة بلون كريمي دافئ */
    .stApp {
        background-color: #FAF6F0;
        color: #4A3E3D;
        font-family: 'Avenir', 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* هيدر فخم ولطيف بتدرج باستيل دافئ */
    .main-header {
        background: linear-gradient(135deg, #FFEBEB 0%, #FFF3E3 50%, #F5E6FF 100%);
        padding: 30px;
        border-radius: 24px;
        text-align: center;
        margin-bottom: 30px;
        border: 2px solid #FFF;
        box-shadow: 0px 8px 20px rgba(224, 195, 195, 0.25);
    }
    .main-header h1 {
        color: #7D5A50 !important;
        font-weight: 800;
        font-size: 2.4rem;
        margin-bottom: 5px;
    }
    .main-header p {
        color: #9E7A7A;
        font-size: 1.1rem;
        font-weight: 500;
    }

    /* العناوين الفرعية الجانبية اللطيفة */
    h3, .stSubheader {
        color: #7D5A50 !important;
        font-weight: bold;
    }
    
    /* تصميم حقول الإدخال لتصبح ناعمة ومريحة للعين */
    div[data-baseweb="input"], div[data-baseweb="textarea"], select {
        background-color: #FFFFFF !important;
        border: 1.5px solid #E8DFD8 !important;
        border-radius: 12px !important;
        color: #4A3E3D !important;
    }
    div[data-baseweb="input"]:focus-within {
        border-color: #E2B2B2 !important;
        box-shadow: 0 0 0 3px rgba(226, 178, 178, 0.2) !important;
    }

    /* تصميم بطاقة عرض الإعلان الجاهز */
    .result-card {
        background: #FFFFFF;
        border-left: 5px solid #F3A3A3;
        border-radius: 16px;
        padding: 22px;
        margin-top: 25px;
        border: 1px solid #F3ECE6;
        box-shadow: 0 6px 18px rgba(210,190,190,0.15);
    }
    
    /* زر التوليد الفخم والكيوت بلون وردي ذهبي ناعم */
    .stButton>button {
        background: linear-gradient(90deg, #F3A3A3, #E8B4B8);
        color: white !important;
        font-weight: bold;
        font-size: 1.15rem;
        border: none;
        border-radius: 14px;
        padding: 12px 28px;
        width: 100%;
        box-shadow: 0 4px 15px rgba(243, 163, 163, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(243, 163, 163, 0.45);
    }
    </style>
""", unsafe_allow_html=True)

# 3. الهيدر الرئيسي (Banner)
st.markdown("""
    <div class="main-header">
        <h1>🔓 Unlock AI</h1>
        <p>مُولّد المحتوى والبوستات التسويقية الذكي اللطيف 💖✨</p>
    </div>
""", unsafe_allow_html=True)

# 4. إدخال الإعدادات
st.subheader("🌸 إعدادات المفتاح")
api_key = st.text_input("مفتاح Gemini API Key الخاص بكِ:", type="password", help="أدخلي مفتاحك للبدء في توليد الأفكار")

st.markdown("<br>", unsafe_allow_html=True)
st.subheader("💡 تفاصيل المحتوى والمنشور")

col1, col2 = st.columns(2)
with col1:
    business_name = st.text_input("🎀 اسم المشروع / الصفحة:", placeholder="مثال: Unlock AI")
    platform = st.selectbox("📱 المنصة الاستهدافة:", ["إنستغرام", "فيسبوك", "تيك توك", "إكس (تويتر)"])

with col2:
    post_type = st.selectbox("📌 نوع المنشور:", ["إعلان عن خصم / عرض", "إطلاق منتج جديد", "منشور تفاعلي", "نصيحة قيّمة"])
    tone = st.selectbox("🕊️ نبرة الصوت (Tone):", ["ودودة وقريبة", "حماسية ومحفزة", "احترافية ورسمية", "فكاهية وشبابية"])

details = st.text_area("🌟 تفاصيل العرض أو الموضوع:", placeholder="مثال: افتتاح منصة تشمل كل مميزات وبرومبتات الذكاء الاصطناعي بطريقة مبسطة ولطيفة...", height=120)

# 5. زر التنفيذ وتوليد المحتوى
if st.button("✨ توليد الإعلان الآن ✨"):
    if not api_key:
        st.error("يرجى إدخال API Key أولاً 🌸")
    elif not business_name or not details:
        st.warning("لطفاً، املئي اسم المشروع والتفاصيل لنتمكن من صياغته!")
    else:
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        أنت خبير تسويق رقمي وكاتب إعلانات محترف.
        قم بكتابة منشور تسويقي مخصص لمنصة {platform}.
        
        معلومات المشروع:
        - اسم المشروع: {business_name}
        - نوع المنشور: {post_type}
        - نبرة الكلام: {tone}
        - التفاصيل والعرض: {details}
        
        المطلوب:
        1. عنوان جذاب، لطيف وملهم يخطف الانتباه.
        2. نص إعلاني مشوق وبأسلوب ودود وقريب من القلب.
        3. دعوة واضحة ومحببة لاتخاذ إجراء (Call to Action).
        4. إضافة إيموجيات مناسبة وجميلة.
        5. اقتراح 5 إلى 8 هاشتاغات قوية.
        """

        with st.spinner("جاري صياغة المنشور الجميل بكل حب... ✨🎀"):
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt,
                )
                
                st.success("تمت صياغة إعلانكِ الجميل بنجاح! 💕")
                
                # عرض النتيجة داخل بطاقة مصممة وناعمة
                st.markdown(f"""
                <div class="result-card">
                    <h3 style="color: #7D5A50; margin-top:0;">📝 منشوركِ الجاهز بكل حب:</h3>
                </div>
                """, unsafe_allow_html=True)
                
                st.text_area("انسخي النص من هنا مباشرة:", value=response.text, height=350)
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء الصياغة، عاودي المحاولة مجدداً: {e}")
                