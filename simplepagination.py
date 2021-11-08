from os import close, write
import requests
from bs4 import BeautifulSoup
import json

database = {}
index_count = 0
for x in range(1, 103):

  url = 'https://apps.irs.gov/app/picklist/list/priorFormPublication.html;jsessionid=4EuDHbdC5JE19wM91nvptz-G.20?resultsPerPage=200&sortColumn=sortOrder&indexOfFirstRow=' + str(index_count) + '&criteria=&value=&isDescending=false'

  response = requests.get(url)

  soup = BeautifulSoup(response.text, "html.parser")

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
    if name in database:
      database[name][date] = {"form_name":name, "title": title, "date":date, "link": pdf}
    else:
      database[name] = {date : {"form_name":name, "title": title, "date":date, "link": pdf}}
    # print({'name': name, 'title': title, 'date':date, 'pdf': pdf })
  
  for el in tr_odd:
    name = el.a.string
    date_ = el.find(class_ ="EndCellSpacer").string
    date = " ".join(date_.split())
    title_ = el.find(class_ = "MiddleCellSpacer").string
    title = " ".join(title_.split())
    pdf = el.a['href']
    if name in database:
      database[name][date] = {"form_name":name, "title": title, "date":date, "link": pdf}
    else:
      database[name] = {date : {"form_name":name, "title": title, "date":date, "link": pdf}}
      # print(database)
  index_count+=200

with open("database.txt", "w") as outfile:
  json.dump(database, outfile)

print("database.txt file downloaded in JSON format")

#First utility 

with open ("database.txt") as json_file:
  data = json.load(json_file)
  form_lookup = input("enter list of forms seperated by comma. ex: Form W-2,Form 1095-C")
  form_list = form_lookup.split(',')
  list = []
  for form in form_list:
    # print(form)
    if data[form]:
      date_range = data[form].keys()
      
      for date in date_range:
        list.append(int(date))    
      form_title = data[form][str(list[0])]["title"]
      print({
        "form_number": form,
        "form_title": form_title,
        "min_year": min(list),
        "max_year": max(list)
        })
      list = []
    else:
      print("form not found")