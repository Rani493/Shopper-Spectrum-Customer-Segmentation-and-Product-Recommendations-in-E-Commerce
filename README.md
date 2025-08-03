The problem statement outlines a three-part project:

1.Exploratory Data Analysis (EDA): You'll begin by analyzing transaction data to understand customer purchasing patterns. This step is crucial for gaining insights into the dataset's characteristics, such as top-selling products, high-value customers, and seasonal trends.

Customer Segmentation with RFM Analysis: After the initial analysis, you will segment customers using the Recency, Frequency, and Monetary (RFM) model.

Recency: How recently a customer made a purchase.

Frequency: How often a customer makes a purchase.

Monetary: How much money a customer spends.
This segmentation will allow you to group customers into meaningful categories (e.g., "Loyal Customers," "New Customers," "At-Risk Customers") for targeted marketing and engagement strategies.

Product Recommendation System: Finally, you'll develop a collaborative filtering-based product recommendation system. Collaborative filtering works by finding patterns in user behavior and then recommending products to a user based on the preferences of other similar users. This system aims to improve the customer experience by suggesting products they are likely to be interested in, which can also increase sales.

Potential Challenges
Data Quality: E-commerce data can be messy and require significant cleaning and preprocessing to handle missing values, duplicate entries, and incorrect data types.

RFM Thresholds: Defining the right thresholds for recency, frequency, and monetary values to create meaningful segments can be subjective. You might need to experiment with different ranges to find the most effective segmentation for your business.

Scalability of Collaborative Filtering: As the number of customers and products grows, collaborative filtering algorithms can become computationally expensive. You may need to consider techniques like matrix factorization to handle large datasets efficiently.

Next step-
I've successfully segmented the customers using the RFM model. Here's a summary of the findings:

2.Data Preprocessing and Cleaning
Before the RFM analysis, I performed the following data cleaning steps on the online_retail.csv file:

Dropped 135,080 rows with missing CustomerID, as these are essential for customer-specific analysis.

Filtered out canceled orders, identified by an InvoiceNo starting with 'C', to ensure the analysis is based on genuine sales.

Converted InvoiceDate to a datetime format and created a TotalPrice column by multiplying Quantity and UnitPrice.

After cleaning, the dataset was reduced from 541,909 to 397,924 entries, resulting in a more reliable foundation for the analysis.

RFM Analysis and Customer Segmentation
Using the cleaned data, I calculated the Recency, Frequency, and Monetary values for each customer. These metrics were then used to create an RFM score and assign each customer to a specific segment.

Here are the segments and the number of customers in each:

Others: 1399

At Risk: 999

Champions: 961

Potential Loyalist: 542

Promising: 383

Loyal Customers: 37

New Customers: 18

The segmentation reveals a clear distribution of customer types, from "Champions" who are recent, frequent, and high-spending customers to "At Risk" customers who have not made a purchase recently and have lower frequency and monetary value.

The dataset containing the customer segments has been saved as rfm_customer_segments.csv for your reference.

The next step is to build the product recommendation system using collaborative filtering. This involves creating a user-item matrix and then applying an algorithm to find patterns and make recommendations.

Unsupervised Learning: Customer Clustering with K-Means
I've successfully performed K-Means clustering to segment customers based on their RFM values. Before clustering, I used the Elbow Method to identify the optimal number of clusters, which was determined to be 4.

The clusters were analyzed based on the average RFM values of their members, providing a clear profile for each segment:

Cluster 0 (High-Value, Active Customers): These customers have the highest frequency and monetary values and very low recency (meaning they purchased recently). This is a highly valuable segment.

Cluster 1 (Lapsed Customers): Characterized by high recency (long time since last purchase) and low frequency and monetary values. These customers may have churned or are "at risk."

Cluster 2 (Top Spenders): This is a small, but extremely valuable segment. They have very high monetary value and a high frequency of purchase.

Cluster 3 (Regular Shoppers): This is a large group of customers with a moderate recency, frequency, and monetary value. They are consistent, but not top-tier shoppers.

The updated customer data, now including their assigned cluster, has been saved to rfm_with_clusters.csv.

Collaborative Filtering: Product Recommendation System
I've also built a collaborative filtering-based recommendation system. This system works by finding users with similar purchasing patterns and suggesting products that those similar users have bought.

User-Item Matrix: I created a matrix where rows represent customers, columns represent products, and the values are the quantity of each product purchased.

Cosine Similarity: I used cosine similarity to measure how similar each customer's purchasing history is to every other customer's.

Recommendation Function: I developed a function that takes a CustomerID as input and returns a list of recommended products. The system identifies the most similar customers and suggests items they've purchased that the target customer has not.

For example, a customer with the ID 12347.0 (a "Champion" customer from our RFM analysis) received the following recommendations based on the purchasing habits of similar users:

Recommendations for Customer 12347.0:

PACK OF 72 RETROSPOT CAKE CASES (StockCode: 21494)

PACK OF 12 RED RETROSPOT PAPER BAG (StockCode: 21976)

ALARM CLOCK BAKELIKE RED (StockCode: 22111)

SET OF 3 CAKE TINS PANTRY DESIGN (StockCode: 21535)

VINTAGE SNAP CARDS (StockCode: 22894)


The project successfully moves from a high-level customer segmentation to a practical, item-level recommendation engine. You can now use these outputs to create targeted marketing campaigns and enhance the shopping experience for your customers.
