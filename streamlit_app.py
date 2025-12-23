import streamlit as st
import pandas as pd

# הגדרת יישור לימין (RTL) ותצוגה
st.set_page_config(page_title="KidSync Weekly", layout="wide")
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    th, td { text-align: right !important; }
    div[data-testid="stExpander"] { text-align: right; direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏃‍♂️ KidSync: הלוז השבועי")
st.markdown("---")

# בסיס נתונים ראשוני - שימוש בגרשיים כפולים למניעת שגיאות
if "events" not in st.session_state:
    st.session_state.events = [
        {"יום": "שני", "שעה": "16:00", "ילד": "נועם", "פעילות": "כדורסל", "מבוגר": "אמא"},
        {"יום": "שני", "שעה": "17:30", "ילד": "מאיה", "פעילות": "חוג ציור", "מבוגר": ""},
        {"יום": "רביעי", "שעה": "16:30", "ילד": "נועם", "פעילות": "ג'ודו", "מבוגר": "בייביסיטר"},
    ]

# צבעים לפי ילדים
child_colors = {
    "נועם": "#CCE5FF",  # כחול בהיר
    "מאיה": "#FFD1DC",  # ורוד בהיר
    "התינוקת": "#D4EDDA", # ירוק בהיר
    "אחר": "#F8F9FA"
}

# תצוגת טאבים לפי ימי השבוע
days = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי"]
tabs = st.tabs(days)

for i, day_tab in enumerate(tabs):
    with day_tab:
        current_day = days[i]
        
        # סינון ומיון לפי שעה
        day_events = [e for e in st.session_state.events if e["יום"] == current_day]
        day_events = sorted(day_events, key=lambda x: x["שעה"])
        
        if not day_events:
            st.info(f"אין פעילויות מתוכננות ליום {current_day}")
        else:
            for ev in day_events:
                bg_color = child_colors.get(ev["ילד"], "#FFFFFF")
                # הגדרת צבע מסגרת - אדום אם אין מבוגר
                border_style = "5px solid red" if not ev["מבוגר"] else "1px solid #ccc"
                
                # תצוגת כרטיס אירוע
                st.markdown(f"""
                    <div style="
                        background-color:{bg_color}; 
                        padding:15px; 
                        border-radius:10px; 
                        border-right:{border_style}; 
                        margin-bottom:10px;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        color: black;
                    ">
                        <div style="flex: 1;"><b>{ev["שעה"]}</b></div>
                        <div style="flex: 3;"><b>{ev["ילד"]}</b>: {ev["פעילות"]}</div>
                        <div style="flex: 2; text-align: left;">
                            {"✅ " + ev["מבוגר"] if ev["מבוגר"] else "🆘 חסר מבוגר!"}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

# טופס הוספה
st.markdown("---")
with st.expander("➕ הוספת פעילות חדשה"):
    with st.form("add_form"):
        col1, col2 = st.columns(2)
        with col1:
            new_day = st.
