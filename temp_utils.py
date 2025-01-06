import json

# Load the JSON data
with open('word-map.json', 'r') as file:
    data = json.load(file)

# Create a new dictionary to store the updated data
updated_data = {}

# Iterate through the original dictionary
for key, value in data.items():
    # Add the original key-value pair to the updated dictionary
    updated_data[key] = value
    
    # Check if the value contains an uppercase character
    if any(char.isupper() for char in value):
        # Create a new key-value pair with the key in lowercase
        updated_data[key.lower()] = value

# Save the updated dictionary back to the JSON file
with open('word-map-updated.json', 'w') as file:
    json.dump(updated_data, file, indent=4)

print("Updated JSON data has been saved to 'word-map-updated.json'")