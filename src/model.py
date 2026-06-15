import pandas as pd
import os
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import joblib

def load_processed_data(filepath):
    print(f"Loading processed data from {filepath}...")
    return pd.read_csv(filepath)

def train_and_segment(df):
    """Trains K-Means model and segments the customer base."""
    print("Training K-Means clustering model...")
    
    # 1. Feature Selection
    features = ['engagement_score', 'customer_count', 'content_age', 'country_count']
    X = df[features]
    
    # 2. Scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 3. K-Means Modeling
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df['cluster'] = kmeans.fit_predict(X_scaled)
    
    # 4. Evaluation
    sil_score = silhouette_score(X_scaled, df['cluster'])
    print(f"Model Silhouette Score: {sil_score:.2f}")
    
    # 5. Dynamic Segment Labeling (Ordering by revenue)
    cluster_means = df.groupby('cluster')['annual_revenue'].mean().sort_values()
    segment_map = {
        cluster_means.index[3]: 'Premium Clients',
        cluster_means.index[2]: 'Growth Clients',
        cluster_means.index[1]: 'Standard Clients',
        cluster_means.index[0]: 'Low Value Clients'
    }
    df['segment'] = df['cluster'].map(segment_map)
    
    return df, kmeans, scaler

if __name__ == "__main__":
    # Ensure models directory exists
    os.makedirs('models', exist_ok=True)
    
    # Execute Pipeline
    df = load_processed_data('data/processed/netflix_business_simulated.csv')
    segmented_df, model, scaler = train_and_segment(df)
    
    # Save Models and Final Data
    joblib.dump(model, 'models/kmeans_model.pkl')
    joblib.dump(scaler, 'models/scaler.pkl')
    
    output_path = 'data/processed/netflix_segmented.csv'
    segmented_df.to_csv(output_path, index=False)
    
    print(f"Modeling complete. Final dataset saved to {output_path}")
    print("Models saved to 'models/' directory.")