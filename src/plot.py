import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load JSON data
with open('hd_strings.json', 'r') as file:
    data = json.load(file)

# Prepare data for plotting
records = []
totalNumber = 0
for entry in data:
    year = entry['year']
    sex = entry['sex']
    for key, value in entry['values'].items():
        totalNumber += value
        records.append({'year': year, 'sex': sex, 'hd-classification': key, 'value': value})

# Create a DataFrame
df = pd.DataFrame(records)
print("total number")
print(totalNumber)
# Pivot the DataFrame for plotting and flatten the columns
pivot_df = df.pivot_table(index='year', columns=['sex', 'hd-classification'], values='value', aggfunc='sum', fill_value=0)
pivot_df.columns = ['{} - {}'.format(sex, hd_class) for sex, hd_class in pivot_df.columns]  # Flatten multi-level columns

# Plotting with wider bars and patterns
fig, ax = plt.subplots(figsize=(15, 6))  # Wider figure

# Colors and patterns for accessibility
colors = ["#000000", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00"] # Colorblind-friendly colors

# Bar width and x position calculation
bar_width = 0.9 / len(pivot_df.columns)  # Adjust width based on number of categories
x = np.arange(len(pivot_df))  # x positions for each year

# Plot each category with unique color
for i, (col_name, col_data) in enumerate(pivot_df.items()):
    bars = ax.bar(
        x + i * bar_width - (bar_width * (len(pivot_df.columns) - 1) / 2),  # Center each group
        col_data,
        width=bar_width,
        color=colors[i % len(colors)],
        label=col_name,
    )

# Adding a vertical line after the last category of each year
for i, year in enumerate(pivot_df.index):
    last_column_position = x[i] + (len(pivot_df.columns) * bar_width) / 2  # Position after last column
    ax.vlines(last_column_position, ymin=0, ymax=df['value'].max(), color='grey', linestyle='--', alpha=0.7)

# Adding labels and legend
ax.set_title('Values by Year, Sex, and HD-Classification')
ax.set_xlabel('Year')
ax.set_ylabel('Values')
ax.set_xticks(x)
ax.set_xticklabels(pivot_df.index, rotation=45)
ax.legend(title='Sex & HD-classification', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

plt.show()
