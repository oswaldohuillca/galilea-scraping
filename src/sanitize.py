import csv
import json
import string
import re


# static_path = "https://apros-qa.com.pe/wp-content/uploads/2023/01"
static_path = "http://localhost/wp-content/uploads/2023/01"
# permalink = "https://apros-qa.com.pe/2023/01/05"
permalink = "http://localhost/2023/01/05"
author_username = "test"
author_email = "oswaldohuillca@gmail.com"
author_firstname = ""
author_lastname = ""


def create_json(result):
  # Writing to sample.json
  with open("data/sanitize-output.json", "w",encoding='utf-8') as outfile:
    json.dump(result, outfile, indent=2,ensure_ascii=False)


def replace_path(item):
  item = item.replace("https://content.app-sources.com/s/0949991663303409/uploads/Home",static_path)
  item = item.replace("https://content.app-sources.com/s/0949991663303409/uploads/Blog", static_path)
  item = item.replace("'h","h")
  item = item.replace("g'", "g")
  return item

def sanitize_url(text):
  clean_text = re.sub(r'[^a-zA-Z0-9 ]', '', text).strip()
  clean_text = re.sub(r'\s+', ' ', clean_text)
  # return " ".join(clean_text.split())
  return clean_text.replace(" ", "-").lower()

def get_fiel(path) :
  # Opening JSON file
  f = open(f'{path}.json')

  # returns JSON object as
  # a dictionary
  data = json.load(f)

  # Iterating through the json
  # list
  return data
  

# def sanitize():
#   result = []
#   data = get_fiel("output")
#   for v in data:
#     temp = {
#       "title": v["title"],
#       "excerpt": v["excerpt"],
#       "categories": v["categories"],
#       "post_date": v["post_date"],
#       "body": replace_path(v["body"]),
#       "featured": {
#         "src": replace_path(v["featured"]["src"]),
#       },
#       "tags": v["tags"]
#     }
#     result.append(temp)
  
#   return result

def sanitize():
  result = []
  counter = 1
  data = get_fiel("data/output")

  for v in data:
    title = v["title"].strip()
    date = v["post_date"].split(" ")[0].split("/")

    temp = {
      "ID": counter,
      "title": v["title"],
      "body": replace_path(v["body"]),
      "excerpt": v["excerpt"],
      "post_date": v["post_date"],
      "post_type": "post",
      "permalink": permalink + "/" + sanitize_url(title),
      "image_url": replace_path(v["featured"]["src"]),
      "image_alt": "",
      "image_caption": "",
      "image_description": "",
      "text_alt": "",
      "image_featured": replace_path(v["featured"]["src"]),
      "athactment": "",
      "categories": ",".join(v["categories"]),
      "tags": ",".join(v["tags"]),
      "status": "publish",
      "autho_id": 1,
      "author_username": author_username,
      "author_email": author_email,
      "author_firstname": author_firstname,
      "author_lastname": author_lastname,
      "slug": sanitize_url(title),
      "format": "",
      "template": "",
      "parent": 0,
      "parent_slug": 0,
      "order": 0,
      "comment_status": "open",
      "ping_status": "open",
      "post_modify": f"{date[2]}-{date[1]}-{date[0]}"
      # "featured": {
      #   "src": replace_path(v["featured"]["src"]),
      # },
    }
    result.append(temp)
    counter += 1
  
  return result


def create_csv(data):
  # now we will open a file for writing
  data_file = open('data/data_file.csv', 'w')
  
  # create the csv writer object
  csv_writer = csv.writer(data_file)
  
  # Counter variable used for writing
  # headers to the CSV file
  count = 0
  
  for emp in data:
    if count == 0:

      # Writing headers of CSV file
      header = ["ID","Title","Content","Excerpt","Date","Post Type","Permalink","Image URL","Image Title","Image Caption","Image Description","Image Alt Text","Image Featured","Attachment URL","Categorías","Etiquetas","Status","Author ID","Author Username","Author Email","Author First Name","Author Last Name","Slug","Format","Template","Parent","Parent Slug","Order","Comment Status","Ping Status","Post Modified Date"]
      csv_writer.writerow(header)
      count += 1
  
    # Writing data of CSV file
    csv_writer.writerow(emp.values())
  
  data_file.close()


if __name__ == "__main__":
  result = sanitize()
  # create_json(result)
  create_csv(result)