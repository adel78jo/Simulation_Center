# app.py
import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------------------
# إعدادات المصادقة (آمنة كاختبار)
# ---------------------------
ADMIN_USER = "AABU"
ADMIN_PASS = "Aabu2025"

# ---------------------------
# مسارات الشعارات (موجودة محلياً ضمن بيئة التنفيذ)
# عدل المسارات إذا نقلت الملفات
# ---------------------------
LOGO_CENTER_PATH = "/mnt/data/simulation_logo.jpg.jpg"
LOGO_UNIV_PATH = "/mnt/data/aabu_logo.png.png"

# ---------------------------
# تهيئة Session State الافتراضية
# ---------------------------
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

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

# ---------------------------
# دوال مساعدة (CRUD)
# ---------------------------
def get_next_id(data_dict):
    return max(list(data_dict.keys())) + 1 if data_dict else 1

def delete_item(data_dict, item_id):
    if item_id in data_dict:
        del data_dict[item_id]
        return True
    return False

# ---------------------------
# دوال المصادقة
# ---------------------------
def login_user(username, password):
    if username == ADMIN_USER and password == ADMIN_PASS:
        st.session_state['logged_in'] = True
        st.success("🎉 تم تسجيل الدخول بنجاح! يمكنك الآن الوصول لإدارة النظام.")
        st.experimental_rerun()
    else:
        st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة.")

def logout_user():
    st.session_state['logged_in'] = False
    st.warning("تم تسجيل الخروج. محتوى الإدارة غير متاح.")
    st.experimental_rerun()

# ---------------------------
# إعداد الصفحة وCSS الفاخر التقني (RTL)
# ---------------------------
st.set_page_config(page_title="مركز النمذجة والمحاكاة - لوحة النخبة", layout="wide", page_icon="⚙️")

