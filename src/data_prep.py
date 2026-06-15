import pandas as pd
import numpy as np
import os

def load_data(filepath):
    """Loads the raw dataset."""
    print(f"Loading data from {filepath}...")
    return pd.read_csv(filepath)

def clean_and_engineer_features(df):
    """Handles missing values and creates new temporal/categorical features."""
    print("Cleaning data and engineering features...")
    
    # Fill missing values
    df['director'] = df['director'].fillna('Unknown')
    df['cast'] = df['cast'].fillna('Unknown')
    df['country'] = df['country'].fillna('United States')
    df.dropna(subset=['date_added', 'rating'], inplace=True)
    
    # Date processing
    df['date_added'] = pd.to_datetime(df['date_added'].str.strip())
    df['added_year'] = df['date_added'].dt.year
    
    # Feature extraction
    df['release_decade'] = (df['release_year'] // 10) * 10
    df['content_age'] = 2024 - df['release_year']
    df['primary_genre'] = df['listed_in'].apply(lambda x: x.split(',')[0])
    df['country_count'] = df['country'].apply(lambda x: len(str(x).split(',')))
    
    return df

def simulate_business_metrics(df):
    """Simulates revenue, contract value, customer count, and engagement."""
    print("Simulating business sales data...")
    np.random.seed(42) # For reproducibility
    
    def calculate_metrics(row):
        base_revenue = 50000 if row['type'] == 'Movie' else 100000
        age_modifier = max(0.5, (50 - row['content_age']) / 50)
        
        annual_revenue = int(base_revenue * age_modifier * np.random.uniform(0.8, 1.5))
        contract_value = int(annual_revenue * np.random.uniform(1.2, 3.0))
        customer_count = int(np.random.normal(5000, 1500) * age_modifier)
        engagement_score = min(100, max(1, int(np.random.normal(70, 15))))
        
        return pd.Series([annual_revenue, contract_value, max(100, customer_count), engagement_score])

    df[['annual_revenue', 'contract_value', 'customer_count', 'engagement_score']] = df.apply(calculate_metrics, axis=1)
    
    # Assign random market regions for segmentation analysis
    regions = ['North America', 'Europe', 'Asia', 'Latin America', 'Oceania']
    df['market_region'] = np.random.choice(regions, size=len(df))
    
    return df

if __name__ == "__main__":
    # Ensure processed directory exists
    os.makedirs('data/processed', exist_ok=True)
    
    # Execute Pipeline
    raw_df = load_data('data/raw/netflix_titles.csv')
    cleaned_df = clean_and_engineer_features(raw_df)
    business_df = simulate_business_metrics(cleaned_df)
    
    # Save processed data
    output_path = 'data/processed/netflix_business_simulated.csv'
    business_df.to_csv(output_path, index=False)
    print(f"Data preparation complete. Saved to {output_path}")