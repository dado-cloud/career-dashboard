# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------------------------------
# Page config
# -------------------------------------------------------
st.set_page_config(
    page_title="Graduate Career Outcomes Dashboard",
    layout="wide"
)

st.title("Graduate Career Outcomes Dashboard")
st.markdown(
    "Interactive visualizations based on the student career outcomes dataset."
)

# -------------------------------------------------------
# Load data
# -------------------------------------------------------
@st.cache_data
def load_data():
    # Make sure the file name matches your CSV
    return pd.read_csv("DS4.3_CE_Student_Career_Outcome.csv")

df = load_data()

st.sidebar.header("Filters")

# Filter by major (Field_of_Study)
field_options = sorted(df["Field_of_Study"].dropna().unique())
selected_fields = st.sidebar.multiselect(
    "Field of Study",
    options=field_options,
    default=field_options
)

# Filter by GPA range
gpa_min = float(df["University_GPA"].min())
gpa_max = float(df["University_GPA"].max())
gpa_range = st.sidebar.slider(
    "University GPA range",
    min_value=gpa_min,
    max_value=gpa_max,
    value=(gpa_min, gpa_max)
)

# Apply filters
filtered = df[
    df["Field_of_Study"].isin(selected_fields)
    & df["University_GPA"].between(gpa_range[0], gpa_range[1])
]

st.markdown("### Overview statistics")
st.dataframe(filtered.describe(include="all"))

# -------------------------------------------------------
# Helper plotting functions (taken from your notebook)
# -------------------------------------------------------

def plot_gpa_hist(data):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(data["University_GPA"], bins=10, edgecolor="black")
    ax.set_title("Histogram of University GPA")
    ax.set_xlabel("University_GPA")
    ax.set_ylabel("Frequency")
    fig.tight_layout()
    return fig


def plot_salary_by_field(data):
    avg_salary_by_field = (
        data.groupby("Field_of_Study")["Starting_Salary"]
        .mean()
        .sort_values(ascending=False)
    )
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(avg_salary_by_field.index, avg_salary_by_field.values)
    ax.set_title("Average Starting Salary by Field of Study")
    ax.set_xlabel("Field_of_Study")
    ax.set_ylabel("Average Starting Salary")
    ax.tick_params(axis="x", rotation=45, labelsize=8)
    fig.tight_layout()
    return fig


def plot_salary_by_promotion_years(data):
    avg_salary_by_years = (
        data.groupby("Years_to_Promotion")["Starting_Salary"]
        .mean()
        .sort_index()
    )
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(avg_salary_by_years.index, avg_salary_by_years.values, marker="o")
    ax.set_title("Average Starting Salary by Years to Promotion")
    ax.set_xlabel("Years to Promotion")
    ax.set_ylabel("Average Starting Salary")
    fig.tight_layout()
    return fig


def plot_job_offers_by_networking(data):
    avg_offers_by_network = (
        data.groupby("Networking_Score")["Job_Offers"]
        .mean()
        .sort_index()
    )
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(avg_offers_by_network.index, avg_offers_by_network.values, marker="o")
    ax.set_title("Average Job Offers by Networking Score")
    ax.set_xlabel("Networking_Score")
    ax.set_ylabel("Average Job Offers")
    fig.tight_layout()
    return fig


def plot_gpa_vs_promotion(data):
    fig, ax = plt.subplots(figsize=(6, 4))
    scatter = ax.scatter(
        data["Years_to_Promotion"],
        data["University_GPA"],
        c="tab:blue",
        alpha=0.7
    )
    ax.set_title("Do Higher GPAs Lead to Faster Promotions?")
    ax.set_xlabel("Years to Promotion")
    ax.set_ylabel("University GPA")
    fig.tight_layout()
    return fig


def plot_satisfaction_by_gender(data):
    fig, ax = plt.subplots(figsize=(6, 4))
    genders = data["Gender"].dropna().unique()
    satisfaction_data = [data[data["Gender"] == g]["Career_Satisfaction"]
                         for g in genders]
    ax.violinplot(satisfaction_data, showmeans=True)
    ax.set_xticks(range(1, len(genders) + 1))
    ax.set_xticklabels(genders)
    ax.set_title("How Does Career Satisfaction Differ by Gender?")
    ax.set_xlabel("Gender")
    ax.set_ylabel("Career Satisfaction")
    fig.tight_layout()
    return fig


