import pandas as pd

# Load datasets
adagok_df = pd.read_csv("Adagok.csv", delimiter=";")
hutopanelek_df = pd.read_csv("Hutopanelek.csv", delimiter=";")

adagok_df = adagok_df.dropna()

# Convert dates and times in Adagok.csv
adagok_df['Kezdet'] = pd.to_datetime(adagok_df['Kezdet_DÁTUM'] + ' ' + adagok_df['Kezdet_IDŐ'], format='%Y.%m.%d %H:%M:%S')
adagok_df['Vége'] = pd.to_datetime(adagok_df['Vége_DÁTUM'] + ' ' + adagok_df['Vége_IDŐ'], format='%Y.%m.%d %H:%M:%S')



# Convert Hutopanelek date-time columns to datetime
time_cols = [col for col in hutopanelek_df.columns if "Time" in col]
for col in time_cols:
    hutopanelek_df[col] = pd.to_datetime(hutopanelek_df[col], format='%Y.%m.%d %H:%M:%S')

# pd.set_option('display.max_columns', None)
# print("Adagok describe")
# print(adagok_df.describe())
# print("Huto describe")
# print(hutopanelek_df.describe(include='all'))

adagok_df['Kezdet'] = pd.to_datetime(adagok_df['Kezdet_DÁTUM'] + ' ' + adagok_df['Kezdet_IDŐ'])
adagok_df['Vége'] = pd.to_datetime(adagok_df['Vége_DÁTUM'] + ' ' + adagok_df['Vége_IDŐ'])

# Calculate the time difference in minutes
adagok_df['Calculated_Adagido'] = (adagok_df['Vége'] - adagok_df['Kezdet']).dt.total_seconds() / 60

# Check if the calculated difference matches the Adagido column
adagok_df['Match'] = adagok_df['Calculated_Adagido'] == adagok_df['ADAGIDŐ']

# Display the result
print(adagok_df[['Kezdet', 'Vége', 'ADAGIDŐ', 'Calculated_Adagido', 'Match']])

# missing_data = hutopanelek_df.isnull()  # Returns a DataFrame of True/False for each cell
# missing_counts = hutopanelek_df.isnull().sum()
# print("Missing values per column:\n", missing_counts)

# # Define a function to get temperature stats within each interval
# def get_temp_stats(start_time, end_time, hutopanelek_df):
#     stats = {}
#     for i in range(1, 16):
#         if i == 7:  # Skip Panel 7 as per the data provided (missing)
#             continue
#         panel_time_col = f'Panel hőfok {i} [°C] Time'
#         panel_value_col = f'Panel hőfok {i} [°C] ValueY'
        
#         # Filter data within the interval
#         interval_data = hutopanelek_df[(hutopanelek_df[panel_time_col] >= start_time) &
#                                        (hutopanelek_df[panel_time_col] <= end_time)][panel_value_col]
        
#         # Calculate stats if there is data in the interval
#         if not interval_data.empty:
#             stats[f'Panel {i} Avg Temp'] = interval_data.mean()
#             stats[f'Panel {i} Min Temp'] = interval_data.min()
#             stats[f'Panel {i} Max Temp'] = interval_data.max()
#         else:
#             stats[f'Panel {i} Avg Temp'] = None
#             stats[f'Panel {i} Min Temp'] = None
#             stats[f'Panel {i} Max Temp'] = None
#     return stats

# # Apply function for each interval in Adagok.csv
# results = []
# for index, row in adagok_df.iterrows():
#     start_time = row['Kezdet']
#     end_time = row['Vége']
    
#     # Get temperature stats
#     temp_stats = get_temp_stats(start_time, end_time, hutopanelek_df)
#     temp_stats['ADAGSZÁM'] = row['ADAGSZÁM']
#     temp_stats['Interval Start'] = start_time
#     temp_stats['Interval End'] = end_time
#     results.append(temp_stats)

# # Create a DataFrame with the results
# results_df = pd.DataFrame(results)

# # Save to a new CSV file for review
# results_df.to_csv("Temperature_Statistics_by_Adagok_Interval.csv", index=False)

# print("Temperature statistics by interval have been saved to 'Temperature_Statistics_by_Adagok_Interval.csv'.")
