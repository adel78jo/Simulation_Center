import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# 🛑 1. إعدادات المصادقة (الأمان) 🛡️
# تم تثبيت هذه القيم
# ==========================================
ADMIN_USER = "AABU"  # اسم المستخدم الخاص بك
ADMIN_PASS = "Aabu2025"  # كلمة المرور الخاصة بك

# --- تهيئة البيانات والتخزين (Session State) ---
# التأكد من تهيئة حالة تسجيل الدخول
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# البيانات الأولية (يمكن للمدير تعديلها وحذفها)
if 'courses' not in st.session_state:
    st.session_state['courses'] = {
        1: {"Name": "أساسيات المحاكاة (Arena)", "Status": "متاحة للتسجيل"},
        2: {"Name": "النمذجة الرياضية (Matlab)", "Status": "متاحة للتسجيل"},
        3: {"Name": "الواقع الافتراضي والمعزز (VR/AR)", "Status": "قيد الإعداد"},
    }
if 'trainees' not in st.session_state:
    st.session_state['trainees'] = {
        101: {"Name": "خالد محمد", "Type": "طالب بكالوريوس", "College": "تكنولوجيا المعلومات", "Course_ID": 1, "Course_Name": "أساسيات المحاكاة (Arena)", "Date": "2025-11-01"},
        102: {"Name": "سارة علي", "Type": "طالب دراسات عليا", "College": "الهندسة", "Course_ID": 2, "Course_Name": "النمذجة الرياضية (Matlab)", "Date": "2025-11-05"},
    }
if 'audit_logs' not in st.session_state:
    st.session_state['audit_logs'] = {
        201: {"Lab": "مختبر النمذجة", "Auditor": "أحمد حسين", "Time": "2025-11-20 09:00", "Status": "ممتاز", "Notes": "جميع البرامج تعمل بامتياز."},
        202: {"Lab": "قاعة التدريب 1", "Auditor": "منى خالد", "Time": "2025-11-21 11:30", "Status": "يحتاج متابعة فورية", "Notes": "عطل في جهاز العرض."},
    }

# --- وظائف المدير العامة (CRUD Helpers) ---
def get_next_id(data_dict):
    """يُرجع المعرف (ID) التالي في القاموس."""
    return max(data_dict.keys()) + 1 if data_dict else 1

def delete_item(data_dict, item_id):
    """يحذف عنصراً من القاموس."""
    if item_id in data_dict:
        del data_dict[item_id]
        return True
    return False

# --- وظيفة تسجيل الدخول ---
def login_user(username, password):
    if username == ADMIN_USER and password == ADMIN_PASS:
        st.session_state['logged_in'] = True
        st.success("🎉 تم تسجيل الدخول بنجاح! يمكنك الآن الوصول لإدارة النظام.")
        st.rerun() # **تم التحديث:** استبدال experimental_rerun() بـ rerun()
    else:
        st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة.")

# --- وظيفة تسجيل الخروج ---
def logout_user():
    st.session_state['logged_in'] = False
    st.warning("تم تسجيل الخروج. محتوى الإدارة غير متاح.")
    st.rerun() # **تم التحديث:** استبدال experimental_rerun() بـ rerun()


# --- إعدادات الصفحة والتصميم الاحترافي ---
st.set_page_config(
    page_title="شعبة التدريب والتطوير والتدقيق والتوعية",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="👨‍🏫" 
)

