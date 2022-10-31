import time
time.sleep(10) # this i will delete, once i found some very good wait condition for other containers as "depens on" is not enough

from selenium import webdriver
from selenium.webdriver.common.by import By

import traceback
import asyncio
import sys
from urllib3.exceptions import MaxRetryError, NewConnectionError
from datetime import date

import db_script

driver: webdriver.Remote

try: 
    driver = webdriver.Remote(
        command_executor = 'http://selenium:4444',
        options=webdriver.ChromeOptions()
    )

    print("Connected to the remote browser...")
    
except (ConnectionRefusedError, MaxRetryError, NewConnectionError) as e:
    print(traceback.format_exc())
    print(f"{e} was raised during driver setup.\nCheck, if the Selenium container is running and then check, if you have the correct driver settings.")
    driver.quit()
    sys.exit(1)
    
except Exception as e:
    print(traceback.format_exc())
    print(f"{e} was raised. Something unexpected happen.")
    driver.quit()
    sys.exit(1)

async def get_elements(driver: webdriver.Remote, link: str, page: int, criteria=By.CLASS_NAME, cri_name="text-wrap") -> list:

    link_part1, link_part2= link.split("strana=1")
    link = f"{link_part1}strana={page}{link_part2}"
    print(f"Getting ads for site: {link}")
    driver.get(link)
    await asyncio.sleep(1)
    return driver.find_elements(criteria,cri_name)

async def main(area_link: str):

    page = 1
    
    get_elements_task = asyncio.create_task(get_elements(driver,area_link,page))
    elements = await get_elements_task

    while elements:
        print(f"Fetched {len(elements)} ads...")

        ads = set()
        for element in elements:
            try:
                price = (
                    element.find_element(By.CSS_SELECTOR,".norm-price.ng-binding")
                    .get_attribute("textContent").replace("\xa0", "")
                )

                ad_price = "".join(price)
                ad_price = int(ad_price[:-2]) if ad_price[-2:]=="Kč" else 0
                

                ad_id = (
                    element.find_element(By.TAG_NAME,"a")
                    .get_attribute("href")
                    .split("/")[-1]
                )
                
                ads.add((ad_id,ad_price))
                
                
            except Exception as e:
                print(traceback.format_exc()) # this is ok, not needed to crash the program, if I couldn´t access some particular ad attributes

                
        # I will pass the web page to the browser and then I will suspend it, so while it is loading, I can do something else
        page += 1
        get_elements_task = asyncio.create_task(get_elements(driver,area_link,page))
        
        # db_script.session.query(Ad_values), filter out those, where the recent one has the same price
        for ad in ads:
            latest_price_of_ad_by_ID = db_script.Ad_values.latest_price(ad[0])

            if latest_price_of_ad_by_ID is None or latest_price_of_ad_by_ID != ad[1]:
                
                db_script.session.merge(db_script.Ad_values(id = ad[0], price = ad[1], date=date.today()))
            
        db_script.session.commit()

        elements = await get_elements_task
        

if __name__ == "__main__":

    try:
        area_file = open("ad_areas.txt", "r")
        areas = area_file.readlines()
        print("Loaded the ad areas...")
        for area in areas:  
            print(f"Looking for ads in this area: {area}")      
            asyncio.run(main(area))

        print("All done...")
    finally:
        area_file.close()
        driver.quit()
        db_script.session.close()

    # maybe print the result in stdout



        