st.markdown(
    """
    <style>
    /* === خلفية و خطوط === */
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;700;900&display=swap');
    .stApp { direction: rtl; font-family: 'Tajawal', system-ui, sans-serif; background: linear-gradient(180deg,#f7fbfc,#f0f4f7); }
    /* === الشريط الجانبي الفاخر === */
    [data-testid="stSidebar"]{ background: linear-gradient(180deg,#022b3a,#04444f); color: #fff; padding-top:18px; }
    [data-testid="stSidebar"] .css-1d391kg{ color: #fff; }
    /* شعارات */
    .logo-row { display:flex; gap:12px; align-items:center; justify-content:center; padding:12px 6px; }
    .logo-row img { width:120px; border-radius:12px; box-shadow:0 6px 20px rgba(0,0,0,0.18); border: 3px solid rgba(212,175,55,0.12); background:#fff; padding:6px; }
    /* العنوان الرئيسي */
    h1, h2, h3 { color:#013243; font-weight:800; }
    h1 { font-size:2.2rem; border-bottom: 3px solid rgba(212,175,55,0.12); padding-bottom:10px; }
    /* البطاقات الإحصائية */
    [data-testid="stMetric"] { background: linear-gradient(180deg,#ffffff,#fcfdff); border-radius:14px; padding:22px 18px; border:1px solid #e6eef2; box-shadow: 0 10px 30px rgba(2,36,47,0.06);}
    [data-testid="stMetricValue"]{ color:#013243; font-weight:900; font-size:2.6rem; }
    [data-testid="stMetricLabel"]{ color:#425b63; font-weight:700; }
    [data-testid="stMetricDelta"]{ color:#D4AF37; font-weight:800; }
    /* الأزرار الفاخرة */
    .stButton>button{ background: linear-gradient(90deg,#013243,#045a6b); color:#fff; border-radius:10px; padding:10px 18px; font-weight:800; box-shadow:0 8px 18px rgba(1,50,60,0.12); }
    .stButton>button:hover{ transform: translateY(-3px); background: linear-gradient(90deg,#0a6b5a,#4dbb78); color:#012; }
    /* النماذج والمربعات */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        border-radius:10px; border:1px solid #dbeaf0; padding:10px;
    }
    /* الجداول */
    .dataframe thead th { background: #013243 !important; color: #fff !important; font-weight:700; }
    .dataframe tbody tr:nth-child(even) { background:#f7fbfc; }
    .dataframe td { padding:8px 10px; }
    /* بطاقات الحالة للتقارير */
    .status-good { background: linear-gradient(90deg,#e7f9ee,#f1fff6); border-left:6px solid #1e8b57; padding:10px; border-radius:8px; }
    .status-warning { background: linear-gradient(90deg,#fff7e6,#fffef6); border-left:6px solid #D4AF37; padding:10px; border-radius:8px; }
    .status-bad { background: linear-gradient(90deg,#fff1f1,#fff8f8); border-left:6px solid #d9534f; padding:10px; border-radius:8px; }
    /* تبويبات */
    .stTabs [data-testid="stTabItem"] { background: #f5fbfc; color:#013243; border-radius:8px 8px 0 0; padding:8px 16px; font-weight:700; }
    .stTabs [data-testid="stTabItem"][data-selected="true"] { background: linear-gradient(90deg,#013243,#045a6b); color:#fff; box-shadow:0 6px 18px rgba(1,50,60,0.08); }
    /* تحسينات عامة */
    .block-container { padding-top: 20px; padding-left: 28px; padding-right: 28px; }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# مساعد: تنسيق عرض الشعارين في الشريط الجانبي
# ---------------------------
with st.sidebar:
    # منطق حماية تحميل الصورة: لو لم توجد الصورة سيظهر نص بديل
    try:
        st.markdown('<div class="logo-row">', unsafe_allow_html=True)
        st.image(LOGO_CENTER_PATH, width=110, use_column_width=False)
        st.image(LOGO_UNIV_PATH, width=110, use_column_width=False)
        st.markdown('</div>', unsafe_allow_html=True)
    except Exception:
        st.markdown("<div style='padding:10px;color:#fff;font-weight:700'>شعار المركز/الجامعة غير متوفران</div>", unsafe_allow_html=True)

    st.markdown("## ⚙️ نظام إدارة المركز")
    st.markdown("### شعبة التدريب والتطوير")
    st.markdown("---")

    menu = st.radio(
        "القائمة الرئيسية:",
        ("🏠 لوحة التحكم", "📚 إدارة الدورات", "🧑‍🏫 إدارة المدربين", "📊 التقارير والإحصائيات", "🔍 التدقيق والمتابعة", "🔑 أدوات الإدارة المتقدمة"),
        index=0
    )
    st.markdown("---")
    st.button("🔐 تسجيل الخروج", on_click=logout_user)

# ---------------------------
# المحتوى الرئيسي بعد الدخول
# ---------------------------
if st.session_state['logged_in']:
    # لوحة التحكم الرئيسية
    if menu == "🏠 لوحة التحكم":
        st.markdown('<div style="display:flex;justify-content:space-between;align-items:center;">', unsafe_allow_html=True)
        st.title("لوحة القيادة — مركز النمذجة والمحاكاة")
        st.markdown('</div>', unsafe_allow_html=True)

        st.write("مرحباً بك، مدير النظام — هذا الملخص التنفيذي لعمليات الشعبة.")
        st.markdown("---")

        total_trainees = len(st.session_state['trainees'])
        active_courses = len([c for c in st.session_state['courses'].values() if c['Status'] == 'متاحة للتسجيل'])
        audit_warnings = len([a for a in st.session_state['audit_logs'].values() if a['Status'] != 'ممتاز'])

        c1, c2, c3 = st.columns(3)
        c1.metric("👥 إجمالي المتدربين", total_trainees)
        c2.metric("📚 دورات متاحة", active_courses, delta=f"+{active_courses} جديد")
        c3.metric("⚠️ تقارير بحاجة متابعة", audit_warnings, delta=audit_warnings if audit_warnings>0 else 0)

        st.markdown("---")
        st.header("توزيع المتدربين حسب الكلية")
        if st.session_state['trainees']:
            df_trainees = pd.DataFrame(st.session_state['trainees']).T
            counts = df_trainees['College'].value_counts()
            col_chart, col_tbl = st.columns([2,1])
            with col_chart:
                st.bar_chart(counts)
            with col_tbl:
                st.dataframe(counts.rename("العدد").reset_index().rename(columns={'index':'الكلية'}), use_container_width=True, hide_index=True)
        else:
            st.info("لا توجد بيانات متدربين حالياً.")

        st.markdown("---")
        st.header("أحدث تقارير التدقيق")
        if st.session_state['audit_logs']:
            df_audit_latest = pd.DataFrame(st.session_state['audit_logs']).T.sort_values(by='Time', ascending=False).head(6)
            st.dataframe(df_audit_latest[['Lab','Auditor','Status','Time']], use_container_width=True)
        else:
            st.info("لا توجد تقارير تدقيق بعد.")

    # إدارة الدورات
    elif menu == "📚 إدارة الدورات":
        st.header("📝 إدارة الدورات التدريبية")
        st.markdown("أضف/عدّل/احذف الدورات، وتفقد المسجلين بسهولة.")
        st.markdown("---")

        if st.session_state['courses']:
            df_courses = pd.DataFrame(st.session_state['courses']).T
            trainer_map = {k: v['Name'] for k, v in st.session_state['trainers'].items()}
            df_courses['Trainer'] = df_courses['Trainer_ID'].apply(lambda x: trainer_map.get(x, 'غير مسند'))
            df_courses['ID'] = df_courses.index
            st.dataframe(df_courses[['ID','Name','Status','Trainer']], use_container_width=True)
            course_ids = list(st.session_state['courses'].keys())
        else:
            st.info("لا توجد دورات.")
            course_ids = []

        st.markdown("---")
        st.subheader("تفقد المسجلين في دورة")
        if course_ids:
            course_name_map = {cid: data['Name'] for cid, data in st.session_state['courses'].items()}
            sel = st.selectbox("اختر الدورة:", options=course_ids, format_func=lambda x: course_name_map[x])
            df_t = pd.DataFrame(st.session_state['trainees']).T if st.session_state['trainees'] else pd.DataFrame()
            df_sel = df_t[df_t['Course_ID'] == sel] if not df_t.empty else pd.DataFrame()
            if not df_sel.empty:
                df_sel['ID'] = df_sel.index
                st.dataframe(df_sel[['ID','Name','College','Type','Date']], use_container_width=True)
            else:
                st.info("لا يوجد مسجلون في هذه الدورة.")
        else:
            st.warning("أضف دورات أولًا.")

        st.markdown("---")
        col_add, col_update, col_del = st.columns(3)

        with col_add.expander("➕ إضافة دورة جديدة"):
            tname = st.text_input("اسم الدورة")
            tstatus = st.selectbox("حالة الدورة", ["متاحة للتسجيل","قيد الإعداد","مكتملة"])
            trainers_list = {k: v['Name'] for k, v in st.session_state['trainers'].items()}
            trainer_choice = st.selectbox("اختر مدرب (إن وجد)", options=["غير مسند"] + list(trainers_list.values()))
            if st.button("حفظ الدورة"):
                if tname:
                    nid = get_next_id(st.session_state['courses'])
                    trainer_id = None
                    if trainer_choice != "غير مسند":
                        # استخراج المعرف من اسم المدرب
                        for tid,info in st.session_state['trainers'].items():
                            if info['Name'] == trainer_choice:
                                trainer_id = tid
                    st.session_state['courses'][nid] = {"Name": tname, "Status": tstatus, "Trainer_ID": trainer_id}
                    if trainer_id:
                        st.session_state['trainers'][trainer_id]['Assigned_Course_ID'] = nid
                    st.success(f"تمت إضافة الدورة: {tname} (ID: {nid})")
                else:
                    st.error("الرجاء إدخال اسم الدورة.")

        with col_update.expander("✍️ تعديل دورة"):
            if course_ids:
                upd = st.selectbox("اختر دورة للتعديل", options=course_ids, format_func=lambda x: f"#{x} - {st.session_state['courses'][x]['Name']}")
                cur = st.session_state['courses'][upd]
                new_name = st.text_input("الاسم الجديد", value=cur['Name'])
                new_status = st.selectbox("الحالة", ["متاحة للتسجيل","قيد الإعداد","مكتملة"], index=["متاحة للتسجيل","قيد الإعداد","مكتملة"].index(cur['Status']))
                new_trainer = st.selectbox("مدرب", options=["غير مسند"] + list(trainers_list.values()), index=0)
                if st.button("تطبيق التعديل"):
                    new_trainer_id = None
                    if new_trainer != "غير مسند":
                        for tid,info in st.session_state['trainers'].items():
                            if info['Name'] == new_trainer:
                                new_trainer_id = tid
                    # إلغاء إسناد سابق
                    old_tid = cur.get('Trainer_ID')
                    if old_tid and old_tid in st.session_state['trainers']:
                        st.session_state['trainers'][old_tid]['Assigned_Course_ID'] = None
                    st.session_state['courses'][upd] = {"Name": new_name, "Status": new_status, "Trainer_ID": new_trainer_id}
                    if new_trainer_id:
                        st.session_state['trainers'][new_trainer_id]['Assigned_Course_ID'] = upd
                    st.success("تم تعديل بيانات الدورة.")

        with col_del.expander("🗑️ حذف دورة"):
            if course_ids:
                delt = st.selectbox("اختر للحذف", options=course_ids, format_func=lambda x: f"#{x} - {st.session_state['courses'][x]['Name']}")
                if st.button("تأكيد الحذف"):
                    # فك الإسناد إن وجد
                    tid_old = st.session_state['courses'][delt].get('Trainer_ID')
                    if tid_old and tid_old in st.session_state['trainers']:
                        st.session_state['trainers'][tid_old]['Assigned_Course_ID'] = None
                    delete_item(st.session_state['courses'], delt)
                    st.success("تم الحذف.")
            else:
                st.info("لا دورات للحذف.")

    # إدارة المدربين
    elif menu == "🧑‍🏫 إدارة المدربين":
        st.header("🧑‍🏫 إدارة المدربين")
        if st.session_state['trainers']:
            df_tr = pd.DataFrame(st.session_state['trainers']).T
            df_tr['ID'] = df_tr.index
            course_names = {k:v['Name'] for k,v in st.session_state['courses'].items()}
            df_tr['Assigned Course'] = df_tr['Assigned_Course_ID'].apply(lambda x: course_names.get(x, "غير مسند"))
            st.dataframe(df_tr[['ID','Name','Specialty','Assigned Course']], use_container_width=True)
        else:
            st.info("لا يوجد مدربين مضافين.")

        st.markdown("---")
        st.subheader("تفقد سجل المسجلين لدى مدرب")
        trainer_map = {f"#{id} - {info['Name']}": id for id,info in st.session_state['trainers'].items()}
        if trainer_map:
            sel_tr = st.selectbox("اختر مدرب:", options=list(trainer_map.keys()))
            tr_id = trainer_map[sel_tr]
            assigned = st.session_state['trainers'][tr_id]['Assigned_Course_ID']
            if assigned:
                st.success(f"المدرب مسند لدورة: {st.session_state['courses'][assigned]['Name']}")
                df_trs = pd.DataFrame(st.session_state['trainees']).T
                df_sel = df_trs[df_trs['Course_ID'] == assigned] if not df_trs.empty else pd.DataFrame()
                if not df_sel.empty:
                    st.dataframe(df_sel[['Name','College','Type','Date']], use_container_width=True)
                else:
                    st.info("لا يوجد مسجلين في الدورة.")
            else:
                st.warning("المدرب غير مسند لدورة حالياً.")
        else:
            st.info("لا مدربين للاختيار.")

    # التدقيق والمتابعة
    elif menu == "🔍 التدقيق والمتابعة":
        st.header("🔍 رفع تقرير تدقيق")
        with st.form("audit_form", clear_on_submit=True):
            lab = st.selectbox("المرفق / المختبر", ["مختبر النمذجة","مختبر المحاكاة","قاعة التدريب 1","قاعة التدريب 2","أخرى"])
            auditor = st.text_input("اسم المدقق")
            st.markdown("**قائمة تحقق**")
            s1 = st.checkbox("البرمجيات تعمل بكفاءة")
            s2 = st.checkbox("الأجهزة والمعدات سليمة")
            s3 = st.checkbox("نظافة القاعة")
            notes = st.text_area("ملاحظات")
            if st.form_submit_button("رفع التقرير"):
                if not auditor:
                    st.warning("أدخل اسم المدقق.")
                else:
                    nid = get_next_id(st.session_state['audit_logs'])
                    status = "ممتاز" if (s1 and s2 and s3) else "يحتاج متابعة فورية"
                    st.session_state['audit_logs'][nid] = {"Lab":lab,"Auditor":auditor,"Time":datetime.now().strftime("%Y-%m-%d %H:%M"),"Status":status,"Notes":notes}
                    if status == "ممتاز":
                        st.success("تم رفع التقرير: المرفق بحالة ممتازة.")
                    else:
                        st.error("تم رفع التقرير: يحتاج متابعة.")

    # التقارير والإحصاءات
    elif menu == "📊 التقارير والإحصائيات":
        st.header("📊 التقارير")
        st.subheader("المتدربين حسب الدورة")
        if st.session_state['trainees']:
            df_t = pd.DataFrame(st.session_state['trainees']).T
            st.bar_chart(df_t['Course_Name'].value_counts())
        else:
            st.info("لا بيانات متدربين.")

        st.markdown("---")
        st.subheader("حالات تقارير التدقيق")
        if st.session_state['audit_logs']:
            df_a = pd.DataFrame(st.session_state['audit_logs']).T
            st.dataframe(df_a[['Lab','Auditor','Status','Time']], use_container_width=True)
        else:
            st.info("لا توجد تقارير.")

        st.markdown("---")
        st.subheader("تصدير البيانات")
        c1,c2,c3 = st.columns(3)
        if st.session_state['trainees']:
            df_full = pd.DataFrame(st.session_state['trainees']).T
            c1.download_button("⬇️ تحميل المتدربين (CSV)", data=df_full.to_csv(index=True).encode('utf-8'), file_name="trainees.csv")
        if st.session_state['audit_logs']:
            df_full_a = pd.DataFrame(st.session_state['audit_logs']).T
            c2.download_button("⬇️ تحميل التدقيق (CSV)", data=df_full_a.to_csv(index=True).encode('utf-8'), file_name="audits.csv")
        if st.session_state['courses']:
            df_full_c = pd.DataFrame(st.session_state['courses']).T
            c3.download_button("⬇️ تحميل الدورات (CSV)", data=df_full_c.to_csv(index=True).encode('utf-8'), file_name="courses.csv")

    # أدوات الإدارة المتقدمة
    elif menu == "🔑 أدوات الإدارة المتقدمة":
        st.header("🔑 أدوات متقدمة (تحذير: عمليات حذف نهائية)")
        tabs = st.tabs(["👥 المتدربين","📝 تقارير التدقيق"])
        with tabs[0]:
            st.subheader("قائمة المتدربين")
            if st.session_state['trainees']:
                df_tt = pd.DataFrame(st.session_state['trainees']).T
                df_tt['ID'] = df_tt.index
                st.dataframe(df_tt[['ID','Name','College','Course_Name','Date']], use_container_width=True)
                del_id = st.selectbox("اختر متدرب للحذف", options=list(st.session_state['trainees'].keys()), format_func=lambda x: f"#{x} - {st.session_state['trainees'][x]['Name']}")
                if st.button("حذف متدرب نهائي"):
                    delete_item(st.session_state['trainees'], del_id)
                    st.success("تم حذف المتدرب.")
            else:
                st.info("لا متدربين.")

        with tabs[1]:
            st.subheader("تقارير التدقيق")
            if st.session_state['audit_logs']:
                df_aa = pd.DataFrame(st.session_state['audit_logs']).T
                df_aa['ID'] = df_aa.index
                st.dataframe(df_aa[['ID','Lab','Auditor','Status','Time','Notes']], use_container_width=True)
                del_a = st.selectbox("اختر تقرير للحذف", options=list(st.session_state['audit_logs'].keys()), format_func=lambda x: f"#{x} - {st.session_state['audit_logs'][x]['Lab']}")
                if st.button("حذف تقرير نهائي"):
                    delete_item(st.session_state['audit_logs'], del_a)
                    st.success("تم حذف التقرير.")
            else:
                st.info("لا تقارير.")

    # شريط سفلي لطيف للتحكم
    st.markdown("---")
    st.markdown("**تم التشغيل بواسطة:** مركز النمذجة والمحاكاة — لوحة إدارة النخبة")
else:
    # صفحة عامة + تسجيل الدخول
    st.title("مركز النمذجة والمحاكاة — جامعة آل البيت")
    st.subheader("منصة تسجيل المتدربين وإدارة الشعبة")

    tabs = st.tabs(["🔑 دخول المدير","📝 تسجيل في دورة"])
    with tabs[0]:
        st.info("الوصول محصور لمديري النظام")
        with st.form("login_form"):
            user = st.text_input("اسم المستخدم")
            pwd = st.text_input("كلمة المرور", type="password")
            if st.form_submit_button("🔐 تسجيل الدخول"):
                login_user(user, pwd)

    with tabs[1]:
        st.header("التسجيل في الدورات المتاحة")
        available = {k:v for k,v in st.session_state['courses'].items() if v['Status']=="متاحة للتسجيل"}
        if not available:
            st.warning("لا دورات متاحة الآن.")
        else:
            with st.form("reg_form", clear_on_submit=True):
                name = st.text_input("الاسم الكامل (بالوثائق)")
                role = st.selectbox("الصفة", ["طالب بكالوريوس","طالب دراسات عليا","موظف جامعة","خريج","من خارج الجامعة"])
                college = st.selectbox("الكلية/الجهة", ["تكنولوجيا المعلومات","الهندسة","العلوم","العلوم الإدارية","الآداب","أخرى"])
                sel_course = st.selectbox("اختر الدورة", options=[f"#{k} - {v['Name']}" for k,v in available.items()])
                if st.form_submit_button("✅ تسجيل"):
                    # استخراج ID من النص
                    cid = int(sel_course.split()[0].lstrip("#"))
                    nid = get_next_id(st.session_state['trainees'])
                    st.session_state['trainees'][nid] = {"Name":name,"Type":role,"College":college,"Course_ID":cid,"Course_Name":st.session_state['courses'][cid]['Name'],"Date":datetime.now().strftime("%Y-%m-%d")}
                    st.success(f"تم التسجيل في دورة {st.session_state['courses'][cid]['Name']}. سيتم التواصل.")

# نهاية التطبيق
