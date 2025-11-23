import streamlit as st
import pandas as pd
from datetime import datetime
import io

# ==========================================
# 🛑 1. إعدادات المصادقة (الأمان) 🛡️
# ==========================================
ADMIN_USER = "AABU"
ADMIN_PASS = "Aabu2025"

# --- تهيئة البيانات والتخزين (Session State) ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# البيانات الأولية (المحدثة بهياكل البيانات الجديدة: Date و Location و National_ID)
if 'courses' not in st.session_state:
    st.session_state['courses'] = {
        1: {"Name": "أساسيات المحاكاة (Arena)", "Status": "متاحة للتسجيل", "Trainer_ID": 502, "Date": "2026-01-15", "Location": "قاعة التدريب 1"},
        2: {"Name": "النمذجة الرياضية (Matlab)", "Status": "متاحة للتسجيل", "Trainer_ID": 501, "Date": "2026-02-10", "Location": "مختبر النمذجة"},
        3: {"Name": "الواقع الافتراضي والمعزز (VR/AR)", "Status": "قيد الإعداد", "Trainer_ID": None, "Date": "2026-03-01", "Location": "قيد التحديد"},
    }
if 'trainees' not in st.session_state:
    st.session_state['trainees'] = {
        101: {"Name": "خالد محمد", "National_ID": "1234567890", "Type": "طالب بكالوريوس", "College": "تكنولوجيا المعلومات", "Course_ID": 1, "Course_Name": "أساسيات المحاكاة (Arena)", "Date": "2025-11-01"},
        102: {"Name": "سارة علي", "National_ID": "2345678901", "Type": "طالب دراسات عليا", "College": "الهندسة", "Course_ID": 2, "Course_Name": "النمذجة الرياضية (Matlab)", "Date": "2025-11-05"},
        103: {"Name": "علي فؤاد", "National_ID": "3456789012", "Type": "موظف جامعة", "College": "العلوم", "Course_ID": 1, "Course_Name": "أساسيات المحاكاة (Arena)", "Date": "2025-11-20"},
    }
if 'audit_logs' not in st.session_state:
    st.session_state['audit_logs'] = {
        201: {"Lab": "مختبر النمذجة", "Auditor": "أحمد حسين", "Time": "2025-11-20 09:00", "Status": "ممتاز", "Notes": "جميع البرامج تعمل بامتياز."},
        202: {"Lab": "قاعة التدريب 1", "Auditor": "منى خالد", "Time": "2025-11-21 11:30", "Status": "يحتاج متابعة فورية", "Notes": "عطل في جهاز العرض."},
    }
