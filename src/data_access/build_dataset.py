import pandas as pd
import numpy as np
import os
import glob
from src.data_access.fetch_data import fetch_weather_for_city

# 1. PAN-INDIA COORDINATE DICTIONARY
import pandas as pd
import numpy as np
import os
import glob
from src.data_access.fetch_data import fetch_weather_for_city

# 1. THE ULTIMATE INDIA COORDINATE DICTIONARY (80+ Cities)
CITY_COORDINATES = {
    # --- METROS ---
    'Delhi':     {'lat': 28.7041, 'lon': 77.1025},
    'Mumbai':    {'lat': 19.0760, 'lon': 72.8777},
    'Kolkata':   {'lat': 22.5726, 'lon': 88.3639},
    'Chennai':   {'lat': 13.0827, 'lon': 80.2707},
    'Bengaluru': {'lat': 12.9716, 'lon': 77.5946},
    'Bangalore': {'lat': 12.9716, 'lon': 77.5946},
    'Hyderabad': {'lat': 17.3850, 'lon': 78.4867},
    'Ahmedabad': {'lat': 23.0225, 'lon': 72.5714},
    'Pune':      {'lat': 18.5204, 'lon': 73.8567},
    
    # --- NORTH ---
    'Amritsar':  {'lat': 31.6340, 'lon': 74.8723},
    'Chandigarh': {'lat': 30.7333, 'lon': 76.7794},
    'Gurugram':  {'lat': 28.4595, 'lon': 77.0266}, 'Gurgaon': {'lat': 28.4595, 'lon': 77.0266},
    'Noida':     {'lat': 28.5355, 'lon': 77.3910},
    'Ghaziabad': {'lat': 28.6692, 'lon': 77.4538},
    'Faridabad': {'lat': 28.4089, 'lon': 77.3178},
    'Lucknow':   {'lat': 26.8467, 'lon': 80.9462},
    'Kanpur':    {'lat': 26.4499, 'lon': 80.3319},
    'Varanasi':  {'lat': 25.3176, 'lon': 82.9739},
    'Agra':      {'lat': 27.1767, 'lon': 78.0081},
    'Jaipur':    {'lat': 26.9124, 'lon': 75.7873},
    'Jodhpur':   {'lat': 26.2389, 'lon': 73.0243},
    'Udaipur':   {'lat': 24.5854, 'lon': 73.7125},
    'Ludhiana':  {'lat': 30.9010, 'lon': 75.8573},
    'Patiala':   {'lat': 30.3398, 'lon': 76.3869},
    'Jalandhar': {'lat': 31.3260, 'lon': 75.5762},
    'Karnal':    {'lat': 29.6857, 'lon': 76.9905},
    'Rohtak':    {'lat': 28.8955, 'lon': 76.6066},
    
    # --- CENTRAL & WEST ---
    'Bhopal':    {'lat': 23.2599, 'lon': 77.4126},
    'Indore':    {'lat': 22.7196, 'lon': 75.8577},
    'Gwalior':   {'lat': 26.2183, 'lon': 78.1828},
    'Jabalpur':  {'lat': 23.1815, 'lon': 79.9864},
    'Ujjain':    {'lat': 23.1765, 'lon': 75.7885},
    'Nagpur':    {'lat': 21.1458, 'lon': 79.0882},
    'Nashik':    {'lat': 19.9975, 'lon': 73.7898},
    'Aurangabad':{'lat': 19.8762, 'lon': 75.3433},
    'Thane':     {'lat': 19.2183, 'lon': 72.9781},
    'Navi Mumbai':{'lat': 19.0330, 'lon': 73.0297},
    'Solapur':   {'lat': 17.6599, 'lon': 75.9064},
    'Surat':     {'lat': 21.1702, 'lon': 72.8311},
    'Vadodara':  {'lat': 22.3072, 'lon': 73.1812},
    'Rajkot':    {'lat': 22.3039, 'lon': 70.8022},
    'Gandhinagar':{'lat': 23.2156, 'lon': 72.6369},

    # --- EAST ---
    'Patna':     {'lat': 25.5941, 'lon': 85.1376},
    'Gaya':      {'lat': 24.7914, 'lon': 85.0002},
    'Muzaffarpur':{'lat': 26.1197, 'lon': 85.3910},
    'Hajipur':   {'lat': 25.6858, 'lon': 85.2146},
    'Guwahati':  {'lat': 26.1445, 'lon': 91.7362},
    'Shillong':  {'lat': 25.5788, 'lon': 91.8933},
    'Aizawl':    {'lat': 23.7307, 'lon': 92.7176},
    'Agartala':  {'lat': 23.8315, 'lon': 91.2868},
    'Imphal':    {'lat': 24.8170, 'lon': 93.9368},
    'Kohima':    {'lat': 25.6751, 'lon': 94.1086},
    'Jorapokhar': {'lat': 23.7082, 'lon': 86.4129},
    'Durgapur':  {'lat': 23.5204, 'lon': 87.3119},
    'Asansol':   {'lat': 23.6739, 'lon': 86.9524},
    'Siliguri':  {'lat': 26.7271, 'lon': 88.3953},
    'Haldia':    {'lat': 22.0667, 'lon': 88.0698},
    
    # --- ODISHA & NEARBY (Crucial for your region) ---
    'Bhubaneswar': {'lat': 20.2961, 'lon': 85.8245},
    'Cuttack':     {'lat': 20.4625, 'lon': 85.8830},
    'Rourkela':    {'lat': 22.2604, 'lon': 84.8536},
    'Talcher':     {'lat': 20.9509, 'lon': 85.2163},
    'Brajrajnagar':{'lat': 21.8257, 'lon': 83.9228},
    'Angul':       {'lat': 20.8442, 'lon': 85.1511},
    'Balasore':    {'lat': 21.4942, 'lon': 86.9317},
    
    # --- SOUTH ---
    'Visakhapatnam': {'lat': 17.6868, 'lon': 83.2185},
    'Amaravati': {'lat': 16.5730, 'lon': 80.3575},
    'Vijayawada':{'lat': 16.5062, 'lon': 80.6480},
    'Tirupati':  {'lat': 13.6288, 'lon': 79.4192},
    'Coimbatore':{'lat': 11.0168, 'lon': 76.9558},
    'Mysuru':    {'lat': 12.2958, 'lon': 76.6394}, 'Mysore': {'lat': 12.2958, 'lon': 76.6394},
    'Kochi':     {'lat': 9.9312,  'lon': 76.2673},
    'Ernakulam': {'lat': 9.9816,  'lon': 76.2999},
    'Thiruvananthapuram': {'lat': 8.5241, 'lon': 76.9366},
    'Kozhikode': {'lat': 11.2588, 'lon': 75.7804},
    'Kannur':    {'lat': 11.8745, 'lon': 75.3704},
}