# تعديل شكل الخطوط والألوان عبر حقن CSS لتحسين الواجهة
st.markdown("""
<style>
    /* دعم الاتجاه من اليمين لليسار بشكل كامل */
    .stApp {
        direction: rtl;
        text-align: right;
        font-family: 'Arial', 'Tahoma', sans-serif; /* خطوط أجمل وأكثر احترافية */
    }
    /* خطوط وعناوين أكثر جاذبية */
    h1, h2, h3, h4, h5, h6 {
        color: #004d40; /* لون الأخضر الداكن (Teal/Emerald) */
        font-family: 'Arial', 'Tahoma', sans-serif;
    }
    /* الألوان الأساسية للأزرار والمكونات */
    .stButton>button {
        background-color: #00796b; /* أخضر غامق احترافي */
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: bold;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #009688; /* لون فاتح عند المرور */
    }
    /* تصميم بطاقات الـ Metrics */
    [data-testid="stMetric"] {
        background-color: #e0f2f1; /* خلفية فاتحة للبطاقات */
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); /* ظل احترافي */
        text-align: center;
    }
    [data-testid="stMetricLabel"] {
        font-size: 1.2em;
        color: #004d40; /* أخضر داكن للعلامة */
        font-weight: bold;
    }
    [data-testid="stMetricValue"] {
        font-size: 3em;
        color: #00796b; /* لون القيمة الرئيسي */
        font-weight: bolder;
    }
    /* تحسين التباعد في الأقسام */
    .stContainer {
        padding-top: 15px;
        padding-bottom: 15px;
    }
    /* إزالة حدود DataFrame الافتراضية */
    .stDataFrame {
        border: 1px solid #ddd !important; /* حدود خفيفة وأنيقة */
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)


# --- القائمة الجانبية للتنقل ---
st.sidebar.markdown("# 🏛️ جامعة آل البيت")
st.sidebar.markdown("## شعبة التدريب والتطوير والتدقيق والتوعية")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "القائمة الرئيسية:",
    ("🏠 الصفحة الرئيسية", "📚 تسجيل الدورات", "🔍 التدقيق والمتابعة", "📊 التقارير والإحصائيات", "🔑 إدارة النظام الكاملة")
)
st.sidebar.markdown("---")

if st.session_state['logged_in']:
    st.sidebar.button("🔐 تسجيل الخروج", on_click=logout_user)
else:
    st.sidebar.info("للوصول لإدارة النظام، يرجى تسجيل الدخول.")


# ==========================================
# 1. الصفحة الرئيسية (واجهة احترافية معبرة)
# ==========================================
if menu == "🏠 الصفحة الرئيسية":
    st.image("https://www.aabu.edu.jo/sites/AABU/Main/SiteAssets/logo.png", width=150) # شعار الجامعة
    st.title("مرحباً بك في نظام إدارة شعبة التدريب والتطوير والتدقيق والتوعية")
    st.subheader("مركز النمذجة والمحاكاة - جامعة آل البيت")
    
    with st.container(border=True): # استخدام حاوية لتحسين الشكل
        st.markdown("""
        **رؤيتنا:** الارتقاء بالكفاءات، ضمان الجودة، وتحفيز الابتكار في مجالات النمذجة والمحاكاة.
        نحن نسعى لتقديم أفضل برامج التدريب، مع تطبيق أعلى معايير التدقيق والمتابعة لضمان التميز.
        """)
    
    st.markdown("---")
    
    # بطاقات معلومات سريعة
    col1, col2, col3 = st.columns(3)
    col1.metric("📚 دورات متاحة حالياً", len([c for c in st.session_state['courses'].values() if c['Status'] == 'متاحة للتسجيل']), "زيادة مستمرة")
    col2.metric("👥 إجمالي المتدربين", len(st.session_state['trainees']), "بما فيهم القدامى")
    col3.metric("✅ تقارير تدقيق ناجحة", len([a for a in st.session_state['audit_logs'].values() if a['Status'] == 'ممتاز']), "نسبة 90%")
    
    st.markdown("---")
    
    st.subheader("أهم خدماتنا")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### 👨‍🏫 التدريب المتخصص")
        st.info("ورش عمل ودورات في أحدث تقنيات النمذجة والمحاكاة.")
    with c2:
        st.markdown("#### 🔎 ضمان الجودة والتدقيق")
        st.info("متابعة دورية لجودة المرافق والبرامج.")
    with c3:
        st.markdown("#### 📢 التوعية والبحث")
        st.info("نشر المعرفة ودعم المشاريع البحثية المبتكرة.")
    
    st.markdown("---")
    
    # صورة معبرة عن النمذجة والمحاكاة (مثال - يمكن تغييرها)
    st.image("https://i.ibb.co/L5Q2j85/simulation.jpg", caption="بيئة محاكاة حديثة", use_column_width=True) # صورة معبرة

# ==========================================
# 2. قسم تسجيل الدورات
# ==========================================
elif menu == "📚 تسجيل الدورات":
    st.header("📝 تسجيل المتدربين في الدورات")
    st.markdown("استخدم هذا النموذج لتسجيل الطلاب والموظفين في الدورات المتاحة.")
    
    course_list = {k: v['Name'] for k, v in st.session_state['courses'].items() if v['Status'] == 'متاحة للتسجيل'}
    
    with st.form("training_form", clear_on_submit=True):
        st.subheader("بيانات المتدرب")
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("الاسم الرباعي", key="reg_name", help="الرجاء إدخال الاسم كاملاً.")
            user_type = st.selectbox("الصفة", ["طالب بكالوريوس", "طالب دراسات عليا", "عضو هيئة تدريس", "إداري"], key="reg_type")
        
        with col2:
            college = st.selectbox("الكلية/القسم", ["تكنولوجيا المعلومات", "الهندسة", "العلوم", "العلوم الإدارية", "أخرى"], key="reg_college")
            
            if course_list:
                selected_course_id = st.selectbox("الدورة المطلوبة", options=list(course_list.keys()), format_func=lambda x: course_list[x], key="reg_course")
            else:
                st.error("لا توجد دورات متاحة للتسجيل حالياً. الرجاء مراجعة إدارة الشعبة.")
                selected_course_id = None
        
        st.markdown("---")
        submitted = st.form_submit_button("✅ تأكيد التسجيل")
        
        if submitted and name and selected_course_id:
            new_id = get_next_id(st.session_state['trainees'])
            new_trainee = {
                "Name": name,
                "Type": user_type,
                "College": college,
                "Course_ID": selected_course_id,
                "Course_Name": course_list[selected_course_id],
                "Date": datetime.now().strftime("%Y-%m-%d")
            }
            st.session_state['trainees'][new_id] = new_trainee
            st.success(f"🎉 تم تسجيل المتدرب **{name}** بنجاح في دورة **{course_list[selected_course_id]}**.")
        elif submitted and not name:
            st.warning("الرجاء إدخال اسم المتدرب كاملاً.")

# ==========================================
# 3. قسم التدقيق والمتابعة
# ==========================================
elif menu == "🔍 التدقيق والمتابعة":
    st.header("🔍 التدقيق اليومي للمرافق والبرامج")
    st.markdown("املأ هذا النموذج لرفع تقارير التدقيق الدورية.")
    
    with st.form("audit_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            lab_id = st.selectbox("المرفق / المختبر", ["مختبر النمذجة", "مختبر المحاكاة", "قاعة التدريب 1", "قاعة التدريب 2", "أخرى"], key="audit_lab")
            auditor = st.text_input("اسم المدقق المسؤول", key="audit_auditor")
        
        st.markdown("---")
        st.markdown("**قائمة التحقق لضمان الجودة:**")
        
        check_col1, check_col2, check_col3 = st.columns(3)
        check_sw = check_col1.checkbox("البرمجيات تعمل بكفاءة (الرخص سارية)", help="تأكد من عمل جميع البرامج والرخص.")
        check_hw = check_col2.checkbox("الأجهزة والمعدات سليمة (تكييف/كهرباء/شبكة)", help="فحص الأجهزة العامة والفرعية.")
        check_cl = check_col3.checkbox("نظافة القاعة والترتيب العام", help="تأكد من النظافة والترتيب بعد الاستخدام.")
        
        notes = st.text_area("ملاحظات تفصيلية أو طلبات صيانة عاجلة", key="audit_notes")
        
        submit_audit = st.form_submit_button("✅ رفع تقرير التدقيق")
        
        if submit_audit and auditor:
            new_id = get_next_id(st.session_state['audit_logs'])
            status_text = "ممتاز" if (check_sw and check_hw and check_cl) else "⚠️ يحتاج متابعة فورية"
            audit_entry = {
                "Lab": lab_id,
                "Auditor": auditor,
                "Time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Status": status_text,
                "Notes": notes
            }
            st.session_state['audit_logs'][new_id] = audit_entry
            if status_text == "ممتاز":
                st.success("👍 تم حفظ التقرير بنجاح. المرافق بحالة ممتازة.")
            else:
                st.error(f"🚨 تم تسجيل التقرير. حالة المرفق **{status_text}**.")
        elif submit_audit and not auditor:
            st.warning("الرجاء إدخال اسم المدقق المسؤول.")

# ==========================================
# 4. التقارير والإحصائيات
# ==========================================
elif menu == "📊 التقارير والإحصائيات":
    st.header("📊 لوحة مؤشرات الأداء والتقارير")
    st.markdown("استعرض الإحصائيات الرئيسية وحمل تقارير البيانات.")
    
    st.subheader("إحصائيات التسجيل حسب الكلية")
    if st.session_state['trainees']:
        df_trainees = pd.DataFrame(st.session_state['trainees']).T
        college_counts = df_trainees['College'].value_counts()
        st.bar_chart(college_counts)
        
    st.markdown("---")
    
    st.subheader("توزيع حالة تقارير التدقيق")
    if st.session_state['audit_logs']:
        df_audit = pd.DataFrame(st.session_state['audit_logs']).T
        audit_counts = df_audit['Status'].value_counts().reset_index()
        audit_counts.columns = ['الحالة', 'العدد']
        st.dataframe(audit_counts, use_container_width=True, hide_index=True)
    else:
        st.info("لا توجد بيانات تدقيق لعرضها.")
    
    st.markdown("---")
    
    st.subheader("تحميل البيانات الخام")
    col_dl1, col_dl2, col_dl3 = st.columns(3)
    if st.session_state['trainees']:
        df_full_trainees = pd.DataFrame(st.session_state['trainees']).T
        csv_trainees = df_full_trainees.to_csv(index=True).encode('utf-8')
        col_dl1.download_button(
            label="⬇️ تحميل بيانات المتدربين (CSV)",
            data=csv_trainees,
            file_name='تقارير_المتدربين.csv',
            mime='text/csv',
        )
    if st.session_state['audit_logs']:
        df_full_audit = pd.DataFrame(st.session_state['audit_logs']).T
        csv_audit = df_full_audit.to_csv(index=True).encode('utf-8')
        col_dl2.download_button(
            label="⬇️ تحميل تقارير التدقيق (CSV)",
            data=csv_audit,
            file_name='تقارير_التدقيق.csv',
            mime='text/csv',
        )
    if st.session_state['courses']:
        df_full_courses = pd.DataFrame(st.session_state['courses']).T
        csv_courses = df_full_courses.to_csv(index=True).encode('utf-8')
        col_dl3.download_button(
            label="⬇️ تحميل بيانات الدورات (CSV)",
            data=csv_courses,
            file_name='بيانات_الدورات.csv',
            mime='text/csv',
        )

# ==========================================
# 5. إدارة النظام الكاملة (بوابة الدخول)
# ==========================================
elif menu == "🔑 إدارة النظام الكاملة":
    st.title("🔐 بوابة إدارة النظام")
    
    if st.session_state['logged_in']:
        # ---------------------------------------------
        # محتوى الإدارة يظهر فقط للمستخدم المسجل دخوله
        # ---------------------------------------------
        st.subheader("لوحة التحكم المركزية بالبيانات")
        st.error("تنبيه: هذا القسم يتيح إضافة، تعديل، وحذف البيانات الأساسية. استخدمه بحذر شديد.")
        
        st.markdown("---")
        
        tab_courses, tab_trainees, tab_audit = st.tabs(["📚 إدارة الدورات", "👥 إدارة المتدربين", "📝 إدارة تقارير التدقيق"])

        # ---------------------------------------------
        # A. إدارة الدورات (Courses CRUD)
        # ---------------------------------------------
        with tab_courses:
            st.subheader("قائمة الدورات الحالية")
            if st.session_state['courses']:
                df_courses = pd.DataFrame(st.session_state['courses']).T
                df_courses['ID'] = df_courses.index
                st.dataframe(df_courses[['ID', 'Name', 'Status']], use_container_width=True, hide_index=True)
                course_ids = list(st.session_state['courses'].keys())
            else:
                st.info("لا توجد دورات حالياً.")
                course_ids = []
                
            st.markdown("### تحكم في الدورات")
            col_c1, col_c2, col_c3 = st.columns(3)
            
            # إضافة دورة
            with col_c1.expander("➕ إضافة دورة جديدة"):
                with st.form("add_course_admin_form", clear_on_submit=True):
                    new_name = st.text_input("اسم الدورة")
                    new_status = st.selectbox("حالة الدورة", ["متاحة للتسجيل", "قيد الإعداد", "مكتملة"])
                    if st.form_submit_button("حفظ الدورة"):
                        if new_name:
                            new_id = get_next_id(st.session_state['courses'])
                            st.session_state['courses'][new_id] = {"Name": new_name, "Status": new_status}
                            st.success(f"✅ تمت إضافة الدورة **{new_name}** بالمعرف #{new_id}")
                        else:
                            st.error("الرجاء إدخال اسم الدورة.")
            
            # تعديل دورة
            with col_c2.expander("✍️ تعديل دورة موجودة"):
                if course_ids:
                    course_to_update = st.selectbox("اختر الدورة للتعديل", options=course_ids, format_func=lambda x: f"#{x} - {st.session_state['courses'][x]['Name']}", key="update_c_select")
                    current_name = st.session_state['courses'][course_to_update]['Name']
                    current_status = st.session_state['courses'][course_to_update]['Status']
                    
                    with st.form("update_course_admin_form"):
                        updated_name = st.text_input("الاسم الجديد للدورة", value=current_name)
                        updated_status = st.selectbox("الحالة الجديدة", ["متاحة للتسجيل", "قيد الإعداد", "مكتملة"], index=["متاحة للتسجيل", "قيد الإعداد", "مكتملة"].index(current_status))
                        
                        if st.form_submit_button("حفظ التعديلات"):
                            st.session_state['courses'][course_to_update] = {"Name": updated_name, "Status": updated_status}
                            st.success(f"✅ تم تعديل الدورة #{course_to_update} بنجاح.")
                else:
                    st.info("لا توجد دورات للتعديل.")
            
            # حذف دورة
            with col_c3.expander("🗑️ حذف دورة"):
                if course_ids:
                    course_to_delete = st.selectbox("اختر الدورة للحذف", options=course_ids, format_func=lambda x: f"#{x} - {st.session_state['courses'][x]['Name']}", key="delete_c_select")
                    if st.button("تأكيد حذف الدورة", key="delete_c_btn"):
                        deleted_name = st.session_state['courses'][course_to_delete]['Name']
                        if delete_item(st.session_state['courses'], course_to_delete):
                            st.success(f"🗑️ تم حذف الدورة **{deleted_name}** نهائياً.")
                else:
                    st.info("لا توجد دورات للحذف.")

        
        # ---------------------------------------------
        # B. إدارة المتدربين (Trainees CRUD)
        # ---------------------------------------------
        with tab_trainees:
            st.subheader("قائمة المتدربين المسجلين")
            if st.session_state['trainees']:
                df_trainees = pd.DataFrame(st.session_state['trainees']).T
                df_trainees['ID'] = df_trainees.index
                st.dataframe(df_trainees[['ID', 'Name', 'College', 'Course_Name', 'Date']], use_container_width=True, hide_index=True)
                trainee_ids = list(st.session_state['trainees'].keys())
            else:
                st.info("لا يوجد متدربون مسجلون.")
                trainee_ids = []

            st.markdown("### تحكم في المتدربين")
            col_t1, col_t2 = st.columns(2)

            # تعديل بيانات متدرب
            with col_t1.expander("✍️ تعديل بيانات متدرب"):
                if trainee_ids and st.session_state['courses']:
                    trainee_to_update = st.selectbox("اختر المتدرب للتعديل", options=trainee_ids, format_func=lambda x: f"#{x} - {st.session_state['trainees'][x]['Name']}", key="update_t_select")
                    current_data = st.session_state['trainees'][trainee_to_update]
                    
                    course_list = {k: v['Name'] for k, v in st.session_state['courses'].items()}
                    course_ids = list(course_list.keys())
                    
                    with st.form("update_trainee_admin_form"):
                        u_name = st.text_input("الاسم", value=current_data['Name'])
                        u_college = st.selectbox("الكلية", ["تكنولوجيا المعلومات", "الهندسة", "العلوم", "العلوم الإدارية", "أخرى"], index=["تكنولوجيا المعلومات", "الهندسة", "العلوم", "العلوم الإدارية", "أخرى"].index(current_data['College']))
                        u_course_id = st.selectbox("الدورة الجديدة", options=course_ids, format_func=lambda x: course_list[x], index=course_ids.index(current_data['Course_ID']))
                        
                        if st.form_submit_button("حفظ تعديلات المتدرب"):
                            st.session_state['trainees'][trainee_to_update]['Name'] = u_name
                            st.session_state['trainees'][trainee_to_update]['College'] = u_college
                            st.session_state['trainees'][trainee_to_update]['Course_ID'] = u_course_id
                            st.session_state['trainees'][trainee_to_update]['Course_Name'] = course_list[u_course_id]
                            st.success(f"✅ تم تحديث بيانات المتدرب **{u_name}** بنجاح.")
                else:
                    st.info("لا توجد بيانات متدربين أو دورات للتعديل.")

            # حذف متدرب
            with col_t2.expander("🗑️ حذف متدرب"):
                if trainee_ids:
                    trainee_to_delete = st.selectbox("اختر المتدرب للحذف", options=trainee_ids, format_func=lambda x: f"#{x} - {st.session_state['trainees'][x]['Name']}", key="delete_t_select")
                    if st.button("تأكيد حذف المتدرب", key="delete_t_btn"):
                        deleted_name = st.session_state['trainees'][trainee_to_delete]['Name']
                        if delete_item(st.session_state['trainees'], trainee_to_delete):
                            st.success(f"🗑️ تم حذف المتدرب **{deleted_name}** نهائياً.")
                else:
                    st.info("لا يوجد متدربون للحذف.")
        
        # ---------------------------------------------
        # C. إدارة تقارير التدقيق (Audit Logs CRUD)
        # ---------------------------------------------
        with tab_audit:
            st.subheader("سجل تقارير التدقيق الكامل")
            if st.session_state['audit_logs']:
                df_audit = pd.DataFrame(st.session_state['audit_logs']).T
                df_audit['ID'] = df_audit.index
                st.dataframe(df_audit[['ID', 'Lab', 'Auditor', 'Status', 'Time', 'Notes']], use_container_width=True, hide_index=True)
                audit_ids = list(st.session_state['audit_logs'].keys())
            else:
                st.info("لا توجد تقارير تدقيق مرفوعة.")
                audit_ids = []

            st.markdown("### تحكم في التقارير")
            col_a1, col_a2 = st.columns(2)
            
            # تعديل تقرير تدقيق
            with col_a1.expander("✍️ تعديل تقرير تدقيق"):
                if audit_ids:
                    audit_to_update = st.selectbox("اختر التقرير للتعديل", options=audit_ids, format_func=lambda x: f"#{x} - {st.session_state['audit_logs'][x]['Lab']} ({st.session_state['audit_logs'][x]['Time']})", key="update_a_select")
                    current_data = st.session_state['audit_logs'][audit_to_update]
                    
                    with st.form("update_audit_admin_form"):
                        u_status = st.selectbox("حالة التدقيق", ["ممتاز", "⚠️ يحتاج متابعة فورية"], index=["ممتاز", "⚠️ يحتاج متابعة فورية"].index(current_data['Status']))
                        u_notes = st.text_area("تعديل الملاحظات", value=current_data['Notes'])
                        
                        if st.form_submit_button("حفظ تعديلات التقرير"):
                            st.session_state['audit_logs'][audit_to_update]['Status'] = u_status
                            st.session_state['audit_logs'][audit_to_update]['Notes'] = u_notes
                            st.success(f"✅ تم تحديث التقرير #{audit_to_update} بنجاح.")
                else:
                    st.info("لا توجد تقارير للتعديل.")

            # حذف تقرير تدقيق
            with col_a2.expander("🗑️ حذف تقرير"):
                if audit_ids:
                    audit_to_delete = st.selectbox("اختر التقرير للحذف", options=audit_ids, format_func=lambda x: f"#{x} - {st.session_state['audit_logs'][x]['Lab']}", key="delete_a_select")
                    if st.button("تأكيد حذف التقرير", key="delete_a_btn"):
                        deleted_lab = st.session_state['audit_logs'][audit_to_delete]['Lab']
                        if delete_item(st.session_state['audit_logs'], audit_to_delete):
                            st.success(f"🗑️ تم حذف التقرير الخاص بـ **{deleted_lab}** نهائياً.")
                else:
                    st.info("لا توجد تقارير للحذف.")


    else:
        # ---------------------------------------------
        # نموذج تسجيل الدخول (تم إزالة بيانات الدليل)
        # ---------------------------------------------
        st.subheader("الرجاء تسجيل الدخول للوصول إلى لوحة الإدارة.")
        
        login_col1, login_col2 = st.columns(2)
        
        with login_col1:
            with st.form("login_form"):
                # **الأمان:** تم إزالة الوسيطة placeholder
                username = st.text_input("اسم المستخدم")
                password = st.text_input("كلمة المرور", type="password")
                
                if st.form_submit_button("🔑 تسجيل الدخول"):
                    login_user(username, password)
        
        with login_col2:
            st.warning("""
            **ملاحظة هامة:**
            * بيانات الاعتماد هي: **AABU** / **Aabu2025**
            
            """)
