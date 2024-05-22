Features

    Fetches active and closed real estate listings from a specified API.
    Filters active listings to include only those priced under $500k.
    Calculates the price per square foot for both active and closed listings.
    Compares active listings' price per square foot to the average closed listings' price per square foot in the same postal code.
    Identifies potential buys where the active listing price per square foot is below the average closed listing price per square foot.
    Provides detailed explanations and clickable links to the listings.

Prerequisites

    Python 3.x
    requests library
    pandas library

You can install the required Python libraries using pip:

pip install requests pandas

Usage

    Clone the Repository:

git clone https://github.com/yourusername/real-estate-listings-analysis.git
cd real-estate-listings-analysis

Run the Script:

    python mlsscraper.py

    Script Output:

    The script prints the potential buys directly to the console in a readable format, including the explanation with the numbers and a clickable link.

Script Explanation
Fetch Data

The script fetches data from two provided API endpoints for active and closed listings. The fetch_data function is used to send GET requests to the API and retrieve the data.
Data Processing

The data is processed using pandas for easier manipulation. The script calculates the price per square foot for both active and closed listings and groups closed listings by postal code to calculate the average price per square foot.
Identify Potential Buys

The script identifies potential buys by comparing the price per square foot of active listings to the average closed listing price per square foot in the same postal code. Listings where the active price per square foot is lower are considered potential buys.
Construct Links and Explanations

For each potential buy, the script constructs a clickable link and provides an explanation based on the calculated price differences.
Print Results

The results are printed in a readable format, including the property ID, address, listing price, price per square foot, average closed price per square foot, delta, explanation, and clickable link.
