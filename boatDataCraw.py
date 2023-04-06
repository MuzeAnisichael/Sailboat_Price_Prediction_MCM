import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import re

def count_elements(elements):
    # 定义一个空字典，用于存储每个元素的出现次数
    counts = {}
    
    for element in elements:
        if element in counts:
            counts[element] += 1
        else:
            counts[element] = 1
    
    # 计算元素总数
    total_count = sum(counts.values())
    
    result = {"elements": counts, "total_count": total_count}
    
    return result


os.environ['NO_PROXY'] = 'sailboatdata.com'

def clean_data(value):
    return re.sub(r'[^0-9.]', '', value)

def get_sailboat_data(boat_name):
    base_url = "https://sailboatdata.com"
    search_url = f"{base_url}/sailboat?filter%5Bname%5D={boat_name.replace(' ', '+')}&paginate=25&units=imperial&sort=name"
    print(search_url)

    try:
        search_response = requests.get(search_url, timeout=120)
    except requests.exceptions.Timeout:
        print(f"搜索请求超时：{boat_name}")
        return None

    if search_response.status_code == 200:
        search_soup = BeautifulSoup(search_response.text, "html.parser")
        search_result = search_soup.find("div", class_="table-responsive")
        if search_result:
            boat_link_element = search_result.find("a")
            if boat_link_element is None:
                print(f"未找到船型链接：{boat_name}")
                return None

            boat_link = boat_link_element["href"]
            boat_url = f"{boat_link}?units=imperial"
            print(boat_url)

            try:
                boat_response = requests.get(boat_url, timeout=120)
            except requests.exceptions.Timeout:
                print(f"船型信息请求超时：{boat_name}")
                return None

            if boat_response.status_code == 200:
                boat_soup = BeautifulSoup(boat_response.text, "html.parser")
                boat_info = {}
                boat_info["Name"] = boat_name

                rows = boat_soup.find_all("div", class_=["row", "row first-row"])
                for row in rows:
                    labels = row.find_all("div", class_="sailboatdata-label")
                    data = row.find_all("div", class_="sailboatdata-data col-xs-6 col-sm-3")

                    if len(labels) == len(data):
                        for i in range(len(labels)):
                            label = labels[i].text.strip()
                            if label == "S.A. (reported):":
                                value = data[i].get_text(strip=True, separator=" ")
                            else:
                                value = data[i].text.strip()
                            boat_info[label] = clean_data(value)

                return boat_info
            else:
                print(f"请求失败，状态码：{boat_response.status_code}")
                return None
        else:
            print(f"未找到船型：{boat_name}")
            return None
    else:
        print(f"请求失败，状态码：{search_response.status_code}")
        return None

data1 = pd.read_excel("2023_MCM_Problem_Y_Boats.xlsx" , sheet_name = "Catamarans")
variant_mono = pd.DataFrame(data1).iloc[:,1].str.rstrip()
variant_counts = count_elements(variant_mono)
boat_names = [str(key) for key in variant_counts['elements'].keys()]
print(boat_names) 
suc = 0
fai = 0
ttl = len(boat_names)
#boat_names = ["X4.6"]

if __name__ == "__main__":
    #boat_names = ["51 Cruiser", "Catalina 22", "Beneteau Oceanis 45", "46", "Sun Odyssey 389"]

    with open("sailboat_data.txt", "w") as f:
        for boat_name in boat_names:
            boat_data = get_sailboat_data(boat_name)
            if boat_data:
                suc = suc + 1
                print(fai+suc,"/",ttl,"succeed!")
                f.write(f"boat: {boat_name}\n")
                for key, value in boat_data.items():
                    f.write(f"{key}: {value}\n")
                f.write("\n")
            else:
                fai = fai + 1
                print(fai+suc,"/",ttl,"failed!")
                f.write(f"boat: {boat_name} failed\n\n")

print(suc)
print(fai)