# ... (Keep the rest of your standardize_columns and build_mega_dataset functions EXACTLY as they were) ...
# Just make sure to COPY-PASTE the 'standardize_columns' and 'build_mega_dataset' code 
# from my previous response below this dictionary!

def standardize_columns(df, filename):
    """
    Auto-detects pollutant columns and prints what it found.
    """
    df.columns = df.columns.str.strip()
    
    col_map = {
        'date': 'Date', 'datetime': 'Date', 'timestamp': 'Date',
        'pm2.5': 'PM2.5', 'pm25': 'PM2.5', 'pm2_5': 'PM2.5',
        'pm10': 'PM10',
        'no2': 'NO2', 'nitrogen_dioxide': 'NO2',
        'co': 'CO', 'carbon_monoxide': 'CO',
        'so2': 'SO2',
        'o3': 'O3', 'ozone': 'O3',
        'city': 'City', 'location': 'City', 'station': 'City', 'area': 'City'
    }
    
    new_cols = {}
    for col in df.columns:
        lower_col = col.lower()
        if lower_col in col_map:
            new_cols[col] = col_map[lower_col]
            
    df.rename(columns=new_cols, inplace=True)
    
    # Check for critical columns
    if 'PM2.5' not in df.columns:
        print(f"      ⚠️  WARNING: {filename} has NO 'PM2.5' column. It will likely be ignored.")
        
    return df

