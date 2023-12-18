import requests
from bs4 import BeautifulSoup
import re
import ast

def str_to_num(s):
    if s[-1].isalpha():
        num = s[:len(s)-1]
        char = s[len(s)-1:]
        int_num = float(num)
        if char=='M':
            int_num*=1000000
        elif char=='B':
            int_num*=1000000000
        elif char=='K':
            int_num*=1000
        return int(int_num)
    return int(s)

def pre_pro(s):
    arr_s = s.split(" ")
    return str_to_num(arr_s[0])


def porn_star_collect(url):
    bios = []
    features_n = []
    social_medias_n = []
    infos_n = []
    weekly = []
    monthly = []
    last = []
    yearly = []
    subs = []
    rq = requests.get(url).text
    soup = BeautifulSoup(rq,'lxml')

    # datas: model_rank, weekly_rank, monthly_rank, last_month, yearly_rank, video_views, subscribers
    datas = soup.find_all("span",class_="big")
    infos = soup.find_all("div",class_="infoPiece")
    social_medias = soup.find_all("a",class_="js-ckeckExternalSource")
    features = soup.find("div",class_="featuredIn")

    print(len(datas))
    print(len(infos))

    # some pages use bio some use about, so we need check here:
    bio = soup.find("div",attrs={"itemprop":"description"})
    if bio:
        b = bio.text.strip()
        print(b)
        bios.append(b)
    else:
        about = soup.find("section",attrs={"class":"aboutMeSection sectionDimensions"})
        if about:
            a = about.text.strip()
            print(a)
            bios.append(a)
        else:
            bios.append("NA")

    # nf is cleaned features
    if features:
        features = features.text.split(":")[1].split("\n")
        nf = []
        for f in features:
            if f.strip()!="":
                nf.append(f.strip())
        print("features in ",nf)
        features_n.append(nf)
    else:
        features_n.append("NA")

    # collection social medias info
    if social_medias:
        social_media_dict = {}
        for sm in social_medias:
            social_media_dict[sm.text.strip()] = sm['href']

        print(social_media_dict)
        social_medias_n.append(str(social_media_dict))
    else:
        social_medias_n.append("NA")

    # datas: model_rank, weekly_rank, monthly_rank, last_month, yearly_rank, video_views, subscribers
    for i in range(len(datas)):
        data = datas[i].text.strip()
        if data!='N/A':
            if i==1:
                weekly.append(int(data))
            elif i==2:
                monthly.append(int(data))
            elif i==3:
                last.append(int(data))
            elif i==4:
                yearly.append(int(data))
            elif i==6:
                subs.append(str_to_num(data))
        print(data)

    # store infos into a dict, 
    if infos:
        dict = {}
        for i in infos:
            txt = i.text.strip()
            arr = txt.split(":")
            arr[1] = arr[1].strip()
            dict[arr[0]] = arr[1]
        print(dict)
        infos_n.append(str(dict))
    else:
        infos_n.append("NA")
    
    return bios,features_n,social_medias_n,infos_n,weekly,monthly,last,yearly,subs

# testing code
""" print(dict)
str_dict = str(dict)
print("Orgin")
odict = ast.literal_eval(str_dict)
print(odict) """

#print(bio.text.strip())

porn_star_collect("https://www.pornhub.com/pornstar/eva-elfie")