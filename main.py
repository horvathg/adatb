import pandas as pd
import sqlite3

connection = sqlite3.connect("adatb.db")

### Adatfájl struktúra megállapítás
# Adatok betoltese
adagok_df = pd.read_csv("Adagok.csv", delimiter=";")
hutopanelek_df = pd.read_csv("Hutopanelek.csv", delimiter=";")

# Az Adagok.csv-ben csak 32 értékes sor van, a többit mely NULL értékeket tartalmaz eldobjuk.
adagok_df.dropna(inplace=True)

# Convert dates and times in Adagok.csv
adagok_df['Kezdet'] = pd.to_datetime(adagok_df['Kezdet_DÁTUM'] + ' ' + adagok_df['Kezdet_IDŐ'], format='%Y.%m.%d %H:%M:%S')
adagok_df['Vége'] = pd.to_datetime(adagok_df['Vége_DÁTUM'] + ' ' + adagok_df['Vége_IDŐ'], format='%Y.%m.%d %H:%M:%S')

adagok_df['Kezdet'] = pd.to_datetime(adagok_df['Kezdet_DÁTUM'] + ' ' + adagok_df['Kezdet_IDŐ'])
adagok_df['Vége'] = pd.to_datetime(adagok_df['Vége_DÁTUM'] + ' ' + adagok_df['Vége_IDŐ'])

# Hutopanelek Time oszlopok datatime formatumra alakitasa
time_cols = [col for col in hutopanelek_df.columns if "Time" in col]
for col in time_cols:
    hutopanelek_df[col] = pd.to_datetime(hutopanelek_df[col], format='%Y.%m.%d %H:%M:%S')

#Adattisztitas

missing_data = hutopanelek_df.isnull()  # Returns a DataFrame of True/False for each cell
missing_counts = hutopanelek_df.isnull().sum()
print("Missing values per column:\n", missing_counts)

# Calculate the time difference in minutes
adagok_df['Calculated_Adagido'] = (adagok_df['Vége'] - adagok_df['Kezdet']).dt.total_seconds() / 60

# Check if the calculated difference matches the Adagido column
adagok_df['Match'] = adagok_df['Calculated_Adagido'] == adagok_df['ADAGIDŐ']

# Display the result
print(adagok_df[['Kezdet', 'Vége', 'ADAGIDŐ', 'Calculated_Adagido', 'Match']])

# Statisztikák - NaN statisztikák a hőmérséklet értékekre
pd.set_option('display.max_columns', None)
print("Adagok describe")
print(adagok_df.describe())
print("Huto describe")
print(hutopanelek_df.describe(include='all'))

# List of value columns to check and convert to float
value_columns = [col for col in hutopanelek_df.columns if 'ValueY' in col]

# Replace commas with dots and convert to float
for col in value_columns:
    hutopanelek_df[col] = hutopanelek_df[col].astype(str).str.replace(',', '.').astype(float)

# Statisztikák - Most már vannak statisztikák a hőmérsékle értékekre
pd.set_option('display.max_columns', None)
print("Adagok describe")
print(adagok_df.describe())
print("Huto describe")
print(hutopanelek_df.describe(include='all'))

# Adagkozi_ido kiszamitasa es hozzaadasa
# Calculate Adagkozi_ido as the difference between the start of the current and the end of the previous dosage
adagok_df['Adagkozi_ido'] = adagok_df['Kezdet'].diff().shift(-1).dt.total_seconds() / 60  # Convert to minutes

# Fill the first row Adagkozi_ido with zero or NaN if desired
adagok_df['Adagkozi_ido'].fillna(0, inplace=True)

print(adagok_df[['ADAGKÖZI_IDŐ','Adagkozi_ido']])

###ER diagram elkeszitese

#Adagszam hozzarendelese minden hutopanel mereshez
hutopanelek_df['ADAGSZÁM'] = None
# Match each time in hutopanelek with the corresponding ADAGSZÁM in adagok
for i, row in adagok_df.iterrows():
    adagszam = row['ADAGSZÁM']
    start_time = row['Kezdet']
    end_time = row['Vége']
    
    # Assign ADAGSZÁM to rows in hutopanelek_df where Time is within the range
    hutopanelek_df.loc[
        (hutopanelek_df['Panel hőfok 1 [°C] Time'] >= start_time) & 
        (hutopanelek_df['Panel hőfok 1 [°C] Time'] <= end_time), 
        'ADAGSZÁM'
    ] = adagszam

# Verify results
print(hutopanelek_df[['Panel hőfok 1 [°C] Time', 'ADAGSZÁM']].head())

# Mivel nem biztos, hogy konzistens adatok vannak egy meresen belul,
# megvizsgaljuk, hogy ugyanazok az ido kertekek szerepelnek egy soron belul
consistent_rows = hutopanelek_df[time_cols].nunique(axis=1) == 1
inconsistent_rows = hutopanelek_df[~consistent_rows]
print("Inconsistent rows:")
print(inconsistent_rows)

print("-------------------------------------------------")
adagok_df.drop(columns=['Kezdet_DÁTUM','Kezdet_IDŐ','Vége_DÁTUM', 'Vége_IDŐ','ADAGKÖZI_IDŐ', 'Calculated_Adagido','Match'], inplace=True)
adagok_df = adagok_df.astype({'ADAGSZÁM': int})

## Betoltes adatbazisba
cur = connection.cursor()
cur.execute('DROP TABLE IF EXISTS adagok;')

adagok_df.to_sql(name='adagok', con=connection, index=False)

cur.execute('SELECT * from adagok limit 1;')
print(cur.fetchall())

panel_dataframes = {}
for i, time_col in enumerate(time_cols):
    # Extract Value column corresponding to this Time column
    value_col = time_col.replace("Time", "ValueY")

    # Select only Time and Value columns for each panel
    panel_df = hutopanelek_df[[time_col, value_col, 'ADAGSZÁM']].copy()

    # Rename columns to 'time' and 'value' for uniformity
    panel_df.columns = ['time', 'value', 'adagszam']

    # Store in dictionary with a key like 'panel1', 'panel2', etc.
    panel_dataframes[f"panel{i+1}"] = panel_df

for panel_name, df in panel_dataframes.items():
    df.to_sql(panel_name, connection, if_exists='replace', index=False)

cur.execute("SELECT * from panel1 limit 1;")
print(cur.fetchall())
cur.execute("SELECT sql from sqlite_schema where name = 'panel1'")
print(cur.fetchall())