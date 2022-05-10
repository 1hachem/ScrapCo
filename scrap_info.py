from scrap import By, webdriver
from os import path
import pandas as pd

  
def get_stats(company):

    p = "data/company_stats/" + company + "_0.csv"

    #check data in data warehouse
    if path.exists(p):
        print("saved stats in " + p)
    else:

        driver = webdriver.Chrome('chromedriver.exe')
        driver.get('https://craft.co/' + company + '/metrics')


        table = driver.find_elements(by=By.TAG_NAME, 
        value='table')
            
        infos = "\n".join([i.get_attribute('outerHTML') for i in table])

        driver.close()

        tables = pd.read_html(infos)

        for i, t in enumerate(tables):
            df = pd.DataFrame(t)
            df.to_csv("data/company_stats/" + company  + f"_{i}.csv")

        print(f"saved {i} tables in " + p)



