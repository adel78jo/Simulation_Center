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
        1: {"Name": "أساسيات المحاكاة (Arena)", "Status": "متاحة للتسجيل", "Trainer_ID": 502},
        2: {"Name": "النمذجة الرياضية (Matlab)", "Status": "متاحة للتسجيل", "Trainer_ID": 501},
        3: {"Name": "الواقع الافتراضي والمعزز (VR/AR)", "Status": "قيد الإعداد", "Trainer_ID": None},
    }
if 'trainees' not in st.session_state:
    st.session_state['trainees'] = {
        101: {"Name": "خالد محمد", "Type": "طالب بكالوريوس", "College": "تكنولوجيا المعلومات", "Course_ID": 1, "Course_Name": "أساسيات المحاكاة (Arena)", "Date": "2025-11-01"},
        102: {"Name": "سارة علي", "Type": "طالب دراسات عليا", "College": "الهندسة", "Course_ID": 2, "Course_Name": "النمذجة الرياضية (Matlab)", "Date": "2025-11-05"},
        103: {"Name": "علي فؤاد", "Type": "موظف جامعة", "College": "العلوم", "Course_ID": 1, "Course_Name": "أساسيات المحاكاة (Arena)", "Date": "2025-11-20"},
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


# --- إعدادات الصفحة والتصميم الاحترافي الجديد ---
st.set_page_config(
    page_title="مركز النمذجة والمحاكاة - جامعة آل البيت",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="⚙️" # أيقونة عامة تعبر عن الهندسة والتقنية
)

# 🎨 تصميم CSS جديد كلياً
st.markdown("""
<style>
    /* دعم الاتجاه من اليمين لليسار بشكل كامل */
    .stApp {
        direction: rtl;
        text-align: right;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; /* خط احترافي */
    }
    
    /* الألوان الأساسية - لوحة ألوان هندسية احترافية */
    :root {
        --primary-blue: #004D80;     /* أزرق داكن للمكونات الرئيسية */
        --secondary-grey: #4A4A4A;   /* رمادي داكن للنصوص */
        --accent-lime: #8BC34A;      /* أخضر زيزفوني للمسات البارزة */
        --light-blue: #ADD8E6;      /* أزرق فاتح للخلفيات */
        --background-light: #F8F9FA; /* خلفية فاتحة جداً */
        --sidebar-bg: #E3F2FD;       /* أزرق فاتح جداً للشريط الجانبي */
        --sidebar-text: #004D80;     /* نص الشريط الجانبي أزرق داكن */
        --card-bg: #FFFFFF;          /* خلفية البطاقات بيضاء */
        --border-color: #E0E0E0;     /* لون الحدود الخفيف */
    }

    /* العناوين والتأكيد */
    h1, h2, h3, h4 {
        color: var(--primary-blue);
        border-bottom: 2px solid var(--light-blue);
        padding-bottom: 10px;
        margin-top: 30px;
        font-weight: 700; /* خط سميك */
    }
    h1 { font-size: 2.5em; }
    h2 { font-size: 2em; }
    h3 { font-size: 1.7em; }

    /* الشريط الجانبي - تصميم أنيق وحديث */
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-bg);
        color: var(--sidebar-text);
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05); /* ظل خفيف */
        min-width: 300px !important;
        max-width: 300px !important;
    }
    .st-emotion-cache-c3y0s5 .st-emotion-cache-1jmpsc2 { /* لروابط القائمة الجانبية */
        font-size: 1.15em;
        font-weight: 600;
        color: var(--sidebar-text);
        padding: 12px 15px;
        border-radius: 8px;
        transition: background-color 0.2s ease;
    }
    .st-emotion-cache-c3y0s5 .st-emotion-cache-1jmpsc2:hover {
        background-color: rgba(0, 77, 128, 0.1); /* ظل أزرق خفيف عند التحويم */
    }
    .st-emotion-cache-c3y0s5 .st-emotion-cache-1jmpsc2[aria-selected="true"] {
        background-color: var(--primary-blue); /* خلفية زرقاء داكنة للعنصر المختار */
        color: white;
        box-shadow: 0 2px 8px rgba(0, 77, 128, 0.2);
    }

    /* الأزرار (Primary Action) */
    .stButton>button {
        background-color: var(--primary-blue);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 25px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        font-size: 1.0em;
        margin-top: 10px;
    }
    .stButton>button:hover {
        background-color: var(--accent-lime); /* يتغير للأخضر الزيزفوني عند التحويم */
        color: var(--secondary-grey);
        transform: translateY(-2px); /* تأثير ارتفاع بسيط */
    }
    
    /* بطاقات الإحصائيات (Metrics) - تصميم جديد */
    [data-testid="stMetric"] {
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        text-align: center;
        transition: transform 0.2s ease;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px); /* تأثير ارتفاع عند التحويم */
    }
    [data-testid="stMetricValue"] {
        font-size: 3.5em; /* حجم أكبر للقيمة */
        color: var(--primary-blue);
        font-weight: bolder;
        margin-bottom: 5px;
    }
    [data-testid="stMetricLabel"] {
        font-size: 1.1em;
        color: var(--secondary-grey);
        font-weight: 500;
    }
    [data-testid="stMetricDelta"] {
        font-size: 0.9em;
        font-weight: bold;
        color: var(--accent-lime); /* لون الدلتا بالأخضر */
    }

    /* تنسيق خاص للشعارين باستخدام HTML */
    .logo-container {
        text-align: center;
        margin-bottom: 25px;
        padding-top: 10px;
    }
    .logo-image-sidebar {
        width: 130px; /* حجم أكبر للشعار في الشريط الجانبي */
        height: auto;
        display: block;
        margin-right: auto;
        margin-left: auto;
        border-radius: 8px; /* حواف دائرية بسيطة */
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    .logo-image-main {
        width: 250px; /* حجم أكبر للشعار الرئيسي */
        height: auto;
        display: block;
        margin-right: auto;
        margin-left: auto;
        border-radius: 12px;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.15);
        margin-bottom: 40px; /* تباعد أكبر */
    }

    /* تحسين تصميم النماذج والحقول */
    .st-emotion-cache-czk5ad { /* Container for forms/expander content */
        background-color: var(--background-light);
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border: 1px solid var(--border-color);
    }
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        border-radius: 8px;
        border: 1px solid var(--border-color);
        padding: 10px;
    }
    .stTextArea>div>div>textarea {
        border-radius: 8px;
        border: 1px solid var(--border-color);
        padding: 10px;
    }
    
    /* تصميم الـ Expander */
    .st-emotion-cache-1ftrzg7 p { /* Expander header text */
        font-weight: 600;
        color: var(--primary-blue);
        font-size: 1.1em;
    }
    .st-emotion-cache-l350x7 { /* Expander button */
        border-radius: 8px;
        background-color: var(--sidebar-bg);
        border: 1px solid var(--light-blue);
    }

    /* Info, Success, Warning, Error messages */
    .stAlert {
        border-radius: 8px;
        font-weight: 500;
        padding: 15px 20px;
    }
    .stAlert.success { background-color: #E6F7D9; border-left: 5px solid #8BC34A; }
    .stAlert.info { background-color: #EBF5FB; border-left: 5px solid #007bff; }
    .stAlert.warning { background-color: #FFF3CD; border-left: 5px solid #FFC107; }
    .stAlert.error { background-color: #F8D7DA; border-left: 5px solid #DC3545; }

    /* Tabs styling */
    .stTabs [data-testid="stTabItem"] {
        background-color: var(--background-light);
        color: var(--secondary-grey);
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 600;
        border: 1px solid var(--border-color);
        border-bottom: none;
        margin-left: 5px; /* تباعد بين علامات التبويب */
    }
    .stTabs [data-testid="stTabItem"][data-selected="true"] {
        background-color: var(--primary-blue);
        color: white;
        border-color: var(--primary-blue);
        border-bottom: none;
    }
    .stTabs [data-testid="stVerticalTabs"] {
        background-color: var(--background-light);
        border-radius: 10px;
        border: 1px solid var(--border-color);
    }
    .stTabs [data-testid="stVerticalTabItem"] {
        background-color: var(--background-light);
        color: var(--secondary-grey);
        border-radius: 8px;
        padding: 10px 15px;
        margin-bottom: 5px;
        font-weight: 500;
    }
    .stTabs [data-testid="stVerticalTabItem"][data-selected="true"] {
        background-color: var(--primary-blue);
        color: white;
    }

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
    st.sidebar.markdown(f"""
    <div class="logo-container">
        <img src="aabu_logo.png" class="logo-image-sidebar">
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("## ⚙️ نظام إدارة المركز")
    st.sidebar.markdown("### شعبة التدريب والتطوير")
    st.sidebar.markdown("---")
    
    # تحديد القائمة (مع أيقونات جديدة)
    menu = st.sidebar.radio(
        "القائمة الرئيسية:",
        (
            "🏠 لوحة التحكم",
            "📚 إدارة الدورات",
            "🧑‍🏫 إدارة المدربين",
            "📊 التقارير والإحصائيات",
            "🔍 التدقيق والمتابعة", # تم تغيير الترتيب ليتناسب مع الأهمية
            "🔑 أدوات الإدارة المتقدمة"
        ),
        icons=["house", "book", "person-badge", "bar-chart", "search", "key"] # أيقونات Bootstrap
    )
    st.sidebar.markdown("---")
    st.sidebar.button("🔐 تسجيل الخروج", on_click=logout_user)


    # ==========================================
    # 1. لوحة التحكم (الصفحة الرئيسية الجديدة)
    # ==========================================
    if menu == "🏠 لوحة التحكم":
        st.markdown(f"""
        <div class="logo-container">
            <img src="simulation_logo.jpg" class="logo-image-main">
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
                st.bar_chart(college_counts, color="#007bff") 
            
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
    # 2. قسم إدارة الدورات (تم إضافة تفقد المسجلين)
    # ==========================================
    elif menu == "📚 إدارة الدورات":
        st.header("📝 إدارة الدورات التدريبية")
        st.markdown("هذا القسم مخصص لإضافة وحذف الدورات المتاحة والتعديل على حالة التسجيل و **عرض قائمة المسجلين**.")
        
        # قائمة الدورات الحالية
        if st.session_state['courses']:
            st.subheader("قائمة الدورات الحالية")
            
            # إضافة اسم المدرب إلى جدول الدورات
            df_courses = pd.DataFrame(st.session_state['courses']).T
            
            # ربط اسم المدرب بالدورة
            trainer_names = {k: v['Name'] for k, v in st.session_state['trainers'].items()}
            df_courses['Trainer_Name'] = df_courses['Trainer_ID'].apply(lambda x: trainer_names.get(x, 'غير مسند'))
            
            df_courses['ID'] = df_courses.index
            st.dataframe(df_courses[['ID', 'Name', 'Status', 'Trainer_Name']], use_container_width=True, hide_index=True)
            course_ids = list(st.session_state['courses'].keys())
        else:
            st.info("لا توجد دورات حالياً.")
            course_ids = []
            
        st.markdown("---")

        # 🛑 خانة تفقد المسجلين 🛑
        st.subheader("👥 تفقد المتدربين المسجلين في دورة")
        
        if course_ids:
            # دالة مساعدة لربط المعرف بالاسم
            course_name_map = {cid: data['Name'] for cid, data in st.session_state['courses'].items()}
            
            selected_course_id = st.selectbox(
                "اختر الدورة لعرض المسجلين:",
                options=course_ids,
                format_func=lambda x: course_name_map[x],
                key="view_trainees_course_select"
            )
            
            if st.session_state['trainees']:
                # تصفية بيانات المتدربين حسب الدورة المختارة
                df_trainees_filtered = pd.DataFrame(st.session_state['trainees']).T
                df_trainees_filtered = df_trainees_filtered[df_trainees_filtered['Course_ID'] == selected_course_id]
                
                if not df_trainees_filtered.empty:
                    df_trainees_filtered['Trainee_ID'] = df_trainees_filtered.index
                    st.success(f"عدد المسجلين في دورة **{course_name_map[selected_course_id]}**: {len(df_trainees_filtered)} متدرب.")
                    
                    # عرض الجدول بالبيانات المطلوبة
                    st.dataframe(
                        df_trainees_filtered[['Trainee_ID', 'Name', 'College', 'Type', 'Date']],
                        use_container_width=True, 
                        hide_index=True
                    )
                else:
                    st.info(f"لا يوجد متدربون مسجلون حالياً في دورة **{course_name_map[selected_course_id]}**.")
            else:
                st.info("لا يوجد أي متدربين مسجلين في النظام بعد.")
        else:
            st.warning("يجب إضافة دورات أولاً لتفقد المسجلين.")

        st.markdown("---")
        st.subheader("تحكم في الدورات (إضافة وحذف وتعديل)")

        col_c1, col_c2, col_c3 = st.columns(3)
        
        # إضافة دورة (تم إضافة خانة المدرب)
        with col_c1.expander("➕ إضافة دورة جديدة"):
            # إعداد قائمة المدربين المتاحين
            trainer_list = {k: v['Name'] for k, v in st.session_state['trainers'].items()}
            trainer_options = {name: id for id, name in trainer_list.items()}
            trainer_options['غير مسند'] = None
            
            with st.form("add_course_admin_form", clear_on_submit=True):
                new_name = st.text_input("اسم الدورة")
                new_status = st.selectbox("حالة الدورة", ["متاحة للتسجيل", "قيد الإعداد", "مكتملة"])
                selected_trainer_name = st.selectbox("إسناد مدرب للدورة", options=list(trainer_options.keys()))
                
                if st.form_submit_button("حفظ الدورة"):
                    if new_name:
                        new_id = get_next_id(st.session_state['courses'])
                        trainer_id_to_assign = trainer_options[selected_trainer_name]
                        
                        st.session_state['courses'][new_id] = {"Name": new_name, "Status": new_status, "Trainer_ID": trainer_id_to_assign}
                        
                        # تحديث بيانات المدرب ليظهر أنه مرتبط بهذه الدورة
                        if trainer_id_to_assign:
                            st.session_state['trainers'][trainer_id_to_assign]['Assigned_Course_ID'] = new_id
                        
                        st.success(f"✅ تمت إضافة الدورة **{new_name}** بالمعرف #{new_id}. المدرب: **{selected_trainer_name}**")
                    else:
                        st.error("الرجاء إدخال اسم الدورة.")
        
        # تعديل دورة (للاختصار، نكتفي بالعرض هنا) 
        with col_c2.expander("✍️ تعديل بيانات دورة"):
            if course_ids:
                course_to_update = st.selectbox("اختر الدورة للتعديل", options=course_ids, format_func=lambda x: f"#{x} - {st.session_state['courses'][x]['Name']}", key="update_c_select")
                current_name = st.session_state['courses'][course_to_update]['Name']
                current_status = st.session_state['courses'][course_to_update]['Status']
                current_trainer_id = st.session_state['courses'][course_to_update].get('Trainer_ID')

                trainer_list = {k: v['Name'] for k, v in st.session_state['trainers'].items()}
                trainer_options = {name: id for id, name in trainer_list.items()}
                trainer_options['غير مسند'] = None
                
                # لتحديد القيمة الافتراضية للمدرب في Selectbox
                default_trainer_name = "غير مسند"
                if current_trainer_id in trainer_list:
                    default_trainer_name = trainer_list[current_trainer_id]
                
                with st.form("update_course_admin_form"):
                    updated_name = st.text_input("الاسم الجديد للدورة", value=current_name)
                    updated_status = st.selectbox("الحالة الجديدة", ["متاحة للتسجيل", "قيد الإعداد", "مكتملة"], index=["متاحة للتسجيل", "قيد الإعداد", "مكتملة"].index(current_status))
                    updated_trainer_name = st.selectbox("إسناد مدرب للدورة", options=list(trainer_options.keys()), index=list(trainer_options.keys()).index(default_trainer_name))
                    
                    if st.form_submit_button("حفظ التعديلات"):
                        updated_trainer_id = trainer_options[updated_trainer_name]
                        
                        # إلغاء إسناد المدرب القديم إذا تغير
                        if current_trainer_id and current_trainer_id != updated_trainer_id and current_trainer_id in st.session_state['trainers']:
                            st.session_state['trainers'][current_trainer_id]['Assigned_Course_ID'] = None
                        
                        # تحديث بيانات الدورة
                        st.session_state['courses'][course_to_update] = {
                            "Name": updated_name,
                            "Status": updated_status,
                            "Trainer_ID": updated_trainer_id
                        }
                        
                        # إسناد الدورة للمدرب الجديد
                        if updated_trainer_id:
                            st.session_state['trainers'][updated_trainer_id]['Assigned_Course_ID'] = course_to_update
                        
                        st.success(f"✅ تم تعديل الدورة #{course_to_update} بنجاح. المدرب الجديد: **{updated_trainer_name}**")
            else:
                st.info("لا توجد دورات للتعديل.")
        
        with col_c3.expander("🗑️ حذف دورة"):
            if course_ids:
                course_to_delete = st.selectbox("اختر الدورة للحذف", options=course_ids, format_func=lambda x: f"#{x} - {st.session_state['courses'][x]['Name']}", key="delete_c_select")
                if st.button("تأكيد حذف الدورة", key="delete_c_btn"):
                    deleted_name = st.session_state['courses'][course_to_delete]['Name']
                    trainer_id = st.session_state['courses'][course_to_delete].get('Trainer_ID')

                    # إلغاء ربط المدرب
                    if trainer_id and trainer_id in st.session_state['trainers']:
                         st.session_state['trainers'][trainer_id]['Assigned_Course_ID'] = None
                         
                    # حذف الدورة
                    if delete_item(st.session_state['courses'], course_to_delete):
                        st.success(f"🗑️ تم حذف الدورة **{deleted_name}** نهائياً.")
            else:
                st.info("لا توجد دورات للحذف.")

    # ==========================================
    # 3. قسم إدارة المدربين (القسم الجديد) 🧑‍🏫
    # ==========================================
    elif menu == "🧑‍🏫 إدارة المدربين":
        st.header("🧑‍🏫 إدارة ومتابعة المدربين")
        st.markdown("هذا القسم يعرض تفاصيل المدربين، الدورات المسندة إليهم، وقائمة المسجلين في كل دورة.")

        # تجهيز البيانات للعرض
        if st.session_state['trainers']:
            df_trainers = pd.DataFrame(st.session_state['trainers']).T
            
            # ربط اسم الدورة بالمدرب
            course_names = {k: v['Name'] for k, v in st.session_state['courses'].items()}
            df_trainers['Assigned_Course_Name'] = df_trainers['Assigned_Course_ID'].apply(lambda x: course_names.get(x, 'غير مسند'))
            
            df_trainers['Trainer_ID'] = df_trainers.index
            
            st.subheader("قائمة المدربين وحالة الإسناد")
            st.dataframe(df_trainers[['Trainer_ID', 'Name', 'Specialty', 'Assigned_Course_Name']], use_container_width=True, hide_index=True)

            st.markdown("---")
            
            st.subheader("تفقد قائمة المسجلين لكل مدرب")
            
            trainer_options = {f"#{id} - {data['Name']} ({data['Specialty']})": id for id, data in st.session_state['trainers'].items()}
            selected_trainer_key = st.selectbox("اختر المدرب لعرض تفاصيل دوره:", options=list(trainer_options.keys()), key="select_trainer_for_view")
            
            trainer_id = trainer_options[selected_trainer_key]
            assigned_course_id = st.session_state['trainers'][trainer_id]['Assigned_Course_ID']
            trainer_name = st.session_state['trainers'][trainer_id]['Name']
            
            if assigned_course_id is not None:
                course_name = st.session_state['courses'][assigned_course_id]['Name']
                st.
