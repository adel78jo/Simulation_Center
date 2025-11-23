import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# 🛑 1. إعدادات المصادقة (الأمان) 🛡️
# ==========================================
ADMIN_USER = "AABU"
ADMIN_PASS = "Aabu2025"

# --- تهيئة البيانات والتخزين (Session State) ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# البيانات الأولية (للتجربة)
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
    return max(data_dict.keys()) + 1 if data_dict else 1

def delete_item(data_dict, item_id):
    if item_id in data_dict:
        del data_dict[item_id]
        return True
    return False

# --- وظيفة تسجيل الدخول ---
def login_user(username, password):
    if username == ADMIN_USER and password == ADMIN_PASS:
        st.session_state['logged_in'] = True
        st.success("🎉 تم تسجيل الدخول بنجاح! يمكنك الآن الوصول لإدارة النظام.")
        st.rerun() 
    else:
        st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة.")

# --- وظيفة تسجيل الخروج ---
def logout_user():
    st.session_state['logged_in'] = False
    st.warning("تم تسجيل الخروج. محتوى الإدارة غير متاح.")
    st.rerun() 


# --- إعدادات الصفحة والتصميم الاحترافي الجديد ---
st.set_page_config(
    page_title="شعبة التدريب والتطوير والتدقيق والتوعية",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="👨‍🏫" 
)

# 🎨 تصميم CSS جديد مستوحى من الشعارات
st.markdown("""
<style>
    /* دعم الاتجاه من اليمين لليسار بشكل كامل */
    .stApp {
        direction: rtl;
        text-align: right;
        font-family: 'Tahoma', 'Arial', sans-serif;
    }
    
    /* الألوان الأساسية المستوحاة من الشعارين */
    :root {
        --primary-green: #008000; /* أخضر داكن من شعار الجامعة */
        --accent-yellow: #FFD700; /* أصفر من شعار المركز */
        --accent-blue: #007bff;   /* أزرق من شعار المركز */
        --accent-red: #dc3545;    /* أحمر من شعار المركز */
        --dark-text: #212121;
        --light-bg: #f9fbfd;      /* خلفية فاتحة جداً */
        --sidebar-bg: #e6ffe6;    /* خلفية أخضر فاتح جداً للشريط الجانبي */
        --sidebar-text: #004d00;  /* أخضر داكن لنصوص الشريط الجانبي */
    }

    /* العناوين والتأكيد */
    h1, h2, h3, h4 {
        color: var(--primary-green);
        border-bottom: 2px solid #e0ffe0; /* خط فاصل أخضر فاتح */
        padding-bottom: 8px; /* مسافة أكبر */
        margin-top: 25px;
        font-weight: bold;
    }
    
    /* زيادة حجم خطوط العناوين */
    h1 { font-size: 2.8em; }
    h2 { font-size: 2.2em; }
    h3 { font-size: 1.8em; }

    /* الشريط الجانبي - قائمة أكبر وخطوط أوضح */
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-bg);
        color: var(--sidebar-text);
        box-shadow: 2px 0 15px rgba(0, 0, 0, 0.08); /* ظل أوضح */
        min-width: 300px !important; /* زيادة عرض الشريط الجانبي */
        max-width: 300px !important;
    }
    .st-emotion-cache-c3y0s5 .st-emotion-cache-1jmpsc2 { /* targeting radio buttons in sidebar */
        font-size: 1.1em; /* حجم خط أكبر لعناصر القائمة */
        font-weight: 600;
        color: var(--sidebar-text);
        padding: 8px 0;
    }
    .st-emotion-cache-c3y0s5 .st-emotion-cache-1jmpsc2:hover {
        background-color: #d6f5d6; /* خلفية خفيفة عند المرور */
        border-radius: 5px;
    }

    /* الأزرار (Primary Action) */
    .stButton>button {
        background-color: var(--primary-green);
        color: white;
        border: none;
        border-radius: 10px; /* حواف أكثر ليونة */
        padding: 12px 25px; /* أزرار أكبر وأوضح */
        font-weight: bold;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
        transition: background-color 0.3s ease;
        font-size: 1.05em;
    }
    .stButton>button:hover {
        background-color: var(--accent-yellow); /* تأثير عند المرور */
        color: var(--dark-text);
    }
    
    /* بطاقات الإحصائيات (Metrics) - تصميم جديد */
    [data-testid="stMetric"] {
        background-color: white;
        border-left: 6px solid var(--accent-blue); /* شريط أزرق مميز */
        border-radius: 15px; /* حواف دائرية أكبر */
        padding: 20px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        text-align: right;
        margin-bottom: 15px; /* تباعد أفضل بين البطاقات */
    }
    [data-testid="stMetricLabel"] {
        font-size: 1.1em;
        color: #555; /* رمادي متوسط للوصف */
        font-weight: 600;
    }
    [data-testid="stMetricValue"] {
        font-size: 3em; /* قيمة أكبر */
        color: var(--primary-green);
        font-weight: bolder;
        margin-top: 5px;
    }
    [data-testid="stMetricDelta"] {
        font-size: 0.9em;
        font-weight: bold;
        margin-top: 10px;
    }

    /* حقول الإدخال والنصوص - وضوح وجمالية */
    .stTextInput>div>div>input, .stSelectbox>div>div, .stTextArea>div>div {
        border: 1px solid #ccc;
        border-radius: 10px; /* حواف أكثر دائرية للخانات */
        padding: 12px 15px;
        font-size: 1.05em; /* خط أوضح */
    }
    .stSelectbox>div>div {
        background-color: white;
    }

    /* الجداول (DataFrames) والحاويات */
    .stDataFrame, .stContainer {
        border-radius: 10px;
        border: 1px solid #e0ffe0; /* إطار أخضر فاتح */
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    .stExpander {
        border: 1px solid #e0ffe0;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .stExpander button {
        background-color: #f0fff0 !important; /* خلفية فاتحة لعنوان الموسع */
        color: var(--primary-green) !important;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px;
    }

    /* رسائل التنبيه */
    .stAlert {
        border-radius: 10px;
        padding: 15px;
        font-size: 1.1em;
    }
    .stAlert.success { background-color: #e6ffe6; color: #006400; } /* أخضر نجاح */
    .stAlert.error { background-color: #ffe6e6; color: #cc0000; } /* أحمر خطأ */
    .stAlert.warning { background-color: #fffacd; color: #a38c00; } /* أصفر تحذير */
    .stAlert.info { background-color: #e0f2f7; color: #006064; } /* أزرق معلومات */

</style>
""", unsafe_allow_html=True)


