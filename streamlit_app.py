import streamlit as st

# הגדרות RTL ועיצוב
st.set_page_config(page_title="KidSync Control", layout="wide")
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    .stButton button { 
        width: 100%; 
        height: 65px; 
        border-radius: 8px; 
        font-weight: bold;
        border: 1px solid #ddd;
        white-space: pre-wrap;
    }
    div[data-testid="stSidebar"] { direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ מגדל הפיקוח של אחה\"צ")

# ניהול נתונים בזיכרון
if "events" not in st.session_state:
    st.session_state.events = []

if "edit_slot" not in st.session_state:
    st.session_state.edit_slot = None

days = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי"]
children = ["נועם", "מאיה", "התינוקת"]
hours = [f"{h}:00" for h in range(14, 21)]
child_colors = {"נועם": "#CCE5FF", "מאיה": "#FFD1DC", "התינוקת": "#D4EDDA"}

# בחירת יום
selected_day = st.selectbox("בחר יום להצגה:", days)

# פונקציה לבדיקת פעילות בשעה ספציפית
def get_event(day, hour, child):
    h_int = int(hour.split(":")[0])
    for ev in st.session_state.events:
        start_h = int(ev['start'].split(":")[0])
        end_h = int(ev['end'].split(":")[0])
        if ev['day'] == day and ev['child'] == child and start_h <= h_int < end_h:
            return ev
    return None

# הצגת לוח השעות
st.subheader(f"לו\"ז יום {selected_day}")
cols = st.columns([1] + [2] * len(children))
cols[0].write("**שעה**")
for i, child in enumerate(children):
    cols[i+1].markdown(f"<p style='text-align:center;'><b>{child}</b></p>", unsafe_allow_html=True)

for hour in hours:
    row = st.columns([1] + [2] * len(children))
    row[0].markdown(f"<div style='padding-top:15px; font-weight:bold;'>{hour}</div>", unsafe_allow_html=True)
    
    for i, child in enumerate(children):
        with row[i+1]:
            ev = get_event(selected_day, hour, child)
            key = f"btn_{selected_day}_{hour}_{child}"
            
            if ev:
                label = f"{ev['act']}\n({ev['guard'] if ev['guard'] else '🆘 חסר!'})"
                bg = "red" if not ev['guard'] else child_colors.get(child, "#eee")
                txt = "white" if not ev['guard'] else "black"
