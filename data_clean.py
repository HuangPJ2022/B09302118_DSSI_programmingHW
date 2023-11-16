import pandas as pd
import numpy
import re
import openpyxl

def clean_price(price_li):
    new_price_li = []
    for idx, price in enumerate(price_li):
        pure_price = re.sub(r'\D', '', price)
        pure_price = int(pure_price)
        new_price_li.append(pure_price)
    
    return(new_price_li)

def clean_dis(dis_li):
    new_dis_li = []
    for idx, text in enumerate(dis_li):

        to_km = float(0)
        if text.find(" km from center") == -1:
            m = re.sub(r'\D', '', text)
            to_km = float(m) / 1000
        else:
            text = text.replace("km from center","")
            to_km = float(text)
        
        new_dis_li.append(to_km)
    
    return(new_dis_li)

def data_cleaning(location, checkIn):
    excel_name = f'{location}_hotels_list.xlsx'       
    df = pd.read_excel(excel_name)

    df.insert(2, "price", clean_price(df.price_c.values.tolist()))
    df = df.drop(["price_c"], axis = 1) 

    df.insert(4, "distance", clean_dis(df.distance_c.values.tolist()))
    df = df.drop(["distance_c"], axis = 1)

    df['rating'] = df['rating'].astype(float)

    df['comment'] = df['comment'].astype(str)

    #改寫
    clean_excel_name = f"{location}_hotels_list_clean_{checkIn}.xlsx"
    df.to_excel(clean_excel_name, index=False)


"""if __name__ == '__main__':
    location = "Taipei"
    checkIn = "2023-11-16"
    data_cleaning(location, checkIn)"""

