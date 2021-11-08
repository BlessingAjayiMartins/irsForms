from os import close, write
import requests
from bs4 import BeautifulSoup
import json

cache = {}
index_count = 0
for x in range(1, 5):

  url = 'https://apps.irs.gov/app/picklist/list/priorFormPublication.html;jsessionid=4EuDHbdC5JE19wM91nvptz-G.20?resultsPerPage=200&sortColumn=sortOrder&indexOfFirstRow=' + str(index_count) + '&criteria=&value=&isDescending=false'

  response = requests.get(url)

  soup = BeautifulSoup(response.text, "html.parser")

  # next_button = soup.find('a', string='Next »')
  # next_page_url = ""
  # page_count = 1
  
  # print(x)
  # next_page_url = next_button.get('href')
  # url = next_page_url

  tr_even = soup.find_all('tr', class_ = 'even')
  tr_odd = soup.find_all('tr', class_ = 'odd')

  for el in tr_even:
    name = el.a.string
    date_ = el.find(class_ ="EndCellSpacer").string
    date = " ".join(date_.split())
    title_ = el.find(class_ = "MiddleCellSpacer").string
    title = " ".join(title_.split())
    pdf = el.a['href']
    # print(name)
    if name in cache:
      cache[name][date] = {"form_name":name, "title": title, "date":date, "link": pdf}
    else:
      cache[name] = {date : {"form_name":name, "title": title, "date":date, "link": pdf}}
    # print({'name': name, 'title': title, 'date':date, 'pdf': pdf })
  for el in tr_odd:
    name = el.a.string
    date_ = el.find(class_ ="EndCellSpacer").string
    date = " ".join(date_.split())
    title_ = el.find(class_ = "MiddleCellSpacer").string
    title = " ".join(title_.split())
    pdf = el.a['href']
    if name in cache:
      cache[name][date] = {"form_name":name, "title": title, "date":date, "link": pdf}
    else:
      cache[name] = {date : {"form_name":name, "title": title, "date":date, "link": pdf}}
      # print(cache)
  index_count+=200
with open("cache.json", "w") as outfile:
  json.dump(cache, outfile)
# db = write([cache])
# db = close()
print("db.json file downloaded")
# while next_button:
#   temp_url = ''
#   next_page_url = next_button.get('href')
#   url = next_page_url
#   page_count+=1
#   print(url)