import re
import json

def generate_summary_text(results):
    #print(results)
    # Initialize the comparison paragraph
    comparison_paragraph = ""
    
    # Sort listings by price (ascending) for better comparison
    results_sorted_by_price = sorted(results, key=lambda x: parse_price(x['price']))
    
    # Initialize lists to hold amenities
    all_amenities = []

    results_sorted_by_reviews = sorted(
    results,
    key=lambda x: float(x.get('review_scores_rating', 0) if str(x.get('review_scores_rating', 0)).replace('.', '', 1).isdigit() else 0),
    reverse=True
)


    
    # Process each result
    for result in results:
        # Extract amenities from each listing
        amenities = result.get('amenities', [])
        
    
    # Find the common amenities across all apartments
    common_amenities = set.intersection(*all_amenities) if all_amenities else set()

    # Find unique amenities for each listing
    unique_amenities_info = []
    most_expensive_info = ""
    cheapest_info = ""

    top_reviews_info = []
    for result in results_sorted_by_reviews[:3]:
        host_name = result.get('host_name', 'Unknown host')
        city = result.get('city', 'Unknown city')
        price = format_price(result.get('price', 'N/A'))
        bed_bath = result.get('bed_bath', '')
        bedrooms, bathrooms = extract_bed_bath(bed_bath)
        review_score = result.get('review_scores_rating', 'No reviews yet')
        amenities = result.get('amenities', [])
        
        
        # Format the amenities string (limit to first 5 for readability)
        amenities_str = format_amenities(amenities)
        
        # Create a description for the top listing
        top_reviews_info.append(
            f"Hosted by {host_name} in {city}, this listing features {bedrooms} bed / {bathrooms} bath, priced at {price}. It has a review score of {review_score} and the amenities included are {amenities_str}."
        )
        #print(top_reviews_info)
        
    # Loop through sorted results to create summary text
    for result, amenities_set in zip(results_sorted_by_price, all_amenities):
        
        host_name = result.get('host_name', 'Unknown host')  # Use .get() for safe access
        city = result.get('city', 'Unknown city')
        price = format_price(result.get('price', 'N/A'))
       
        bed_bath = result.get('bed_bath', '')
        bedrooms, bathrooms = extract_bed_bath(bed_bath)
        
        # Extract review score
        review_score = result.get('review_scores_rating', 'No reviews yet') if result.get('review_scores_rating', 'N/A') != "N/A" else 'No reviews yet'
        
        # Find unique amenities for this listing (exclude common amenities)
        unique_listing_amenities = amenities_set - common_amenities
        
        # Limit the unique amenities to 4 or 5 items and add etc.
        unique_listing_amenities_list = list(unique_listing_amenities)[:5]
        unique_amenities_str = ", ".join(unique_listing_amenities_list) + (" etc." if len(unique_listing_amenities_list) > 4 else "")
        
        # Special handling for the most expensive and cheapest listings
        if result == results_sorted_by_price[-1]:  # Most expensive
            most_expensive_info = f"Hosted by {host_name} with {bedrooms} bed / {bathrooms} bath priced at {price} in {city} comes with amenities like {unique_amenities_str}, and currently there are {review_score}."
            continue  # Skip adding it to the general unique amenities info
        
        if result == results_sorted_by_price[0]:  # Cheapest
            cheapest_info = f"Hosted by {host_name} with {bedrooms} bed / {bathrooms} bath priced at {price} in {city} comes with amenities like {unique_amenities_str}, and currently there are {review_score}."
            continue  # Skip adding it to the general unique amenities info
        
        # Add the unique amenities info for other listings
        unique_amenities_info.append(f"Hosted by {host_name} with {bedrooms} bed / {bathrooms} bath priced at {price} in {city} comes with amenities like {unique_amenities_str}, and currently there are {review_score}.")
    
    # Short analysis (comparison between high and low priced apartments)
    if len(results) > 1:
        most_expensive = results_sorted_by_price[-1]
        cheapest = results_sorted_by_price[0]
        most_expensive_price = format_price(most_expensive.get('price', 'N/A'))
        cheapest_price = format_price(cheapest.get('price', 'N/A'))
        
        e_bedrooms, e_bathrooms = extract_bed_bath(most_expensive.get('bed_bath', ''))
        c_bedrooms, c_bathrooms = extract_bed_bath(cheapest.get('bed_bath', ''))
        
        most_expensive_bed_bath = f"{e_bedrooms} bed / {e_bathrooms} bath"
        cheapest_bed_bath = f"{c_bedrooms} bed / {c_bathrooms} bath"
        
        comparison_paragraph += f"The most expensive apartment is hosted by {most_expensive.get('host_name', 'Unknown host')} in {most_expensive.get('city', 'Unknown city')} with a price of {most_expensive_price} and {most_expensive_bed_bath}."
        comparison_paragraph += f" It comes with amenities like {format_amenities(most_expensive.get('amenities'))}." if most_expensive_info else ""
        
        comparison_paragraph += f" On the other hand, the cheapest apartment is hosted by {cheapest.get('host_name', 'Unknown host')} in {cheapest.get('city', 'Unknown city')} priced at {cheapest_price}, with {cheapest_bed_bath}."
        comparison_paragraph += f" It comes with amenities like {format_amenities(most_expensive.get('amenities'))}." if cheapest_info else ""
    
    # Combine everything into one paragraph
    
    num_unique_listings = len(unique_amenities_info)
    comparison_paragraph += f" Additionally the top 3 reviewed listing are,: " + " ".join(top_reviews_info)
    
    return comparison_paragraph


def format_amenities(amenities):
    # Check if amenities is a string (assumed to be in invalid JSON format)
    if isinstance(amenities, str):
        # Clean up the string if it looks like a set
        amenities = amenities.strip('{}').replace('"', '').replace("'", "").split(',')
        amenities = [item.strip() for item in amenities if item]  # Remove any empty strings
        
    return ", ".join(amenities[:5]) + (" etc." if len(amenities) > 5 else "")

def extract_bed_bath(bed_bath_str):
    """
    Helper function to extract the number of bedrooms and bathrooms from the 'bed_bath' string.
    E.g., '5b7b' -> (5, 7) and '4b2.5b' -> (4, 2.5)
    """
    match = re.match(r'(\d+(\.\d+)?)b(\d+(\.\d+)?)b', bed_bath_str)
    if match:
        bedrooms = float(match.group(1))  # Convert to float to allow decimal values
        bathrooms = float(match.group(3))  # Convert to float to allow decimal values
        return bedrooms, bathrooms
    return 0, 0  # If the format is incorrect or missing, return default values

def format_number(num):
    # Format the number (bedrooms/bathrooms) to a cleaner version if it's None or has decimal points
    if not num:
        return 0
    return int(num) if num % 1 == 0 else num

def format_price(price):
    # Format the price (remove any currency symbols and parse it as a float)
    if price == "N/A" or not price:
        return "N/A"
    return f"${float(parse_price(price)):,.2f}"  # Formatting price to include commas and 2 decimal points

def parse_price(price):
    """
    Helper function to safely parse the price and convert it to a float.
    It handles both string and integer types for price.
    """
    if isinstance(price, str):
        return float(price.replace('$', '').replace(',', '')) if price != "N/A" else 0
    elif isinstance(price, (int, float)):
        return float(price)
    return 0  # In case price is not available