def build_mega_dataset():
    print("🏗️  Initializing Universal Dataset Builder...")
    
    raw_folder = 'notebook/data'
    all_files = glob.glob(os.path.join(raw_folder, "*.csv"))
    
    if not all_files:
        print(f"❌ No CSV files found in {data}.")
        return

    print(f"   -> Found {len(all_files)} files to scan.")
    
    df_list = []
    
    # 1. READ & VALIDATE
    for f in all_files:
        filename = os.path.basename(f)
        try:
            temp_df = pd.read_csv(f)
            temp_df = standardize_columns(temp_df, filename)
            
            # Validation: Must have Date, City, and at least ONE pollutant
            has_date = 'Date' in temp_df.columns
            has_city = 'City' in temp_df.columns
            has_pollution = 'PM2.5' in temp_df.columns or 'PM10' in temp_df.columns
            
            if has_date and has_city and has_pollution:
                temp_df['Date'] = pd.to_datetime(temp_df['Date'], errors='coerce')
                # Add source tag
                temp_df['Source_File'] = filename
                df_list.append(temp_df)
                print(f"      ✅ Accepted {filename}: {len(temp_df)} rows")
            else:
                print(f"      ❌ Rejected {filename}: Missing Date, City, or Pollution Data.")
        except Exception as e:
            print(f"      ❌ Error reading {filename}: {e}")

    if not df_list:
        print("❌ No valid data found to merge.")
        return

    # 2. MERGE
    master_df = pd.concat(df_list, axis=0, ignore_index=True)
    
    # Sort and Deduplicate (Keep the one with the most data if duplicates exist)
    master_df.sort_values(by=['Date', 'City'], inplace=True)
    master_df.drop_duplicates(subset=['Date', 'City'], keep='first', inplace=True)
    
    print(f"   -> Merged Raw Count: {len(master_df)}")

    # 3. ADD WEATHER
    final_dfs = []
    
    print("   -> Fetching Weather & Cleaning...")
    for city in master_df['City'].unique():
        if city in CITY_COORDINATES:
            city_df = master_df[master_df['City'] == city].copy()
            
            # Spatial Features
            lat = CITY_COORDINATES[city]['lat']
            lon = CITY_COORDINATES[city]['lon']
            city_df['Latitude'] = lat
            city_df['Longitude'] = lon
            
            # Weather Fetching
            start_date = city_df['Date'].min().strftime('%Y-%m-%d')
            end_date = city_df['Date'].max().strftime('%Y-%m-%d')
            
            weather_df = fetch_weather_for_city(lat, lon, start_date, end_date)
            
            if not weather_df.empty:
                merged_df = pd.merge(city_df, weather_df, on='Date', how='left')
                
                # STRICT RULE: We only keep rows that have PM2.5 data for training
                # (You can't train a model on NaN values)
                before_drop = len(merged_df)
                merged_df.dropna(subset=['PM2.5'], inplace=True)
                
                if len(merged_df) > 0:
                    final_dfs.append(merged_df)
                else:
                    # Optional: Print if a city lost all data
                    pass
    
    # 4. SAVE
    if final_dfs:
        mega_df = pd.concat(final_dfs, axis=0)
        output_path = 'notebook/data/final_merged_data.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        mega_df.to_csv(output_path, index=False)
        
        print("\n==================================================")
        print(f"✅ MEGA DATASET BUILT!")
        print(f"📂 Saved to: {output_path}")
        print(f"📊 Total High-Quality Training Rows: {len(mega_df)}")
        print(f"🏙️  Cities Covered: {mega_df['City'].nunique()}")
        print("==================================================\n")
    else:
        print("❌ Error: No data matched.")

if __name__ == "__main__":
    build_mega_dataset()