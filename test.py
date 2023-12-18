from bs4 import BeautifulSoup
import requests
import re

url1 = "https://gcn.nasa.gov/circulars/35209"

req1 = requests.get(url1).text
soup1 = BeautifulSoup(req1,'lxml')

links = soup1.find_all("div",attrs={"data-testid":"grid","class":"grid-col-fill"})
code = soup1.find("code")
for l in links:
    print(l.text)

print(code.text)
print(len(links))



