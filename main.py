import pandas as pd
import sqlite3

connection = sqlite3.connect("adatb.db")

### Adatfájl struktúra megállapítás
# Adatok betoltese
adagok_df = pd.read_csv("Adagok.csv", delimiter=";")
hutopanelek_df = pd.read_csv("Hutopanelek.csv", delimiter=";")

# Az Adagok.csv-ben csak 32 értékes sor van, a többit mely NULL értékeket tartalmaz eldobjuk.
adagok_df.dropna(inplace=True)

# Datum+ido oszopok konvertalasa datetime formatumra
adagok_df['Kezdet'] = pd.to_datetime(adagok_df['Kezdet_DÁTUM'] + ' ' + adagok_df['Kezdet_IDŐ'], format='%Y.%m.%d %H:%M:%S')
adagok_df['Vége'] = pd.to_datetime(adagok_df['Vége_DÁTUM'] + ' ' + adagok_df['Vége_IDŐ'], format='%Y.%m.%d %H:%M:%S')

adagok_df['Kezdet'] = pd.to_datetime(adagok_df['Kezdet_DÁTUM'] + ' ' + adagok_df['Kezdet_IDŐ'])
adagok_df['Vége'] = pd.to_datetime(adagok_df['Vége_DÁTUM'] + ' ' + adagok_df['Vége_IDŐ'])

# Hutopanelek Time oszlopok datatime formatumra alakitasa
time_cols = [col for col in hutopanelek_df.columns if "Time" in col]
for col in time_cols:
    hutopanelek_df[col] = pd.to_datetime(hutopanelek_df[col], format='%Y.%m.%d %H:%M:%S')

#Adattisztitas

# Hianyzo adatok keresese
missing_data = hutopanelek_df.isnull()
missing_counts = hutopanelek_df.isnull().sum()
print("Missing values per column:\n", missing_counts)

# Kalulalat adagido szamitasa
adagok_df['Calculated_Adagido'] = (adagok_df['Vége'] - adagok_df['Kezdet']).dt.total_seconds() / 60

# Ellenorizzuk, hogy a kalkulalt adagido egyezik-e az elore meghatarozottal
# Match oszlopot toltjuk fel
adagok_df['Match'] = adagok_df['Calculated_Adagido'] == adagok_df['ADAGIDŐ']

# Adagok tabla megjelenitese
print(adagok_df[['Kezdet', 'Vége', 'ADAGIDŐ', 'Calculated_Adagido', 'Match']])

# Statisztikák - NaN statisztikák a hőmérséklet értékekre
pd.set_option('display.max_columns', None)
print("Adagok describe")
print(adagok_df.describe())
print("Huto describe")
print(hutopanelek_df.describe(include='all'))

# Listazzuk meyik a mert ertek oszlop
value_columns = [col for col in hutopanelek_df.columns if 'ValueY' in col]

# Vesszo pontra cserelese a lebegopontos ertekekben
for col in value_columns:
    hutopanelek_df[col] = hutopanelek_df[col].astype(str).str.replace(',', '.').astype(float)

# Statisztikák - Most már vannak statisztikák a hőmérsékle értékekre
pd.set_option('display.max_columns', None)
print("Adagok describe")
print(adagok_df.describe())
print("Huto describe")
print(hutopanelek_df.describe(include='all'))

# Adagkozi_ido kiszamitasa es hozzaadasa
adagok_df['Adagkozi_ido'] = adagok_df['Kezdet'].diff().shift(-1).dt.total_seconds() / 60  # Convert to minutes

# az utolso meres utan nincs meres, igy ahogy NaN ertek van, oda 0-t irunk
adagok_df['Adagkozi_ido'].fillna(0, inplace=True)

print(adagok_df[['ADAGKÖZI_IDŐ','Adagkozi_ido']])

###ER diagram elkeszitese

#Adagszam hozzarendelese minden hutopanel mereshez
hutopanelek_df['ADAGSZÁM'] = None
for i, row in adagok_df.iterrows():
    adagszam = row['ADAGSZÁM']
    start_time = row['Kezdet']
    end_time = row['Vége']
    
    hutopanelek_df.loc[
        (hutopanelek_df['Panel hőfok 1 [°C] Time'] >= start_time) & 
        (hutopanelek_df['Panel hőfok 1 [°C] Time'] <= end_time), 
        'ADAGSZÁM'
    ] = adagszam

# Ellenorzes
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

# Hutopanelek szetmontasa szenzorokra es dedikalt tablakba helyezese
panel_dataframes = {}
for i, time_col in enumerate(time_cols):
    value_col = time_col.replace("Time", "ValueY")
    panel_df = hutopanelek_df[[time_col, value_col, 'ADAGSZÁM']].copy()
    panel_df.columns = ['time', 'value', 'adagszam']
    panel_dataframes[f"panel{i+1}"] = panel_df
for panel_name, df in panel_dataframes.items():
    df.to_sql(panel_name, connection, if_exists='replace', index=False)

# Gyors ellenorzes
cur.execute("SELECT * from panel1 limit 1;")
print(cur.fetchall())
cur.execute("SELECT sql from sqlite_schema where name = 'panel1'")
print(cur.fetchall())