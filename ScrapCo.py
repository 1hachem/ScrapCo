# get_contacts give name of company -> get contacts
# get_stats give name of comapny -> get statistics 
# get_names give name of field -> get statistics

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from os import path



##########################################################
def get_names(field):
#example field : artificial-intelligence, machine-learning, cloud
    p = "data/company_names_by_field/"+ field + ".txt"

#look for data in data lake if it exsit, else scrap data
    if path.exists(p):
        print("saved names in " + p)
        with open(p, "r") as file:
            names = file.readlines()
            names = list(map(lambda x: x.replace(",\n",""), names))
    else:
        #connect to driver
        driver = webdriver.Chrome('chromedriver.exe')
        driver.get('https://craft.co/search?layout=grid&order=relevance&q=&tags%5B0%5D=' + field)

        #scrap names (class name jDAm)
        names_ = driver.find_elements(by=By.CLASS_NAME, value='jDAmA')
        names = [i.text for i in names_]

        driver.close()
        
        #if data is scraped save it, else log that no data is saved
        if len(names) != 0:
            with open(p, "w") as file:
                file.write(",\n".join(names))

            print("saved names in " + p)
        else: 
            print("no companies found try another keyword")
        
    return names



#######################################################
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

########################################################
def get_contacts(company):
    
    p = "data/company_contacts/"+ company + ".csv"

    #check for data in data warehouse
    if path.exists(p):
        print("saved contacts in " + p)
    else:

        #connect to the chrome driver 
        driver = webdriver.Chrome('chromedriver.exe')
        driver.get('https://craft.co/' + company + '/executives')

        #scrap contacts by class name with (person css class name is _3zS68 on craft.co) 
        contacts_ = driver.find_elements(by=By.CLASS_NAME, value='_3zS68')
        contacts = [i.text for i in contacts_]

        #(linkedin contact css class name is _6rb73 on craft.co) 
        linkedin_ = driver.find_elements(by=By.CLASS_NAME, value='_6rb73')
        linkedin = [i.get_attribute('href') for i in linkedin_]

        #scrap postion
        position_ = driver.find_elements(by=By.CLASS_NAME, value='_3FhAT')
        position = [i.text for i in position_]

        driver.close() #close browser

        #text formating to save as .csv
        line = ""
        for i,j,k in zip(contacts, position, linkedin):
            line+= i.replace(",","|")+","+j.replace(",","|")+","+k.replace(",","|")+"\n"
        
        if len(line)!=0:
            with open(p, "w") as file:
                file.write("name, position, linkedin \n")
                file.write(line)
        
            print("saved contacts in " + p)
        else:
            print("no contact found")
