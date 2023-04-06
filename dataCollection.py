import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
os.environ['NO_PROXY'] = 'sailboatdata.com'

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

data1 = pd.read_excel("2023_MCM_Problem_Y_Boats.xlsx" , sheet_name = "Monohulled")
data2 = pd.read_excel("2023_MCM_Problem_Y_Boats.xlsx" , sheet_name = "Catamarans")

variant_mono = data1.values[:,1]
variant_cata = data2.values[:,1]
make_mono = pd.DataFrame(data1).iloc[:,4].str.rstrip()
make_cata = pd.DataFrame(data2).iloc[:,4].str.rstrip()


variant_ttl = variant_mono
#ariant_ttl.extend(variant_cata)


variant_counts1 = count_elements(variant_ttl)
make_counts1 = count_elements(make_cata)

print(make_counts1)
print(len(make_counts1['elements']))

make_list = [str(key) for key in make_counts1['elements'].keys()]
print(make_list) 

for i in make_list:
	print(i)


market_caps = {}
for symbol in make_list:
    url = f'https://finance.yahoo.com/quote/{symbol}/key-statistics?p={symbol}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    market_cap = soup.find('span', string='Market cap').find_next('span').text
    market_caps[symbol] = market_cap

print(market_caps)




'''
print("\n(1)全部数据：")
print(data.values)
 
print("\n(2)第2行第3列的值：")
print(data.values[1,2])
 
print("\n(3)第3行数据：")
print(data.values[2])
 
print("\n(4)获取第2、3行数据：")
print(data.values[[1,2]])
 
print("\n(5)第2列数据：")
print(data.values[:,1])
 
print("\n(6)第2、3列数据：")
print(data.values[:,[1,2]])
 
print("\n(7)第2至4行、第3至5列数据：")
print(data.values[1:4,2:5])
'''




'''
def get_market_cap(stock_symbol):
    url = f"https://finance.yahoo.com/quote/{stock_symbol}"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        market_cap_element = soup.find("td", {"data-test": "MARKET_CAP-value"})
        if market_cap_element:
            market_cap = market_cap_element.find("span").text
            return market_cap
        else:
            return None
    else:
        print(f"请求失败，状态码：{response.status_code}")
        return None

if __name__ == "__main__":
    stock_symbol = "AAPL"  # 以苹果公司为例
    market_cap = get_market_cap(stock_symbol)
    if market_cap:
        print(f"{stock_symbol} 的市值为：{market_cap}")
    else:
        print(f"无法获取 {stock_symbol} 的市值")
'''



