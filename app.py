from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

urls = []
subjects = []
dates = []
froms = []
vias = []
contents = []

def search(link,subjects,dates,froms,vias,contents,urls):
    url = link
    
    req = requests.get(url).text
    soup = BeautifulSoup(req,'lxml')

    #print(soup.prettify())

    links = soup.find_all("a",attrs={"href":re.compile("^/circulars/"),"class":"usa-link"})
    names_list = []
    links_list = []

    for l in links:
        names_list.append(l.text)
        links_list.append("https://gcn.nasa.gov"+l.get("href"))
        urls.append("https://gcn.nasa.gov"+l.get("href"))
    
    for l in links_list:
        print("Extract Data from "+l+"...")
        subsearch(l,subjects,dates,froms,vias,contents)

def subsearch(link,subjects,dates,froms,vias,contents):
    url1 = link

    req1 = requests.get(url1).text
    soup1 = BeautifulSoup(req1,'lxml')

    links = soup1.find_all("div",attrs={"data-testid":"grid","class":"grid-col-fill"})
    code = soup1.find("code")
    print("Getting the data from "+link+"...")
    subjects.append(links[0].text)
    dates.append(links[1].text.split(" (")[0])
    froms.append(links[2].text)
    if len(links)==4:
        vias.append(links[3].text)
    else:
        vias.append('NA')

    #print(code.text)
    print("Getting the detailed info...")
    contents.append(code.text)
    #print(len(links))

link = "https://gcn.nasa.gov/circulars"
search(link,subjects,dates,froms,vias,contents,urls)

for i in range(2,353):
    link = "https://gcn.nasa.gov/circulars?page="+str(i)
    search(link,subjects,dates,froms,vias,contents,urls)

urls_pd = pd.Series(urls)
subjects_pd = pd.Series(subjects)
dates_pd = pd.Series(dates)
froms_pd = pd.Series(froms)
vias_pd = pd.Series(vias)
contents_pd = pd.Series(contents)


web_data = pd.concat([subjects_pd,dates_pd,froms_pd,vias_pd,contents_pd,urls_pd],axis=1)
web_data.columns = ['Subjects','Dates','From','Via','Contents','URLs']
print(web_data.head())
web_data.to_csv('nasa_gcn.csv',index=True)