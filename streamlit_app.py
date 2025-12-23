import streamlit as st
import pandas as pd

# הגדרות RTL ועיצוב
st.set_page_config(page_title="KidSync Interactive", layout="wide")
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    .stButton button { width: 100%; height: 80px; white-space: pre-wrap; margin-bottom: 5px; border-radius: 10px; }
    div[data-testid="stExpander"] { direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ מגדל הפיקוח של אחה\"צ")

# ניהול נתונים
if "events" not in st.session_state:
    st.session_state.events = {} # שימוש במילון לגישה מהירה: (יום, שעה, ילד) -> נתונים

if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = None

days = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי"]
children = ["נועם", "מאיה", "התינוקת"]
hours = [f"{h}:00" for h in range(14, 21)]

# בורר יום
selected_day = st.selectbox("בחר יום להצגה ועריכה:", days)

# יצירת לוח השעות (הדשבורד)
st.subheader(f"לו\"ז יום {selected_day} - לחצי על משבצת לעריכה")

# כותרות הילדים
header_cols = st.columns([1] + [2] * len(children))
with header_cols[0]: st.write("**שעה**")
for i, child in enumerate(children):
    with header_cols[i+1]: st.markdown(f"### {child}")

# בניית המטריצה
for hour in hours:
    row_cols = st.columns([1] + [2] * len(children))
    with row_cols[0]:
        st.markdown(f"<div style='padding-top:25px; font-weight:bold;'>{hour}</div>", unsafe_allow_html=True)
    
    for i, child in enumerate(children):
        with row_cols[i+1]:
            # מפתח ייחודי לכל משבצת
            key = (selected_day, hour, child)
            event = st.session_state.events.get(key)
            
            # עיצוב הכפתור לפי הסטטוס
            label = "➕ הוסף"
            type_button = "secondary"
            
            if event:
                guard = event['מבוגר'] if event['מבוגר'] else "🆘 חסר!"
                label = f"{event['פעילות']}\n({guard})"
                type_button = "primary" if event['מבוגר'] else "secondary"
                # צבע אדום למבוגר חסר מושג דרך HTML/CSS (בעקיפין דרך ה-label)

            if st.button(label, key=f"btn_{key}", type=type_button):
                st.session_state.edit_mode = key
                st.rerun()

# אזור עריכה שצף/מופיע רק כשלוחצים
if st.session_state.edit_mode:
    st.divider()
    e_day, e_hour, e_child = st.session_state.edit_mode
    st.subheader(f"עריכת פעילות: {e_child} ביום {e_day} בשעה {e_hour}")
    
    current_val = st.session_state.events.get(st.session_state.edit_mode, {"פעילות": "", "מבוגר": ""})
    
    with st.form("edit_form"):
        new_act = st.text_input("פעילות:", value=current_val["פעילות"])
        new_guard = st.text_input("מבוגר אחראי (השאירי ריק אם אין):", value=current_val["מבוגר"])
        
        c1, c2 = st.columns(2)
        with c1:
            if st.form_submit_button("שמור עדכון"):
                st.session_state.events[st.session_state.edit_mode] = {"פעילות": new_act, "מבוגר": new_guard}
                st.session_state.edit_mode = None
                st.rerun()
        with c2:
            if st.form_submit_button("מחק פעילות"):
                if st.session_state.edit_mode in st.session_state.events:
                    del st.session_state.events[st.session_state.edit_mode]
                st.session_state.edit_mode = None
                st.rerun()
    if st.button("ביטול"):
        st.session_state.edit_mode = None
        st.rerun()

# כפתור איפוס שבועי
st.sidebar.divider()
if st.sidebar.button("איפוס כל הלו\"ז השבועי"):
    st.session_state.events = {}
    st.rerun()
