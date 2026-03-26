import cloudscraper
import pandas as pd
import io

# We use the internal 'bitstream' URL that points directly to the file
url = 'https://www.research-collection.ethz.ch/bitstream/handle/20.500.11850/383116/rawdata_new.csv?sequence=1&isAllowed=y'
file_name = "data_raw.csv"

print("Bypassing repository protection...")
scraper = cloudscraper.create_scraper() # Creates a session that mimics a browser

try:
    response = scraper.get(url)
    response.raise_for_status()

    # Check if we actually got the CSV content
    if response.text.strip().startswith('<!DOCTYPE'):
        print("Error: Still being redirected to HTML. The server requires a manual browser session.")
    else:
        # Save the file for DVC tracking
        with open(file_name, "wb") as f:
            f.write(response.content)
        print(f"Success! {file_name} saved.")

        # Load into Pandas (using ; as the separator for this specific dataset)
        df = pd.read_csv(io.BytesIO(response.content), sep=';')
        print("\n--- Data Preview ---")
        print(df.head())

except Exception as e:
    print(f"Failed: {e}")