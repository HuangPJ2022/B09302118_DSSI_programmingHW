from playwright.sync_api import sync_playwright
import playwright
import pandas as pd
import openpyxl
import time

def process_time(start):
    now = time.time()
    return(now - start)


def get_num_pages(totalHotel):
    beforePages = totalHotel.find("…")
    afterPages = totalHotel.find("Showing")

    howManyPages = totalHotel[beforePages + 1 : afterPages]
    howManyPages = howManyPages.replace(" ", "")
    howManyPages = howManyPages.replace("\n", "")
    return(howManyPages)

def scrap(location, checkIn, checkOut, start):

    with sync_playwright() as p:

        #page_url = f'https://www.booking.com/searchresults.en-us.html?checkin={checkIn}&checkout={checkOut}&selected_currency=TWD&ss=London&ssne=London&ssne_untouched=London&lang=en-us&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure'

        page_url = f'https://www.booking.com/searchresults.en-us.html?checkin={checkIn}&checkout={checkOut}&lang=en-us&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure'

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(page_url, timeout=60000)
        
        page.wait_for_selector('input[name=\"ss\"]')
        page.click('input[name=\"ss\"]')
        #page.locator('input[name=\"ss\"]').fill(location)
        
        with page.expect_navigation():
            page.keyboard.type(location)
            with page.expect_request_finished():
                page.press('input[name=\"ss\"]', 'Enter')

        totalHotel = page.locator("//div[@id='bodyconstraint-inner']").inner_text(timeout = 0)
        howManyPages = int(get_num_pages(totalHotel))

        hotels_list = []
        for loop_count in range(1, howManyPages):
            page.wait_for_selector('//div[@data-testid="property-card"]')
            hotels = page.locator('//div[@data-testid="property-card"]').all()
            
            hotel_count = 0
            for hotel in hotels:
                hotel_count += 1
                print(loop_count, hotel_count)
                hotel_dict = {}
                hotel_dict['name'] = hotel.locator('//div[@data-testid="title"]').inner_text()
                hotel_dict['location'] = hotel.locator('//span[@data-testid="address"]').inner_text()
                hotel_dict['price_c'] = hotel.locator('//span[@data-testid="price-and-discounted-price"]').inner_text()

                try:
                    hotel_dict['rating'] = hotel.locator('//div[@data-testid="review-score"]/div[1]').inner_text(timeout = 5000)
                except playwright._impl._api_types.TimeoutError:
                    hotel_dict['rating'] = "0"

                hotel_dict['distance_c'] = hotel.locator('//span[@data-testid="distance"]').inner_text()
                
                if hotel_dict['rating'] == "0":
                    hotel_dict['comment'] = "No Comment Yet."
                else:
                    try:
                        hotel_dict['comment'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[1]').inner_text(timeout = 5000)
                    except playwright._impl._api_types.TimeoutError:
                        hotel_dict['comment'] = "No Comment Yet or Cannot be achieved."
                
                

                hotels_list.append(hotel_dict)
            print(f"complete {loop_count} pages with {process_time(start)}")

            if loop_count > 4 and process_time(start) > 90:
                break
            else:
                nextPage = page.get_by_role("button", name = "Next page")
                nextPage.click(timeout = 0)
                nextPage.wait_for(state = "attached")
        
        df = pd.DataFrame(hotels_list)
        excel_name = f'{location}_hotels_list.xlsx'
        df.to_excel(excel_name, index=False)
        
        browser.close()

"""if __name__ == '__main__':
    scrap("Taichung", "2023-11-17", "2023-11-18")"""



