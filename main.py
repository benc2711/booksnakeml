import json
import os
import time
import requests





# Function to process JSON URLs and extract "Physical Description"
def scrape(file_handle):
    """
    Iterates over predefined sections and item IDs to fetch and process JSON manifests.

    Args:
        file_handle (file object): The open file handle to write descriptions to.
    """
    #     sections = ["p15150coll4", "p15150coll7", "p15150coll8"]
    sections = ["p15150coll8"]
    for section in sections:
        print(f"Processing section: {section}")
        for i in range(200, 1000):
            url = f"https://hdl.huntington.org/iiif/info/{section}/{i}/manifest.json"
            fetch_json(url, file_handle)

            # Optional: Print progress every 100 items
            if (i + 1) % 100 == 0:
                print(f"Processed {i + 1} items in section {section}")


# Function to fetch JSON and write to file
def fetch_json(json_url, file_handle):
    """
    Fetches the physical description from the JSON URL and writes it to the file.

    Args:
        json_url (str): The URL of the JSON manifest.
        file_handle (file object): The open file handle to write descriptions to.
    """
    physical_description = process_json(json_url)

    if physical_description:
        try:
            file_handle.write(physical_description + '\n')  # Add newline after each description
            print(f"Written Physical Description to data.txt")
        except Exception as e:
            print(f"Failed to write to data.txt: {e}")
    else:
        print(f"No Physical Description found for {json_url}")

    # Introduce a small delay to avoid hitting the server too frequently
    # time.sleep(.5)

# Helper function to fetch and extract "Physical Description" from a JSON URL
def process_json(json_url: str) -> str:
    """
    Fetches the JSON data from the given URL and extracts the "Physical Description" field.

    Args:
        json_url (str): The URL of the JSON manifest.

    Returns:
        str or None: The physical description if found; otherwise, None.
    """
    try:
        response = requests.get(json_url)
        response.raise_for_status()
        data = response.json()

        metadata = data.get('metadata', [])
        for item in metadata:
            if item.get('label') == 'Physical Description':
                return item.get('value')

        # If "Physical Description" not found
        return None

    except requests.RequestException as e:
        print(f"Error fetching {json_url}: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {json_url}: {e}")
        return None
# Main execution flow
def main():
    """
    Main function to orchestrate the scraping process.
    """
    # Define the output directory and file path
    output_dir = "physical_descriptions"
    os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist
    filepath = os.path.join(output_dir, "data.txt")



    try:
        # Open the file once in append mode. Use 'w' mode to overwrite each time.
        with open(filepath, 'a', encoding='utf-8') as file:
            scrape(file)
        print("Scraping process completed successfully.")
    except Exception as e:
        print(f"An error occurred during scraping: {e}")


if __name__ == "__main__":
    main()
