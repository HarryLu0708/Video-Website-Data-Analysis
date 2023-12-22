import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from pornstar import porn_star_collect, str_to_num, pre_pro


# all links we need traverse
urls = []
urls.append('https://www.pornhub.com/pornstars')
for i in range(1,1700):
    url = "https://www.pornhub.com/pornstars?page="+str(i)
    urls.append(url)

#print(urls)


def overallSearch(url,index):
    print(f"--------------------------{index}------------------------------------")
    #url = 'https://www.pornhub.com/pornstars'
    rq = requests.get(url).text
    soup = BeautifulSoup(rq,'lxml')

    name_eles = soup.find_all("span",class_=re.compile("^modelName performerCardName"))
    name_eles_2 = soup.find_all("span",class_=re.compile("pornStarName performerCardName"))

    # majorpage info
    names = []
    links = []
    ranks = []
    videos = []
    views = []
    imgs = []
    verified = []
    awards = []

    # homepage info
    bios = []
    features_n = []
    social_medias_n = []
    infos_n = []
    weekly = []
    monthly = []
    last = []
    yearly = []
    subs = []

    performer_cards = soup.find_all("li",class_="pornstarLi performerCard")
    model_cards = soup.find_all("li",class_="modelLi performerCard")

    print(len(performer_cards))
    print(len(model_cards))

    trv = 0
    total_len = len(performer_cards)+len(model_cards)
    for card in performer_cards:
        print(f"-------------------------Collection Task {trv}/{total_len} in total-------------------------------")
        # find data
        name = card.find("span",class_="pornStarName performerCardName").text.strip()
        rank = card.find("span",class_="rank_number").text.strip()
        video = card.find("span", class_="videosNumber performerCount").text.strip()
        view = card.find("span", class_="viewsNumber performerCount").text.strip()
        link = "https://www.pornhub.com"+card.find("a")['href']
        img = card.find("img")['src']
        # check if she's a verified model or not/ check if she has any awards
        if card.find("span",{"data-title":"Verified Model"}):
            verified.append(True)
        else:
            verified.append(False)
        if card.find("i",{"data-title":"Pornhub Awards Winner"}):
            awards.append(True)
        else:
            awards.append(False)
        # append elements
        names.append(name)
        links.append(link)
        ranks.append(rank)
        videos.append(pre_pro(video))
        views.append(pre_pro(view))
        imgs.append(img)
        # print
        #print(name,rank,video,view,link,img)
        bios_n,features_n_n,social_medias_n_n,infos_n_n,weekly_n,monthly_n,last_n,yearly_n,subs_n=porn_star_collect(link)
        bios+=bios_n
        features_n+=features_n_n
        social_medias_n+=social_medias_n_n
        infos_n+=infos_n_n
        weekly+=weekly_n
        monthly+=monthly_n
        last+=last_n,
        yearly+=yearly_n
        subs+=subs_n
        trv+=1


    for card in model_cards:
        print(f"-------------------------Collection Task {trv}/{total_len} in total-------------------------------")
        # find data
        name = card.find("span",class_="modelName performerCardName").text.strip()
        rank = card.find("span",class_="rank_number").text.strip()
        video = card.find("span", class_="videosNumber performerCount").text.strip()
        view = card.find("span", class_="viewsNumber performerCount").text.strip()
        link = "https://www.pornhub.com"+card.find("a")['href']
        img = card.find("img")['src']
        # check if she's a verified model or not/ check if she has any awards
        if card.find("span",{"data-title":"Verified Model"}):
            verified.append(True)
        else:
            verified.append(False)
        if card.find("i",{"data-title":"Pornhub Awards Winner"}):
            awards.append(True)
        else:
            awards.append(False)
        # append elements
        names.append(name)
        links.append(link)
        ranks.append(rank)
        videos.append(pre_pro(video))
        views.append(pre_pro(view))
        imgs.append(img)
        # print
        #print(name,rank,video,view,link,img)
        bios_n,features_n_n,social_medias_n_n,infos_n_n,weekly_n,monthly_n,last_n,yearly_n,subs_n=porn_star_collect(link)
        bios+=bios_n
        features_n+=features_n_n
        social_medias_n+=social_medias_n_n
        infos_n+=infos_n_n
        weekly+=weekly_n
        monthly+=monthly_n
        last+=last_n,
        yearly+=yearly_n
        subs+=subs_n
        trv+=1

    pd_names = pd.Series(names)
    pd_links = pd.Series(links)
    pd_ranks = pd.Series(ranks)
    pd_videos = pd.Series(videos)
    pd_views = pd.Series(views)
    pd_imgs = pd.Series(imgs)
    pd_verified = pd.Series(verified)
    pd_awards = pd.Series(awards)

    # homepage info
    pd_bios = pd.Series(bios)
    pd_features_n = pd.Series(features_n)
    pd_social_medias_n = pd.Series(social_medias_n)
    pd_infos_n = pd.Series(infos_n)
    pd_weekly = pd.Series(weekly)
    pd_monthly = pd.Series(monthly)
    pd_last = pd.Series(last)
    pd_yearly = pd.Series(yearly)
    pd_subs = pd.Series(subs)

    file = pd.concat([
        pd_names,
        pd_links,
        pd_ranks,
        pd_videos,
        pd_views,
        pd_imgs,
        pd_verified,
        pd_awards,
        pd_bios,
        pd_features_n,
        pd_social_medias_n,
        pd_infos_n,
        pd_weekly,
        pd_monthly,
        pd_last,
        pd_yearly,
        pd_subs 
    ],axis=1)

    print()
    print(file.head())
    file.to_csv(f"pornstars/pornstars_{index}.csv")
    print("Finished processing!")
    print("--------------------------Finished------------------------------------")
    return file

