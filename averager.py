# import pandas as pd

# # Assuming your data is in a CSV file named 'Manager-data 23-02-24.csv'
# # Adjust the file name and column names accordingly

# file_path = 'Manager-data 23-02-24.csv'
# df = pd.read_csv(file_path)

# # Convert 'Delay_Assigned' column to numeric
# df['Delay_Assigned'] = pd.to_numeric(df['Delay_Assigned'], errors='coerce')

# # Num_Leads
# num_leads = len(df)

# # Percentage_Assigned
# percentage_assigned = (df['Is_Assigned'].sum() / num_leads) * 100

# # Average_Delay_Assigned
# average_delay_assigned = df['Delay_Assigned'].sum() / num_leads

# # People_Assigned
# people_assigned = df.groupby('Person_Assigned')['Is_Assigned'].sum().sort_values(ascending=False)

# # Average_Communication
# average_communication = df.groupby('Person_Assigned')['Num_Actions'].sum() / df.groupby('Person_Assigned')['Is_Assigned'].count()

# # Percentage_Texted
# percentage_texted = df['Is_Texted'].sum() / df['Is_Texted'].count() * 100

# # Percentage_Appointment
# percentage_appointment = df['Is_Appointment'].sum() / num_leads * 100

# # Percentage_Sold
# percentage_sold = df['Is_Sold'].sum() / num_leads * 100

# # Average Percentage_Appointment
# average_percentage_appointment = df.groupby('Person_Assigned')['Is_Appointment'].mean() * 100

# # Average Percentage_Texted
# average_percentage_texted = df.groupby('Person_Assigned')['Is_Texted'].mean() * 100

# # Average Average_Communication
# average_average_communication = df.groupby('Person_Assigned')['Num_Actions'].mean()

# # Average Average_Delay_Assigned
# average_average_delay_assigned = df.groupby('Person_Assigned')['Delay_Assigned'].mean()

# # Create a DataFrame with the results
# results_df = pd.DataFrame({
#     'Person_Assigned': people_assigned.index,
#     'Num_Assigned': people_assigned.values,
#     'Num_Appointments': df.groupby('Person_Assigned')['Is_Appointment'].sum().values,
#     'Average_Percentage_Appointment': average_percentage_appointment.values,
#     'Average_Percentage_Texted': average_percentage_texted.values,
#     'Average_Average_Communication': average_average_communication.values,
#     'Average_Average_Delay_Assigned': average_average_delay_assigned.values
# })

# # Print or store the results as needed
# print(f"Num_Leads: {num_leads}")
# print(f"Percentage_Assigned: {percentage_assigned:.2f}%")
# print(f"Average_Delay_Assigned: {average_delay_assigned:.2f}")
# print("\nPeople_Assigned:")
# print(people_assigned)
# print("\nAverage_Communication:")
# print(average_communication)
# print(f"Percentage_Texted: {percentage_texted:.2f}%")
# print(f"Percentage_Appointment: {percentage_appointment:.2f}%")
# print(f"Percentage_Sold: {percentage_sold:.2f}%")

# # Merge the original data with the calculated metrics
# merged_df = pd.merge(df, results_df, on='Person_Assigned', how='left')

# # Export the merged DataFrame to a new CSV file
# results_df.round(2).to_csv('salesperson_insights_with_data.csv', index=False)
# # List of numbers


import pandas as pd

# Assuming your data is in a CSV file named 'Manager-data 23-02-24.csv'
# Adjust the file name and column names accordingly

file_path = 'Manager-data 23-02-24.csv'
df = pd.read_csv(file_path)

# Convert 'Delay_Assigned' column to numeric
df['Delay_Assigned'] = pd.to_numeric(df['Delay_Assigned'], errors='coerce')

# Num_Leads
num_leads = len(df)

# Percentage_Assigned
percentage_assigned = (df['Is_Assigned'].sum() / num_leads) * 100

# Average_Delay_Assigned
average_delay_assigned = df['Delay_Assigned'].sum() / num_leads

# People_Assigned
people_assigned = df.groupby('Person_Assigned')['Is_Assigned'].sum().sort_values(ascending=False)

# Average_Communication
average_communication = df.groupby('Person_Assigned')['Num_Actions'].sum() / df.groupby('Person_Assigned')['Is_Assigned'].count()

# Percentage_Texted
percentage_texted = df['Is_Texted'].sum() / df['Is_Texted'].count() * 100

# Percentage_Appointment
percentage_appointment = df['Is_Appointment'].sum() / num_leads * 100

# Percentage_Sold
percentage_sold = df['Is_Sold'].sum() / num_leads * 100

# Average Percentage_Appointment
average_percentage_appointment = df.groupby('Person_Assigned')['Is_Appointment'].mean() * 100

# Average Percentage_Texted
average_percentage_texted = df.groupby('Person_Assigned')['Is_Texted'].mean() * 100

# Average Average_Communication
average_average_communication = df.groupby('Person_Assigned')['Num_Actions'].mean()

# Average Average_Delay_Assigned
average_average_delay_assigned = df.groupby('Person_Assigned')['Delay_Assigned'].mean()

# Create a DataFrame with the results
results_df = pd.DataFrame({
    'Person_Assigned': people_assigned.index,
    'Num_Assigned': people_assigned.values,
    'Num_Appointments': df.groupby('Person_Assigned')['Is_Appointment'].sum().values,
    'Percentage_Appointment': average_percentage_appointment.values,
    'Percentage_Texted': average_percentage_texted.values,
    'Average_Communication': average_average_communication.values,
    'Average_Delay_Assigned': average_average_delay_assigned.values
})

# # Include additional columns for each salesperson
# for person in results_df['Person_Assigned']:
#     person_data = df[df['Person_Assigned'] == person][['Time_Assigned', 'Delay_Assigned', 'Num_Actions', 'Is_Assigned', 'Is_Texted', 'Is_Appointment', 'Is_Sold']]
#     results_df.loc[results_df['Person_Assigned'] == person, person_data.columns] = person_data.values

# Print or store the results as needed
print(f"Num_Leads: {num_leads}")
print(f"Percentage_Assigned: {percentage_assigned:.2f}%")
print(f"Average_Delay_Assigned: {average_delay_assigned:.2f}")
print("\nPeople_Assigned:")
print(people_assigned)
print("\nAverage_Communication:")
print(average_communication)
print(f"Percentage_Texted: {percentage_texted:.2f}%")
print(f"Percentage_Appointment: {percentage_appointment:.2f}%")
print(f"Percentage_Sold: {percentage_sold:.2f}%")


summary_df = pd.DataFrame({
    'Metric': ['Num_Leads', 'Percentage_Assigned', 'Average_Delay_Assigned', 'People_Assigned', 'Average_Communication', 'Percentage_Texted', 'Percentage_Appointment', 'Percentage_Sold'],
    'Value': [num_leads, percentage_assigned, average_delay_assigned, str(people_assigned), str(average_communication), percentage_texted, percentage_appointment, percentage_sold]
})

# Print or store the summary results as needed
print(summary_df)

# Save the summary DataFrame to a new CSV file
summary_df.to_csv('sales_summary.csv', index=False)
# Merge the original data with the calculated metrics
# merged_df = pd.merge(df, results_df, on='Person_Assigned', how='left')

# Export the merged DataFrame to a new CSV file
results_df.round(2).to_csv('salesperson_insights_with_data.csv', index=False)