import streamlit as st
import pandas as pd
from datetime import datetime

# --- تهيئة البيانات والتخزين (Session State) ---
# التخزين المؤقت للبيانات. هذه البيانات ستمحى عند إيقاف تشغيل الكود في Colab.
if 'courses' not in st.session_state:
    st.session_state['courses'] = {
        1: {"Name": "أساسيات المحاكاة (Arena)", "Status": "متاحة للتسجيل"},
        2: {"Name": "النمذجة الرياضية (Matlab)", "Status": "متاحة للتسجيل"},
    }
if 'trainees' not in st.session_state:
    st.session_state['trainees'] = {
        101: {"Name": "خالد محمد", "Type": "طالب بكالوريوس", "College": "تكنولوجيا المعلومات", "Course_ID": 1, "Course_Name": "أساسيات المحاكاة (Arena)", "Date": "2025-11-01"},
        102: {"Name": "سارة علي", "Type": "طالب دراسات عليا", "College": "الهندسة", "Course_ID": 2, "Course_Name": "النمذجة الرياضية (Matlab)", "Date": "2025-11-05"},
    }
if 'audit_logs' not in st.session_state:
    st.session_state['audit_logs'] = {
        201: {"Lab": "Lab A (Simulation)", "Auditor": "أحمد حسين", "Time": "2025-11-20 09:00", "Status": "ممتاز", "Notes": "جميع البرامج تعمل بامتياز."},
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

# --- إعدادات الصفحة والتصميم الاحترافي ---
st.set_page_config(
    page_title="نظام إدارة شعبة التدريب والتدقيق",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تعديل شكل الخطوط والألوان عبر حقن CSS
st.markdown("""
<style>
    /* تغيير الخطوط والألوان الأساسية */
    .stApp {
        direction: rtl; /* دعم الاتجاه من اليمين لليسار */
        text-align: right;
    }
    h1, h2, h3, h4 {
        color: #004d40; /* لون الأخضر الداكن */
    }
    .stButton>button {
        background-color: #004d40;
        color: white;
        border-radius: 8px;
    }
    /* تصميم البطاقات المترية */
    [data-testid="stMetricValue"] {
        font-size: 32px;
        color: #d9534f; /* لون الأحمر لإبراز الأرقام */
    }
</style>
""", unsafe_allow_html=True)


# --- القائمة الجانبية للتنقل ---
st.sidebar.title("🏛️ نظام الإدارة والتدقيق")
st.sidebar.header("لوحة التحكم الرئيسية")

menu = st.sidebar.radio(
    "اختر القسم:",
    ("🏠 الصفحة الرئيسية", "📚 تسجيل الدورات", "🔍 التدقيق والمتابعة", "📊 التقارير والإحصائيات", "👑 إدارة النظام الكاملة")
)

# ==========================================
# 1. الصفحة الرئيسية (Dashboard Overview)
# ==========================================
if menu == "🏠 الصفحة الرئيسية":
    st.title("لوحة بيانات رئيس الشعبة")
    st.markdown(f"**تاريخ اليوم:** {datetime.now().strftime('%Y-%m-%d')}")
    st.markdown("---")

    # عرض العدادات في كروت واضحة (Metrics)
    col1, col2, col3 = st.columns(3)
    col1.metric("👥 عدد المتدربين المسجلين", len(st.session_state['trainees']))
    col2.metric("📋 عدد الدورات النشطة", len(st.session_state['courses']))
    col3.metric("🚨 سجلات التدقيق المرفوعة", len(st.session_state['audit_logs']))

    st.markdown("---")

    st.header("سجل النشاطات الحديثة")

    # عرض آخر 5 متدربين
    recent_trainees = pd.DataFrame(st.session_state['trainees']).T.sort_index(ascending=False).head(5)
    st.subheader("أحدث المتدربين")
    if not recent_trainees.empty:
        st.dataframe(recent_trainees[['Name', 'Course_Name', 'Date']], use_container_width=True, hide_index=True)
    else:
        st.info("لا يوجد متدربون حديثون.")

# ==========================================
# 2. قسم تسجيل الدورات
# (الكود القديم للتسجيل لم يتغير كثيراً لتركيز التعديل على الإدارة)
# ==========================================
elif menu == "📚 تسجيل الدورات":
    st.header("📝 تسجيل المتدربين في الدورات")

    course_list = {k: v['Name'] for k, v in st.session_state['courses'].items()}

    with st.form("training_form", clear_on_submit=True):
        st.subheader("بيانات المتدرب")
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("الاسم الرباعي", key="reg_name")
            user_type = st.selectbox("الصفة", ["طالب بكالوريوس", "طالب دراسات عليا", "عضو هيئة تدريس", "إداري"], key="reg_type")

        with col2:
            college = st.selectbox("الكلية", ["تكنولوجيا المعلومات", "الهندسة", "العلوم", "العلوم الإدارية", "أخرى"], key="reg_college")

            # التأكد من وجود دورات متاحة قبل الاختيار
            if course_list:
                selected_course_id = st.selectbox("الدورة المطلوبة", options=list(course_list.keys()), format_func=lambda x: course_list[x], key="reg_course")
            else:
                st.error("لا توجد دورات متاحة حالياً. الرجاء مراجعة قسم الإدارة.")
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
            st.success(f"تم تسجيل المتدرب **{name}** بنجاح.")

# ==========================================
# 3. قسم التدقيق والمتابعة
# ==========================================
elif menu == "🔍 التدقيق والمتابعة":
    st.header("🔍 التدقيق اليومي للمختبرات والمرافق")

    with st.form("audit_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            lab_id = st.selectbox("اسم المرفق", ["Lab A (Simulation)", "Lab B (Modeling)", "قاعة التدريب"], key="audit_lab")
            auditor = st.text_input("اسم المدقق المسؤول", key="audit_auditor")

        st.markdown("**قائمة التحقق لضمان الجودة:**")

        check_col1, check_col2, check_col3 = st.columns(3)
        check_sw = check_col1.checkbox("البرمجيات تعمل بكفاءة")
        check_hw = check_col2.checkbox("الأجهزة سليمة (تكييف/كهرباء)")
        check_cl = check_col3.checkbox("نظافة القاعة والترتيب")

        notes = st.text_area("ملاحظات تفصيلية أو طلبات صيانة عاجلة", key="audit_notes")

        submit_audit = st.form_submit_button("✅ رفع تقرير التدقيق")

        if submit_audit and auditor:
            new_id = get_next_id(st.session_state['audit_logs'])
            status_text = "ممتاز" if (check_sw and check_hw and check_cl) else "يحتاج متابعة فورية"
            audit_entry = {
                "Lab": lab_id,
                "Auditor": auditor,
                "Time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Status": status_text,
                "Notes": notes
            }
            st.session_state['audit_logs'][new_id] = audit_entry
            if status_text == "ممتاز":
                st.success("تم حفظ التقرير بنجاح. المرافق بحالة ممتازة.")
            else:
                st.error(f"تم تسجيل التقرير. حالة المرفق **{status_text}**.")
        elif submit_audit and not auditor:
            st.warning("الرجاء إدخال اسم المدقق المسؤول.")

# ==========================================
# 4. التقارير والإحصائيات (Read Only)
# ==========================================
elif menu == "📊 التقارير والإحصائيات":
    st.header("📊 لوحة مؤشرات الأداء والتقارير")

    # ------------------
    st.subheader("إحصائيات التسجيل حسب الكلية")
    if st.session_state['trainees']:
        df_trainees = pd.DataFrame(st.session_state['trainees']).T
        college_counts = df_trainees['College'].value_counts()
        st.bar_chart(college_counts)

    # ------------------
    st.subheader("توزيع حالة التدقيق")
    if st.session_state['audit_logs']:
        df_audit = pd.DataFrame(st.session_state['audit_logs']).T
        audit_counts = df_audit['Status'].value_counts()
        st.dataframe(audit_counts.rename("العدد"), use_container_width=True)

    st.markdown("---")

    # تحميل البيانات كملف CSV
    if st.session_state['trainees']:
        df_full = pd.DataFrame(st.session_state['trainees']).T
        csv = df_full.to_csv(index=True).encode('utf-8')
        st.download_button(
            label="⬇️ تحميل بيانات المتدربين كاملة",
            data=csv,
            file_name='trainees_full_report.csv',
            mime='text/csv',
        )

# ==========================================
# 5. إدارة النظام الكاملة (Full Admin CRUD)
# ==========================================
elif menu == "👑 إدارة النظام الكاملة":
    st.title("👑 التحكم المركزي ببيانات النظام")
    st.error("تنبيه: هذا القسم يتيح حذف وتعديل البيانات الأساسية. استخدمه بحذر.")

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

        st.markdown("### تحكم")
        col_c1, col_c2, col_c3 = st.columns(3)

        # إضافة دورة
        with col_c1.expander("➕ إضافة دورة"):
            with st.form("add_course_admin_form", clear_on_submit=True):
                new_name = st.text_input("اسم الدورة")
                new_status = st.selectbox("حالة الدورة", ["متاحة للتسجيل", "قيد الإعداد", "مكتملة"])
                if st.form_submit_button("حفظ الدورة"):
                    if new_name:
                        new_id = get_next_id(st.session_state['courses'])
                        st.session_state['courses'][new_id] = {"Name": new_name, "Status": new_status}
                        st.success(f"تمت إضافة الدورة **{new_name}** بالمعرف #{new_id}")
                    else:
                        st.error("الرجاء إدخال اسم الدورة.")

        # تعديل دورة
        with col_c2.expander("✍️ تعديل دورة"):
            if course_ids:
                course_to_update = st.selectbox("اختر الدورة للتعديل", options=course_ids, format_func=lambda x: f"#{x} - {st.session_state['courses'][x]['Name']}", key="update_c_select")
                current_name = st.session_state['courses'][course_to_update]['Name']
                current_status = st.session_state['courses'][course_to_update]['Status']

                with st.form("update_course_admin_form"):
                    updated_name = st.text_input("الاسم الجديد للدورة", value=current_name)
                    updated_status = st.selectbox("الحالة الجديدة", ["متاحة للتسجيل", "قيد الإعداد", "مكتملة"], index=["متاحة للتسجيل", "قيد الإعداد", "مكتملة"].index(current_status))

                    if st.form_submit_button("حفظ التعديلات"):
                        st.session_state['courses'][course_to_update] = {"Name": updated_name, "Status": updated_status}
                        st.success(f"تم تعديل الدورة #{course_to_update} بنجاح.")
            else:
                st.info("لا توجد دورات للتعديل.")

        # حذف دورة
        with col_c3.expander("🗑️ حذف دورة"):
            if course_ids:
                course_to_delete = st.selectbox("اختر الدورة للحذف", options=course_ids, format_func=lambda x: f"#{x} - {st.session_state['courses'][x]['Name']}", key="delete_c_select")
                if st.button("تأكيد حذف الدورة", key="delete_c_btn"):
                    deleted_name = st.session_state['courses'][course_to_delete]['Name']
                    if delete_item(st.session_state['courses'], course_to_delete):
                        st.success(f"تم حذف الدورة **{deleted_name}** نهائياً.")
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

        st.markdown("### تحكم")
        col_t1, col_t2 = st.columns(2)

        # تعديل بيانات متدرب
        with col_t1.expander("✍️ تعديل متدرب"):
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
                        st.success(f"تم تحديث بيانات المتدرب **{u_name}** بنجاح.")
            else:
                st.info("لا توجد بيانات متدربين أو دورات للتعديل.")

        # حذف متدرب
        with col_t2.expander("🗑️ حذف متدرب"):
            if trainee_ids:
                trainee_to_delete = st.selectbox("اختر المتدرب للحذف", options=trainee_ids, format_func=lambda x: f"#{x} - {st.session_state['trainees'][x]['Name']}", key="delete_t_select")
                if st.button("تأكيد حذف المتدرب", key="delete_t_btn"):
                    deleted_name = st.session_state['trainees'][trainee_to_delete]['Name']
                    if delete_item(st.session_state['trainees'], trainee_to_delete):
                        st.success(f"تم حذف المتدرب **{deleted_name}** نهائياً.")
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

        st.markdown("### تحكم")
        col_a1, col_a2 = st.columns(2)

        # تعديل تقرير تدقيق
        with col_a1.expander("✍️ تعديل تقرير"):
            if audit_ids:
                audit_to_update = st.selectbox("اختر التقرير للتعديل", options=audit_ids, format_func=lambda x: f"#{x} - {st.session_state['audit_logs'][x]['Lab']} ({st.session_state['audit_logs'][x]['Time']})", key="update_a_select")
                current_data = st.session_state['audit_logs'][audit_to_update]

                with st.form("update_audit_admin_form"):
                    u_status = st.selectbox("حالة التدقيق", ["ممتاز", "يحتاج متابعة فورية"], index=["ممتاز", "يحتاج متابعة فورية"].index(current_data['Status']))
                    u_notes = st.text_area("تعديل الملاحظات", value=current_data['Notes'])

                    if st.form_submit_button("حفظ تعديلات التقرير"):
                        st.session_state['audit_logs'][audit_to_update]['Status'] = u_status
                        st.session_state['audit_logs'][audit_to_update]['Notes'] = u_notes
                        st.success(f"تم تحديث التقرير #{audit_to_update} بنجاح.")
            else:
                st.info("لا توجد تقارير للتعديل.")

        # حذف تقرير تدقيق
        with col_a2.expander("🗑️ حذف تقرير"):
            if audit_ids:
                audit_to_delete = st.selectbox("اختر التقرير للحذف", options=audit_ids, format_func=lambda x: f"#{x} - {st.session_state['audit_logs'][x]['Lab']} ({st.session_state['audit_logs'][x]['Time']})", key="delete_a_select")
                if st.button("تأكيد حذف التقرير", key="delete_a_btn"):
                    deleted_lab = st.session_state['audit_logs'][audit_to_delete]['Lab']
                    if delete_item(st.session_state['audit_logs'], audit_to_delete):
                        st.success(f"تم حذف تقرير التدقيق لـ **{deleted_lab}** نهائياً.")
            else:
                st.info("لا توجد تقارير للحذف.")
