import streamlit as st
import pandas as pd

# הגדרות תצוגה
st.set_page_config(page_title='KidSync', layout='centered')

# כותרת האפליקציה - תיקון הגרשיים
st.title('🏃‍♂️ KidSync: ניהול לוז הילדים')
st.markdown('---')

# בסיס נתונים זמני
if 'events' not in st.session_state:
    st.session_state.events = [
        {'ילד': 'נועם', 'פעילות': 'כדורסל', 'שעה': '17:00', 'מבוגר': 'אמא', 'סטטוס': 'מאויש'},
        {'ילד': 'מאיה', 'פעילות': 'חוג ציור', 'שעה': '16:30', 'מבוגר': '', 'סטטוס': 'חור בלוז'}
    ]

# פונקציה לבדיקת חורים
def check_for_gaps():
    return [e for e in st.session_state.events if not e['מבוגר']]

# התראת חורים
gaps = check_for_gaps()
if gaps:
    st.error(f'⚠️ שימי לב! יש {len(gaps)} פעילויות ללא מבוגר אחראי!')

st.subheader('הלוז להיום')
if st.session_state.events:
    df = pd.DataFrame(st.session_state.events)
    
    def highlight_empty(val):
        return 'background-color: #ffcccc' if val == '' else ''
    
    st.table(df.style.applymap(highlight_empty, subset=['מבוגר']))

st.markdown('---')
st.subheader('הוספת פעילות חדשה')
with st.form('new_event'):
    c1, c2 = st.columns(2)
    with c1:
        child = st.selectbox('ילד/ה', ['נועם', 'מאיה', 'התינוקת', 'אחר'])
        activity = st.text_input('מה הפעילות?')
    with c2:
        time = st.text_input('באיזו שעה?')
        guardian = st.text_input('מי המבוגר? (השאירי ריק אם חסר)')
    
    submit = st.form_submit_button('הוסף ללוז')
    
    if submit:
        new_entry = {
            'ילד': child, 
            'פעילות': activity, 
            'שעה': time, 
            'מבוגר': guardian,
            'סטטוס': 'מאויש' if guardian else 'חור בלוז'
        }
        st.session_state.events.append(new_entry)
        st.rerun()

if st.button('נקה הכל'):
    st.session_state.events = []
    st.rerun()
