import streamlit as st
import pandas as pd
from datetime import datetime

# הגדרות תצוגה וכיוון כתיבה
st.set_page_config(page_title="KidSync Pro", layout="wide")
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    div[data-testid="stExpander"] { text-align: right; direction: rtl; }
    .stTabs [data-baseweb="tab-list"] { direction: rtl; gap: 10px; }
    p, h1, h2, h3, span, label { text-align: right; justify-content: right; }
    .stRadio > div { direction: rtl; gap: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏃‍♂️ KidSync Pro")

# אתחול נתונים (כולל תמיכה בחוגים קבועים)
if "events" not in st.session_state:
    st.session_state.events = [
        {"יום": "שני", "שעה": "16:00", "ילד": "נועם", "פעילות": "כדורסל", "מבוגר": "אמא", "קבוע": True},
        {"יום": "שני", "שעה": "17:30", "ילד": "מאיה", "פעילות": "חוג ציור", "מבוגר": "", "קבוע": True},
        {"יום": "רביעי", "שעה": "16:30", "ילד": "נועם", "פעילות": "ג'ודו", "מבוגר": "בייביסיטר", "קבוע": True}
    ]

child_colors = {"נועם": "#CCE5FF", "מאיה": "#FFD1DC", "התינוקת": "#D4EDDA", "אחר": "#F8F9FA"}
days = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי"]

# --- תפריט עליון: בחירת תצוגה ---
view_option = st.radio("בחר תצוגה:", ["יום אחד", "3 ימים", "שבוע מלא"], horizontal=True)

def render_event(ev):
    bg = child_colors.get(ev["ילד"], "#FFFFFF")
    border = "5px solid red" if not ev["מבוגר"] else "1px solid #ccc"
    repeat_icon = "🔄" if ev.get("קבוע") else "📍"
    st.markdown(f"""
        <div style="background-color:{bg}; padding:12px; border-radius:10px; border-right:{border}; margin-bottom:8px; color: black; display: flex; justify-content: space-between; align-items: center;">
            <div style="font-weight: bold; width: 60px;">{ev["שעה"]}</div>
            <div style="flex-grow: 1; margin-right: 15px;">{repeat_icon} <b>{ev["ילד"]}</b>: {ev["פעילות"]}</div>
            <div style="text-align: left; min-width: 100px;">{"✅ " + ev["מבוגר"] if ev["מבוגר"] else "🆘 חסר!"}</div>
        </div>
    """, unsafe_allow_html=True)

# --- לוגיקת תצוגה ---
if view_option == "שבוע מלא":
    tabs = st.tabs(days)
    for i, day_tab in enumerate(tabs):
        with day_tab:
            day_events = sorted([e for e in st.session_state.events if e["יום"] == days[i]], key=lambda x: x["שעה"])
            if not day_events: st.info(f"אין פעילויות ליום {days[i]}")
            for ev in day_events: render_event(ev)

elif view_option == "3 ימים":
    col1, col2, col3 = st.columns(3)
    # נניח שהיום יום שני לצורך הדוגמה (ניתן לחבר לתאריך אמיתי)
    selected_3_days = ["ראשון", "שני", "שלישי"] 
    for idx, col in enumerate([col1, col2, col3]):
        with col:
            st.subheader(selected_3_days[idx])
            d_events = sorted([e for e in st.session_state.events if e["יום"] == selected_3_days[idx]], key=lambda x: x["שעה"])
            for ev in d_events: render_event(ev)

else: # יום אחד
    target_day = st.selectbox("בחר יום להצגה:", days)
    d_events = sorted([e for e in st.session_state.events if e["יום"] == target_day], key=lambda x: x["שעה"])
    if not d_events: st.info("יום פנוי!")
    for ev in d_events: render_event(ev)

# --- הוספת פעילות ---
st.markdown("---")
with st.expander("➕ הוספת פעילות חדשה / חוג קבוע"):
    with st.form("add_new"):
        c1, c2 = st.columns(2)
        with c1:
            n_day = st.selectbox("יום", days)
            n_child = st.selectbox("ילד", list(child_colors.keys()))
            n_time = st.text_input("שעה (למשל 16:00)")
        with c2:
            n_act = st.text_input("פעילות")
            n_guard = st.text_input("מבוגר אחראי")
            n_is_fixed = st.checkbox("חוג קבוע (חוזר כל שבוע)")
        
        if st.form_submit_button("שמור"):
            st.session_state.events.append({
                "יום": n_day, "שעה": n_time, "ילד": n_child, 
                "פעילות": n_act, "מבוגר": n_guard, "קבוע": n_is_fixed
            })
            st.rerun()

if st.button("איפוס נתונים"):
    st.session_state.events = []
    st.rerun()
