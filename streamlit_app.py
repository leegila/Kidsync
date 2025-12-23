import streamlit as st
import pandas as pd

# הגדרות תצוגה בסיסיות
st.set_page_config(page_title="KidSync", layout="centered")

# כותרת האפליקציה
st.title("🏃‍♂️ KidSync: ניהול לו"ז הילדים")
st.markdown("---")

# בסיס נתונים זמני (נשמר כל עוד האפליקציה רצה)
if 'events' not in st.session_state:
    st.session_state.events = [
        {"ילד": "נועם", "פעילות": "כדורסל", "שעה": "17:00", "מבוגר": "אמא", "משימה": "איסוף מהגן"},
        {"ילד": "מאיה", "פעילות": "חוג ציור", "שעה": "16:30", "מבוגר": "", "משימה": "פיזור לחוג"}
    ]

# פונקציה לבדיקת "חורים" בלו"ז
def check_for_gaps():
    gaps = [e for e in st.session_state.events if not e["מבוגר"] or e["מבוגר"] == "דרוש פתרון"]
    return gaps

# הצגת התראות על חורים
gaps = check_for_gaps()
if gaps:
    st.error(f"⚠️ שים לב! יש {len(gaps)} פעילויות ללא מבוגר אחראי!")

# תצוגת הלו"ז היומי
st.subheader("הלו"ז להיום")
if st.session_state.events:
    df = pd.DataFrame(st.session_state.events)
    # עיצוב הטבלה
    def highlight_empty(val):
        color = '#ffcccc' if val == "" or val == "דרוש פתרון" else ''
        return f'background-color: {color}'
    
    st.table(df.style.applymap(highlight_empty, subset=['מבוגר']))
else:
    st.write("הלו"ז ריק. הוסיפו פעילות למטה.")

# טופס הוספת פעילות
st.markdown("---")
st.subheader("הוספת פעילות חדשה")
with st.form("new_event"):
    c1, c2 = st.columns(2)
    with c1:
        child = st.selectbox("ילד/ה", ["נועם", "מאיה", "התינוקת", "אחר"])
        activity = st.text_input("מה הפעילות? (למשל: חוג ג'ודו)")
    with c2:
        time = st.text_input("באיזו שעה? (למשל: 16:00)")
        guardian = st.text_input("מי המבוגר האחראי? (השאירי ריק אם אין)")
    
    submit = st.form_submit_button("הוסף ללו"ז")
    
    if submit:
        new_entry = {
            "ילד": child, 
            "פעילות": activity, 
            "שעה": time, 
            "מבוגר": guardian if guardian else "",
            "משימה": "פעילות חדשה"
        }
        st.session_state.events.append(new_entry)
        st.success("הפעילות נוספה!")
        st.rerun()

# אפשרות לאיפוס הלו"ז
if st.button("נקה לו"ז"):
    st.session_state.events = []
    st.rerun()
