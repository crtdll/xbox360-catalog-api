import os, json, platform
from datetime import datetime
from database import Database

db = Database()

def get_file_data(file_path):
  with open(file_path, 'r', encoding='utf-8') as file:
    return json.load(file)

def truncate_url(url, length=30):
  if len(url) > length:
    return url[:length] + '...'
  return url

def iso_to_hooman(iso):
  formats = [
    '%Y-%m-%dT%H:%M:%S.%fZ',
    '%Y-%m-%dT%H:%M:%S'
  ]
  
  parsed_date = ''
  for fmt in formats:
    try:
      parsed_date = datetime.strptime(iso, fmt)
      break
    except ValueError:
      continue
  
  return parsed_date.strftime('%B %d, %Y %H:%M:%S') if parsed_date else iso

def clear_console():
  os.system('cls' if platform.system() == 'Windows' else 'clear')

def print_result(result, truncate = False):
  url = truncate_url(result['ImageURL']) if truncate else result['ImageURL']
  print(f"\nTitle     : {result['Title']}")
  print(f"Media ID  : {result['MediaID']}")
  print(f"Developer : {result['Developer']}")
  print(f"Publisher : {result['Publisher']}")
  print(f"Rating    : {result['Rating']}/5.00 ({result['Ratings']} reviews)")
  print(f"Released  : {result['Released']}")
  print(f"Updated   : {result['LastUpdate']}")
  print(f"Image     : {url}")
  print(f"Download  : {result['DownloadURL']}")
  print('-' * 40)

def search_and_display(query: str, directory='data'):
  results = []
  query = query.lower()
  
  for data in db.search_full_title(query):
    title = data['full_title'].strip()
    if query not in title.lower():
      continue
    
    media_id = data['id'][-8:]
    ratings = '{:,}'.format(data['number_of_ratings']) if data['number_of_ratings'] is not None else 0
    rating = data['rating_aggregate'] if data['rating_aggregate'] is not None else 0
    developer = data['developer']
    publisher = data['publisher']
    release_date = iso_to_hooman(data['availability_date'])
    last_update = iso_to_hooman(data['last_updated'])
    
    image_url = db.search_banner_img(data['id'])
    download_url = data['download_url'] if data['download_url'] is not None else 'No download available'
    
    results.append({
      'Title': title,
      'MediaID': media_id,
      'Developer': developer,
      'Publisher': publisher,
      'Rating': rating,
      'Ratings': ratings,
      'ImageURL': image_url,
      'DownloadURL': download_url,
      'Released': release_date,
      'LastUpdate': last_update
    })
  
  if results:
    for result in results:
      print_result(result, False)
  else:
    print('No matches found')

def main():
  if not db.connect():
    print('Failed database connection')
    return
  
  while True:
    query = input('Enter query: ').strip()
    if not query:
      print('Query cannot be empty. Please try again.')
      continue
    search_and_display(query)

if __name__ == "__main__":
  main()