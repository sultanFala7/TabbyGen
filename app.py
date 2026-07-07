import streamlit as st
from openai import OpenAI

# 1. تهيئة الصفحة وتصميم مخصص لتابي
st.set_page_config(page_title="Tabby Support Assistant", page_icon="💳", layout="centered")
st.title("💳 مساعد سلطان - خدمة عملاء تابي")
st.write("اكتب المعطيات الخام من Helpjuice وخلي الذكاء الاصطناعي يصيغها بأسلوبك فوراً.")

# 2. شريط الإعدادات الجانبي لحفظ مفتاح الأمان
st.sidebar.header("⚙️ إعدادات النظام")
api_key = st.sidebar.text_input("أدخل مفتاح OpenAI API Key", type="password")
st.sidebar.markdown("---")
st.sidebar.info("هذا المساعد مخصص لـ تابي ويطبق قواعد الصياغة المعتمدة لسلطان فلاح باللغتين العربية والإنجليزية.")

# 3. مدخلات البيانات من العميل و Helpjuice
col1, col2 = st.columns(2)
with col1:
    customer_name = st.text_input("اسم العميل:", placeholder="مثال: فهد، John...")
    language = st.radio("لغة العميل:", ["عربي (Arabic)", "إنجليزي (English)"])
with col2:
    channel = st.radio("نوع القناة:", ["إيميل (Email)", "محادثة (Chat)"])
    vibe = st.selectbox("حالة ونبرة العميل:", [
        "هادي ومستفسر (ودود ومطمئن)",
        "معصب ومستعجل (مباشر، سريع، وبدون مقدمات طويلة)"
    ])

helpjuice_text = st.text_area("انسخ النص الخام من قاعدة المعرفة (Helpjuice) هنا:", height=200, 
                              placeholder="To change your email address, please follow these steps...")

# 4. زر السحر والصياغة
if st.button("✨ صياغة الرد الاحترافي"):
    if not api_key:
        st.error("الرجاء إدخال الAPI Key في الشريط الجانبي أولاً!")
    elif not customer_name or not helpjuice_text:
        st.warning("الرجاء تعبئة اسم العميل والنص القادم من Helpjuice!")
    else:
        with st.spinner("جاري صياغة الرد بأسلوبك..."):
            try:
                client = OpenAI(api_key=api_key)
                
                # إعداد التوجيهات بناءً على اللغة المختارة
                if language == "عربي (Arabic)":
                    lang_instructions = """
                    - اللغة: العامية البيضاء السعودية اللطيفة والدافية (مثل: أبشر، ولا تشيل هم، حياك).
                    - ممنوع نهائياً استخدام كلمة 'خدمة' واستبدلها بكلمة 'مساعدة' أو 'تعليمات'.
                    - اختم الرد دائماً بـ: 'أتمنى أني غطيت النقاط اللي تحتاجها...' متبوعاً بالتوقيع:
                      مع أطيب التحيات،
                      سلطان فلاح
                      فريق دعم تابي
                    """
                else:
                    lang_instructions = """
                    - Language: English (Clear, warm, and highly professional).
                    - Never use robotic or overly complex technical terms.
                    - End the response always with: 'I hope this covers everything you need...' followed by the signature:
                      Best regards,
                      Sultan Falah
                      Tabby Support Team
                    """

                # الهندسة السرية للأمر (Prompt Engineering) الموحدة
                system_prompt = f"""
                أنت ممثل دعم عملاء محترف في شركة "تابي" (Tabby) واسمك "سلطان فلاح".
                المطلوب منك صياغة رد على عميل اسمه ({customer_name}) عبر قناة ({channel}) بناءً على المعلومة الخام المقدمة من Helpjuice.
                
                قواعد صارمة تطبق على جميع الردود بغض النظر عن اللغة:
                1. حالة العميل الحالية: {vibe}. إذا كان معصباً أو مستعجلاً، ادخل في صلب الموضوع فوراً، اختصر الخطوات، وضع الروابط المباشرة في البداية لتوفير وقته.
                2. أظهر التفهم التام والاهتمام، والجاهزية للمساعدة (بدون وعود كاذبة).
                3. اشرح السبب خلف السياسة ببساطة ومنطقية (بناءً على Helpjuice).
                4. لا تعتذر أبداً عن سياسات الشركة (مثل سياسات الأمان أو التأخير التلقائي)، بل ركز على أن الهدف هو حماية العميل.
                5. استخدم الترقيم والنقاط لجعل الخطوات سهلة القراءة (Scannability).
                
                تعليمات اللغة والتوقيع:
                {lang_instructions}
                """
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"المعلومة من Helpjuice:\n{helpjuice_text}"}
                    ]
                )
                
                generated_text = response.choices[0].message.content
                st.success("🎉 الرد جاهز! انسخه وأرسله:")
                st.text_area("الرد النهائي:", value=generated_text, height=350)
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {e}")
