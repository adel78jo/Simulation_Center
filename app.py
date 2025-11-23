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

    body {
        background-color: var(--primary-light);
        color: var(--text-dark);
    }
    
    /* تطبيق الخلفية البيضاء على العناصر الرئيسية */
    .stApp, [data-testid="stHeader"] {
        background-color: var(--primary-light) !important;
        color: var(--text-dark) !important;
    }

    /* العناوين والتأكيد */
    h1, h2, h3, h4 {
        color: var(--text-dark); /* العناوين باللون الداكن */
        border-bottom: 1px solid var(--border-color-light);
        padding-bottom: 10px;
        margin-top: 30px;
        font-weight: 700; 
    }
    h1 { font-size: 2.5em; color: var(--text-dark); } 
    h2 { font-size: 2em; color: var(--accent-gold); } /* عناوين فرعية بالذهبي */
    h3 { font-size: 1.7em; }

    /* ======================================================== */
    /* 📱 تحسين الاستجابة للشاشات الصغيرة (مثل الآيفون) 📱 */
    /* ======================================================== */
    
    /* الشريط الجانبي وتنسيق القائمة - الإعدادات الأساسية */
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-bg);
        border-right: 1px solid var(--border-color-light);
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1); 
        /* إزالة min/max-width الثابتة لصالح الأبعاد النسبية لتجنب شريط التمرير الأفقي في الآيفون */
        width: 300px; /* العرض الافتراضي للشاشات الكبيرة */
    }
    
    @media (max-width: 768px) { /* تطبيق التعديلات على الشاشات الأصغر من 768 بكسل */
        /* تقليل عرض الشريط الجانبي لترك مساحة أكبر للمحتوى */
        [data-testid="stSidebar"] {
            width: 250px !important; 
            max-width: 80% !important; /* لضمان عدم تجاوز عرض الشاشة */
        }
        
        /* تقليل حجم الخطوط قليلاً لتحسين القراءة على الشاشات الصغيرة */
        h1 { font-size: 2.0em; } 
        h2 { font-size: 1.6em; } 
        h3 { font-size: 1.4em; }

        /* تصغير حجم أيقونات المتركس */
        [data-testid="stMetricValue"] {
            font-size: 2.5em; 
        }
        
        /* جعل الأكواد تعمل بشكل أفضل على الشاشات الصغيرة */
        div.stDataFrame {
            overflow-x: auto; /* إضافة تمرير أفقي للجداول الكبيرة فقط عند الحاجة */
        }
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
        background-color: rgba(205, 164, 52, 0.1); /* ظل خفيف من الذهبي */
        color: var(--accent-gold);
    }
    .st-emotion-cache-c3y0s5 .st-emotion-cache-1jmpsc2[aria-selected="true"] {
        background-color: var(--accent-gold); /* الخلفية باللون الذهبي النحاسي عند الاختيار */
        color: var(--primary-light); /* نص فاتح على خلفية ذهبية */
        font-weight: 700;
    }

    /* الأزرار (Primary Action) - تأثير معدني هادئ */
    .stButton>button {
        background: var(--accent-gold);
        color: var(--primary-light); /* نص فاتح على خلفية ذهبية */
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
        background: #DDC873; /* درجة أفتح قليلاً عند التحويم */
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
        color: var(--accent-gold); /* القيمة باللون الذهبي النحاسي */
        font-weight: bolder;
    }
    [data-testid="stMetricLabel"] {
        font-size: 1.0em;
        color: var(--text-dark);
        font-weight: 500;
    }

    /* تنسيق خاص للشعارين */
    .logo-container {
        text-align: center;
        margin-bottom: 25px;
        padding-top: 10px;
    }
    .logo-image-sidebar {
        width: 130px; 
        filter: drop-shadow(0 0 5px rgba(205, 164, 52, 0.2)); 
        border-radius: 8px;
    }
    .logo-image-main {
        width: 250px;
        filter: drop-shadow(0 0 10px rgba(205, 164, 52, 0.3));
        border-radius: 12px;
        margin-bottom: 40px; 
    }
    
    /* تحسين تصميم النماذج والحقول والجداول */
    .st-emotion-cache-czk5ad { 
        background-color: var(--secondary-light);
        border-radius: 10px;
        padding: 20px;
        border: 1px solid var(--border-color-light);
        box-shadow: 0 1px 5px rgba(0,0,0,0.05);
    }
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea {
        border-radius: 8px;
        border: 1px solid var(--border-color-light); 
        background-color: var(--primary-light);
        color: var(--text-dark);
        padding: 10px;
    }
    .st-emotion-cache-1ftrzg7 p { 
        font-weight: 700;
        color: var(--accent-gold);
        font-size: 1.1em;
    }
    
    /* تنسيق التابات */
    .stTabs [data-testid="stTabItem"] {
        background-color: var(--secondary-light);
        color: var(--text-muted);
        border: 1px solid var(--border-color-light);
        border-bottom: none;
    }
    .stTabs [data-testid="stTabItem"][data-selected="true"] {
        background-color: var(--primary-light);
        color: var(--accent-gold);
        border-color: var(--border-color-light);
        border-bottom: 3px solid var(--accent-gold);
    }

    /* رسائل التنبيهات */
    .stAlert {
        border-radius: 8px;
        font-weight: 500;
        padding: 15px 20px;
        background-color: var(--secondary-light);
        color: var(--text-dark);
        border: 1px solid var(--border-color-light);
    }
    .stAlert.success { border-left: 5px solid #28a745; background-color: #e6ffe6; color: #155724; } /* أخضر فاتح */
    .stAlert.info { border-left: 5px solid #17a2b8; background-color: #e0f7fa; color: #0c5460; } /* أزرق فاتح */
    .stAlert.warning { border-left: 5px solid var(--accent-gold); background-color: #fff8e1; color: #856404; } /* ذهبي فاتح */
    .stAlert.error { border-left: 5px solid #dc3545; background-color: #f8d7da; color: #721c24; } /* أحمر فاتح */


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
        
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("## ⚙️ نظام الإدارة")
    st.sidebar.markdown("### شعبة التدريب المتقدم")
    st.sidebar.markdown("---")
    
    # 🚀 القائمة الجانبية المصححة (تجنب خطأ TypeError عن طريق دمج الإيموجي في النص)
    menu = st.sidebar.radio(
        "القائمة الرئيسية:",
        (
            "🖥️ لوحة التحكم",
            "📖 إدارة الدورات",
            "👨‍🏫 إدارة المدربين",
            "📈 التقارير والإحصائيات",
            "🔎 التدقيق والمتابعة", 
            "🔒 أدوات الإدارة المتقدمة"
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
                # استخدام ألوان تناسب السمة البيضاء (ذهبي نحاسي)
                st.bar_chart(college_counts, color=["#CDA434"]) 
            
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
    elif menu == "📖 إدارة الدورات":
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
                        if trainer_id_to_assign and trainer_id_to_assign != None:
                            st.session_state['trainers'][trainer_id_to_assign]['Assigned_Course_ID'] = new_id
                        
                        st.success(f"✅ تمت إضافة الدورة **{new_name}** بالمعرف #{new_id}. المدرب: **{selected_trainer_name}**")
                    else:
                        st.error("الرجاء إدخال اسم الدورة.")
        
        # تعديل دورة
        with col_c2.expander("✍️ تعديل بيانات دورة"):
            if course_ids:
                course_to_update = st.selectbox("اختر الدورة للتعديل", options=course_ids, format_func=lambda x: f"#{x} - {st.session_state['courses'][x]['Name']}", key="update_c_select")
                current_data = st.session_state['courses'][course_to_update]
                current_name = current_data['Name']
                current_status = current_data['Status']
                current_trainer_id = current_data.get('Trainer_ID')

                trainer_list = {k: v['Name'] for k, v in st.session_state['trainers'].items()}
                trainer_options_names = list(trainer_list.values())
                trainer_options_names.append('غير مسند')
                
                # لتحديد القيمة الافتراضية للمدرب في Selectbox
                default_trainer_name = "غير مسند"
                if current_trainer_id in trainer_list:
                    default_trainer_name = trainer_list[current_trainer_id]
                
                with st.form("update_course_admin_form"):
                    updated_name = st.text_input("الاسم الجديد للدورة", value=current_name)
                    updated_status = st.selectbox("الحالة الجديدة", ["متاحة للتسجيل", "قيد الإعداد", "مكتملة"], index=["متاحة للتسجيل", "قيد الإعداد", "مكتملة"].index(current_status))
                    updated_trainer_name = st.selectbox("إسناد مدرب للدورة", options=trainer_options_names, index=trainer_options_names.index(default_trainer_name))
                    
                    if st.form_submit_button("حفظ التعديلات"):
                        # إيجاد الـ ID للمدرب الجديد من اسمه
                        updated_trainer_id = next((k for k, v in trainer_list.items() if v == updated_trainer_name), None)

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
    # 3. قسم إدارة المدربين
    # ==========================================
    elif menu == "👨‍🏫 إدارة المدربين":
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
            
            # استخدام الأقواس المعقوفة {} لإنشاء قاموس (Dict Comprehension)
            trainer_options_keys = {f"#{id} - {data['Name']} ({data['Specialty']})": id for id, data in st.session_state['trainers'].items()}
            
            if trainer_options_keys:
                selected_trainer_key_name = st.selectbox("اختر المدرب لعرض تفاصيل دوره:", options=list(trainer_options_keys.keys()), key="select_trainer_for_view")
                
                trainer_id = trainer_options_keys[selected_trainer_key_name]
                assigned_course_id = st.session_state['trainers'][trainer_id]['Assigned_Course_ID']
                trainer_name = st.session_state['trainers'][trainer_id]['Name']
                
                if assigned_course_id is not None:
                    course_name = st.session_state['courses'][assigned_course_id]['Name']
                    st.success(f"المدرب **{trainer_name}** مسند لدورة: **{course_name}** (ID: {assigned_course_id})")

                    # عرض تفاصيل المسجلين في دورة المدرب
                    if st.session_state['trainees']:
                        df_trainees_trainer = pd.DataFrame(st.session_state['trainees']).T
                        df_trainees_trainer = df_trainees_trainer[df_trainees_trainer['Course_ID'] == assigned_course_id]
                        
                        if not df_trainees_trainer.empty:
                            df_trainees_trainer['Trainee_ID'] = df_trainees_trainer.index
                            st.info(f"عدد المسجلين في دورة **{course_name}**: {len(df_trainees_trainer)} متدرب.")
                            
                            st.dataframe(
                                df_trainees_trainer[['Trainee_ID', 'Name', 'College', 'Type', 'Date']],
                                use_container_width=True, 
                                hide_index=True
                            )
                        else:
                            st.warning(f"لا يوجد متدربون مسجلون حالياً في دورة المدرب **{course_name}**.")
                    else:
                        st.info("لا يوجد متدربون في النظام بعد.")
                        
                else:
                    st.warning(f"المدرب **{trainer_name}** غير مسند لأي دورة حالياً.")
        
        else:
            st.info("لا يوجد مدربون مضافون في النظام.")
        
    # ==========================================
    # 4. قسم التدقيق والمتابعة (المصحح)
    # ==========================================
    elif menu == "🔎 التدقيق والمتابعة":
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
    # 5. التقارير والإحصائيات (المصحح)
    # ==========================================
    elif menu == "📈 التقارير والإحصائيات":
        st.header("📊 تقارير الأداء والبيانات")
        st.markdown("استعرض الإحصائيات الرئيسية وحمل تقارير البيانات.")
        
        st.subheader("سجل المتدربين حسب الدورة")
        if st.session_state['trainees']:
            df_trainees = pd.DataFrame(st.session_state['trainees']).T
            course_counts = df_trainees['Course_Name'].value_counts()
            st.bar_chart(course_counts, color=["#CDA434"]) # لون ذهبي نحاسي
            
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
            # استخدام io.BytesIO لتجنب مشاكل ترميز (Encoding) البيانات العربية عند التحميل
            buffer = io.BytesIO()
            df_full_trainees.to_csv(buffer, index=True, encoding='utf-8-sig') # استخدام sig لترميز صحيح في Excel
            csv_trainees = buffer.getvalue()
            
            col_dl1.download_button(
                label="⬇️ تحميل بيانات المتدربين (CSV)", data=csv_trainees, file_name='تقارير_المتدربين.csv', mime='text/csv;charset=utf-8',)
        
        if st.session_state['audit_logs']:
            df_full_audit = pd.DataFrame(st.session_state['audit_logs']).T
            buffer = io.BytesIO()
            df_full_audit.to_csv(buffer, index=True, encoding='utf-8-sig')
            csv_audit = buffer.getvalue()

            col_dl2.download_button(
                label="⬇️ تحميل تقارير التدقيق (CSV)", data=csv_audit, file_name='تقارير_التدقيق.csv', mime='text/csv;charset=utf-8',)
        
        if st.session_state['courses']:
            df_full_courses = pd.DataFrame(st.session_state['courses']).T
            buffer = io.BytesIO()
            df_full_courses.to_csv(buffer, index=True, encoding='utf-8-sig')
            csv_courses = buffer.getvalue()
            
            col_dl3.download_button(
                label="⬇️ تحميل بيانات الدورات (CSV)", data=csv_courses, file_name='بيانات_الدورات.csv', mime='text/csv;charset=utf-8',)

    # ==========================================
    # 6. أدوات الإدارة المتقدمة (المصحح)
    # ==========================================
    elif menu == "🔒 أدوات الإدارة المتقدمة":
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
                    trainee_to_update = st.selectbox("اختر المتدرب للتعديل", options=trainee_ids, format_func=lambda x: f"#{x} - {st.session_state['trainees'][x]['Name']}", key="update_t_select_advanced")
                    current_data = st.session_state['trainees'][trainee_to_update]
                    
                    course_list = {k: v['Name'] for k, v in st.session_state['courses'].items()}
                    course_ids = list(course_list.keys())
                    
                    with st.form("update_trainee_admin_form_advanced"):
                        u_name = st.text_input("الاسم", value=current_data['Name'], key="u_name_t_advanced")
                        u_college = st.selectbox("الكلية", ["تكنولوجيا المعلومات", "الهندسة", "العلوم", "العلوم الإدارية", "أخرى"], index=["تكنولوجيا المعلومات", "الهندسة", "العلوم", "العلوم الإدارية", "أخرى"].index(current_data['College']), key="u_college_t_advanced")
                        u_course_id = st.selectbox("الدورة الجديدة", options=course_ids, format_func=lambda x: course_list[x], index=course_ids.index(current_data['Course_ID']), key="u_course_id_t_advanced")
                        
                        if st.form_submit_button("حفظ تعديلات المتدرب", key="submit_t_advanced"):
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
                    trainee_to_delete = st.selectbox("اختر المتدرب للحذف", options=trainee_ids, format_func=lambda x: f"#{x} - {st.session_state['trainees'][x]['Name']}", key="delete_t_select_admin_advanced")
                    if st.button("تأكيد حذف المتدرب", key="delete_t_btn_admin_advanced"):
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
                    audit_to_update = st.selectbox("اختر التقرير للتعديل", options=audit_ids, format_func=lambda x: f"#{x} - {st.session_state['audit_logs'][x]['Lab']}", key="update_a_select_admin_advanced")
                    current_data = st.session_state['audit_logs'][audit_to_update]
                    
                    with st.form("update_audit_admin_form_audit_advanced"):
                        u_status = st.selectbox("حالة التدقيق", ["ممتاز", "⚠️ يحتاج متابعة فورية"], index=["ممتاز", "⚠️ يحتاج متابعة فورية"].index(current_data['Status']), key="u_status_audit_advanced")
                        u_notes = st.text_area("تعديل الملاحظات", value=current_data['Notes'], key="u_notes_audit_advanced")
                        
                        if st.form_submit_button("حفظ تعديلات التقرير", key="submit_a_advanced"):
                            st.session_state['audit_logs'][audit_to_update]['Status'] = u_status
                            st.session_state['audit_logs'][audit_to_update]['Notes'] = u_notes
                            st.success(f"✅ تم تحديث التقرير #{audit_to_update} بنجاح.")
                else:
                    st.info("لا توجد تقارير للتعديل.")

            # حذف تقرير تدقيق
            with col_a2.expander("🗑️ حذف تقرير"):
                if audit_ids:
                    audit_to_delete = st.selectbox("اختر التقرير للحذف", options=audit_ids, format_func=lambda x: f"#{x} - {st.session_state['audit_logs'][x]['Lab']}", key="delete_a_select_admin_advanced")
                    if st.button("تأكيد حذف التقرير", key="delete_a_btn_admin_advanced"):
                        deleted_lab = st.session_state['audit_logs'][audit_to_delete]['Lab']
                        if delete_item(st.session_state['audit_logs'], audit_to_delete):
                            st.success(f"🗑️ تم حذف التقرير الخاص بـ **{deleted_lab}** نهائياً.")
                else:
                    st.info("لا توجد تقارير للحذف.")


else:
    # ---------------------------------------------
    # شاشة تسجيل الدخول والصفحة العامة (Public View)
    # ---------------------------------------------
    st.title("مركز النمذجة والمحاكاة بجامعة آل البيت")
    st.subheader("تسجيل المتدربين ودخول نظام الإدارة")
    
    # قائمة الدورات المتاحة للتسجيل
    available_courses = {k: v for k, v in st.session_state['courses'].items() if v['Status'] == 'متاحة للتسجيل'}
    course_options = {f"#{k} - {v['Name']}": k for k, v in available_courses.items()}
    
    # تقسيم الصفحة إلى تسجيل دخول المدير وتسجيل المتدرب
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
                    نحن ملتزمون بتوفير بيئة تدريب وتطوير عالية الجودة في مجالات النمذجة والمحاكاة والواقع الافتراضي، باستخدام أحدث التقنيات.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
    # ------------------
    # 2. علامة تبويب تسجيل المتدرب
    # ------------------
    with tab_register:
        st.header("التسجيل في الدورات التدريبية المتاحة")
        st.markdown("يرجى ملء النموذج أدناه للتسجيل في إحدى الدورات التي يتم قبول طلبات التسجيل فيها حالياً.")
        
        if not available_courses:
            st.warning("⚠️ لا توجد دورات متاحة للتسجيل حالياً. يرجى مراجعة الموقع لاحقاً.")
        else:
            with st.form("trainee_registration_form", clear_on_submit=True):
                t_name = st.text_input("الاسم الرباعي الكامل (كما في الوثائق الرسمية)")
                t_type = st.selectbox("النوع / الصفة", ["طالب بكالوريوس", "طالب دراسات عليا", "موظف جامعة", "خريج", "من خارج الجامعة"])
                t_college = st.selectbox("الكلية / الجهة المنتمي إليها", ["تكنولوجيا المعلومات", "الهندسة", "العلوم", "العلوم الإدارية", "الآداب", "أخرى"])
                
                selected_course_key = st.selectbox("اختر الدورة للتسجيل", options=list(course_options.keys()))
                
                register_button = st.form_submit_button("✅ إرسال طلب التسجيل")
                
                if register_button:
                    if t_name and selected_course_key:
                        course_id_selected = course_options[selected_course_key]
                        course_name_selected = available_courses[course_id_selected]['Name']
                        
                        # إنشاء إدخال المتدرب الجديد
                        new_trainee_id = get_next_id(st.session_state['trainees'])
                        st.session_state['trainees'][new_trainee_id] = {
                            "Name": t_name,
                            "Type": t_type,
                            "College": t_college,
                            "Course_ID": course_id_selected,
                            "Course_Name": course_name_selected,
                            "Date": datetime.now().strftime("%Y-%m-%d")
                        }
                        
                        st.success(f"🎉 تم تسجيلك بنجاح في دورة **{course_name_selected}**! سيتم التواصل معك قريباً لتأكيد موعد الدورة.")
                    else:
                        st.error("الرجاء تعبئة جميع الحقول المطلوبة (الاسم واختيار الدورة).")
