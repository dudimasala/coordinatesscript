from geopy.geocoders import Nominatim
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common import exceptions
import time

class ScrapStreetBot:
    def __init__(self):
        self.driver = webdriver.Chrome('/Users/amitrajpal/Downloads/Instagram_bot/chromedriver') 
        self.geolocator = Nominatim(user_agent='coordinatefinder')
        self.access_website()
        hk_mini_district = self.get_mini_district_names()
        hk_streets = self.get_street_names()
        hk_street_with_coordinates = self.get_street_coordinates(hk_streets)
        print(self.order_street_name_with_mini_district(hk_mini_district, hk_street_with_coordinates))

        
    
    def access_website(self):
        self.driver.get('https://en.wikipedia.org/wiki/List_of_streets_and_roads_in_Hong_Kong')
        
    
    def get_mini_district_names(self):
        streetNames = WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, 'mw-headline')))
        streetText = []
        for i in streetNames:
            streetText.append(i.text)
            if(i.text == 'Sheung Shui'):
                streetText.append('Yuen Long')
        
        return streetText[4:-5]
    
    def get_street_names(self):
        finalStreetArray = []
        miniDistrictUl =  WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_all_elements_located((By.TAG_NAME, 'ul')))
        miniDistrictUl = miniDistrictUl[7:25]
        
        for i in miniDistrictUl:
            children = i.find_elements_by_xpath(".//*")
            childrentext = []
            for u in children: 
                if(u.text not in childrentext):
                    childrentext.append(u.text)
            
            finalStreetArray.append(childrentext)
            if(childrentext[-1] == "Wan Po Road"):
                finalStreetArray.append([])
                finalStreetArray.append(["Chung Yan Road", "Keung Shan Road", "Lantau Link", "Ngong Ping Road", "Sham Wat Road", "South Island Road", "Tai O Road", "Tung Chun Road"])
       
        return finalStreetArray 
    
    def get_street_coordinates(self, streets):
        streetCoordinateArray = []
        for i in streets:
            coordinates = []
            for u in i:
                location = self.geolocator.geocode(u + " Hong Kong")
                try:
                    try: 
                        print([u, location.latitude, location.longitude])
                        coordinates.append([u, location.latitude, location.longitude])    
                    except ConnectionError:
                        print([u, "street not found"])
                        coordinates.append(["coordinate not found"])                        
                except AttributeError:
                    print([u, "street not found"])
                    coordinates.append(["coordinate not found"])
            streetCoordinateArray.append(coordinates)
        
        return streetCoordinateArray    
    
    def order_street_name_with_mini_district(self, mini_dist, streets):
        streetDict = {}
        for i in range(len(mini_dist)):
            streetDict[mini_dist[i]] = streets[i]
        
        return streetDict    
            
        
        
        
        

if __name__ == "__main__":
    SortBot = ScrapStreetBot()