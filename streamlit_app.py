import streamlit as st
import pandas as pd

# הגדרת יישור לימין (RTL) ותצוגה
st.set_page_config(page_title='KidSync Weekly', layout='wide')
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    th, td { text-align: right !important; }
    </style>
    """, unsafe_allow_html=True)

st.title('🏃‍♂️ KidSync: הלוז השבועי שלי')

# בסיס נתונים עם חוגים קבועים (דוגמה)
if 'events' not in st.session_state:
    st.session_state.events = [
        {'יום': 'שני', 'שעה': '16:00', 'ילד': 'נועם', 'פעילות': 'כדורסל', 'מבוגר': 'אמא'},
        {'יום': 'שני', 'שעה': '17:30', 'ילד': 'מאיה', 'פעילות': 'חוג ציור', 'מבוגר': ''},
        {'יום': 'רביעי', 'שעה': '16:30', 'ילד': 'נועם', 'פעילות': 'ג'ודו', 'מבוגר': 'בייביסיטר'},
    ]

# צבעים לפי ילדים
child_colors = {
    'נועם': '#CCE5FF',  # כחול בהיר
    'מאיה': '#FFD1DC',  # ורוד בהיר
    'התינוקת': '#D4EDDA', # ירוק בהיר
    'אחר': '#F8F9FA'
}

# תצוגת טאבים לפי ימי השבוע
days = ['ראשון', 'שני', 'שלישי', 'רביעי', 'חמישי', 'שישי']
selected_day = st.tabs(days)

for i, day_tab in enumerate(selected_day):
    with day_tab:
        current_day = days[i]
        st.subheader(f'תוכנית ליום {current_day}')
        
        # סינון ומיון לפי שעה
        day_events = [e for e in st.session_state.events if e['יום'] == current_day]
        day_events = sorted(day_events, key=lambda x: x['שעה'])
        
        if not day_events:
            st.info('אין פעילויות מתוכננות ליום זה.')
        else:
            for ev in day_events:
                bg_color = child_colors.get(ev['ילד'], '#FFFFFF')
                border_color = 'red' if not ev['מבוגר'] else '#ccc'
                
                # כרטיס ויזואלי לכל אירוע
                with st.container():
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col1:
                        st.markdown(f"**{ev['שעה']}**")
                    with col2:
                        st.markdown(f"<div style='background-color:{bg_color}; padding:10px; border-radius:5px; border-right: 5px solid {border_color}'>"
                                    f"<b>{ev['ילד']}</b>: {ev['פעילות']}</div>", unsafe_allow_html=True)
                    with col3:
                        if ev['מבוגר']:
                            st.success(f"✅ {ev['מבוגר']}")
                        else:
                            st.error("🆘 חסר מבוגר!")

# טופס הוספה
st.divider()
with st.expander("➕ הוספת פעילות חדשה / חוג קבוע"):
    with st.form("add_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            new_day = st.selectbox("יום", days)
            new_child = st.selectbox("ילד", list(child_colors.keys()))
        with c2:
            new_time = st.text_input("שעה (למשל 16:30)")
            new_act = st.text_input("מה הפעילות?")
        with c3:
            new_guard = st.text_input("מבוגר אחראי")
        
        if st.form_submit_button("שמור בלוז"):
            st.session_state.events.append({
                'יום': new_day, 'שעה': new_time, 'ילד': new_child, 'פעילות': new_act, 'מבוגר': new_guard
            })
            st.rerun()

if st.button("נקה הכל"):
    st.session_state.events = []
    st.rerun()
