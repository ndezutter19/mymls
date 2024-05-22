import requests
import pandas as pd

# URLs of the API endpoints
url_active = 'https://api.umeprojects.com/api/v1/public/listings?orderBy=certified,verified&order=DESC,DESC&location=AZ&rooms=&bathrooms=&loanType=&sqft={"min":"","max":""}&rate={"min":"","max":""}&price={"min":"","max":""}&maxDownPayment={"min":"","max":""}&status=["Active"]&perPage=50&page=0&bounds={"southwest":{"lng":-152.8367536824697,"lat":23.577542464748248},"northeast":{"lng":-68.82587508904831,"lat":50.589771501309826}}&center={"lat":38.32564000799414,"lng":-110.83131438575917}&zoom=2.5952038733357656'

url_closed = 'https://api.umeprojects.com/api/v1/public/listings?orderBy=certified,verified&order=DESC,DESC&location=AZ&rooms=&bathrooms=&loanType=&sqft={"min":"","max":""}&rate={"min":"","max":""}&price={"min":"","max":""}&maxDownPayment={"min":"","max":""}&status=["Closed"]&perPage=50&page=0&bounds={"southwest":{"lng":-152.8367536824697,"lat":23.577542464748248},"northeast":{"lng":-68.82587508904831,"lat":50.589771501309826}}&center={"lat":38.32564000799414,"lng":-110.83131438575917}&zoom=2.5952038733357656'

# Function to fetch data from an API
def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['items']
    else:
        print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
        return []

# Fetch active and closed listings data
active_listings = fetch_data(url_active)
closed_listings = fetch_data(url_closed)

# Convert to DataFrames for easier manipulation
active_df = pd.json_normalize(active_listings)
closed_df = pd.json_normalize(closed_listings)

# Filter active listings to include only those priced under $500k
active_df = active_df[active_df['Property.listPrice'] < 500000]

# Calculate price per square foot for both active and closed listings
active_df['price_per_sqft'] = active_df['Property.listPrice'] / active_df['Property.livingArea']
closed_df['price_per_sqft'] = closed_df['Property.listPrice'] / closed_df['Property.livingArea']

# Group closed listings by postal code and calculate the average price per square foot
avg_closed_price_per_sqft = closed_df.groupby('Property.postal')['price_per_sqft'].mean().reset_index()
avg_closed_price_per_sqft.columns = ['Property.postal', 'avg_price_per_sqft_closed']

# Merge active listings with the average closed price per square foot by postal code
merged_df = pd.merge(active_df, avg_closed_price_per_sqft, on='Property.postal', how='left')

# Calculate the delta between the asking price per square foot of active listings and the average sold price per square foot of closed listings
merged_df['delta'] = merged_df['price_per_sqft'] - merged_df['avg_price_per_sqft_closed']

# Identify potential buys where the active listing price per square foot is below the average closed listing price per square foot
potential_buys = merged_df[merged_df['delta'] < 0].copy()

# Construct the link and explanation for each property
base_url = "https://listings.takemylowrate.com/listing"
potential_buys.loc[:, 'link'] = potential_buys.apply(
    lambda row: f"{base_url}/{row['Property.streetNumber']}_{row['Property.route'].replace(' ', '')}_{row['Property.city'].replace(' ', '')}_{row['Property.state']}/{row['id']}", axis=1
)
potential_buys.loc[:, 'explanation'] = potential_buys.apply(
    lambda row: f"The asking price per square foot is ${row['price_per_sqft']:.2f}, which is ${-row['delta']:.2f} lower than the average sold price per square foot in this area (${row['avg_price_per_sqft_closed']:.2f}). This makes it a potentially good buy.", axis=1
)

# Print the results in a readable format
for index, row in potential_buys.iterrows():
    print(f"ID: {row['id']}")
    print(f"Address: {row['Property.streetNumber']} {row['Property.route']}, {row['Property.city']}, {row['Property.state']}")
    print(f"Listing Price: ${row['Property.listPrice']}")
    print(f"Price per Sqft: ${row['price_per_sqft']:.2f}")
    print(f"Average Closed Price per Sqft: ${row['avg_price_per_sqft_closed']:.2f}")
    print(f"Delta: ${row['delta']:.2f}")
    print(f"Explanation: {row['explanation']}")
    print(f"Link: {row['link']}")
    print("\n" + "-"*80 + "\n")

print("Potential buys printed with explanations and links.")
