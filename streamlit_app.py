import streamlit as st

# הגדרות בסיסיות למראה נקי
st.set_page_config(page_title="KidSync Simple", layout="wide")
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    .stButton button { 
        width: 100%; 
        height: 50px; 
        margin-bottom: 5px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ ניהול אחה\"צ - פשוט וקל")

# אתחול הנתונים
if "events" not in st.session_state:
    st.session_state.events = {} # מפתח: (יום, ילד, שעה)

if "selected_slot" not in st.session_state:
    st.session_state.selected_slot = None

days = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי"]
children = ["נועם", "מאיה", "התינוקת"]
hours = [f"{h}:00" for h in range(14, 21)]

# בחירת יום
selected_day = st.selectbox("בחר יום:", days)

# יצירת הטבלה
st.write(f"### לו\"ז ליום {selected_day}")
cols = st.columns([1, 2, 2, 2])
cols[0].write("**שעה**")
for i, child in enumerate(children):
    cols[i+1].write(f"**{child}**")

for hour in hours:
    row = st.columns([1, 2, 2, 2])
    row[0].write(hour)
    for i, child in enumerate(children):
        with row[i+1]:
            slot_key = (selected_day, child, hour)
            event = st.session_state.events.get(slot_key)
            
            # עיצוב הכפתור
            if event:
                label = f"{event['act']} ({event['guard'] or '🆘'})"
                btn_type = "primary" if event['guard'] else "secondary"
            else:
                label = "➕"
                btn_type = "secondary"
            
            if st.button(label, key=f"{slot_key}", type=btn_type):
                st.session_state.selected_slot = slot_key
                st.rerun()

# חלון עריכה פשוט מתחת לטבלה
if st.session_state.selected_slot:
    st.divider()
    day, child, hour = st.session_state.selected_slot
    st.subheader(f"עדכון: {child} ביום {day} שעה {hour}")
    
    with st.form("edit_form"):
        act = st.text_input("מה הפעילות?")
        guard = st.text_input("מי משגיח?")
        col_save, col_del, col_cancel = st.columns(3)
        
        if col_save.form_submit_button("שמור"):
            st.session_state.events[st.session_state.selected_slot] = {"act": act, "guard": guard}
            st.session_state.selected_slot = None
            st.rerun()
            
        if col_del.form_submit_button("מחק"):
            st.session_state.events.pop(st.session_state.selected_slot, None)
            st.session_state.selected_slot = None
            st.rerun()
            
    if st.button("סגור ללא שינוי"):
        st.session_state.selected_slot = None
        st.rerun()