# ==========================================
# 🛑 2. التحكم في وصول المحتوى بالكامل 🛑
# ==========================================

if st.session_state['logged_in']:
    # ---------------------------------------------
    # المحتوى يظهر فقط إذا كان المستخدم مسجلاً دخوله
    # ---------------------------------------------
    
    # --- القائمة الجانبية للتنقل (تظهر فقط بعد الدخول) ---
    st.sidebar.image("download-removebg-preview (1).png", width=120) # شعار الجامعة
    st.sidebar.markdown("## شعبة التدريب والتطوير")
    st.sidebar.markdown("### مركز النمذجة والمحاكاة")
    st.sidebar.markdown("---")
    
    # تحديد القائمة
    menu = st.sidebar.radio(
        "القائمة الرئيسية:",
        ("🏠 لوحة التحكم", "📚 إدارة الدورات", "🔍 التدقيق والمتابعة", "📊 التقارير والإحصائيات", "🔑 أدوات الإدارة المتقدمة")
    )
    st.sidebar.markdown("---")
    st.sidebar.button("🔐 تسجيل الخروج", on_click=logout_user)


    # ==========================================
    # 1. لوحة التحكم (الصفحة الرئيسية الجديدة)
    # ==========================================
    if menu == "🏠 لوحة التحكم":
        # شعار المركز - صورة 2
        st.image("logo.jpg", width=200) 
        st.title("لوحة التحكم الرئيسية للمركز")
        st.subheader("مرحباً بك، مدير النظام. ملخص بيانات شعبة التدريب")
        
        st.markdown("---")
        
        # بيانات حسابات المتدربين والدورات
        total_trainees = len(st.session_state['trainees'])
        active_courses = len([c for c in st.session_state['courses'].values() if c['Status'] == 'متاحة للتسجيل'])
        audit_warnings = len([a for a in st.session_state['audit_logs'].values() if a['Status'] != 'ممتاز'])

        col1, col2, col3 = st.columns(3)
        col1.metric("👥 إجمالي المتدربين", total_trainees)
        col2.metric("📚 دورات متاحة حالياً", active_courses, delta=f"+{active_courses} جديد", delta_color="normal")
        col3.metric("⚠️ تقارير تدقيق بحاجة للمتابعة", audit_warnings, delta=audit_warnings if audit_warnings > 0 else 0, delta_color="inverse")
        
        st.markdown("---")

        # ملخص التسجيل حسب الكلية
        st.header("توزيع المتدربين حسب الكلية")
        
        chart_col, data_col = st.columns([2, 1])
        
        if st.session_state['trainees']:
            df_trainees = pd.DataFrame(st.session_state['trainees']).T
            college_counts = df_trainees['College'].value_counts()
            
            with chart_col:
                st.bar_chart(college_counts, color="#007bff") # استخدام الأزرق من الشعار
            
            with data_col:
                with st.expander("جدول البيانات التفصيلي"):
                    st.dataframe(college_counts.rename("العدد").reset_index().rename(columns={'index': 'الكلية'}), use_container_width=True, hide_index=True)
        else:
            st.info("لا توجد بيانات متدربين لعرضها حالياً.")

        st.markdown("---")
        
        st.header("آخر الأنشطة والتقارير")
        
        if st.session_state['audit_logs']:
            df_audit_latest = pd.DataFrame(st.session_state['audit_logs']).T.sort_values(by='Time', ascending=False).head(5)
            st.dataframe(df_audit_latest[['Lab', 'Auditor', 'Status', 'Time']], use_container_width=True, hide_index=True)
        else:
            st.info("لا توجد سجلات تدقيق لعرضها.")

    # ==========================================
    # 2. قسم إدارة الدورات 
    # ==========================================
    elif menu == "📚 إدارة الدورات":
        st.header("📝 إدارة الدورات التدريبية")
        st.markdown("هذا القسم مخصص لإضافة وحذف الدورات المتاحة والتعديل على حالة التسجيل.")
        
        if st.session_state['courses']:
            st.subheader("قائمة الدورات الحالية")
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
        with col_c2.expander("✍️ تعديل بيانات دورة"):
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
        
        with col_c3.expander("🗑️ حذف دورة"):
            if course_ids:
                course_to_delete = st.selectbox("اختر الدورة للحذف", options=course_ids, format_func=lambda x: f"#{x} - {st.session_state['courses'][x]['Name']}", key="delete_c_select")
                if st.button("تأكيد حذف الدورة", key="delete_c_btn"):
                    deleted_name = st.session_state['courses'][course_to_delete]['Name']
                    if delete_item(st.session_state['courses'], course_to_delete):
                        st.success(f"🗑️ تم حذف الدورة **{deleted_name}** نهائياً.")
            else:
                st.info("لا توجد دورات للحذف.")

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
        st.header("📊 تقارير الأداء والبيانات")
        st.markdown("استعرض الإحصائيات الرئيسية وحمل تقارير البيانات.")
        
        st.subheader("سجل المتدربين حسب الدورة")
        if st.session_state['trainees']:
            df_trainees = pd.DataFrame(st.session_state['trainees']).T
            course_counts = df_trainees['Course_Name'].value_counts()
            st.bar_chart(course_counts, color="#FFD700") # استخدام الأصفر من الشعار
            
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
                label="⬇️ تحميل بيانات المتدربين (CSV)", data=csv_trainees, file_name='تقارير_المتدربين.csv', mime='text/csv',)
        if st.session_state['audit_logs']:
            df_full_audit = pd.DataFrame(st.session_state['audit_logs']).T
            csv_audit = df_full_audit.to_csv(index=True).encode('utf-8')
            col_dl2.download_button(
                label="⬇️ تحميل تقارير التدقيق (CSV)", data=csv_audit, file_name='تقارير_التدقيق.csv', mime='text/csv',)
        if st.session_state['courses']:
            df_full_courses = pd.DataFrame(st.session_state['courses']).T
            csv_courses = df_full_courses.to_csv(index=True).encode('utf-8')
            col_dl3.download_button(
                label="⬇️ تحميل بيانات الدورات (CSV)", data=csv_courses, file_name='بيانات_الدورات.csv', mime='text/csv',)

    # ==========================================
    # 5. إدارة النظام الكاملة (التحكم بالحذف والتعديل المتقدم)
    # ==========================================
    elif menu == "🔑 أدوات الإدارة المتقدمة":
        st.title("🔑 أدوات الإدارة المتقدمة")
        st.error("تنبيه: هذا القسم يتيح حذف المتدربين وتقارير التدقيق. استخدمه بحذر شديد.")
        
        st.markdown("---")
        
        tab_trainees, tab_audit = st.tabs(["👥 إدارة المتدربين", "📝 إدارة تقارير التدقيق"])

        # ---------------------------------------------
        # A. إدارة المتدربين (حذف وتعديل)
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
                            # 🛑 تم تصحيح الخطأ هنا 
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
                    trainee_to_delete = st.selectbox("اختر المتدرب للحذف", options=trainee_ids, format_func=lambda x: f"#{x} - {st.session_state['trainees'][x]['Name']}", key="delete_t_select_admin")
                    if st.button("تأكيد حذف المتدرب", key="delete_t_btn_admin"):
                        deleted_name = st.session_state['trainees'][trainee_to_delete]['Name']
                        if delete_item(st.session_state['trainees'], trainee_to_delete):
                            st.success(f"🗑️ تم حذف المتدرب **{deleted_name}** نهائياً.")
                else:
                    st.info("لا يوجد متدربون للحذف.")
        
        # ---------------------------------------------
        # B. إدارة تقارير التدقيق (حذف وتعديل)
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
                    audit_to_update = st.selectbox("اختر التقرير للتعديل", options=audit_ids, format_func=lambda x: f"#{x} - {st.session_state['audit_logs'][x]['Lab']}", key="update_a_select_admin")
                    current_data = st.session_state['audit_logs'][audit_to_update]
                    
                    with st.form("update_audit_admin_form_audit"):
                        u_status = st.selectbox("حالة التدقيق", ["ممتاز", "⚠️ يحتاج متابعة فورية"], index=["ممتاز", "⚠️ يحتاج متابعة فورية"].index(current_data['Status']), key="u_status_audit")
                        u_notes = st.text_area("تعديل الملاحظات", value=current_data['Notes'], key="u_notes_audit")
                        
                        if st.form_submit_button("حفظ تعديلات التقرير"):
                            st.session_state['audit_logs'][audit_to_update]['Status'] = u_status
                            st.session_state['audit_logs'][audit_to_update]['Notes'] = u_notes
                            st.success(f"✅ تم تحديث التقرير #{audit_to_update} بنجاح.")
                else:
                    st.info("لا توجد تقارير للتعديل.")

            # حذف تقرير تدقيق
            with col_a2.expander("🗑️ حذف تقرير"):
                if audit_ids:
                    audit_to_delete = st.selectbox("اختر التقرير للحذف", options=audit_ids, format_func=lambda x: f"#{x} - {st.session_state['audit_logs'][x]['Lab']}", key="delete_a_select_admin")
                    if st.button("تأكيد حذف التقرير", key="delete_a_btn_admin"):
                        deleted_lab = st.session_state['audit_logs'][audit_to_delete]['Lab']
                        if delete_item(st.session_state['audit_logs'], audit_to_delete):
                            st.success(f"🗑️ تم حذف التقرير الخاص بـ **{deleted_lab}** نهائياً.")
                else:
                    st.info("لا توجد تقارير للحذف.")


else:
    # ---------------------------------------------
    # شاشة تسجيل الدخول (إذا لم يتم تسجيل الدخول) - آمنة
    # ---------------------------------------------
    st.title("🔐 بوابة الوصول المقيد")
    st.subheader("الوصول إلى لوحة التحكم يقتصر على مديري النظام المصرح لهم فقط.")
    
    st.sidebar.info("الرجاء تسجيل الدخول للمتابعة.")

    login_col1, login_col2 = st.columns([1, 1]) 
    
    with login_col1:
        with st.form("login_form"):
            username = st.text_input("اسم المستخدم")
            password = st.text_input("كلمة المرور", type="password")
            
            if st.form_submit_button("🔑 تسجيل الدخول"):
                login_user(username, password)
    
    with login_col2:
        # رسالة توجيهية عامة ومحايدة
        st.info("""
        **مركز النمذجة والمحاكاة - جامعة آل البيت:**
        نحن ملتزمون بتوفير بيئة تدريب وتطوير عالية الجودة.
        """)