total_table = pd.read_csv("test_concat_data.csv")
#subtable = pd.read_csv("pornstars/pornstars_100.csv")
files = pd.DataFrame()
for i in range(247,500):
    file = overallSearch(urls[i],i)
    files = pd.concat([files,file],axis=0,ignore_index=True)
    print("-----------------------HEAD------------------------")
    print(files.head())
files.columns = [
        "Names",
        "Links",
        "Ranks",
        "Total Videos",
        "Total Views",
        "Images",
        "Verified",
        "Pornhub Award",
        "Abouts",
        "Featured In",
        "Social Medias",
        "Detailed Infos",
        "Weekly Ranks",
        "Monthly Rank",
        "Last Month Rank",
        "Yearly Rank",
        "Subscribers"
    ]
total_table = pd.concat([total_table,files],axis=0,ignore_index=True)
#total_table = total_table.drop(['unknow'],axis=1)
total_table = total_table.drop(['Unnamed: 0'],axis=1)
print(total_table.head())
#files = overallSearch(urls[100],100)






#files = pd.concat([total_table,files],axis=0,ignore_index=True)
#files.drop(['Unnamed: 0'],axis=1)
total_table.to_csv("concat_data5.csv")
# print(total_table.head())


"""     print()
    print(names)
    print(ranks)
    print(videos)
    print(views)
    print(img)
    print(links)
    print(awards)
    print(verified)
    print()
    print(len(names))
    print(len(ranks))
    print(len(videos))
    print(len(views))
    print(len(imgs))
    print(len(links))
    print(len(awards))
    print(len(verified))
    print()
    print(len(bios))
    print(len(features_n))
    print(len(social_medias_n))
    print(len(infos_n))
    print(len(weekly))
    print(len(monthly))
    print(len(last))
    print(len(yearly))
    print(len(subs)) """

""" def porn_star_collect(url):
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
        if i==1:
            weekly.append(data)
        elif i==2:
            monthly.append(data)
        elif i==3:
            last.append(data)
        elif i==4:
            yearly.append(data)
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
        infos_n.append("NA") """



""" bios = []
features_n = []
social_medias = []
infos_n = []
weekly = []
monthly = []
last = []
yearly = []
subs = [] """