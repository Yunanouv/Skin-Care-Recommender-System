# Skincare Recommender System Based on Skin Problem Using Content-Based Filtering  

<div align="center">
<img src="https://img.freepik.com/free-vector/realistic-cosmetic-background-with-beauty-products_79603-609.jpg?w=1060&t=st=1700021678~exp=1700022278~hmac=454cd6d713db22a83f07121746330bb49e23b2ae4a6eacf0502aae5455da5020" alt="eCommerce" style="width:800px;height:500px;" align="center">
</div> 

<br>
Nowadays, skin care is becoming one of the most essential things in our lives. Skincare products have grown rapidly everywhere and tend to increase year by year. So do not be surprised if there are so many skin care products circulating in the community. However, the large number of product choices makes it difficult for people to choose the product that best suits their facial needs. Therefore, the author took the initiative to create a system that is able to recommend skin care products based on facial skin problems. In this study, the author uses the method of content-based filtering in making the recommendation system. This recommendation system is made without using rating data, so the algorithm approach used is cosine similarity and TF-IDF in finding similarity features. Then, the first output that appears will be used by the machine as historical data to then enter the content-based filtering stage. So, users will get recommendations according to the selected keywords and similar products.   
</br>

<br>
This project uses datasets scraped independently from various skincare product websites with details:  
<br></br>

| Feature Name | Description | 
| --- | --- | 
|**product_href** | Product URL link |
|**product_name** | Product name |
|**product_type** |Type of product (Facial wash, Toner, Serum, Moisturizer, Sunscreen) |
|**brand** | Product brand |
|**notable_effects** | What it's good for |
|**skin type** | The suitable type of skin for the product (Normal, Dry, Oily, Combination, Sensitive) |
|**price** | Product price (in IDR Rp) |
|**description** | Product description |
|**picture_src** | Product image URL link |

# Data Overview  

1. In total, there are 1224 products scrapped from websites.  
2. Because this data was scrapped and arranged by me, it looks neater and cleaner. There's no null value.  
3. Unfortunately, there are 14 duplicate rows. Need to be removed.  
4. Of 5 types of products, serum is more hype than others.   
5. From many pairs of notable effects, 150 products are good for pore care, brightening, and anti-aging all in one product.  
6. Looks like many skin care products suitable for oily skin.

# Exploratory Data Analysis (EDA)  
**1. Top Brands With Their Products**  
  From 211 beauty brands, here are the top 10 brands with the most products. SOMETHINC is the top brand, which means they have many kinds of products just 5 types (basic skincare).
<br>
<img width="550" alt="eda1" src="https://github.com/Yunanouv/Skin-Care-Recommender-System/assets/146415555/a02811cd-3150-49b7-9df5-5276f659cac4">
</br>

**2. Skin Care Product Type**  
As mentioned before, the types of products in this dataset are only basic skincare, they are facial wash, toner, serum, moisturizer, and sunscreen. The picture below shows the percentage of each product.  
<br>
<img width="650" alt="image" src="https://github.com/Yunanouv/Skin-Care-Recommender-System/assets/146415555/79ccdabe-0b40-416e-8a96-55bd925eefd8"> 
</br>  

**3. Product Skin Type**  
Each skincare product is formulated to be suitable for certain skin types so that the benefits obtained are more precise. Skin types are normal, dry, oily, combination, and sensitive. There are products that are suitable for all skin types, some are suitable only for dry skin, only for oily skin, or specifically for sensitive skin. The following are the skin types that are most often found in skincare products.  
<br>
<img width="600" alt="image" src="https://github.com/Yunanouv/Skin-Care-Recommender-System/assets/146415555/dd618585-bab4-4f56-94e6-28b1d9860a12">
</br>

**4. Skin Care Product Notable Effects**  
Just like the type of skin that is suitable for a skin care product, the perceived benefits are also directed at the facial skin problem that we want to overcome. There are products specifically for treating acne and controlling oil, brightening products, anti-aging products, and many other benefits that can be found in one product. The following are the top 5 notable effects that can be obtained in one product.  
<br>
<img width="735" alt="image" src="https://github.com/Yunanouv/Skin-Care-Recommender-System/assets/146415555/02fec82f-ab46-443f-834b-8505188e01b6">
</br>


# App  
This project has been deployed using Streamlit. Please visit the link here https://skin-care-recommender-system-141.streamlit.app/.  
App in overall  
<br>
<img width="881" alt="image" src="https://github.com/Yunanouv/Skin-Care-Recommender-System/assets/146415555/b03251c5-8605-4c98-9b5c-09e647832eeb">
<br>
----
<img width="857" alt="image" src="https://github.com/Yunanouv/Skin-Care-Recommender-System/assets/146415555/c9b2336c-b3d3-4e39-b1ad-c733801d308b">
<br>
-----
<img width="856" alt="image" src="https://github.com/Yunanouv/Skin-Care-Recommender-System/assets/146415555/d7042f8d-7ed9-4fdb-990e-a7eccd6b67e8">
<br>


Thank You!
