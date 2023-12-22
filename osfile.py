import pandas as pd
import os

origin_data = pd.read_csv("concat_data4.csv")

# 200-247
files_need_to_process = []

for i in range(200,247):
    s = "pornstars/pornstars_"+str(i)+".csv"
    files_need_to_process.append(s)

# reading data
process_data = pd.read_csv(files_need_to_process[0])
i = 0

for file in files_need_to_process:
    data = pd.read_csv(file)
    process_data = pd.concat([process_data,data],axis=0,ignore_index=True)
    print(f"--------------------Process file {i}----------------------")
    i+=1


# concat data
process_data.columns = [
        "unknow",
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
origin_data = pd.concat([origin_data,process_data],axis=0,ignore_index=True)
total_table = origin_data.drop(['unknow'],axis=1)
total_table = total_table.drop(['Unnamed: 0'],axis=1)
print(total_table.head())
total_table.to_csv("test_concat_data.csv")


