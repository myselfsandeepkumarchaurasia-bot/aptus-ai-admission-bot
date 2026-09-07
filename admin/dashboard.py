from pathlib import Path
import sqlite3

import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Aptus Academy | CRM Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# DATABASE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DB_NAME = BASE_DIR / "aptus_leads.db"


def get_connection():
    return sqlite3.connect(str(DB_NAME))


# ============================================================
# CREATE TABLES
# ============================================================

def create_tables():

    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            email TEXT,
            education TEXT,
            interested_course TEXT,
            career_goal TEXT,
            experience TEXT,
            counselling_required TEXT,
            created_at TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT,
            user_message TEXT,
            bot_response TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


create_tables()


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data(ttl=10)
def load_data():

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT
            id,
            name,
            phone,
            email,
            education,
            interested_course,
            career_goal,
            experience,
            counselling_required,
            created_at
        FROM leads
        ORDER BY id DESC
        """,
        conn
    )

    conn.close()

    return df


leads = load_data()


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #F4F7FB;
}

/* Page width */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #102E23,
        #12372A
    );
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* KPI containers */
[data-testid="stMetric"] {
    background: white;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0px 5px 18px rgba(0,0,0,0.08);
    border-left: 5px solid #2E8B68;
}

/* Metric label */
[data-testid="stMetricLabel"] {
    font-weight: 700;
}

/* Metric value */
[data-testid="stMetricValue"] {
    font-size: 30px;
    font-weight: 800;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 15px;
}

/* Buttons */
.stButton button,
.stDownloadButton button {
    border-radius: 10px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.title("🎓 Aptus Academy")

st.subheader(
    "AI Admission CRM • Lead Management • Counselling Analytics"
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🎓 Aptus Academy")

    st.subheader("Admin CRM")

    st.divider()

    st.markdown("### 📊 Dashboard")

    st.markdown("""
    **Features**

    👥 Lead Management

    📞 Counselling Requests

    📚 Course Analytics

    🎯 Career Goals

    📈 Admission Trends

    📥 Export Leads
    """)

    st.divider()

    st.caption("Database")

    st.code(
        str(DB_NAME),
        language="text"
    )

    st.divider()

    if st.button(
        "🔄 Refresh Dashboard",
        width="stretch"
    ):

        st.cache_data.clear()
        st.rerun()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_leads = len(leads)


if total_leads > 0:

    counselling_yes = (
        leads["counselling_required"]
        .astype(str)
        .str.strip()
        .str.lower()
        .eq("yes")
        .sum()
    )

    counselling_no = (
        leads["counselling_required"]
        .astype(str)
        .str.strip()
        .str.lower()
        .eq("no")
        .sum()
    )

    total_courses = (
        leads["interested_course"]
        .dropna()
        .nunique()
    )

    total_students = (
        leads["name"]
        .dropna()
        .nunique()
    )

else:

    counselling_yes = 0
    counselling_no = 0
    total_courses = 0
    total_students = 0


# ============================================================
# ADMISSION OVERVIEW
# ============================================================

st.header("📊 Admission Overview")


c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        label="👥 Total Leads",
        value=total_leads,
        help="Total admission enquiries"
    )


with c2:

    st.metric(
        label="📞 Counselling Requests",
        value=counselling_yes,
        help="Students requesting counselling"
    )


with c3:

    st.metric(
        label="📚 Courses",
        value=total_courses,
        help="Courses generating enquiries"
    )


with c4:

    st.metric(
        label="🎓 Unique Students",
        value=total_students,
        help="Distinct student enquiries"
    )


# ============================================================
# EMPTY DATABASE
# ============================================================

if leads.empty:

    st.divider()

    st.info(
        """
        📭 No counselling leads found.

        Open the main chatbot and submit
        **Request Counselling**.
        """
    )

    st.stop()


# ============================================================
# FILTERS
# ============================================================

st.divider()

st.header("🔎 Lead Filters")


f1, f2, f3, f4 = st.columns(4)


# Course
with f1:

    course_options = ["All"] + sorted(
        leads["interested_course"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_course = st.selectbox(
        "📚 Course",
        course_options
    )


# Experience
with f2:

    experience_options = ["All"] + sorted(
        leads["experience"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_experience = st.selectbox(
        "💼 Experience",
        experience_options
    )


# Counselling
with f3:

    selected_counselling = st.selectbox(
        "📞 Counselling",
        [
            "All",
            "Yes",
            "No"
        ]
    )


# Search
with f4:

    search = st.text_input(
        "🔍 Search",
        placeholder="Name / Phone / Email"
    )


# ============================================================
# APPLY FILTERS
# ============================================================

filtered = leads.copy()


if selected_course != "All":

    filtered = filtered[
        filtered["interested_course"]
        == selected_course
    ]


if selected_experience != "All":

    filtered = filtered[
        filtered["experience"]
        == selected_experience
    ]


if selected_counselling != "All":

    filtered = filtered[
        filtered["counselling_required"]
        .astype(str)
        .str.strip()
        .str.lower()
        == selected_counselling.lower()
    ]


if search:

    search_text = search.lower()

    mask = (
        filtered["name"]
        .astype(str)
        .str.lower()
        .str.contains(
            search_text,
            na=False
        )
        |
        filtered["phone"]
        .astype(str)
        .str.lower()
        .str.contains(
            search_text,
            na=False
        )
        |
        filtered["email"]
        .astype(str)
        .str.lower()
        .str.contains(
            search_text,
            na=False
        )
    )

    filtered = filtered[mask]


# ============================================================
# FILTER RESULT
# ============================================================

st.info(
    f"Showing **{len(filtered)}** of **{len(leads)}** leads"
)


# ============================================================
# CHART 1 + CHART 2
# ============================================================

st.divider()

chart1, chart2 = st.columns(2)


# ============================================================
# COURSE CHART
# ============================================================

with chart1:

    st.subheader("📚 Course-wise Leads")

    course_data = (
        filtered["interested_course"]
        .fillna("Not Provided")
        .value_counts()
        .reset_index()
    )

    course_data.columns = [
        "Course",
        "Leads"
    ]

    fig = px.bar(
        course_data,
        x="Course",
        y="Leads",
        text="Leads",
        title=""
    )

    fig.update_traces(
        marker_color="#2E8B68",
        textposition="outside"
    )

    fig.update_layout(
        height=380,
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis_title="",
        yaxis_title="Number of Leads",
        margin=dict(
            l=20,
            r=20,
            t=30,
            b=80
        )
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


# ============================================================
# COUNSELLING CHART
# ============================================================

with chart2:

    st.subheader("📞 Counselling Requests")

    counselling_data = pd.DataFrame({

        "Status": [
            "Counselling Required",
            "Not Required"
        ],

        "Leads": [

            filtered[
                "counselling_required"
            ]
            .astype(str)
            .str.lower()
            .eq("yes")
            .sum(),

            filtered[
                "counselling_required"
            ]
            .astype(str)
            .str.lower()
            .eq("no")
            .sum()
        ]
    })

    fig = px.pie(
        counselling_data,
        names="Status",
        values="Leads",
        hole=0.55
    )

    fig.update_traces(
        textinfo="label+percent"
    )

    fig.update_layout(
        height=380,
        paper_bgcolor="white",
        margin=dict(
            l=20,
            r=20,
            t=30,
            b=30
        )
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


# ============================================================
# CHART 3 + CHART 4
# ============================================================

st.divider()

chart3, chart4 = st.columns(2)


# ============================================================
# EXPERIENCE CHART
# ============================================================

with chart3:

    st.subheader("💼 Experience Distribution")

    experience_data = (
        filtered["experience"]
        .fillna("Not Provided")
        .value_counts()
        .reset_index()
    )

    experience_data.columns = [
        "Experience",
        "Leads"
    ]

    fig = px.bar(
        experience_data,
        x="Leads",
        y="Experience",
        orientation="h",
        text="Leads"
    )

    fig.update_traces(
        marker_color="#42B883",
        textposition="outside"
    )

    fig.update_layout(
        height=350,
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis_title="Leads",
        yaxis_title="",
        margin=dict(
            l=20,
            r=40,
            t=30,
            b=30
        )
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


# ============================================================
# EDUCATION CHART
# ============================================================

with chart4:

    st.subheader("🎓 Education Distribution")

    education_data = (
        filtered["education"]
        .replace("", "Not Provided")
        .fillna("Not Provided")
        .value_counts()
        .head(10)
        .reset_index()
    )

    education_data.columns = [
        "Education",
        "Leads"
    ]

    fig = px.pie(
        education_data,
        names="Education",
        values="Leads",
        hole=0.45
    )

    fig.update_traces(
        textinfo="label+percent"
    )

    fig.update_layout(
        height=350,
        paper_bgcolor="white",
        margin=dict(
            l=20,
            r=20,
            t=30,
            b=30
        )
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


# ============================================================
# LEAD TREND
# ============================================================

st.divider()

st.header("📈 Lead Generation Trend")


trend = filtered.copy()

trend["created_at"] = pd.to_datetime(
    trend["created_at"],
    errors="coerce"
)

trend["date"] = trend["created_at"].dt.date


daily = (
    trend
    .dropna(subset=["date"])
    .groupby("date")
    .size()
    .reset_index(
        name="Leads"
    )
)


if not daily.empty:

    fig = px.line(
        daily,
        x="date",
        y="Leads",
        markers=True
    )

    fig.update_traces(
        line_color="#1F6F54",
        line_width=3,
        marker_size=8
    )

    fig.update_layout(
        height=350,
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis_title="Date",
        yaxis_title="Leads",
        margin=dict(
            l=20,
            r=20,
            t=30,
            b=40
        )
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

else:

    st.info("No valid date information available.")


# ============================================================
# LEAD TABLE
# ============================================================

st.divider()

st.header("👥 Student Leads")


st.write(
    f"Showing **{len(filtered)}** of **{len(leads)}** leads"
)


display_df = filtered.copy()


display_df = display_df.rename(
    columns={

        "id": "ID",

        "name": "Name",

        "phone": "Phone",

        "email": "Email",

        "education": "Education",

        "interested_course":
            "Interested Course",

        "career_goal":
            "Career Goal",

        "experience":
            "Experience",

        "counselling_required":
            "Counselling",

        "created_at":
            "Created At"
    }
)


st.dataframe(
    display_df,
    width="stretch",
    hide_index=True
)


# ============================================================
# CSV DOWNLOAD
# ============================================================

st.divider()

csv_data = filtered.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="📥 Download Leads CSV",

    data=csv_data,

    file_name="aptus_academy_leads.csv",

    mime="text/csv",

    width="stretch"
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🎓 Aptus Academy • AI Admission CRM • Lead Management • Counselling Analytics"
)