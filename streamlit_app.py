import streamlit as st

# הגדרות RTL ומראה נקי
st.set_page_config(page_title="KidSync Control", layout="wide")
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    /* כפתור עם פעילות ומבוגר - ירוק */
    .stButton button[kind="primary"] { background-color: #28a745 !important; color: white !important; border: none; }
    /* כפתור עם פעילות ללא מבוגר - אדום בוהק */
    .stButton button[kind="secondary"] { background-color: #dc3545 !important; color: white !important; border: none; }
    /* כפתור ריק (הבעיה) - כתום/צהוב תשומת לב */
    .empty-btn button { background-color: #ffc107 !important; color: black !important; border: 1px dashed black; font-weight: bold; }
    
    .hour-label { font-weight: bold; height: 50px; display: flex; align-items: center; justify-content: center; border-bottom: 1px solid #eee; }
    .child-header { text-align: center; font-weight: bold; background: #343a40; color: white; padding: 12px; border-radius: 8px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ מפת השגחה: 16:00-20:00")

# אתחול נתונים
if "events" not in st.session_state:
    st.session_state.events = []

days = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי"]
children = ["נועם", "מאיה", "התינוקת"]
# הגבלת השעות לטווח המבוקש
hours = [f"{h}:00" for h in range(16, 21)]

# --- אזור הוספת פעילות ---
with st.expander("➕ עדכון לו\"ז (ילדים / שעות / חוגים)", expanded=False):
    with st.form("quick_add"):
        col1, col2 = st.columns(2)
        with col1:
            sel_day = st.selectbox("יום", days)
            sel_children = st.multiselect("עבור איזה ילדים?", children)
            sel_start = st.selectbox("שעת התחלה", hours)
            sel_end = st.selectbox("שעת סיום", hours + ["21:00"])
        with col2:
            sel_act = st.text_input("מה הפעילות?")
            sel_guard = st.text_input("מי המבוגר האחראי?")
        
        if st.form_submit_button("עדכן מפה"):
            if sel_children and sel_act:
                # הוספת הפעילות
                st.session_state.events.append({
                    "day": sel_day, "children": sel_children, 
                    "start": int(sel_start.split(":")[0]), "end": int(sel_end.split(":")[0]),
                    "act": sel_act, "guard": sel_guard
                })
                st.rerun()

# --- הצ
