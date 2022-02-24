import requests
from bs4 import BeautifulSoup
import lxml
from fake_useragent import UserAgent
import csv
import datetime
import os

class Parser:
    def __init__(self) -> None:
        self.ip = os.getenv("ip")
        self.password = os.getenv("password")
        self.login = os.getenv("login")
        self.url = "https://www.bls.gov/regions/midwest/data/AverageEnergyPrices_SelectedAreas_Table.htm"
        self.ua = UserAgent()
        self.headers = {"accept": "*/*", "user-agent": self.ua.random}
        self.proxies = {"https": f"http://{self.login}:{self.password}@{self.ip}"}
        self.date = datetime.datetime.now().strftime("%d_%m_%Y_%H:%M")

    def dowmload_page(self):
        response = requests.get(url=self.url,
                                headers=self.headers,
                                proxies=self.proxies)
        return response.text
            
    
    
    def parse_table(self, table_block: BeautifulSoup):
        all_info = []
        table_name = table_block.find(class_="tableTitle").text.strip()
        second_line_head = ["Area"] + table_block.find("thead").find_all("tr")[-1].text.strip().split("\n")
        with open(f"data/{table_name}_{self.date}.csv", "a") as file:
            writer = csv.writer(file)
            writer.writerow(second_line_head)    
            all_area = table_block.find("tbody").find_all("tr")
            for area in all_area:
                area_name = area.find("th").text.strip()
                all_info.append(area_name)
                for i in area.find_all("td"):
                    if i.find("a"):
                        value = i.find("a").get("href")
                    elif i.text:
                        value = i.text
                    else:
                        value = None
                    
                    all_info.append(value)
                writer.writerow(all_info)
                all_info.clear()
        
    
    def find_tables(self):
        soup = BeautifulSoup(self.dowmload_page(), "lxml")
        tables = soup.find_all("table", class_="regular")
        for table in tables:
            self.parse_table(table)
            
    def create_data(self):
        if not os.path.exists("data"):
            os.mkdir("data")

    
    def main(self):
        self.create_data()
        self.find_tables()
 
if __name__ == "__main__":
    Parser().main()
