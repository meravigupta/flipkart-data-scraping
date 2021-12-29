import pandas as pd
import requests
from bs4 import BeautifulSoup
from glob import glob
from datetime import datetime
import re
inputfile = ("C:/Users/Prabhat/Documents/ravi_test/input_categories.xlsx")
inputfile
indata = pd.read_excel(inputfile)
categories = indata["categories"].to_list()

columns = ["ProductName","Price","OrigionalPrice","Discount","Size"]

for category in categories:
    search_url = "https://www.flipkart.com/search?q="+category.lower().replace(" ","%20")+"&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    res = requests.get(search_url)
    html = res.content
    f = open("C:/Users/Prabhat/Documents/ravi_test/"+category+".html","wb")
    f.write(html)
    f.close()
files = glob("C:/Users/Prabhat/Documents/ravi_test/*.html")
for file in files:
    output = []
    print(file)
    f = open(file,"rb")
    content = f.read().decode("utf-8")
    print(type(content))
    f.close()
    soup = BeautifulSoup(content)
    page_tag = soup.find("div","_1YokD2 _2GoDe3 col-12-12")
    products_rows = page_tag.find_next_siblings("div","_1AtVbE col-12-12")
    for row in products_rows:
        products = row.findAll("div",{"data-id":re.compile(".*")})

        for product in products:
            Product_name = product.find("a","s1Q9rs")["title"]
            Price = product.find("div","_30jeq3").text.strip() 
            try : 
                OrigionalPrice = product.find("div","_3I9_wc").text.strip()
            except :
                OrigionalPrice = None
            try : 
                Discount = product.find("div","_3Ay6Sb").text.strip()
            except :
                Discount = None
            try :
                Size = product.find("div","rcweVK").text.strip()
            except :
                Size = None
            out_row = [Product_name,Price,OrigionalPrice,Discount,Size]
            output.append(out_row)
    outfile = file.replace(".html",".xlsx")
    out_data = pd.DataFrame(output,columns=columns)
    out_data.to_excel(outfile,index=False)    