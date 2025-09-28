import os
import random
import pandas as pd
import streamlit as st
from io import BytesIO

# ---- fix matplotlib import issues ----
os.environ["MPLCONFIGDIR"] = "/tmp/matplotlib"

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------------------------
# Convert DataFrame to PNG
# ---------------------------
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
    tbl.scale(1.2, 1.4)
    plt.title(title, fontsize=12, pad=10)

    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=200)
    plt.close(fig)
    buf.seek(0)
    return buf

# ---------------------------
# Simple Login Simulation
# ---------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Smart Classroom & Timetable Scheduler")
    st.subheader("Authorized Personnel Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    login_clicked = st.button("Login")

    if login_clicked:
        # For demo: any username/pwd works
        st.session_state.logged_in = True
        st.success("Login successful! Proceeding to scheduler...")

    # Stop here until login is successful
    if not st.session_state.logged_in:
        st.stop()



# ---------------------------
# Main App after Login
# ---------------------------
st.title("Smart Classroom & Timetable Scheduler")

st.sidebar.header("Input Parameters")

# Input form
classrooms = st.sidebar.number_input("Number of Classrooms", 1, 20, 3)
batches = st.sidebar.number_input("Number of Student Batches", 1, 10, 2)

subjects = st.sidebar.text_area("Subjects (comma separated)", "Math, Physics, Chemistry, English")
faculty = st.sidebar.text_area("Faculty (comma separated)", "Dr. A, Dr. B, Dr. C, Dr. D")

max_classes_day = st.sidebar.slider("Max Classes per Day per Faculty", 1, 6, 4)
classes_week = st.sidebar.slider("Classes per Subject per Week", 1, 10, 3)

# Process input
subject_list = [s.strip() for s in subjects.split(",") if s.strip()]
faculty_list = [f.strip() for f in faculty.split(",") if f.strip()]

days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
slots = ["9-10", "10-11", "11-12", "2-3", "3-4"]

def generate_timetable(option_seed=0):
    random.seed(option_seed)
    data = []
    faculty_load = {f: 0 for f in faculty_list}
    for d in days:
        row = {}
        for s in slots:
            subj = random.choice(subject_list)
            fac = min(faculty_list, key=lambda f: faculty_load[f])
            faculty_load[fac] += 1
            row[s] = f"{subj} ({fac})"
        data.append(row)
    return pd.DataFrame(data, index=days)

# ---------------------------
# Generate Timetables on demand
# ---------------------------
st.subheader("Generated Timetables")

if st.button("Generate Timetables"):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Option 1**")
        df1 = generate_timetable(option_seed=1)
        st.dataframe(df1)
        st.download_button("Download CSV (Option 1)", df1.to_csv().encode("utf-8"), "timetable1.csv")
        img_buf1 = df_to_image(df1, "Timetable Option 1")
        st.download_button("Download PNG (Option 1)", img_buf1, "timetable1.png", mime="image/png")

    with col2:
        st.markdown("**Option 2**")
        df2 = generate_timetable(option_seed=2)
        st.dataframe(df2)
        st.download_button("Download CSV (Option 2)", df2.to_csv().encode("utf-8"), "timetable2.csv")
        img_buf2 = df_to_image(df2, "Timetable Option 2")
        st.download_button("Download PNG (Option 2)", img_buf2, "timetable2.png", mime="image/png")

    st.subheader("Review & Approval")
    choice = st.radio("Action", ["Approve Timetable", "Request Rearrangement"])
    if choice == "Approve Timetable":
        st.success("Timetable approved and saved for deployment.")
    else:
        st.warning("Rearrangement requested — new options will be generated in the final version.")



