import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

# Load dataset
df = pd.read_csv("travel_data.csv")

# Fix incorrect headers if needed
if "State" not in df.columns:
    df = pd.read_csv("travel_data.csv", skiprows=1)

# Mapping dictionaries
category_mapping = {
    "Mountain": 0, "Sea": 1, "Historical": 2, "Holy": 3, "Adventure": 4,
    "Cultural": 5, "Natural": 6, "Desert": 7
}

geo_mapping = {
    "Mountainous": 0, "Desert": 1, "Coastal": 2, "Plains": 3, "Riverine": 4,
    "Lake": 5, "Forest": 6, "Wetland": 7, "Valley": 8, "Waterfalls": 9, "Plateau": 10
}

# Apply mappings
df["Category"] = df["Category"].str.strip().map(category_mapping)
df["Geo_Type"] = df["Geo_Type"].str.strip().map(geo_mapping)

# Clean and convert climate
df["Climate"] = df["Climate"].astype(str).str.replace("°C", "", regex=True).str.strip()
df["Climate"] = pd.to_numeric(df["Climate"], errors='coerce')

# Ensure features are numeric
features = ["Price", "Rating", "Popularity", "Climate"]
df[features] = df[features].apply(pd.to_numeric, errors='coerce')

# Drop rows with missing values in those features
df = df.dropna(subset=features)

# Normalize features
scaler = MinMaxScaler()
df_scaled = scaler.fit_transform(df[features])

# KMeans clustering
kmeans = KMeans(n_clusters=5, random_state=42, n_init="auto")
df["cluster"] = kmeans.fit_predict(df_scaled)

# Recommendation by state and rating
def recommend_places_by_state_rating(user_state, min_rating):
    user_state = user_state.strip().title()
    min_rating = float(min_rating)
    
    filtered_df = df[(df["State"].str.title() == user_state) & (df["Rating"] >= min_rating)]

    if filtered_df.empty:
        print(f"\n❌ No matches found for state '{user_state}' with a rating of {min_rating} or higher. Try a different search!")
        return
    
    print(f"\n🌍 Recommended places in {user_state} with rating {min_rating} or higher:")
    for _, row in filtered_df.iterrows():
        print(f"\n📍 {row['Destination']}")
        print(f"   - Description: {row.get('Description', 'N/A')}")
        print(f"   - Offbeat Places: {row.get('Offbeat_place', 'N/A')}")
        print(f"   - Local Food: {row.get('Local_Food', 'N/A')}")
        print(f"   - 🖼️ Picture Place: {row.get('picture_place', 'N/A')}")
        print(f"   - 🍲 Food Image 1: {row.get('picture_food', 'N/A')}")
        print(f"   - 🍲 Food Image 2: {row.get('picture_food1', 'N/A')}")
        print(f"   - 🌄 Offbeat Image 1: {row.get('picture_offbit', 'N/A')}")
        print(f"   - 🌄 Offbeat Image 2: {row.get('picture_offbit1', 'N/A')}")

# Recommendation by category and geo type
def recommend_places_by_category_geo(user_category, user_geo_type):
    user_category_num = category_mapping.get(user_category.strip().title())
    user_geo_type_num = geo_mapping.get(user_geo_type.strip().title())
    
    if user_category_num is None or user_geo_type_num is None:
        print("\n❌ Invalid category or geo-type selection. Try again!")
        return
    
    filtered_df = df[(df["Category"] == user_category_num) & (df["Geo_Type"] == user_geo_type_num)]

    if filtered_df.empty:
        print(f"\n❌ No matches found for category '{user_category}' in geo-type '{user_geo_type}'. Try a different search!")
        return
    
    print(f"\n🌍 Recommended places ({user_category} in {user_geo_type} areas):")
    for _, row in filtered_df.iterrows():
        print(f"\n📍 {row['Destination']}")
        print(f"   - Description: {row.get('Description', 'N/A')}")
        print(f"   - Offbeat Places: {row.get('Offbeat_place', 'N/A')}")
        print(f"   - Local Food: {row.get('Local_Food', 'N/A')}")
        print(f"   - 🖼️ Picture Place: {row.get('picture_place', 'N/A')}")
        print(f"   - 🍲 Food Image 1: {row.get('picture_food', 'N/A')}")
        print(f"   - 🍲 Food Image 2: {row.get('picture_food1', 'N/A')}")
        print(f"   - 🌄 Offbeat Image 1: {row.get('picture_offbit', 'N/A')}")
        print(f"   - 🌄 Offbeat Image 2: {row.get('picture_offbit1', 'N/A')}")

# --- CLI ---
print("🏞️ Welcome to AI Travel Planner 🏝️")
print("\nSearch by:")
print("1️⃣ State & Rating")
print("2️⃣ Category & Geo-Type")

choice = input("\nEnter 1 or 2: ").strip()

if choice == "1":
    state_input = input("\nEnter the state you want to visit: ").strip()
    rating_input = input("\nEnter minimum rating (e.g., 4.0): ").strip()
    recommend_places_by_state_rating(state_input, rating_input)
elif choice == "2":
    category_input = input("\nEnter the category (e.g., Adventure, Cultural): ").strip()
    geo_input = input("\nEnter the geo-type (e.g., Mountainous, Coastal): ").strip()
    recommend_places_by_category_geo(category_input, geo_input)
else:
    print("\n❌ Invalid choice! Please restart and enter 1 or 2.")
