from scrap import By, webdriver
from os import path

#### name of company
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