def plot_worklife_by_field(data):
    fig, ax = plt.subplots(figsize=(8, 4))
    # Boxplot of WorkLifeBalance by Field_of_Study
    fields = data["Field_of_Study"].dropna().unique()
    wlb_data = [data[data["Field_of_Study"] == f]["WorkLifeBalance_Score"]
                for f in fields]
    ax.boxplot(wlb_data, labels=fields)
    ax.set_title("Which Majors Achieve Better Work-Life Balance?")
    ax.set_xlabel("Field of Study")
    ax.set_ylabel("Work-Life Balance Score")
    ax.tick_params(axis="x", rotation=45, labelsize=8)
    fig.tight_layout()
    return fig


def plot_joblevel_pie(data):
    # You used a pie chart of job levels in the notebook
    job_counts = data["Current_Job_Level"].value_counts()
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(job_counts.values, labels=job_counts.index, autopct="%1.1f%%")
    ax.set_title("Distribution of Job Levels Among Graduates")
    fig.tight_layout()
    return fig


def plot_offers_vs_certifications(data):
    avg_offers = (
        data.groupby("Certifications")["Job_Offers"]
        .mean()
        .sort_index()
    )
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(avg_offers.index, avg_offers.values, marker="o")
    ax.set_title("Job Offers vs Certifications")
    ax.set_xlabel("Certifications")
    ax.set_ylabel("Average Job Offers")
    fig.tight_layout()
    return fig


def plot_satisfaction_heatmap(data):
    # Average Career Satisfaction by Major (Field_of_Study)
    avg_sat = (
        data.groupby("Field_of_Study")["Career_Satisfaction"]
        .mean()
        .sort_values(ascending=True)
    )
    fig, ax = plt.subplots(figsize=(6, 4))
    # Simple heatmap using imshow on a column vector
    cax = ax.imshow(avg_sat.values.reshape(-1, 1), aspect="auto")
    ax.set_yticks(range(len(avg_sat.index)))
    ax.set_yticklabels(avg_sat.index)
    ax.set_xticks([0])
    ax.set_xticklabels(["Career Satisfaction"])
    ax.set_title("Average Career Satisfaction by Major")
    fig.colorbar(cax, ax=ax)
    fig.tight_layout()
    return fig

# -------------------------------------------------------
# Layout – put the charts on the page
# (Choose any 5–7 for your assignment)
# -------------------------------------------------------

st.markdown("### 1. Student Performance & Outcomes")

col1, col2 = st.columns(2)
with col1:
    st.pyplot(plot_gpa_hist(filtered))
    st.caption("Distribution of students' university GPA.")
with col2:
    st.pyplot(plot_salary_by_field(filtered))
    st.caption("Average starting salary by field of study.")

st.markdown("### 2. Promotions, Networking and Offers")

col3, col4 = st.columns(2)
with col3:
    st.pyplot(plot_salary_by_promotion_years(filtered))
    st.caption("How starting salary changes with years to first promotion.")
with col4:
    st.pyplot(plot_job_offers_by_networking(filtered))
    st.caption("Average job offers for each networking score.")

st.markdown("### 3. GPA, Satisfaction and Work–Life Balance")

col5, col6 = st.columns(2)
with col5:
    st.pyplot(plot_gpa_vs_promotion(filtered))
    st.caption("Relationship between GPA and time to promotion.")
with col6:
    st.pyplot(plot_satisfaction_by_gender(filtered))
    st.caption("Career satisfaction distribution by gender.")

st.markdown("### 4. Job Levels and Overall Satisfaction")

col7, col8 = st.columns(2)
with col7:
    st.pyplot(plot_worklife_by_field(filtered))
    st.caption("Which majors report better work–life balance.")
with col8:
    st.pyplot(plot_joblevel_pie(filtered))
    st.caption("Proportion of graduates at each job level.")

st.markdown("### 5. Extra: Offers vs Certifications and Satisfaction by Major")

col9, col10 = st.columns(2)
with col9:
    st.pyplot(plot_offers_vs_certifications(filtered))
    st.caption("Average job offers by number of certifications.")
with col10:
    st.pyplot(plot_satisfaction_heatmap(filtered))
    st.caption("Average career satisfaction across majors.")

st.markdown(
    """
**Story Summary:**
- GPA and networking both relate to faster promotions and more job offers.
- Some majors clearly lead to higher starting salaries and better work–life balance.
- Job levels and satisfaction vary across fields and genders, highlighting where support or guidance may be needed.
"""
)
