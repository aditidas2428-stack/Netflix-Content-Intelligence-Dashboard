# 🎬 Netflix Content Sales & Customer Segmentation Dashboard

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.22+-FF4B4B.svg)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-F7931E.svg)

An end-to-end data science portfolio project transforming static Netflix metadata into a dynamic, simulated B2B business analytics environment.

## 📌 Project Overview
This project takes the public Kaggle Netflix Titles dataset and engineers a realistic business scenario. By simulating business metrics (Annual Revenue, Contract Value, Customer Count), we apply **Machine Learning (K-Means Clustering)** to identify high-value customer segments and visualize the insights in an interactive **Streamlit** dashboard.

## 🏗️ Project Architecture
1. **Data Prep (`src/data_prep.py`)**: Data cleaning, datetime formatting, and business logic simulation.
2. **Modeling (`src/model.py`)**: Feature scaling and K-Means segmentation (Premium, Growth, Standard, Low Value).
3. **Dashboard (`app.py`)**: Interactive Plotly/Streamlit UI for executive-level data exploration.

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone <your-repo-link>
   cd netflix-sales-dashboard