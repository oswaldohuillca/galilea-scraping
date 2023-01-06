import json

if __name__ == "__main__":
  results = []

  # Opening JSON file
  f = open('output.json')
    
  # returns JSON object as 
  # a dictionary
  data = json.load(f)
    
  # Iterating through the json
  # list
  for i in data:
    src = i["featured"]["src"]
    src = src.replace("'","")
    results.append(src)
    
  # Closing file
  f.close()

  # Writing to sample.json
  with open("featured_images.json", "w", encoding='utf-8') as outfile:
    json.dump(results, outfile, indent=4)