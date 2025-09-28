import streamlit as st
import pandas as pd
import random
import matplotlib
matplotlib.use("Agg")  # safe backend
import matplotlib.pyplot as plt
from io import BytesIO

st.title("Smart Classroom & Timetable Scheduler (Prototype)")

# Input form
st.sidebar.header("Inputs")
subjects = st.sidebar.text_area("Subjects (comma separated)", "Math, Physics, Chemistry, English")
faculty = st.sidebar.text_area("Faculty (comma separated)", "Dr. A, Dr. B, Dr. C, Dr. D")

subject_list = [s.strip() for s in subjects.split(",") if s.strip()]
faculty_list = [f.strip() for f in faculty.split(",") if f.strip()]

days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
slots = ["9-10", "10-11", "11-12", "2-3", "3-4"]

def generate_timetable():
    random.seed(42)  # fixed for repeatability
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

if st.button("Generate Timetable"):
    df = generate_timetable()
    st.subheader("Generated Timetable")
    st.dataframe(df)

    # CSV download
    st.download_button("Download CSV", df.to_csv().encode("utf-8"), "timetable.csv")

    # PNG download
    img_buf = df_to_image(df, "Generated Timetable")
    st.download_button("Download PNG", img_buf, "timetable.png", mime="image/png")