if 'trainers' not in st.session_state:
    st.session_state['trainers'] = {
        501: {"Name": "د. أحمد علي", "Specialty": "النمذجة الرياضية", "Assigned_Course_ID": 2},
        502: {"Name": "م. سناء خالد", "Specialty": "المحاكاة الحاسوبية", "Assigned_Course_ID": 1},
        503: {"Name": "أ. عمر فوزي", "Specialty": "الواقع الافتراضي", "Assigned_Course_ID": None},
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


# --- إعدادات الصفحة والتصميم الاحترافي الجديد (الواجهة البيضاء) ---
st.set_page_config(
    page_title="مركز النمذجة والمحاكاة - جامعة آل البيت",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="⚙️" 
)

# 💎 تصميم CSS الفاخر (Clean Light Mode with Gold Accents)
st.markdown("""
<style>
    /* دعم الاتجاه من اليمين لليسار بشكل كامل */
    .stApp {
        direction: rtl;
        text-align: right;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* الألوان الأساسية - سمة بيضاء نظيفة مع لمسات ذهبية */
    :root {
        --primary-light: #FFFFFF;        /* خلفية أساسية بيضاء */
        --secondary-light: #F9F9F9;      /* خلفية ثانوية (مثل البطاقات) */
        --accent-gold: #CDA434;          /* لون ذهبي نحاسي (الرئيسي للتأكيد) */
        --text-dark: #333333;            /* لون النص الداكن */
        --text-muted: #666666;           /* لون النص الثانوي */
        --border-color-light: #E0E0E0;   /* لون الحدود الفاتح */
        --sidebar-bg: #F0F0F0;           /* خلفية الشريط الجانبي الفاتحة */
    }

    /* تطبيق الخلفية البيضاء على العناصر الرئيسية */
    .stApp, [data-testid="stHeader"] {
        background-color: var(--primary-light) !important;
        color: var(--text-dark) !important;
    }

    /* العناوين والتأكيد */
    h1, h2, h3, h4 {
        color: var(--text-dark); 
        border-bottom: 1px solid var(--border-color-light);
        padding-bottom: 10px;
        margin-top: 30px;
        font-weight: 700; 
    }
    h1 { font-size: 2.5em; color: var(--text-dark); } 
    h2 { font-size: 2em; color: var(--accent-gold); } 
    h3 { font-size: 1.7em; }

    /* ======================================================== */
    /* 📱 تحسين الاستجابة للشاشات الصغيرة (مثل الآيفون) 📱 */
    /* ======================================================== */
    
    /* الشريط الجانبي وتنسيق القائمة - الإعدادات الأساسية */
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-bg);
        border-right: 1px solid var(--border-color-light);
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1); 
        width: 300px;
    }
    
    @media (max-width: 768px) { 
        [data-testid="stSidebar"] {
            width: 250px !important; 
            max-width: 80% !important; 
        }
        h1 { font-size: 2.0em; } 
        h2 { font-size: 1.6em; } 
        h3 { font-size: 1.4em; }

        [data-testid="stMetricValue"] {
            font-size: 2.5em; 
        }
        
        div.stDataFrame {
            overflow-x: auto; 
        }
    }
    /* تحسين إظهار الـ Tabs على الهواتف */
    [data-testid="stTabItem"] {
        flex: 1 1 auto; /* لجعل التابات تأخذ مساحة متساوية */
        font-size: 0.9em !important;
    }


    /* تنسيق خيارات الراديو (القائمة الجانبية) */
    .st-emotion-cache-c3y0s5 .st-emotion-cache-1jmpsc2 { 
        font-size: 1.1em;
        font-weight: 500;
        color: var(--text-dark);
        padding: 12px 15px;
        border-radius: 8px;
        transition: background-color 0.2s ease;
    }
    .st-emotion-cache-c3y0s5 .st-emotion-cache-1jmpsc2:hover {
        background-color: rgba(205, 164, 52, 0.1); 
        color: var(--accent-gold);
    }
    .st-emotion-cache-c3y0s5 .st-emotion-cache-1jmpsc2[aria-selected="true"] {
        background-color: var(--accent-gold); 
        color: var(--primary-light); 
        font-weight: 700;
    }

    /* الأزرار (Primary Action) */
    .stButton>button {
        background: var(--accent-gold);
        color: var(--primary-light); 
        border: 1px solid var(--accent-gold);
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 700;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        font-size: 1.0em;
        margin-top: 10px;
    }
    .stButton>button:hover {
        background: #DDC873; 
        border-color: #DDC873;
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    /* بطاقات الإحصائيات (Metrics) */
    [data-testid="stMetric"] {
        background-color: var(--secondary-light);
        border: 1px solid var(--border-color-light);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        border-bottom: 3px solid var(--accent-gold); 
    }
    [data-testid="stMetricValue"] {
        font-size: 3.0em; 
        color: var(--accent-gold); 
        font-weight: bolder;
    }
    
    /* تنسيق خاص للشعارين */
    .logo-container {
        text-align: center;
        margin-bottom: 25px;
        padding-top: 10px;
    }

</style>
""", unsafe_allow_html=True)


# ==========================================
# 🛑 2. التحكم في وصول المحتوى بالكامل 🛑
# ==========================================

if st.session_state['logged_in']:
    
    # --- القائمة الجانبية للتنقل (المحدثة) ---
    st.sidebar.markdown(f"""
    <div class="logo-container">
        
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("## ⚙️ نظام الإدارة")
    st.sidebar.markdown("### صلاحيات التعديل الكاملة")
    st.sidebar.markdown("---")
    
    menu = st.sidebar.radio(
        "القائمة الرئيسية:",
        (
            "🖥️ لوحة التحكم",
            "📖 إدارة الدورات والمواعيد",          # صلاحيات تعديل الدورة، الموعد، الموقع، المدرب
            "👨‍🏫 إدارة المدربين",
            "👥 إدارة المتدربين المسجلين",        # صلاحيات تعديل وحذف المتدربين
            "📈 التقارير والإحصائيات والطباعة",  # صلاحيات تقارير شاملة وطباعة
            "🔎 التدقيق والمتابعة" 
        ),
        key="main_admin_menu"
    )

    st.sidebar.markdown("---")
    st.sidebar.button("🔐 تسجيل الخروج", on_click=logout_user)


    # ==========================================
    # 1. لوحة التحكم (الصفحة الرئيسية)
    # ==========================================
    if menu == "🖥️ لوحة التحكم":
        st.markdown(f"""
        <div class="logo-container">
            

[Image of logo.jpg]

        </div>
        """, unsafe_allow_html=True)
        
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
                st.bar_chart(college_counts, color=["#CDA434"]) 
            
            with data_col:
                with st.expander("جدول البيانات التفصيلي"):
                    st.dataframe(college_counts.rename("العدد").reset_index().rename(columns={'index': 'الكلية'}), use_container_width=True, hide_index=True)
        else:
            st.info("لا توجد بيانات متدربين لعرضها حالياً.")

    # ==========================================
    # 2. قسم إدارة الدورات والمواعيد (صلاحية التعديل الكاملة)
    # ==========================================
    elif menu == "📖 إدارة الدورات والمواعيد":
        st.header("📝 إدارة الدورات والمواعيد والمواقع")
        st.markdown("تحكم كامل في بيانات الدورات، بما في ذلك الاسم، الحالة، المدرب، الموعد، والموقع.")
        
        # 🛑 المنطقة المصححة: تحقق من وجود بيانات الدورات قبل العرض 🛑
        if st.session_state['courses']:
            st.subheader("قائمة الدورات الحالية وتفاصيلها")
            
            # إنشاء DataFrame وبناء الأعمدة المطلوبة
            df_courses = pd.DataFrame(st.session_state['courses']).T
            trainer_names = {k: v['Name'] for k, v in st.session_state['trainers'].items()}
            
            df_courses['Trainer_Name'] = df_courses['Trainer_ID'].apply(lambda x: trainer_names.get(x, 'غير مسند'))
            
            df_courses['ID'] = df_courses.index
            st.dataframe(df_courses[['ID', 'Name', 'Status', 'Trainer_Name', 'Date', 'Location']], use_container_width=True, hide_index=True)
            course_ids = list(st.session_state['courses'].keys())
        else:
            st.info("لا توجد دورات حالياً. ابدأ بإضافة دورة جديدة من الأسفل.")
            course_ids = []
            
        st.markdown("---")

        st.subheader("تحكم في الدورات (إضافة وحذف وتعديل)")

        col_c1, col_c2, col_c3 = st.columns(3)
        
        # إضافة دورة (بما في ذلك الموعد والموقع)
        with col_c1.expander("➕ إضافة دورة جديدة"):
            trainer_list = {k: v['Name'] for k, v in st.session_state['trainers'].items()}
            trainer_options = {name: id for id, name in trainer_list.items()}
            trainer_options['غير مسند'] = None
            
            with st.form("add_course_admin_form", clear_on_submit=True):
                new_name = st.text_input("اسم الدورة")
                new_status = st.selectbox("حالة الدورة", ["متاحة للتسجيل", "قيد الإعداد", "مكتملة"])
                new_date = st.date_input("موعد بدء الدورة", value=datetime.today().date(), min_value=datetime.today().date())
                new_location = st.text_input("موقع انعقاد الدورة (قاعة/مختبر)")
                selected_trainer_name = st.selectbox("إسناد مدرب للدورة", options=list(trainer_options.keys()))
                
                if st.form_submit_button("حفظ الدورة"):
                    if new_name and new_location:
                        new_id = get_next_id(st.session_state['courses'])
                        trainer_id_to_assign = trainer_options[selected_trainer_name]
                        
                        st.session_state['courses'][new_id] = {
                            "Name": new_name, 
                            "Status": new_status, 
                            "Trainer_ID": trainer_id_to_assign,
                            "Date": new_date.strftime("%Y-%m-%d"),
                            "Location": new_location
                        }
                        
                        if trainer_id_to_assign is not None:
                            st.session_state['trainers'][trainer_id_to_assign]['Assigned_Course_ID'] = new_id
                        
                        st.success(f"✅ تمت إضافة الدورة **{new_name}** بالموعد {new_date} والموقع **{new_location}**.")
                        st.rerun() 
                    else:
                        st.error("الرجاء إدخال اسم الدورة والموقع.")
        
        # تعديل دورة (بما في ذلك الموعد والموقع)
        with col_c2.expander("✍️ تعديل بيانات دورة"):
            if course_ids:
                course_to_update = st.selectbox("اختر الدورة للتعديل", options=course_ids, format_func=lambda x: f"#{x} - {st.session_state['courses'][x]['Name']}", key="update_c_select")
                current_data = st.session_state['courses'][course_to_update]
                
                # تهيئة القيم الحالية
                current_date = datetime.strptime(current_data['Date'], "%Y-%m-%d").date()
                current_trainer_id = current_data.get('Trainer_ID')

                trainer_list = {k: v['Name'] for k, v in st.session_state['trainers'].items()}
                trainer_options_names = list(trainer_list.values())
                trainer_options_names.append('غير مسند')
                
                default_trainer_name = trainer_list.get(current_trainer_id, "غير مسند")
                
                with st.form("update_course_admin_form"):
                    updated_name = st.text_input("الاسم الجديد للدورة", value=current_data['Name'])
                    updated_status = st.selectbox("الحالة الجديدة", ["متاحة للتسجيل", "قيد الإعداد", "مكتملة"], index=["متاحة للتسجيل", "قيد الإعداد", "مكتملة"].index(current_data['Status']))
                    updated_date = st.date_input("موعد بدء الدورة الجديد", value=current_date)
                    updated_location = st.text_input("موقع انعقاد الدورة الجديد", value=current_data['Location'])
                    updated_trainer_name = st.selectbox("إسناد مدرب للدورة", options=trainer_options_names, index=trainer_options_names.index(default_trainer_name))
                    
                    if st.form_submit_button("حفظ التعديلات"):
                        updated_trainer_id = next((k for k, v in trainer_list.items() if v == updated_trainer_name), None)

                        # تحديث إسناد المدربين
                        if current_trainer_id and current_trainer_id != updated_trainer_id and current_trainer_id in st.session_state['trainers']:
                            st.session_state['trainers'][current_trainer_id]['Assigned_Course_ID'] = None
                        if updated_trainer_id:
                            st.session_state['trainers'][updated_trainer_id]['Assigned_Course_ID'] = course_to_update
                        
                        # تحديث بيانات الدورة
                        st.session_state['courses'][course_to_update].update({
                            "Name": updated_name,
                            "Status": updated_status,
                            "Trainer_ID": updated_trainer_id,
                            "Date": updated_date.strftime("%Y-%m-%d"),
                            "Location": updated_location
                        })
                        
                        st.success(f"✅ تم تعديل الدورة #{course_to_update} بنجاح. الموعد الجديد: {updated_date} والموقع: **{updated_location}**")
                        st.rerun()
            else:
                st.info("لا توجد دورات للتعديل.")
        
        with col_c3.expander("🗑️ حذف دورة"):
            if course_ids:
                course_to_delete = st.selectbox("اختر الدورة للحذف", options=course_ids, format_func=lambda x: f"#{x} - {st.session_state['courses'][x]['Name']}", key="delete_c_select")
                if st.button("تأكيد حذف الدورة", key="delete_c_btn"):
                    deleted_name = st.session_state['courses'][course_to_delete]['Name']
                    trainer_id = st.session_state['courses'][course_to_delete].get('Trainer_ID')

                    if trainer_id and trainer_id in st.session_state['trainers']:
                         st.session_state['trainers'][trainer_id]['Assigned_Course_ID'] = None
                         
                    if delete_item(st.session_state['courses'], course_to_delete):
                        st.success(f"🗑️ تم حذف الدورة **{deleted_name}** نهائياً.")
                        st.rerun()
            else:
                st.info("لا توجد دورات للحذف.")

    # ==========================================
    # 3. قسم إدارة المدربين (تمت إضافة شروط الحماية من البيانات الفارغة)
    # ==========================================
    elif menu == "👨‍🏫 إدارة المدربين":
        st.header("🧑‍🏫 إدارة ومتابعة المدربين")
        st.markdown("هذا القسم يعرض تفاصيل المدربين، الدورات المسندة إليهم، وقائمة المسجلين في كل دورة.")

        # تجهيز البيانات للعرض
        if st.session_state['trainers']:
            df_trainers = pd.DataFrame(st.session_state['trainers']).T
            
            # يجب أن يكون القاموس موجوداً لإجراء الربط
            if st.session_state['courses']:
                course_names = {k: v['Name'] for k, v in st.session_state['courses'].items()}
            else:
                course_names = {}
                
            df_trainers['Assigned_Course_Name'] = df_trainers['Assigned_Course_ID'].apply(lambda x: course_names.get(x, 'غير مسند'))
            
            df_trainers['Trainer_ID'] = df_trainers.index
            
            st.subheader("قائمة المدربين وحالة الإسناد")
            st.dataframe(df_trainers[['Trainer_ID', 'Name', 'Specialty', 'Assigned_Course_Name']], use_container_width=True, hide_index=True)

            st.markdown("---")
            
            st.subheader("تفقد قائمة المسجلين لكل مدرب")
            
            trainer_options_keys = {f"#{id} - {data['Name']} ({data['Specialty']})": id for id, data in st.session_state['trainers'].items()}
            
            if trainer_options_keys:
                selected_trainer_key_name = st.selectbox("اختر المدرب لعرض تفاصيل دوره:", options=list(trainer_options_keys.keys()), key="select_trainer_for_view")
                
                trainer_id = trainer_options_keys[selected_trainer_key_name]
                assigned_course_id = st.session_state['trainers'][trainer_id]['Assigned_Course_ID']
                trainer_name = st.session_state['trainers'][trainer_id]['Name']
                
                if assigned_course_id is not None and assigned_course_id in st.session_state['courses']:
                    course_name = st.session_state['courses'][assigned_course_id]['Name']
                    st.success(f"المدرب **{trainer_name}** مسند لدورة: **{course_name}** (ID: {assigned_course_id})")

                    if st.session_state['trainees']:
                        df_trainees_trainer = pd.DataFrame(st.session_state['trainees']).T
                        df_trainees_trainer = df_trainees_trainer[df_trainees_trainer['Course_ID'] == assigned_course_id]
                        
                        if not df_trainees_trainer.empty:
                            df_trainees_trainer['Trainee_ID'] = df_trainees_trainer.index
                            st.info(f"عدد المسجلين في دورة **{course_name}**: {len(df_trainees_trainer)} متدرب.")
                            
                            st.dataframe(
                                df_trainees_trainer[['Trainee_ID', 'Name', 'College', 'Type', 'National_ID']],
                                use_container_width=True, 
                                hide_index=True
                            )
                        else:
                            st.warning(f"لا يوجد متدربون مسجلون حالياً في دورة المدرب **{course_name}**.")
                    else:
                        st.info("لا يوجد متدربون في النظام بعد.")
                        
                else:
                    st.warning(f"المدرب **{trainer_name}** غير مسند لأي دورة حالياً أو الدورة المسندة غير موجودة.")
        
        else:
            st.info("لا يوجد مدربون مضافون في النظام.")
    
    # ==========================================
    # 4. قسم إدارة المتدربين المسجلين (صلاحية التعديل الكاملة)
    # ==========================================
    elif menu == "👥 إدارة المتدربين المسجلين":
        st.header("👥 إدارة وتعديل بيانات المتدربين")
        st.markdown("تحكم كامل في بيانات المتدربين (الاسم، رقم الهوية، الكلية، الدورة المسجل بها، إلخ).")
        
        # 🛑 التصحيح هنا: نتحقق من وجود المتدربين أولاً
        if st.session_state['trainees']:
            st.subheader("قائمة المتدربين المسجلين")
            df_trainees = pd.DataFrame(st.session_state['trainees']).T
            df_trainees['ID'] = df_trainees.index
            
            st.dataframe(df_trainees[['ID', 'Name', 'National_ID', 'College', 'Course_Name', 'Date']], use_container_width=True, hide_index=True)
            trainee_ids = list(st.session_state['trainees'].keys())
        else:
            st.info("لا يوجد متدربون مسجلون.")
            trainee_ids = []

        st.markdown("---")
        st.subheader("تحكم وحذف المتدربين")
        
        col_t1, col_t2 = st.columns(2)

        # تعديل بيانات متدرب (بما في ذلك رقم الهوية)
        with col_t1.expander("✍️ تعديل بيانات متدرب"):
            if trainee_ids and st.session_state['courses']:
                trainee_to_update = st.selectbox("اختر المتدرب للتعديل", options=trainee_ids, format_func=lambda x: f"#{x} - {st.session_state['trainees'][x]['Name']}", key="update_t_select_advanced")
                current_data = st.session_state['trainees'][trainee_to_update]
                
                course_list = {k: v['Name'] for k, v in st.session_state['courses'].items()}
                course_ids = list(course_list.keys())
                
                with st.form("update_trainee_admin_form_advanced"):
                    u_name = st.text_input("الاسم", value=current_data['Name'], key="u_name_t_advanced")
                    u_national_id = st.text_input("رقم الهوية/الوطني", value=current_data['National_ID'], key="u_national_id_t_advanced")
                    u_college = st.selectbox("الكلية", ["تكنولوجيا المعلومات", "الهندسة", "العلوم", "العلوم الإدارية", "أخرى"], index=["تكنولوجيا المعلومات", "الهندسة", "العلوم", "العلوم الإدارية", "أخرى"].index(current_data['College']), key="u_college_t_advanced")
                    u_type = st.selectbox("النوع / الصفة", ["طالب بكالوريوس", "طالب دراسات عليا", "موظف جامعة", "خريج", "من خارج الجامعة"], index=["طالب بكالوريوس", "طالب دراسات عليا", "موظف جامعة", "خريج", "من خارج الجامعة"].index(current_data['Type']), key="u_type_t_advanced")
                    u_course_id = st.selectbox("الدورة الجديدة", options=course_ids, format_func=lambda x: course_list[x], index=course_ids.index(current_data['Course_ID']), key="u_course_id_t_advanced")
                    
                    if st.form_submit_button("حفظ تعديلات المتدرب", key="submit_t_advanced"):
                        st.session_state['trainees'][trainee_to_update]['Name'] = u_name
                        st.session_state['trainees'][trainee_to_update]['National_ID'] = u_national_id
                        st.session_state['trainees'][trainee_to_update]['College'] = u_college
                        st.session_state['trainees'][trainee_to_update]['Type'] = u_type
                        st.session_state['trainees'][trainee_to_update]['Course_ID'] = u_course_id
                        st.session_state['trainees'][trainee_to_update]['Course_Name'] = course_list[u_course_id]
                        st.success(f"✅ تم تحديث بيانات المتدرب **{u_name}** ورقم الهوية **{u_national_id}** بنجاح.")
                        st.rerun()
            else:
                st.info("لا توجد بيانات متدربين أو دورات للتعديل.")

        # حذف متدرب
        with col_t2.expander("🗑️ حذف متدرب"):
            if trainee_ids:
                trainee_to_delete = st.selectbox("اختر المتدرب للحذف", options=trainee_ids, format_func=lambda x: f"#{x} - {st.session_state['trainees'][x]['Name']}", key="delete_t_select_admin_advanced")
                if st.button("تأكيد حذف المتدرب", key="delete_t_btn_admin_advanced"):
                    deleted_name = st.session_state['trainees'][trainee_to_delete]['Name']
                    if delete_item(st.session_state['trainees'], trainee_to_delete):
                        st.success(f"🗑️ تم حذف المتدرب **{deleted_name}** نهائياً.")
                        st.rerun()
            else:
                st.info("لا يوجد متدربون للحذف.")


    # ==========================================
    # 5. التقارير والإحصائيات والطباعة (المحدث)
    # ==========================================
    elif menu == "📈 التقارير والإحصائيات والطباعة":
        st.header("📊 تقارير الأداء والبيانات والطباعة")
        st.markdown("استعرض الإحصائيات الرئيسية وحمل تقارير البيانات، أو قم بإعداد تقارير طباعية لدورة محددة.")
        
        tab_stats, tab_download, tab_print = st.tabs(["الإحصائيات الرئيسية", "تحميل البيانات الخام", "📄 تقارير الدورة للطباعة"])
        
        with tab_stats:
            st.subheader("سجل المتدربين حسب الدورة")
            if st.session_state['trainees']:
                df_trainees = pd.DataFrame(st.session_state['trainees']).T
                course_counts = df_trainees['Course_Name'].value_counts()
                st.bar_chart(course_counts, color=["#CDA434"])
            else:
                st.info("لا توجد بيانات متدربين للعرض.")
            
            st.markdown("---")
            st.subheader("توزيع حالة تقارير التدقيق")
            if st.session_state['audit_logs']:
                df_audit = pd.DataFrame(st.session_state['audit_logs']).T
                audit_counts = df_audit['Status'].value_counts().reset_index()
                audit_counts.columns = ['الحالة', 'العدد']
                st.dataframe(audit_counts, use_container_width=True, hide_index=True)
            else:
                st.info("لا توجد تقارير تدقيق للعرض.")
        
        with tab_download:
            st.subheader("تحميل البيانات الخام (CSV)")
            col_dl1, col_dl2, col_dl3 = st.columns(3)
            
            # تحميل المتدربين
            if st.session_state['trainees']:
                df_full_trainees = pd.DataFrame(st.session_state['trainees']).T
                df_full_trainees['ID'] = df_full_trainees.index # إضافة ID للملف
                buffer = io.BytesIO()
                df_full_trainees.to_csv(buffer, index=False, encoding='utf-8-sig') 
                csv_trainees = buffer.getvalue()
                
                col_dl1.download_button(
                    label="⬇️ تحميل بيانات المتدربين", data=csv_trainees, file_name='تقارير_المتدربين.csv', mime='text/csv;charset=utf-8',)
            
            # تحميل التدقيق
            if st.session_state['audit_logs']:
                df_full_audit = pd.DataFrame(st.session_state['audit_logs']).T
                buffer = io.BytesIO()
                df_full_audit.to_csv(buffer, index=True, encoding='utf-8-sig')
                csv_audit = buffer.getvalue()

                col_dl2.download_button(
                    label="⬇️ تحميل تقارير التدقيق", data=csv_audit, file_name='تقارير_التدقيق.csv', mime='text/csv;charset=utf-8',)
            
            # تحميل الدورات
            if st.session_state['courses']:
                df_full_courses = pd.DataFrame(st.session_state['courses']).T
                buffer = io.BytesIO()
                df_full_courses.to_csv(buffer, index=True, encoding='utf-8-sig')
                csv_courses = buffer.getvalue()
                
                col_dl3.download_button(
                    label="⬇️ تحميل بيانات الدورات", data=csv_courses, file_name='بيانات_الدورات.csv', mime='text/csv;charset=utf-8',)

        # 🛑 قسم الطباعة المصحح (لحل مشكلة KeyError عند اختيار دورة محذوفة) 🛑
        with tab_print:
            st.subheader("إعداد تقرير تفصيلي لدورة للطباعة")
            
            course_ids = list(st.session_state['courses'].keys())
            if course_ids:
                course_name_map = {cid: data['Name'] for cid, data in st.session_state['courses'].items()}
                
                selected_course_id = st.selectbox(
                    "اختر الدورة لطباعة التقرير:",
                    options=course_ids,
                    format_func=lambda x: course_name_map[x],
                    key="print_report_course_select"
                )
                
                if selected_course_id in st.session_state['courses']:
                    course_data = st.session_state['courses'][selected_course_id]
                    trainer_name = st.session_state['trainers'].get(course_data.get('Trainer_ID'), {}).get('Name', 'غير مسند')
                    
                    st.markdown("---")
                    
                    st.info("التقرير جاهز. اضغط **Ctrl+P** أو **Cmd+P** لطباعة الصفحة.")
                    
                    # 📄 محتوى التقرير 
                    st.markdown(f"""
                    <div style="direction: rtl; padding: 20px; border: 1px solid #ddd; border-radius: 10px; margin-top: 20px; background-color: #ffffff;">
                        <h2 style="color: #CDA434; text-align: center; border-bottom: 2px solid #CDA434; padding-bottom: 10px;">
                            تقرير تفصيلي لدورة تدريبية
                        </h2>
                        
                        <h3 style="color: #333; margin-top: 20px;">
                            بيانات الدورة الأساسية
                        </h3>
                        <p><strong>اسم الدورة:</strong> {course_data['Name']}</p>
                        <p><strong>رمز الدورة (ID):</strong> {selected_course_id}</p>
                        <p><strong>حالة التسجيل:</strong> {course_data['Status']}</p>
                        <p><strong>موعد الانعقاد:</strong> {course_data['Date']}</p>
                        <p><strong>موقع الانعقاد:</strong> <strong>{course_data['Location']}</strong></p>
                        <p><strong>المدرب المسؤول:</strong> <strong>{trainer_name}</strong></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("---")
                    st.markdown("### قائمة المتدربين المسجلين")

                    # استخراج قائمة المتدربين
                    if st.session_state['trainees']: # تحقق إضافي
                        df_trainees_filtered = pd.DataFrame(st.session_state['trainees']).T
                        df_trainees_filtered = df_trainees_filtered[df_trainees_filtered['Course_ID'] == selected_course_id]
                        
                        if not df_trainees_filtered.empty:
                            df_report = df_trainees_filtered[['Name', 'National_ID', 'College', 'Type', 'Date']].reset_index(names=['Trainee_ID'])
                            df_report.columns = ['رقم المتدرب', 'الاسم الكامل', 'رقم الهوية', 'الكلية/الجهة', 'الصفة', 'تاريخ التسجيل']
                            
                            st.dataframe(df_report, use_container_width=True, hide_index=True)
                            st.markdown(f"**إجمالي عدد المشاركين:** {len(df_report)}")
                        else:
                            st.warning("لا يوجد متدربون مسجلون في هذه الدورة حتى الآن.")
                    else:
                        st.info("لا يوجد متدربون مسجلون في النظام لعرضهم.")

                else:
                    st.warning("الدورة المختارة غير موجودة حالياً في النظام.")
            else:
                st.warning("يجب إضافة دورات أولاً لإعداد التقارير.")


    # ==========================================
    # 6. قسم التدقيق والمتابعة (المصحح)
    # ==========================================
    elif menu == "🔎 التدقيق والمتابعة":
        st.header("🔍 التدقيق اليومي للمرافق والبرامج")
        st.markdown("املأ هذا النموذج لرفع تقارير التدقيق الدورية.")
        
        # ... (منطق التدقيق كما هو) ...
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
                st.rerun()
            elif submit_audit and not auditor:
                st.warning("الرجاء إدخال اسم المدقق المسؤول.")


# ==========================================
# 🛑 7. شاشة تسجيل الدخول والصفحة العامة 🛑
# ==========================================
else:
    st.title("مركز النمذجة والمحاكاة بجامعة آل البيت")
    st.subheader("تسجيل المتدربين ودخول نظام الإدارة")
    
    available_courses = {k: v for k, v in st.session_state['courses'].items() if v['Status'] == 'متاحة للتسجيل'}
    course_options = {f"#{k} - {v['Name']} - الموعد: {v['Date']}": k for k, v in available_courses.items()}
    
    tab_login, tab_register = st.tabs(["🔑 دخول المدير", "📝 تسجيل في دورة"])
    
    # ------------------
    # 1. علامة تبويب دخول المدير
    # ------------------
    with tab_login:
        st.info("الوصول إلى لوحة التحكم يقتصر على مديري النظام المصرح لهم فقط.")
        
        login_col1, login_col2 = st.columns([1, 1]) 
        
        with login_col1:
            with st.form("login_form"):
                username = st.text_input("اسم المستخدم")
                password = st.text_input("كلمة المرور", type="password")
                
                if st.form_submit_button("🔑 تسجيل الدخول"):
                    login_user(username, password)
        
        with login_col2:
            st.markdown(f"""
            <div style="margin-top: 30px; border-right: 3px solid var(--accent-gold); padding-left: 15px;">
                <p style="font-size: 1.1em; font-weight: bold; color: var(--accent-gold);">
                    مركز النمذجة والمحاكاة - جامعة آل البيت:
                </p>
                <p style="color: var(--text-muted);">
                    نحن ملتزمون بتوفير بيئة تدريب وتطوير عالية الجودة في مجالات النمذجة والمحاكاة والواقع الافتراضي.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
    # ------------------
    # 2. علامة تبويب تسجيل المتدرب (تم إضافة رقم الهوية)
    # ------------------
    with tab_register:
        st.header("التسجيل في الدورات التدريبية المتاحة")
        st.markdown("يرجى ملء النموذج أدناه للتسجيل. مطلوب إدخال رقم الهوية للتوثيق الرسمي.")
        
        if not available_courses:
            st.warning("⚠️ لا توجد دورات متاحة للتسجيل حالياً. يرجى مراجعة الموقع لاحقاً.")
        else:
            with st.form("trainee_registration_form", clear_on_submit=True):
                t_name = st.text_input("الاسم الرباعي الكامل")
                t_national_id = st.text_input("رقم الهوية / الرقم الوطني (للتوثيق)")
                t_type = st.selectbox("النوع / الصفة", ["طالب بكالوريوس", "طالب دراسات عليا", "موظف جامعة", "خريج", "من خارج الجامعة"])
                t_college = st.selectbox("الكلية / الجهة المنتمي إليها", ["تكنولوجيا المعلومات", "الهندسة", "العلوم", "العلوم الإدارية", "الآداب", "أخرى"])
                
                selected_course_key = st.selectbox("اختر الدورة للتسجيل", options=list(course_options.keys()))
                
                register_button = st.form_submit_button("✅ إرسال طلب التسجيل")
                
                if register_button:
                    if t_name and selected_course_key and t_national_id:
                        course_id_selected = course_options[selected_course_key]
                        course_name_selected = available_courses[course_id_selected]['Name']
                        
                        new_trainee_id = get_next_id(st.session_state['trainees'])
                        st.session_state['trainees'][new_trainee_id] = {
                            "Name": t_name,
                            "National_ID": t_national_id,
                            "Type": t_type,
                            "College": t_college,
                            "Course_ID": course_id_selected,
                            "Course_Name": course_name_selected,
                            "Date": datetime.now().strftime("%Y-%m-%d")
                        }
                        
                        st.success(f"🎉 تم تسجيلك بنجاح في دورة **{course_name_selected}**! رقم هويتك المسجل هو **{t_national_id}**.")
                        st.rerun()
                    else:
                        st.error("الرجاء تعبئة جميع الحقول المطلوبة (الاسم ورقم الهوية واختيار الدورة).")
