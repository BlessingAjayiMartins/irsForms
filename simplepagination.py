from os import path
import os
import requests
from bs4 import BeautifulSoup
import json
import math




def main():
  # find number of files to determine how many pages to scrape
  url = 'https://apps.irs.gov/app/picklist/list/priorFormPublication.html'

  response = requests.get(url)

  temp_soup = BeautifulSoup(response.text, "html.parser")

  column_with_number_of_files = temp_soup.find('th', class_= "ShowByColumn")
  get_string = column_with_number_of_files.string.rstrip()
  create_list = get_string.split(" ")
  
  split_ = create_list[-2].split(",")
  loose_number = "".join(split_)
 
  number_of_files = int(loose_number)
  pages = math.ceil(number_of_files/200)
  

  database = {}
  index_count = 0
  

  for x in range(0, pages):
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
      
      if name in database:
        database[name][date] = {"form_name":name, "title": title, "date":date, "link": pdf}
      else:
        database[name] = {date : {"form_name":name, "title": title, "date":date, "link": pdf}}
      
    
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
        
    index_count+=200
  with open("database.txt", "w") as outfile:
    json.dump(database, outfile)
  print("database.txt file downloaded in JSON format")
  #First utility 
  with open ("database.txt") as json_file:
    data = json.load(json_file)
    form_lookup = input("enter list of forms seperated by comma. ex: Form W-2,Form 1095-C : ")
    form_list = form_lookup.split(',')
    date_list = []
    result = []
    for form in form_list:
      # print(form)
      if data[form]:
        date_range = data[form].keys()
        
        for date in date_range:
          date_list.append(int(date))
            
        form_title = data[form][str(date_list[0])]["title"]
        result.append({
          "form_number": form,
          "form_title": form_title,
          "min_year": min(date_list),
          "max_year": max(date_list)
          })
        date_list = []
      else:
        print("form not found")
    print(result)
  # Second utility
  with open ("database.txt") as json_file:
    data = json.load(json_file)
    form_lookup = input("please type in form name you would like to download : ")
    if data[form_lookup]:
      range_input = input("please type in the year in xxxx format or range seperated by -  ex:xxxx-xxxx : ")
      if len(range_input) == 9:
        range_array = range_input.split('-')
        available_date_in_range = []
        pdf_link_list = []
        
        for x in range (int(range_array[0]), int(range_array[1])):
          if str(x) in data[form_lookup]:
            pdf_link_list.append(data[form_lookup][str(x)]["link"])
            available_date_in_range.append(str(x))
            
        
        x=0
        for pdf in pdf_link_list:
          
          date_as_key = available_date_in_range[x]
          # if the directory does NOT exist
          if not os.path.exists(form_lookup):
            print("creating subdirectory..")
            os.mkdir(form_lookup, mode = 0o666)
            # request_download = requests.get(pdf, stream=True)
            response = requests.get(pdf)
            # request_download = BeautifulSoup(response.content, "html.parser")
            # Navigate to the desired directory
            os.chdir(f"{form_lookup}")
            # Stream and save the data
            with open(f"{form_lookup} - {date_as_key}.pdf", 'wb') as f:
                f.write(response.content)
            
            # print(f"Downloading {date_as_key} \n")
              # Go up a level
            os.chdir('..')
            print("Enjoy your downloads!")
          # Else if the directory does exist
          elif os.path.exists(form_lookup):
              # Change to the desired directory
              os.chdir(f'{form_lookup}')
              # Get the data from the url
              response = requests.get(pdf)
              # Stream the data to be saved
              with open(f"{form_lookup} - {date_as_key}.pdf", 'wb') as f:
                f.write(response.content)
              print("Enjoy your download! \n")
              # Go up a level, useful if cell is ran multiple times
              os.chdir('..')
          
          x = x+1
      elif len(range_input) == 4:
        
        if range_input in data[form_lookup]:
          pdf_link = data[form_lookup][range_input]["link"]
          # if directory does not exist
          if not os.path.exists(form_lookup):
            print("creating subdirectory..")
            os.mkdir(form_lookup, mode = 0o666)
          
            response = requests.get(pdf_link)
            
            # Navigate to the desired directory
            os.chdir(f"{form_lookup}")
            # Save the data
            with open(f"{form_lookup} - {range_input}.pdf", 'wb') as f:
                f.write(response.content)
              # Go up a level
            os.chdir('..')
            print("Enjoy your downloads!")
          # Else if the directory does exist
          elif os.path.exists(form_lookup):
              # Change to the desired directory
              os.chdir(f'{form_lookup}')
              # Get the data from the url
              response = requests.get(pdf_link)
              # Stream the data to be saved
              with open(f"{form_lookup} - {range_input}.pdf", 'wb') as f:
                f.write(response.content)
              print("Enjoy your download! ")
              # Go up a level
              os.chdir('..')
        else:
          print("Date not available")
    else:
      print("Form not available.")
  
main()


