from scrap import By, webdriver
from os import path
import pandas as pd

  
def get_stats(company):

    p = "data/company_stats/" + company + "_0.csv"

    #check data in data warehouse
    if path.exists(p):
        print("saved stats in " + p)
    else:
        #connect to driver
        driver = webdriver.Chrome('chromedriver.exe')
        driver.get('https://craft.co/' + company + '/metrics')

        #scrap tables from webpage
        table = driver.find_elements(by=By.TAG_NAME, 
        value='table')
        
        #join the outerhtml source code of these tabels
        infos = "\n".join([i.get_attribute('outerHTML') for i in table])

        driver.close() #close browser

        tables = pd.read_html(infos) #use pandas to read these tables

        #save tables
        for i, t in enumerate(tables):
            df = pd.DataFrame(t)
            df.to_csv("data/company_stats/" + company  + f"_{i}.csv")

        print(f"saved {i+1} tables in " + p)



