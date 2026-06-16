
# Graduate Career Outcomes Dashboard

**Exploring the Relationship Between Education and Career Success**

This project was created for **DS 413: Data Exploration and Visualization**.  
It focuses on **SDG 4: Quality Education** and explores how educational factors may influence career success.

## Project Overview

This project analyzes the relationship between education and early career outcomes using an interactive Streamlit dashboard.

The dashboard helps users explore how factors such as:

- University GPA
- Field of study
- Starting salary
- Networking score
- Job offers
- Certifications
- Years to promotion
- Career satisfaction
- Work-life balance
- Current job level

are connected to graduate career success.

The goal of this project is to turn the dataset into clear visual insights that can be understood by students, educators, HR professionals, and policymakers.

## Dataset

The dataset used in this project is:

```text
Education and Career Success from Kaggle
````

The dataset contains student academic and career outcome information.
According to the project report, the dataset includes **400 complete records** and **19 columns**.

The dataset was taken from Kaggle:

```text
Education and Career Success
https://www.kaggle.com/datasets/adilshamim8/education-and-career-success
```

## Project Files

```text
career-dashboard/
│
├── app.py
├── education_career_success.csv
└── README.md
```

## Dashboard Features

The Streamlit dashboard includes:

* Interactive field-of-study filter
* Interactive GPA range filter
* Overview statistics table
* Histogram of University GPA
* Bar chart of average starting salary by field of study
* Line chart of average starting salary by years to promotion
* Line chart of job offers by networking score
* Scatter plot of GPA vs. years to promotion
* Violin plot of career satisfaction by gender
* Box plot of career satisfaction by field of study
* Pie chart of current job levels
* Line chart of job offers vs. certifications
* Heatmap of average career satisfaction by major

## Dashboard Link

The interactive dashboard can be accessed here:

```text
https://career-dashboard-f9b5c4itybqbdn9nja7gyh.streamlit.app/
```

## How to Use the Dashboard

1. Open the Streamlit dashboard.
2. Use the sidebar to filter by field of study.
3. Adjust the GPA range slider.
4. Review the overview statistics.
5. Explore the charts to understand how academic and career factors relate to graduate success.

## Main Insights

The dashboard supports the following insights:

* Most students have strong academic performance, with many GPAs between 3.3 and 3.8.
* Students from fields such as Computer Science, Medicine, and Engineering tend to have higher starting salaries.
* Higher networking scores are associated with more job offers.
* Higher GPA may be related to faster promotion.
* Career satisfaction and work-life balance vary across majors.
* Certifications may help improve job opportunities.
* Job level distribution helps show how graduates progress in their careers.

## Visualization Story

The dashboard is organized as a visual story. It begins with general academic performance, then moves into career outcomes such as salary, job offers, promotions, satisfaction, and job levels.

This structure helps users understand how students move from academic life into career paths and how education-related factors can shape professional success.


## Author
Daad Alhassan

## References

1. A. Shamim, "Education and Career Success," Kaggle.
2. GeeksforGeeks, "Types of Data Visualization Charts: From Basic to Advanced."
3. S. Few, *Show Me the Numbers: Designing Tables and Graphs to Enlighten*, Analytics Press, 2012.


