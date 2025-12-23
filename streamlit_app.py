import streamlit as st

# הגדרות RTL ומראה נקי
st.set_page_config(page_title="KidSync", layout="wide")
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    .stButton button { width: 100%; height: 45px; margin-bottom: 2px; border-radius: 4px; font-size: 12px; }
    .hour-label { font-weight: bold; padding-top: 10px; border-bottom: 1px solid #eee; height: 45px; }
    .child-header { text-align: center; font-weight: bold; background: #f8f9fa; padding: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ ניהול אחה\"צ משפחתי")

# אתחול נתונים
if "events" not in st.session_state:
    st.session_state.events = [] # רשימת פעילויות

days = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי"]
children = ["נועם", "מאיה", "התינוקת"]
hours = [f"{h}:00" for h in range(14, 21)]

# --- אזור הוספת פעילות (למעלה כדי שלא ילך לאיבוד) ---
with st.expander("➕ הוספת פעילות חדשה (לכמה ילדים/שעות)", expanded=False):
    with st.form("quick_add"):
        col1, col2 = st.columns(2)
        with col1:
            sel_day = st.selectbox("יום", days)
            sel_children = st.multiselect("עבור איזה ילדים?", children)
            sel_start = st.selectbox("שעת התחלה", hours)
            sel_end = st.selectbox("שעת סיום", hours[hours.index(sel_start)+1:] + ["21:00"])
        with col2:
            sel_act = st.text_input("מה הפעילות? (למשל: ג'ודו)")
            sel_guard = st.text_input("מי המבוגר? (השאירי ריק אם חסר)")
            sel_weekly = st.checkbox("זו פעילות קבועה בכל שבוע")
        
        if st.form_submit_button("הוסף ללוח"):
            if sel_children and sel_act:
                st.session_state.events.append({
                    "day": sel_day, "children": sel_children, 
                    "start": int(sel_start.split(":")[0]), "end": int(sel_end.split(":")[0]),
                    "act": sel_act, "guard": sel_guard, "weekly": sel_weekly
                })
                st.success("הפעילות נוספה!")
                st.rerun()

# --- הצגת הלוח ---
selected_day_view = st.selectbox("הצגת לו\"ז ליום:", days)

# שורת כותרת של שמות הילדים
st.markdown("---")
h_cols = st.columns([1, 2, 2, 2])
h_cols[0].write("") # עמודת השעות
for i, child in enumerate(children):
    h_cols[i+1].markdown(f"<div class='child-header'>{child}</div>", unsafe_allow_html=True)

# בניית הלוח שעה-שעה
for h_str in hours:
    h_val = int(h_str.split(":")[0])
    r_cols = st.columns([1, 2, 2, 2])
    
    # עמודת השעה
    r_cols[0].markdown(f"<div class='hour-label'>{h_str}</div>", unsafe_allow_html=True)
    
    # עמודות הילדים
    for i, child in enumerate(children):
        with r_cols[i+1]:
            # חיפוש האם יש פעילות לילד הזה בשעה הזו
            current_ev = None
            for ev in st.session_state.events:
                if ev['day'] == selected_day_view and child in ev['children'] and ev['start'] <= h_val < ev['end']:
                    current_ev = ev
                    break
            
            if current_ev:
                label = f"{current_ev['act']}\n({current_ev['guard'] or '🆘 חסר'})"
                color = "primary" if current_ev['guard'] else "secondary"
                if st.button(label, key=f"{child}_{h_str}_{selected_day_view}", type=color):
                    # אפשרות מחיקה בלחיצה
                    st.session_state.events.remove(current_ev)
                    st.rerun()
            else:
                st.button("➕", key=f"empty_{child}_{h_str}_{selected_day_view}", disabled=True)

# כפתור ניקוי
if st.sidebar.button("ניקוי כל הלוח"):
    st.session_state.events = []
    st.rerun()
