import streamlit as st
import pandas as pd
from datetime import datetime
import os

#PAGE CONFIG
st.set_page_config(page_title="Data Analysis Quiz", layout="wide")

#DATA FILE
CSV_FILE = "results.csv"

# Create CSV if it doesn't exist
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=[
        "Name", "Topic", "Score", "Total Questions", "Percentage", "Date"
    ])
    df.to_csv(CSV_FILE, index=False)

#QUESTIONS DATABASE
questions = {
    "Data Pipeline": [
        ("What is a data pipeline?",
         ["A data storage system", "A process to move and transform data", "A database", "A UI tool"],
         1),
        ("Which stage comes first?",
         ["Processing", "Visualization", "Collection", "Deployment"],
         2)
    ],

    "Streamlit": [
        ("What is Streamlit mainly used for?",
         ["Game development", "Web dashboards for data apps", "Mobile apps", "Operating systems"],
         1),
        ("Which command runs a Streamlit app?",
         ["python app.py", "streamlit start", "streamlit run app.py", "run streamlit"],
         2)
    ],

    "Python Pandas": [
        ("What is a DataFrame?",
         ["A chart", "A table-like data structure", "A list", "A function"],
         1),
        ("Which function reads a CSV?",
         ["read.csv()", "open_csv()", "pd.read_csv()", "load_csv()"],
         2)
    ],

    "Jupyter": [
        ("Jupyter is mainly used for?",
         ["Game design", "Interactive coding & notebooks", "Web hosting", "Databases"],
         1),
        ("What file extension does Jupyter use?",
         [".py", ".txt", ".ipynb", ".csv"],
         2)
    ]
}

#SIDEBAR NAV
st.sidebar.title("Navigation")

menu = st.sidebar.radio(
    "Go to",
    ["Home", "Tasks (Quiz)", "Results Dashboard"]
)

#LOAD DATA
df = pd.read_csv(CSV_FILE)

#HOME (EDITED)
if menu == "Home":
    st.title("Data Analysis Learning Quiz Dashboard")

    st.write("""
    This dashboard displays quiz performance data collected from users.
    Select a topic to view progress and related results.
    """)

    if df.empty:
        st.info("No quiz data available yet.")
    else:
        # Topic selector
        selected_topic = st.selectbox(
            "Select a topic to view progress",
            df["Topic"].unique()
        )

        # Filter data by selected topic
        topic_df = df[df["Topic"] == selected_topic]

        st.subheader(f"Progress for {selected_topic}")

        # Group data for bar chart
        topic_progress = (
            topic_df.groupby("Date")["Percentage"]
            .mean()
        )

        st.bar_chart(topic_progress)

        st.subheader("Results Table (Selected Topic)")
        st.dataframe(topic_df)

#TASKS / QUIZ
elif menu == "Tasks (Quiz)":
    st.header("Select a Topic")

    name = st.text_input("Enter your name")
    topic = st.selectbox("Choose a topic", list(questions.keys()))

    if name and topic:
        score = 0
        total = min(5, len(questions[topic]))

        for i in range(total):
            q, options, correct = questions[topic][i]
            answer = st.radio(q, options, key=f"{topic}_{i}")

            if answer == options[correct]:
                score += 1

        if st.button("Submit Quiz"):
            percentage = (score / total) * 100

            new_data = {
                "Name": name,
                "Topic": topic,
                "Score": score,
                "Total Questions": total,
                "Percentage": percentage,
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M")
            }

            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            df.to_csv(CSV_FILE, index=False)

            st.success(f"You scored {score}/{total} ({percentage:.0f}%)")

#RESULTS DASHBOARD
elif menu == "Results Dashboard":
    st.header("Quiz Results & Progress")

    if df.empty:
        st.info("No quiz data available yet.")
    else:
        st.subheader("Completed Tasks")
        st.dataframe(df)

        st.subheader("Average Score per Topic")
        progress = df.groupby("Topic")["Percentage"].mean()
        st.bar_chart(progress)

        st.subheader("🏆 Overall Average Performance")
        st.metric("Overall Average (%)", round(df["Percentage"].mean(), 1))

