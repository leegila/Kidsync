import streamlit as st

st.set_page_config(page_title="KidSync", layout="wide")

# עיצוב RTL וצבעים
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    .child-header { text-align: center; font-weight: bold; background: #343a40; color: white; padding: 10px; border-radius: 5px; }
    .hour-col { font-weight: bold; font-size: 18px; padding-top: 10px; }
    /* עיצוב כפתור ריק (חור) */
    div.stButton > button { background-color: #ffebcc !important; color: #cc7a00 !important; border: 2px dashed #ffad33 !important; }
    /* עיצוב כפתור מאויש (תקין) */
    div.stButton > button[kind="primary"] { background-color: #d4edda !important; color: #155724 !important; border: 1px solid #c3e6cb !important; }
    /* עיצוב כפתור ללא בייביסיטר (בעיה) */
    div.stButton > button[kind="secondary"] { background-color: #f8d7da !important; color: #721c24 !important; border: 2px solid #f5c6cb !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ מפת השגחה אחה\"צ")

if "events" not in st.session_state:
    st.session_state.events = []

days = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי"]
kids = ["נועם", "מאיה", "התינוקת"]
hours = [f"{h}:00" for h in range(16, 21)]

# טופס הוספה
with st.expander("➕ הוספת פעילות / חוג", expanded=True):
    with st.form("add_form"):
        c1, c2 = st.columns(2)
        with c1:
            d_sel = st.selectbox("יום", days)
            k_sel = st.multiselect("ילדים", kids)
        with c2:
            s_sel = st.selectbox("התחלה", hours)
            e_sel = st.selectbox("סיום", hours + ["21:00"], index=1)
        
        act_sel = st.text_input("מה הפעילות?")
        gr
