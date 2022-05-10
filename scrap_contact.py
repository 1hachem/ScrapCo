from scrap import By, webdriver
from os import path

#### name of company
def get_contacts(company):
    
    p = "data/company_contacts/"+ company + ".csv"

    #check for data in data warehouse
    if path.exists(p):
        print("saved contacts in " + p)
    else:
        driver = webdriver.Chrome('chromedriver.exe')
        driver.get('https://craft.co/' + company + '/executives')

        contacts_ = driver.find_elements(by=By.CLASS_NAME, value='_3zS68')
        contacts = [i.text for i in contacts_]

        linkedin_ = driver.find_elements(by=By.CLASS_NAME, value='_6rb73')
        linkedin = [i.get_attribute('href') for i in linkedin_]

        position_ = driver.find_elements(by=By.CLASS_NAME, value='_3FhAT')
        position = [i.text for i in position_]

        driver.close()
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



