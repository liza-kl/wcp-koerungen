import json
import pandas as pd
import matplotlib.pyplot as plt

# Your JSON data
with open('hd_strings.json', 'r') as file:
    # Step 2: Load the contents into a Python object
    data = json.load(file)

# Step 3: Convert the Python object back to a JSON string
json_data= json.dumps(data)

# Load JSON data
data = json.loads(json_data)

# Prepare data for plotting
records = []
for entry in data:
    year = entry['year']
    sex = entry['sex']
    for key, value in entry['values'].items():
        records.append({'year': year, 'sex': sex, 'hd-classification': key, 'value': value})

# Create a DataFrame
df = pd.DataFrame(records)

# Pivot the DataFrame for plotting
pivot_df = df.pivot_table(index='year', columns=['sex', 'hd-classification'], values='value', aggfunc='sum', fill_value=0)

# Plotting
pivot_df.plot(kind='bar', figsize=(12, 6))
plt.title('Values by Year, Sex, and HD-Classification')
plt.xlabel('Year')
plt.ylabel('Values')
plt.xticks(rotation=45)
plt.legend(title='Sex & HD-classification', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()