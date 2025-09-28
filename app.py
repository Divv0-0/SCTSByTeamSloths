import streamlit as st
import pandas as pd
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from io import BytesIO

# Initialize login state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Function: convert dataframe to PNG
def df_to_image(df, title="Timetable"):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis("off")
    tbl = ax.table(cellText=df.values,
                   colLabels=df.columns,
                   rowLabels=df.index,
                   cellLoc="center",
                   loc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9)
    tbl.scale(1.2, 1.3)
    plt.title(title, fontsize=12, pad=10)
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=200)
    plt.close(fig)
    buf.seek(0)
    return buf

# Function: generate timetable
def generate_timetable(subjects, faculty):
    days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    slots = ["9-10", "10-11", "11-12", "2-3", "3-4"]
    random.seed(42)
    data = []
    faculty_load = {f: 0 for f in faculty}
    for d in days:
        row = {}
        for s in slots:
            subj = random.choice(subjects)
            fac = min(faculty, key=lambda f: faculty_load[f])
            faculty_load[fac] += 1
            row[s] = f"{subj} ({fac})"
        data.append(row)
    return pd.DataFrame(data, index=days)

# -------------------
# Scene: Login
# -------------------
if not st.session_state.logged_in:
    st.title("Smart Classroom & Timetable Scheduler")
    st.subheader("Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user and pwd:   # demo: accept any login
            st.session_state.logged_in = True
            st.session_state.username = user
            st.experimental_rerun()
        else:
            st.error("Please enter both username and password")

# -------------------
# Scene: Main App
# -------------------
else:
    st.title("Smart Classroom & Timetable Scheduler")
    st.write(f"Welcome, **{st.session_state.username}** 👋")

    # Logout button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.experimental_rerun()

    # Sidebar inputs
    st.sidebar.header("Inputs")
    subjects = st.sidebar.text_area("Subjects (comma separated)", "Math, Physics, Chemistry, English")
    faculty = st.sidebar.text_area("Faculty (comma separated)", "Dr. A, Dr. B, Dr. C, Dr. D")

    subject_list = [s.strip() for s in subjects.split(",") if s.strip()]
    faculty_list = [f.strip() for f in faculty.split(",") if f.strip()]

    if st.button("Generate Timetable"):
        df = generate_timetable(subject_list, faculty_list)
        st.subheader("Generated Timetable")
        st.dataframe(df)

        # CSV download
        st.download_button("Download CSV", df.to_csv().encode("utf-8"), "timetable.csv")

        # PNG download
        img_buf = df_to_image(df, "Generated Timetable")
        st.download_button("Download PNG", img_buf, "timetable.png", mime="image/png")

