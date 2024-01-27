import pandas as pd
import matplotlib.pyplot as plt

# Your CSV data
csv_data = "JDB_DF_Data_File.csv"
# ... (paste your CSV data here)

# Create a DataFrame from the CSV data
# df = pd.read_csv(pd.compat.StringIO(csv_data))
df = pd.read_csv(csv_data)

# Group by job title and count the number of occurrences for each
job_titles_count = df['job_title'].value_counts()

# Display the top 10 job titles and the number of occurrences for each
top_10_job_titles = job_titles_count.head(10)
print(top_10_job_titles)

job_company_count = df['job_company_name'].value_counts()

# Display the top 10 job titles and the number of occurrences for each
top_10_job_company = job_company_count.head(10)
print(top_10_job_company)

df['job_date_posted'] = pd.to_datetime(df['job_date_posted'], errors='coerce')

# Group by week and count the number of job postings per week
jobs_per_week = df.groupby(df['job_date_posted'].dt.week)['job_id'].count()

# Display the report
print("Report of Number of Jobs Posted Per Week:")
print(jobs_per_week)

# Convert 'job_date_posted' column to datetime format
df['job_date_posted'] = pd.to_datetime(df['job_date_posted'], errors='coerce')

# Extract week and year from the 'job_date_posted' column
df['week'] = df['job_date_posted'].dt.strftime('%Y-%U')

# Group by week and count the number of job postings per week
jobs_per_week = df.groupby(df['week']).size()

# Plot the timeline
plt.figure(figsize=(15, 6))
plt.plot(jobs_per_week.index, jobs_per_week.values, marker='o', linestyle='-', color='b')
plt.title('Number of Jobs Posted Per Week')
plt.xlabel('Week')
plt.ylabel('Number of Jobs Posted')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()