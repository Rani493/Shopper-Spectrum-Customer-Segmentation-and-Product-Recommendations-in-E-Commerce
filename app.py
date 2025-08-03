import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from datetime import timedelta


# Function to load and preprocess data
@st.cache_resource
def load_data():
    try:
        df = pd.read_csv('online_retail.csv', encoding='latin1')
        df.dropna(subset=['CustomerID'], inplace=True)
        df = df[~df['InvoiceNo'].astype(str).str.contains('C', na=False)]
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
        df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
        return df
    except FileNotFoundError:
        st.error("Error: online_retail.csv not found.")
        return None


# Load the data
df = load_data()

if df is not None:
    # --- Clustering Model Setup ---
    # Calculate RFM values for the clustering model
    reference_date = df['InvoiceDate'].max() + timedelta(days=1)
    rfm_df = df.groupby('CustomerID').agg(
        Recency=('InvoiceDate', lambda x: (reference_date - x.max()).days),
        Frequency=('InvoiceNo', lambda x: x.nunique()),
        Monetary=('TotalPrice', 'sum')
    ).reset_index()

    # Standardize the RFM values
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm_df[['Recency', 'Frequency', 'Monetary']])

    # Fit the K-Means model (using k=4 as determined previously)
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    kmeans.fit(rfm_scaled)

    # --- Recommendation System Setup ---
    # Create the user-item matrix for collaborative filtering
    user_item_matrix = df.pivot_table(index='CustomerID', columns='StockCode', values='Quantity', aggfunc='sum').fillna(
        0)

    # Calculate item-to-item similarity for product recommendations
    # This is more efficient for product-based queries than user-based similarity
    item_similarity = cosine_similarity(user_item_matrix.T)
    item_similarity_df = pd.DataFrame(item_similarity, index=user_item_matrix.columns, columns=user_item_matrix.columns)

    # Get a list of all unique product descriptions for the dropdown
    products = df[['StockCode', 'Description']].drop_duplicates().sort_values('Description')
    product_dict = pd.Series(products.StockCode.values, index=products.Description).to_dict()

    # --- Streamlit UI Layout ---
    st.title("🛍️ Shopper Spectrum: E-Commerce Analytics")
    st.write("---")

    # --- Product Recommendation Section ---
    st.header("🛒 Product Recommendation")
    st.write("Select a product to get 5 similar product recommendations.")

    # Get a list of descriptions for the user dropdown
    product_descriptions = list(product_dict.keys())
    selected_product_description = st.selectbox(
        'Choose a product:',
        options=product_descriptions
    )

    if selected_product_description:
        selected_stock_code = product_dict[selected_product_description]
        st.write(f"You selected: **{selected_product_description}**")

        # Get similar items from the item-similarity matrix
        similar_items = item_similarity_df[selected_stock_code].sort_values(ascending=False).iloc[1:6]

        st.subheader("Recommended Products:")
        if similar_items.empty:
            st.warning("Could not find similar products.")
        else:
            # Map stock codes back to descriptions
            recommended_descriptions = [
                products[products['StockCode'] == stock_code]['Description'].iloc[0]
                for stock_code in similar_items.index
            ]
            for desc in recommended_descriptions:
                st.write(f"- {desc}")

    st.write("---")

    # --- Customer Segmentation Section ---
    st.header("🧑‍🤝‍🧑 Customer Segmentation")
    st.write("Enter a customer's RFM values to predict their cluster.")

    # Create input fields for Recency, Frequency, and Monetary values
    with st.form("rfm_form"):
        recency = st.number_input('Recency (Days since last purchase)', min_value=0, value=50)
        frequency = st.number_input('Frequency (Number of purchases)', min_value=0, value=5)
        monetary = st.number_input('Monetary ($ spent)', min_value=0.0, value=500.0)

        submitted = st.form_submit_button("Predict Cluster")

    if submitted:
        # Scale the new RFM values using the same scaler
        new_customer_data = pd.DataFrame([[recency, frequency, monetary]],
                                         columns=['Recency', 'Frequency', 'Monetary'])
        new_customer_scaled = scaler.transform(new_customer_data)

        # Predict the cluster using the trained K-Means model
        predicted_cluster = kmeans.predict(new_customer_scaled)[0]

        st.subheader("Prediction:")
        st.success(f"This customer belongs to **Cluster {predicted_cluster}**.")
        st.info("You can use the mean RFM values from the notebook to understand this cluster's profile.")