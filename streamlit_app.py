import streamlit as st
import pandas as pd

# הגדרות תצוגה וכיוון כתיבה
st.set_page_config(page_title="KidSync Weekly", layout="wide")
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    div[data-testid="stExpander"] { text-align: right; direction: rtl; }
    .stTabs [data-baseweb="tab-list"] { direction: rtl; }
    p, h1, h2, h3, span { text-align: right; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏃‍♂️ KidSync: הלוז השבועי")
st.write("נהלי את חלוקת המשימות והבייביסיטר בקלות")

# אתחול נתונים
if "events" not in st.session_state:
    st.session_state.events = [
        {"יום": "שני", "שעה": "16:00", "ילד": "נועם", "פעילות": "כדורסל", "מבוגר": "אמא"},
        {"יום": "שני", "שעה": "17:30", "ילד": "מאיה", "פעילות": "חוג ציור", "מבוגר": ""},
        {"יום": "רביעי", "שעה": "16:30", "ילד": "נועם", "פעילות": "ג'ודו", "מבוגר": "בייביסיטר"}
    ]

# צבעים לפי ילדים
child_colors = {
    "נועם": "#CCE5FF", 
    "מאיה": "#FFD1DC", 
    "התינוקת": "#D4EDDA", 
    "אחר": "#F8F9FA"
}

# תצוגת ימים בטאבים
days = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי"]
tabs = st.tabs(days)

for i, day_tab in enumerate(tabs):
    with day_tab:
        current_day = days[i]
        day_events = [e for e in st.session_state.events if e["יום"] == current_day]
        day_events = sorted(day_events, key=lambda x: x["שעה"])
        
        if not day_events:
            st.info(f"אין פעילויות ליום {current_day}")
        else:
            for ev in day_events:
                bg = child_colors.get(ev["ילד"], "#FFFFFF")
                border = "5px solid red" if not ev["מבוגר"] else "1px solid #ccc"
                
                st.markdown(f"""
                    <div style="background-color:{bg}; padding:15px; border-radius:10px; border-right:{border}; margin-bottom:10px; color: black; display: flex; justify-content: space-between;">
                        <div style="font-weight: bold;">{ev["שעה"]}</div>
                        <div><b>{ev["ילד"]}</b>: {ev["פעילות"]}</div>
                        <div style="text-align: left;">{"✅ " + ev["מבוגר"] if ev["מבוגר"] else "🆘 חסר מבוגר!"}</div>
                    </div>
                """, unsafe_allow_html=True)

# הוספת פעילות
st.markdown("---")
with st.expander("➕ הוספת פעילות או חוג"):
    with st.form("add_new"):
        c1, c2 = st.columns(2)
        with c1:
            n_day = st.selectbox("יום", days)
            n_child = st.selectbox("ילד", list(child_colors.keys()))
            n_time = st.text_input("שעה (למשל 16:00)")
        with c2:
            n_act = st.text_input("פעילות")
            n_guard = st.text_input("מבוגר אחראי (השאירי ריק לסימון חסר)")
        
        if st.form_submit_button("שמור"):
            st.session_state.events.append({"יום": n_day, "שעה": n_time, "ילד": n_child, "פעילות": n_act, "מבוגר": n_guard})
            st.rerun()

if st.button("איפוס כל הלוז"):
    st.session_state.events = []
    st.rerun()
