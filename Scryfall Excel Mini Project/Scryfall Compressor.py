
##===============================================================================
##Scryfall Card Data Extractor
##-------------------------------------------------------------------------------
##This script is designed to process the complete Magic: The Gathering card dataset 
##from Scryfall (a JSON file), extract key relevant information about each card, and 
##save the result as a CSV file. This CSV can then be opened in Excel for analysis, 
##deck-building, or just exploring card data.
##
##Why do this?
##- The original dataset is huge and complicated.
##- Excel works best with smaller, clean tables.
##- We filter out unwanted cards (tokens, emblems, etc.) and non-English cards.
##- We select only the most useful fields to keep the CSV readable and manageable.
##- Demonstrates both good python and excel skills
##
##Author: George Hunt
##Date: 2025-07-03
##===============================================================================


# We import the json module to read and parse the JSON file.
# JSON (JavaScript Object Notation) is a text-based format for storing structured data.
import json

# The csv module helps us create CSV (Comma-Separated Values) files.
# CSVs are simple text files where data is organized in rows and columns,
# separated by commas, which Excel can easily open and display as tables.
import csv

# ===================== File Paths =====================
# Locations of the files on the computer.
# Using raw strings (prefix r) to avoid confusion with Windows backslashes.
INPUT_FILE = r'C:\Users\George\Downloads\Scryfall Excel Mini Project\scryfall-default-cards.json'
OUTPUT_FILE = r'C:\Users\George\Downloads\Scryfall Excel Mini Project\trimmed_scryfall_cards.csv'

# ===================== Data Filtering Rules =====================
# Some card layouts (types) are irrelevant for typical deckbuilding or data analysis,
# like tokens or emblems which are not standalone cards.
# We list these to skip them during processing, reducing CSV clutter and simplyfying the dataset.
SKIP_LAYOUTS = {'token', 'emblem', 'art_series', 'augment','host', 'double_faced_token'}
# ===================== CSV Headers =====================
# This list defines the columns in the output CSV.
# Each string corresponds to a piece of information extracted from each card.
# Explanation of each field:
# - 'name': The card's official name.
# - 'set': The abbreviation code of the card set it belongs to.
# - 'rarity': How rare the card is (common, uncommon, rare, mythic).
# - 'cmc': Converted Mana Cost, a numeric value representing how expensive the card is to cast.
# - 'colors': What colors the card belongs to, joined as a comma-separated string.
# - 'type_line': The card type and subtype(s), e.g., "Creature — Elf".
# - 'usd': The price of the card in USD (non-foil version).
# - 'usd_foil': The price of the foil (shiny) version in USD.
# - 'image': URL to a standard-sized card image for easy viewing.
CSV_HEADERS = ['name', 'set', 'rarity', 'cmc', 'colors','type_line', 'usd', 'usd_foil', 'image']

def extract_card(card):
  
##    This function receives a dictionary representing a single card's data from the JSON file.
##    It returns a new dictionary containing only the fields we want in the CSV.
##
##    Detailed explanation:
##    - We use the `.get()` method on dictionaries to safely get values for keys that might not exist.
##      This avoids errors if some cards are missing certain data.
##    - 'colors' is a list, so we join its elements into a string separated by commas.
##      If no colors are present, we return an empty string.
##    - For the price fields and image URL, we first check if the nested dictionaries exist.
##      If they don't, we safely return None.
##    
    return {
        'name': card.get('name'),  # Card name as a string
        'set': card.get('set'),    # Set code like 'm21' or 'znr'
        'rarity': card.get('rarity'),  # Card rarity
        'cmc': card.get('cmc'),    # Converted mana cost, a float or int
        # Join colors list like ['R', 'G'] to "R, G"; empty if no colors
        'colors': ', '.join(card.get('colors') or []),
        'type_line': card.get('type_line'),  # Card type description
        # Access 'prices' dictionary and get the USD price; None if missing
        'usd': card.get('prices', {}).get('usd'),
        'usd_foil': card.get('prices', {}).get('usd_foil'),
        # If 'image_uris' exists, get the URL for 'normal' sized image
        'image': card.get('image_uris', {}).get('normal') if 'image_uris' in card else None
    }

def main():
    
##    Main function controlling the flow of the script.
##    Steps:
##    1. Open and load the JSON file into a Python list of card dictionaries.
##    2. Filter out unwanted cards according to our rules.
##    3. Extract only the fields we care about from each card.
##    4. Write the cleaned, filtered data to a CSV file.
##   
    print("Reading Scryfall card database JSON file...")

    # Open the JSON file for reading:
    # - 'r' mode means read-only
    # - encoding='utf-8' ensures proper reading of all characters including special symbols
    # The 'with' statement creates a context where the file is open and assigned to 'json_file'.
    with open(INPUT_FILE, 'r', encoding='utf-8') as json_file:
    # Read the entire content of the file and parse it from JSON text into Python data structures.
    # json.load reads the file object and converts JSON arrays/dictionaries into Python lists/dicts.
        all_cards = json.load(json_file) 

    print(f"Total cards loaded: {len(all_cards):,}")

    filtered = []  # This will hold only the cards we want in the CSV

    print("Filtering cards...")

    # Loop through every card dictionary in the loaded list
    for card in all_cards:
        # Skip cards that are not in English to keep dataset consistent
        if card.get('lang') != 'en':
            continue
        # Skip cards with layouts we don't want (tokens, emblems, etc.)
        if card.get('layout') in SKIP_LAYOUTS:
            continue
        # Skip digital-only cards that only exist in online games
        if card.get('digital'):
            continue

        # Extract relevant fields from this card and add it to filtered list
        filtered.append(extract_card(card))

    print(f"Cards after filtering: {len(filtered):,}")

    # Write filtered card data to a CSV file with UTF-8 BOM encoding
    # BOM ensures Excel recognizes Unicode characters correctly (like accented letters)
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=CSV_HEADERS)
        writer.writeheader()  # Write the header row (column titles)
        writer.writerows(filtered)  # Write all card rows

    print("CSV file created at:")
    print(OUTPUT_FILE)

# Python entry point check.
# This ensures that the script only runs if executed directly,
# and prevents running if imported as a module in another script.
if __name__ == '__main__':
    main()
