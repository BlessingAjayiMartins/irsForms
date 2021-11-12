

WELCOME TO IRS-FORM-SCRAPER

THIS PROJECT WAS PUT TOGETHER SO YOU CAN DO TWO THINGS:

  1. SEARCH FOR AN IRS FORM AT YOU TERMINAL(INTERNET ACCESS NEEDED) AND RECIEVE DETAILS AVAILABLE SUCH AS THE NAME, TITLE, AND RANGE OF YEARS THE FORM EXISTED... 
 
      {
        "form_number": Form W-2,
        "form_title" : "Wage and Tax Statement (Info Copy only)",
        "min_year" : 1954,
        "max_year" : 2021
      }
  
  YOU WILL BE PROMPTED TO ENTER A LIST OF FROMS YOU WOULD LIKE DETAILS ON.
    - MAKE SURE YOU TYPE THE EXACT FORM/s YOUR'RE LOOKING FOR. (CASE SENSITIVE)
    - IF YOU WANT TO TYPE IN MULTIPLE FORMS MAKE SURE TO SEPERATE EACH FORM BY A COMMA ","...

      EX:
        "Form W-2,Publ 1,Publ 1 (AR)"

      All INQUERIES WILL BE AVAILABLE IN THE CURRENT DIRECTORY UNDER "result.json"


  2. DOWNLOAD FORMS IN A SUBDIRECTORY GIVEN A SPECIFIC RANGE...

    YOU WILL BE PROMPTED TO ENTER A FORM NAME.
      - MAKE SURE YOU TYPE THE EXACT FORM YOUR'RE LOOKING FOR. (CASE SENSITIVE)
      EX:
        Form W-2
    
    NEXT, YOU WILL BE PROMPTED TO ENTER THE YEAR OR THE RANGE OF YEARS YOU WOULD LIKE TO DOWNLOAD (IF FORM AVAILABLE).
    PLEASE ENTER DATE/RANGE IN ONE OF TWO FORMATS. "XXXX" OR "XXXX-XXXX"
      EX:
        1945-2021
      EX:
        2017


THIS PROJECT WAS BUILT USING PYTHON 3.10.0
LIBRARIES USED ARE ALL PUBLIC LIBRARIES


OVERVIEW AND FEEBACK ON PROJECT:

  I created a data stucture named "database" and cached it to a local directory. While this takes up space the lookup time is minimal.

  I would've liked to implement a cache with a validator that would check if a form exists. That way you dont have to scrape and download the data at the beginning of every run. This would have saved network bandwith and requests. I chose not to because the idea came after I already structured my data and implemented logic.

  Overall it was a good coding experience

  Biggest challenge was brushing up on my python(practically re-learned python for this project) and finding a way to paginate this particular website.

  Hope the code is to your liking!