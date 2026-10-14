from google import genai
import streamlit as st
import time

# 🔑 ضع مفتاح API الخاص بك هنا
DEFAULT_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

# 1. إعدادات الصفحة الرسمية
st.set_page_config(
    page_title="Unlock AI - منصة صياغة المحتوى الذكي",
    page_icon="⚡",
    layout="centered"
)

# 2. تصميم CSS مخصص (خط Tajawal، ألوان باستيل بيج/أزرق/أورنج، وتأثيرات حركية)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'Tajawal', sans-serif !important;
        background-color: #FAF7F2;
        color: #2C2825;
    }

    /* الهيدر الرئيسي الاحترافي */
    .main-header {
        background: linear-gradient(135deg, #FFE8DC 0%, #FAF7F2 50%, #E3EFFB 100%);
        padding: 35px 25px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
        border: 1px solid #EFE6DC;
        box-shadow: 0px 10px 30px rgba(220, 205, 190, 0.25);
    }
    .main-header h1 {
        color: #2C2825 !important;
        font-weight: 800;
        font-size: 2.3rem;
        margin-bottom: 8px;
        letter-spacing: -0.5px;
    }
    .main-header p {
        color: #6C635B;
        font-size: 1.1rem;
        font-weight: 500;
        margin: 0;
    }

    /* التسميات والعناوين */
    label, .stWidgetLabel, label p {
        color: #2C2825 !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }
    
    .stSubheader h3 {
        color: #2C2825 !important;
        font-weight: 800 !important;
        font-size: 1.25rem !important;
    }

    /* حقول الإدخال والقوائم المنسدلة */
    div[data-baseweb="input"], div[data-baseweb="textarea"], select, div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border: 1.5px solid #E5DCD3 !important;
        border-radius: 12px !important;
        color: #2C2825 !important;
        transition: all 0.25s ease-in-out !important;
    }
    
    div[data-baseweb="input"]:focus-within, div[data-baseweb="textarea"]:focus-within {
        border-color: #F79D65 !important;
        box-shadow: 0 0 0 3px rgba(247, 157, 101, 0.15) !important;
    }

    input, textarea, div[role="button"] {
        color: #2C2825 !important;
        font-weight: 500 !important;
    }

    /* بطاقة نتائج المحتوى */
    .result-card {
        background: #FFFFFF;
        border-right: 4px solid #F79D65;
        border-radius: 14px;
        padding: 18px 22px;
        margin-top: 25px;
        margin-bottom: 10px;
        border: 1px solid #EFE6DC;
        box-shadow: 0 4px 15px rgba(220, 205, 190, 0.15);
    }

    /* زر التوليد التفاعلي */
    .stButton>button {
        background: linear-gradient(90deg, #F79D65 0%, #3B82F6 100%);
        color: #FFFFFF !important;
        font-weight: 700;
        font-size: 1.1rem;
        border: none;
        border-radius: 12px;
        padding: 14px 28px;
        width: 100%;
        box-shadow: 0 6px 20px rgba(247, 157, 101, 0.25);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.35);
        opacity: 0.96;
    }
    </style>
""", unsafe_allow_html=True)

# 3. الهيدر الرئيسي
st.markdown("""
    <div class="main-header">
        <h1>Unlock AI</h1>
        <p>منصة صياغة وتوليد المحتوى التسويقي الذكي والاحترافي</p>
    </div>
""", unsafe_allow_html=True)

# 4. تفاصيل وشروط المحتوى
st.subheader("إعدادات تفاصيل المنشور")

col1, col2 = st.columns(2)
with col1:
    business_name = st.text_input("اسم المشروع / العلامة التجارية:", placeholder="مثال: Unlock AI")
    platform = st.selectbox("المنصة المستهدفة:", ["إنستغرام", "فيسبوك", "لينكد إن (LinkedIn)", "إكس (تويتر)", "تيك توك"])
    post_length = st.selectbox("طول المنشور المطلوب:", ["متوسط ومركز", "مختصر وسريع", "تفصيلي وشامل"])

with col2:
    post_type = st.selectbox("نوع المنشور:", [
        "إعلان بيعي مباشر (Direct Sales)",
        "إطلاق منتج / خدمة جديدة",
        "قصة نجاح / حالة دراسية (Case Study)",
        "محتوى تثقيفي / نصيحة قيمة",
        "تفاعلي / أسئلة ومسابقات",
        "تحديث سريع / Story Caption"
    ])
    tone = st.selectbox("نبرة التحدث (Tone of Voice):", [
        "إقناعية وموجهة للمبيعات",
        "احترافية ورسمية (B2B)",
        "قصصية وملهمة",
        "ودودة وقريبة من الجمهور",
        "شبابية وحماسية"
    ])

details = st.text_area("تفاصيل المنتج، الفكرة، أو العرض المطلوب:", placeholder="أدخل هنا التفاصيل الأساسية، مثل: الميزات الرئيسية، الخصومات، أو الهدف من المنشور...", height=120)

# 5. التنفيذ وتوليد المحتوى الاحترافي
if st.button("صياغة المحتوى الاحترافي الان"):
    if DEFAULT_API_KEY == "ألصق_مفتاح_API_الخاص_بك_هنا" or not DEFAULT_API_KEY:
        st.error("يرجى إدخال مفتاح API في الكود أولاً.")
    elif not business_name or not details:
        st.warning("يرجى إدخال اسم المشروع والتفاصيل الأساسية لمتابعة التوليد.")
    else:
        client = genai.Client(api_key=DEFAULT_API_KEY)
        
        prompt = f"""
        أنت خبير تسويق رقمي وكاتب إعلانات محترف (Senior Copywriter) متمرس في بناء استراتيجيات المحتوى.
        المطلوب: كتابة 3 نماذج مسودة مختلفة ومبتكرة لمنشور موجه لمنصة {platform}.

        معلومات العلامة التجارية والمنشور:
        - اسم المشروع/العلامة التجارية: {business_name}
        - نوع المنشور: {post_type}
        - نبرة الصوت المطلوب اعتمادها: {tone}
        - حجم وطول المنشور: {post_length}
        - التفاصيل والعناصر المطلوبة: {details}

        شروط الصياغة لضمان أعلى مستوى من الاحترافية:
        1. كتابة لغة عربية فصحى تسويقية سليمة ورصينة خالية من الحشو والركاكة.
        2. هيكلة كل نموذج بوضوح:
           - خطاف اعلاني (Hook) قوي يجذب الانتباه فوراً.
           - متن المنشور (Body) يشرح القيمة المضافة بأسلوب سلس يناسب نبرة الصوت المحددة.
           - دعوة واضحة ومباشرة لاتخاذ إجراء (Call to Action).
           - استخدام متوازن ورصين للإيموجي (بدون مبالغة).
           - مجموعة مختارة من 5 إلى 7 هاشتاغات ذات صلة وموجهة.
        3. افصل بين النماذج الثلاثة بوضوح (النموذج الأول، النموذج الثاني، النموذج الثالث).
        """

        with st.spinner("جاري تحليل المعطيات وصياغة النماذج الاحترافية..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt,
                )
                
                st.success("تمت صياغة النماذج بنجاح!")
                
                st.markdown("""
                <div class="result-card">
                    <h3 style="margin:0;">النماذج المقترحة جاهزة للاستخدام:</h3>
                </div>
                """, unsafe_allow_html=True)
                
                # عرض النتيجة في صندوق مخصص
                generated_text = response.text
                st.text_area("المحتوى المولد (يمكنك نسخه أو تعديله مباشرة):", value=generated_text, height=420)
                
                # زر تنزيل النص كملف نصي محلي
                st.download_button(
                    label="تنزيل النماذج كملف نصي (.txt)",
                    data=generated_text,
                    file_name=f"{business_name}_posts.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء معالجة الطلب: {e}")
