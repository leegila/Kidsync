import streamlit as st

st.set_page_config(layout="wide")

# עיצוב בסיסי לרמזור
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    .child-header { text-align: center; font-weight: bold; background: #333; color: white; padding: 5px; border-radius: 5px; }
    div.stButton > button[kind="primary"] { background-color: #d4edda !important; color: black !important; } /* ירוק */
    div.stButton > button[kind="secondary"] { background-color: #f8d7da !important; color: black !important; } /* אדום */
    div.stButton > button { background-color: #fff3cd !important; color: black !important; } /* כתום */
    </style>
    """, unsafe_allow_html=True)

if "events" not in st.session_state:
    st.session_state.events = []

days = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי"]
kids = ["נועם", "מאיה", "התינוקת"]
hours = [f"{h}:00" for h in range(16, 21)]

st.title("🛡️ KidSync - מפת השגחה")

# טופס הוספה פשוט
with st.form("add_form"):
    st.write("➕ הוספת פעילות")
    col1, col2, col3 = st.columns(3)
    d_s = col1.selectbox("יום", days)
    k_s = col1.multiselect("ילדים", kids)
    s_s = col2.selectbox("מהשעה", hours)
    e_s = col2.selectbox("עד שעה", hours + ["21:00"], index=1)
    act = col3.text_input("פעילות")
    grd = col3.text_input("מבוגר")
    
    if st.form_submit_button("עדכן לו\"ז"):
        if k_s and act:
            st.session_state.events.append({
                "day": d_s, "kids": k_s, "act": act, "grd": grd,
                "start": int(s_s.split(":")[0]), "end": int(e_s.split(":")[0])
            })
            st.rerun()

# תצוגת הלוח
view_d = st.selectbox("הצג יום:", days)
st.divider()

h_cols = st.columns([1, 2, 2, 2])
h_cols[0].write("שעה")
for i, name in enumerate(kids):
    h_cols[i+1].markdown(f"<div class='child-header'>{name}</div>", unsafe_allow_html=True)

for h_str in hours:
    h_val = int(h_str.split(":")[0])
    r_cols = st.columns([1, 2, 2, 2])
    r_cols[0].write(f"**{h_str}**")
    
    for i, child in enumerate(kids):
        with r_cols[i+1]:
            match = next((e for e in st.session_state.events if e['day'] == view_d and child in e['kids'] and e['start'] <= h_val < e['end']), None)
            
            if match:
                lbl = f"{match['act']}\n({match['grd'] or '🆘 חסר'})"
                knd = "primary" if match['grd'] else "secondary"
                if st.button(lbl, key=f"{child}_{h_str}", type=knd):
                    st.session_state.events.remove(match)
                    st.rerun()
            else:
                if st.button("❓ חור", key=f"empty_{child}_{h_str}"):
                    st.info("השתמשי בטופס למעלה")
