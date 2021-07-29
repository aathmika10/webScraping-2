from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import time
import requests

START_URL= "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser= webdriver.Chrome("chromedriver")
browser.get(START_URL)
time.sleep(10)

headers=["name","light-years_from_earth","planet_mass","stellar_magnitude","discovery_date","hyperlink","planet_type","planet_radius","orbital_radius","orbital_period","eccentricity"]
planet_data=[]
new_planet_data=[]

def scrape():
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
            hyperlinkLiTag=liTags[0]
            tempList.append("https://exoplanets.nasa.gov"+hyperlinkLiTag.find_all("a",href=True)[0]["href"])
            planet_data.append(tempList)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        print(f"{i} page 1 is done")

def scrapeMoreData(hyperlink):
    try:
        page=requests.get(hyperlink)
        soup=BeautifulSoup(page.content,"html.parser")
        tempList=[]
        for trTag in soup.find_all("tr",attrs={"class":"fact_row"}):
            tdTags=trTag.find_all("td")
            for tdtag in tdTags:
                try:
                    tempList.append(tdtag.find_all("div",attrs={"class":"value"})[0].contents[0])
                except:
                    tempList.append("")
        new_planet_data.append(tempList)
    except:
        time.sleep(1)
        scrapeMoreData(hyperlink)

scrape()

for index,data in enumerate(planet_data):
    scrapeMoreData(data[5])
    print(f"{index+1} page 2 is done")

final_Planet_Data=[]
for index,data in enumerate(planet_data):
    new_planet_data_element=new_planet_data[index]
    new_planet_data_element=[elem.replace("\n","")for elem in new_planet_data_element]
    new_planet_data_element=new_planet_data_element[:7]
    final_Planet_Data.append(data+new_planet_data_element)

with open("webScrapingData-2.csv","w") as f:
        csvWriter=csv.writer(f)
        csvWriter.writerow(headers)
        csvWriter.writerows(final_Planet_Data)