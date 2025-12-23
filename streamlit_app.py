import streamlit as st
import pandas as pd

# הגדרות RTL ועיצוב כפתורים
st.set_page_config(page_title="KidSync Control Tower", layout="wide")
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    /* עיצוב כפתורי המשבצות */
    .stButton button { 
        width: 100%; 
        height: 60px; 
        border-radius: 8px; 
        font-weight: bold;
        border: 1px solid #ddd;
    }
    /* צבעים לפי מצבים */
    div.stButton > button:first-child { background-color: #f0f2f6; color: #555; } /* ריק */
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ מגדל הפיקוח של אחה\"צ")

# ניהול נתונים
if "events" not in st.session_state:
    st.session_state.events = [] # רשימת מילונים: {day, start_hour, end_hour, child, activity, guardian}

if "edit_slot" not in st.session_state:
    st.session_state.edit_slot = None

days = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי"]
children = ["נועם", "מאיה", "התינוקת"]
hours = [f"{h}:00" for h in range(14, 21)]

child_colors = {"נועם": "#CCE5FF", "מאיה": "#FFD1DC", "התינוקת": "#D4EDDA"}

# בורר יום
selected_day = st.selectbox("בחר יום להצגה:", days)

# פונקציה לבדיקה מה קורה בשעה ספציפית
def get_event_for_slot(day, hour, child):
    h_int = int(hour.split(":")[0])
    for ev in st.session_state.events:
        start_h = int(ev['start_hour'].split(":")[0])
        end_h = int(ev['end_hour'].split(":")[0])
        if ev['day'] == day and ev['child'] == child and start_h <= h_int < end_h:
            return ev
    return None

# הצגת הדשבורד
st.subheader(f"לו\"ז יום {selected_day}")
header_cols = st.columns([1] + [2] * len(children))
with header_cols[0]: st.write("**שעה**")
for i, child in enumerate(children):
    with header_cols[i+1]: st.markdown(f"<p style='text-align:center;'><b>{child}</b></p>", unsafe_allow_html=True)

for hour in hours:
    row_cols = st.columns([1] + [2] * len(children))
    with row_cols[0]:
        st.markdown(f"<div style='padding-top:15px; font-weight:bold;'>{hour}</div>", unsafe_allow_html=True)
    
    for i, child in enumerate(children):
        with row_cols[i+1]:
            event = get_event_for_slot(selected_day, hour, child)
            key = f"{selected_day}_{hour}_{child}"
            
            if event:
                label = f"{event['activity']}\n({event['guardian'] if event['guardian'] else '🆘 חסר!'})"
                # בחירת צבע: אדום אם חסר מבוגר, אחרת צבע הילד
                bg_color = "red" if not event['guardian'] else child_colors.get(child, "#eee")
                text_color = "white" if not event['guardian'] else "black"
                
                # כפתור מעוצב לאירוע קיים
                st.markdown(f"<style>div[data-testid='stHorizontalBlock'] div:nth-child({i+2}) button[key='btn_{key}'] {{ background-color: {bg_color} !important; color: {text_color} !important; }}</style>", unsafe_allow_html=True)
            else:
                label = "➕ פנוי"
            
            if st.button(label, key=f"btn_{key}"):
                st.session_state.edit_slot = {"day": selected_day, "hour": hour, "child": child}
                st.rerun()

# "חלון עריכה" (מוצג כסיידבר או אזור ייעודי)
if st.session_state.edit_slot:
    st.sidebar.header("עריכת פעילות")
    slot = st.session_state.edit_slot
    st.sidebar.write(f"הוספה ל{slot['child']} ביום {slot['day']} משעה {slot['hour']}")
    
    with st.sidebar.form("edit_form"):
        act = st.text_input("פעילות:", placeholder="למשל: חוג ג'ודו")
        end_h = st.selectbox("עד שעה:", hours[hours.index(slot['hour'])+1:] + ["21:00"])
        guard = st.text_input("מבוגר אחראי:", placeholder="השאירי ריק אם אין")
        
        submitted = st.form_submit_button("שמור")
        if
