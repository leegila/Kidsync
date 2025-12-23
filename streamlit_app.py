import streamlit as st
import pandas as pd

# הגדרות RTL ועיצוב מתקדם
st.set_page_config(page_title="KidSync Control Tower", layout="wide")
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    .main-table { width: 100%; border-collapse: collapse; margin-top: 20px; }
    .main-table th, .main-table td { border: 1px solid #ddd; padding: 10px; text-align: center; }
    .header-row { background-color: #f2f2f2; font-weight: bold; }
    .gap-cell { background-color: #ffcccc; color: #cc0000; font-weight: bold; }
    .filled-cell { background-color: #d4edda; border-right: 10px solid; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ מגדל הפיקוח של אחה\"צ")

# ניהול נתונים
if "events" not in st.session_state:
    st.session_state.events = [
        {"יום": "שני", "שעה": "16:00", "ילד": "נועם", "פעילות": "כדורסל", "מבוגר": "אמא"},
        {"יום": "שני", "שעה": "17:00", "ילד": "מאיה", "פעילות": "חוג ציור", "מבוגר": ""}
    ]

days = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי"]
children = ["נועם", "מאיה", "התינוקת"]
hours = ["14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00"]

# בורר תצוגה
view_mode = st.radio("בחר טווח זמן:", ["יומי מפורט", "שבועי ריכוזי"], horizontal=True)

if view_mode == "יומי מפורט":
    selected_day = st.selectbox("בחר יום:", days)
    st.subheader(f"סטטוס השגחה - יום {selected_day}")
    
    # יצירת מטריצת תצוגה
    cols = st.columns(len(children))
    for idx, child in enumerate(children):
        with cols[idx]:
            st.markdown(f"### {child}")
            for hour in hours:
                # חיפוש פעילות לשעה ולילד הספציפיים
                act = next((e for e in st.session_state.events if e["יום"] == selected_day and e["שעה"] == hour and e["ילד"] == child), None)
                
                if act:
                    color = "#CCE5FF" if child == "נועם" else "#FFD1DC"
                    status = f"✅ {act['מבוגר']}" if act['מבוגר'] else "🆘 אין השגחה!"
                    border = "5px solid green" if act['מבוגר'] else "5px solid red"
                    st.markdown(f"""
                        <div style="background:{color}; padding:10px; border-radius:5px; border-right:{border}; margin-bottom:5px;">
                            <b>{hour}</b><br>{act['פעילות']}<br><small>{status}</small>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    # כאן הפיצ'ר החשוב: סימון שעות ריקות כ"חור"
                    st.markdown(f"""
                        <div style="background:#f9f9f9; padding:10px; border-radius:5px; border: 1px dashed #ccc; margin-bottom:5px; color:#999;">
                            <b>{hour}</b><br>זמן בית / לא ידוע
                        </div>
                    """, unsafe_allow_html=True)

else: # שבועי ריכוזי
    st.subheader("ריכוז חוסרים שבועי")
    missing = [e for e in st.session_state.events if not e["מבוגר"]]
    if missing:
        for m in missing:
            st.warning(f"יום {m['יום']} ב-{m['שעה']}: {m['ילד']} ב{m['פעילות']} ללא מבוגר!")
    else:
        st.success("כל החוגים המתוכננים מאוישים!")

# טופס הוספה חכם
st.divider()
with st.expander("➕ עדכון לו\"ז / הוספת חוג"):
    with st.form("add_event"):
        c1, c2, c3 = st.columns(3)
        with c1:
            d = st.selectbox("יום", days)
            c = st.selectbox("ילד", children)
        with c2:
            t = st.selectbox("שעה", hours)
            a = st.text_input("פעילות (חוג/בית/חבר)")
        with c3:
            g = st.text_input("מי משגיח?")
        
        if st.form_submit_button("עדכן לו\"ז"):
            # מחיקת אירוע קיים באותה שעה אם יש
            st.session_state.events = [e for e in st.session_state.events if not (e["יום"] == d and e["שעה"] == t and e["ילד"] == c)]
            st.session_state.events.append({"יום": d, "שעה": t, "ילד": c, "פעילות": a, "מבוגר": g})
            st.rerun()
