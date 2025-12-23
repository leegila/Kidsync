import streamlit as st

# הגדרות בסיסיות ויישור לימין
st.set_page_config(page_title="KidSync Control", layout="wide")
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    /* כותרות הילדים */
    .child-label { 
        text-align: center; 
        font-weight: bold; 
        background-color: #343a40; 
        color: white; 
        padding: 10px; 
        border-radius: 5px;
        margin-bottom: 10px;
    }
    /* עיצוב השעות */
    .hour-text { font-weight: bold; font-size: 18px; padding-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ מפת השגחה: 16:00-20:00")

# אתחול נתונים
if "events" not in st.session_state:
    st.session_state.events = []

days = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי"]
children = ["נועם", "מאיה", "התינוקת"]
hours = ["16:00", "17:00", "18:00", "19:00", "20:00"]

# --- טופס הוספה ---
with st.expander("➕ עדכון פעילות (לכמה ילדים/שעות)", expanded=True):
    with st.form("add_form"):
        c1, c2 = st.columns(2)
        with c1:
            sel_day = st.selectbox("יום", days)
            sel_kids = st.multiselect("ילדים", children)
            sel_start = st.selectbox("מהשעה", hours)
            sel_end = st.selectbox("עד השעה", hours + ["21:00"])
        with c2:
            sel_act = st.text_input("מה הפעילות?")
            sel_guard = st.text_input("מי המבוגר? (השאירי ריק לסימון חור)")
        
        if st.form_submit_button("עדכן את הלוח"):
            if sel_kids and sel_act:
                st.session_state.events.append({
                    "day": sel_day, "kids": sel_kids, 
                    "start": int(sel_start.split(":")[0]), 
                    "end": int(sel_end.split
