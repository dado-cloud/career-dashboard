```python
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
    return pd.read_csv("education_career_success.csv")


df = load_data()

# -------------------------------------------------------
# Clean / prepare data
# -------------------------------------------------------
numeric_columns = [
    "University_GPA",
    "Starting_Salary",
    "Years_to_Promotion",
    "Networking_Score",
    "Job_Offers",
    "Career_Satisfaction",
    "Certifications"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# -------------------------------------------------------
# Sidebar filters
# -------------------------------------------------------
st.sidebar.header("Filters")

field_options = sorted(df["Field_of_Study"].dropna().unique())

selected_fields = st.sidebar.multiselect(
    "Field of Study",
    options=field_options,
    default=field_options
)

gpa_min = float(df["University_GPA"].min())
gpa_max = float(df["University_GPA"].max())

gpa_range = st.sidebar.slider(
    "University GPA range",
    min_value=gpa_min,
    max_value=gpa_max,
    value=(gpa_min, gpa_max)
)

# -------------------------------------------------------
# Apply filters
# -------------------------------------------------------
filtered = df[
    df["Field_of_Study"].isin(selected_fields)
    & df["University_GPA"].between(gpa_range[0], gpa_range[1])
]

if filtered.empty:
    st.warning("No data matches the selected filters. Please adjust the sidebar filters.")
    st.stop()

# -------------------------------------------------------
# Overview statistics
# -------------------------------------------------------
st.markdown("### Overview statistics")

# Convert to string to avoid Streamlit / Arrow mixed-type errors
overview = filtered.describe(include="all").fillna("").astype(str)
st.dataframe(overview)

# -------------------------------------------------------
# Helper function for empty charts
# -------------------------------------------------------
def no_data_figure(title="No data available"):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.text(
        0.5,
        0.5,
        "No data available for this chart",
        ha="center",
        va="center"
    )
    ax.set_title(title)
    ax.axis("off")
    fig.tight_layout()
    return fig

# -------------------------------------------------------
# Helper plotting functions
# -------------------------------------------------------
def plot_gpa_hist(data):
    chart_data = data["University_GPA"].dropna()

    if chart_data.empty:
        return no_data_figure("Histogram of University GPA")

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(chart_data, bins=10, edgecolor="black")
    ax.set_title("Histogram of University GPA")
    ax.set_xlabel("University GPA")
    ax.set_ylabel("Frequency")
    fig.tight_layout()
    return fig


def plot_salary_by_field(data):
    avg_salary_by_field = (
        data.dropna(subset=["Field_of_Study", "Starting_Salary"])
        .groupby("Field_of_Study")["Starting_Salary"]
        .mean()
        .sort_values(ascending=False)
    )

    if avg_salary_by_field.empty:
        return no_data_figure("Average Starting Salary by Field of Study")

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(avg_salary_by_field.index, avg_salary_by_field.values)
    ax.set_title("Average Starting Salary by Field of Study")
    ax.set_xlabel("Field of Study")
    ax.set_ylabel("Average Starting Salary")
    ax.tick_params(axis="x", rotation=45, labelsize=8)
    fig.tight_layout()
    return fig


def plot_salary_by_promotion_years(data):
    avg_salary_by_years = (
        data.dropna(subset=["Years_to_Promotion", "Starting_Salary"])
        .groupby("Years_to_Promotion")["Starting_Salary"]
        .mean()
        .sort_index()
    )

    if avg_salary_by_years.empty:
        return no_data_figure("Average Starting Salary by Years to Promotion")

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(avg_salary_by_years.index, avg_salary_by_years.values, marker="o")
    ax.set_title("Average Starting Salary by Years to Promotion")
    ax.set_xlabel("Years to Promotion")
    ax.set_ylabel("Average Starting Salary")
    fig.tight_layout()
    return fig


def plot_job_offers_by_networking(data):
    avg_offers_by_network = (
        data.dropna(subset=["Networking_Score", "Job_Offers"])
        .groupby("Networking_Score")["Job_Offers"]
        .mean()
        .sort_index()
    )

    if avg_offers_by_network.empty:
        return no_data_figure("Average Job Offers by Networking Score")

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(avg_offers_by_network.index, avg_offers_by_network.values, marker="o")
    ax.set_title("Average Job Offers by Networking Score")
    ax.set_xlabel("Networking Score")
    ax.set_ylabel("Average Job Offers")
    fig.tight_layout()
    return fig


def plot_gpa_vs_promotion(data):
    chart_data = data.dropna(subset=["Years_to_Promotion", "University_GPA"])

    if chart_data.empty:
        return no_data_figure("Do Higher GPAs Lead to Faster Promotions?")

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(
        chart_data["Years_to_Promotion"],
        chart_data["University_GPA"],
        alpha=0.7
    )
    ax.set_title("Do Higher GPAs Lead to Faster Promotions?")
    ax.set_xlabel("Years to Promotion")
    ax.set_ylabel("University GPA")
    fig.tight_layout()
    return fig


def plot_satisfaction_by_gender(data):
    chart_data = data.dropna(subset=["Gender", "Career_Satisfaction"])
    genders = chart_data["Gender"].unique()

    satisfaction_data = [
        chart_data[chart_data["Gender"] == g]["Career_Satisfaction"]
        for g in genders
    ]

    if len(satisfaction_data) == 0:
        return no_data_figure("How Does Career Satisfaction Differ by Gender?")

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.violinplot(satisfaction_data, showmeans=True)
    ax.set_xticks(range(1, len(genders) + 1))
    ax.set_xticklabels(genders)
    ax.set_title("How Does Career Satisfaction Differ by Gender?")
    ax.set_xlabel("Gender")
    ax.set_ylabel("Career Satisfaction")
    fig.tight_layout()
    return fig


def plot_worklife_by_field(data):
    chart_data = data.dropna(subset=["Field_of_Study", "Career_Satisfaction"])
    fields = chart_data["Field_of_Study"].unique()

    sat_data = [
        chart_data[chart_data["Field_of_Study"] == f]["Career_Satisfaction"]
        for f in fields
    ]

    if len(sat_data) == 0:
        return no_data_figure("Career Satisfaction by Field of Study")

    fig, ax = plt.subplots(figsize=(8, 4))

    # IMPORTANT FIX:
    # Newer Matplotlib uses tick_labels instead of labels
    ax.boxplot(sat_data, tick_labels=fields)

    ax.set_title("Career Satisfaction by Field of Study")
    ax.set_xlabel("Field of Study")
    ax.set_ylabel("Career Satisfaction")
    ax.tick_params(axis="x", rotation=45, labelsize=8)
    fig.tight_layout()
    return fig


def plot_joblevel_pie(data):
    job_counts = data["Current_Job_Level"].dropna().value_counts()

    if job_counts.empty:
        return no_data_figure("Distribution of Job Levels Among Graduates")

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(
        job_counts.values,
        labels=job_counts.index,
        autopct="%1.1f%%",
        startangle=90
    )
    ax.set_title("Distribution of Job Levels Among Graduates")
    fig.tight_layout()
    return fig


def plot_offers_vs_certifications(data):
    avg_offers = (
        data.dropna(subset=["Certifications", "Job_Offers"])
        .groupby("Certifications")["Job_Offers"]
        .mean()
        .sort_index()
    )

    if avg_offers.empty:
        return no_data_figure("Job Offers vs Certifications")

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(avg_offers.index, avg_offers.values, marker="o")
    ax.set_title("Job Offers vs Certifications")
    ax.set_xlabel("Certifications")
    ax.set_ylabel("Average Job Offers")
    fig.tight_layout()
    return fig


def plot_satisfaction_heatmap(data):
    avg_sat = (
        data.dropna(subset=["Field_of_Study", "Career_Satisfaction"])
        .groupby("Field_of_Study")["Career_Satisfaction"]
        .mean()
        .sort_values(ascending=True)
    )

    if avg_sat.empty:
        return no_data_figure("Average Career Satisfaction by Major")

    fig, ax = plt.subplots(figsize=(6, 4))
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
# Layout
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
    st.caption("Which fields report better career satisfaction.")

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
- Some majors clearly lead to higher starting salaries and better career satisfaction.
- Job levels and satisfaction vary across fields and genders, highlighting where support or guidance may be needed.
"""
)
```
