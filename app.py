import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="Netflix B2B Analytics", page_icon="🎬", layout="wide")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    try:
        return pd.read_csv('data/processed/netflix_segmented.csv')
    except FileNotFoundError:
        st.error("Data file not found. Please run src/data_prep.py and src/model.py first.")
        st.stop()

df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg", width=150)
st.sidebar.header("Dashboard Filters")

selected_type = st.sidebar.multiselect("Content Type", df['type'].unique(), default=df['type'].unique())

# Year slider
min_year, max_year = int(df['added_year'].min()), int(df['added_year'].max())
selected_years = st.sidebar.slider("Year Added to Netflix", min_year, max_year, (min_year, max_year))

# Apply filters
filtered_df = df[
    (df['type'].isin(selected_type)) & 
    (df['added_year'].between(selected_years[0], selected_years[1]))
]

# --- MAIN LAYOUT ---
st.title("🎬 Netflix Content Intelligence Dashboard")
st.markdown("Explore Netflix content trends, catalog composition, and regional distribution patterns.")
# KPI Cards
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Titles in Catalog", f"{len(filtered_df):,}")
kpi2.metric("Avg Content Age (Years)", f"{filtered_df['content_age'].mean():.1f}")
kpi3.metric("Top Country by Volume", filtered_df['country'].str.split(',').str[0].str.strip().value_counts().index[0])
kpi4.metric("Movies to TV Show Ratio", f"{(filtered_df['type']=='Movie').sum() / max((filtered_df['type']=='TV Show').sum(), 1):.1f}x")

st.markdown("---")

# Visualizations Row 1
col1, col2 = st.columns(2)

with col1:
    st.subheader("Content Type Distribution")
    type_df = filtered_df['type'].value_counts().reset_index()
    type_df.columns = ['type', 'count']
    fig_pie = px.pie(type_df, names='type', values='count',
                 hole=0.4,
                 color='type',
                 color_discrete_map={"Movie": "#E50914", "TV Show": "#F5A623"})
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.subheader("Content by Country (Top 10)")
    country_df = filtered_df['country'].str.split(',').str[0].str.strip().value_counts().head(10).reset_index()
    country_df.columns = ['country', 'count']
    fig_bar = px.bar(country_df, x='count', y='country', orientation='h',
                 color='country',
                 color_discrete_sequence=px.colors.qualitative.Set2,
                 title="Top 10 Content Producing Countries")
    fig_bar.update_layout(showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

# Content Trend Over Time
st.markdown("### 📈 Content Added to Netflix Over Time")
trend_df = filtered_df.groupby(['added_year', 'type']).size().reset_index(name='count')
fig_trend = px.line(trend_df, x='added_year', y='count', color='type',
                    markers=True,
                    title="Movies vs TV Shows Added Per Year",
                    color_discrete_map={"Movie": "#E50914", "TV Show": "#F5A623"})
st.plotly_chart(fig_trend, use_container_width=True)

# Top Genres
st.markdown("### 🎭 Top 10 Content Genres")
genre_df = filtered_df['primary_genre'].value_counts().head(10).reset_index()
genre_df.columns = ['genre', 'count']
fig_genre = px.bar(genre_df, x='count', y='genre', orientation='h',
                   color='count', color_continuous_scale='Reds',
                   title="Most Common Genres on Netflix")
st.plotly_chart(fig_genre, use_container_width=True)

# Data Table
st.markdown("### 📄 Filtered Data View")
st.dataframe(filtered_df[['title', 'type', 'primary_genre', 'country', 'added_year', 'release_year']].head(50), use_container_width=True)