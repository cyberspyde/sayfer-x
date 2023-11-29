import os
import json

# Specify the folder containing the JSON files
folder_path = 'D:\\Github\\sayferai\\testing\\Knowledge Base'
knowledge_conf_file = 'D:\\Github\\sayferai\\assets\\knowledge-configuration.json'

with open(knowledge_conf_file, 'r') as config_file:
    knowledge_config = json.load(config_file)

# Initialize a dictionary to store the data counts
data_counts = {}

# Iterate through the files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        
        # Initialize a counter for the current file
        file_count = 0
        
        # Open and read the JSON file
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            
            # Count the number of unique IDs in the JSON data
            unique_ids = set()
            for item in data:
                if 'id' in item:
                    unique_ids.add(item['id'])
            
            file_count = len(unique_ids)
        
        # Store the data count for this file in the dictionary
        data_counts[filename] = file_count

# Update the knowledge configuration with data counts and remove word_count and technology keys
for config_item in knowledge_config:
    filename = config_item["name"] + ".json"
    config_item["data_count"] = data_counts.get(filename, 0)
    config_item.pop("word_count", None)
    config_item.pop("technology", None)

# Rewrite the updated knowledge configuration to knowledge_config.json
with open('knowledge_config.json', 'w') as config_file:
    json.dump(knowledge_config, config_file, indent=4)

print("Updated knowledge configuration (with data_count) written to knowledge_config.json")
