from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import time

START_URL= "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser= webdriver.Chrome("chromedriver")
browser.get(START_URL)
time.sleep(10)

def scrape():
    headers=["name","light-years_from_earth","planet_mass","stellar_magnitude","discovery_date"]
    planet_data=[]
    for i in range(0,440):
        soup=BeautifulSoup(browser.page_source,"html.parser")
        for ulTag in soup.find_all("ul",attrs={"class","exoplanet"}):
            liTags=ulTag.find_all("li")
            tempList=[]
            for index,liTag in enumerate(liTags):
                if index == 0:
                    tempList.append(liTag.find_all("a")[0].contents[0])
                else:
                    try:
                        tempList.append(liTag.contents[0])
                    except:
                        tempList.append(" ")
            planet_data.append(tempList)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
    with open("webScrapingData.csv","w") as f:
        csvWriter=csv.writer(f)
        csvWriter.writerow(headers)
        csvWriter.writerows(planet_data)

scrape()