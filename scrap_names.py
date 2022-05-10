from scrap import By, webdriver
from os import path

def get_names(field):
#example field : artificial-intelligence, machine-learning, cloud
    p = "data/company_names_by_field/"+ field + ".txt"

#look for data in data warehouse if it exsit, else scrap data
    if path.exists(p):
        print("saved names in " + p)
        with open(p, "r") as file:
            names = file.readlines()
            names = list(map(lambda x: x.replace(",\n",""), names))
    else:
        driver = webdriver.Chrome('chromedriver.exe')
        driver.get('https://craft.co/search?layout=grid&order=relevance&q=&tags%5B0%5D=' + field)

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

