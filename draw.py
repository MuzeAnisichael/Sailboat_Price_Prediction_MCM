import openpyxl
import re

# 打开Excel文件
wb = openpyxl.load_workbook('example.xlsx')
# 选择工作表
ws = wb['Catamarans']

# 打开txt文件
with open('sailboat_data2.txt', 'r') as f:
    data = f.read()

# 按照boat:分割txt文档
boats = re.split('boat:\s', data)

print(boats)
print('|')

# 遍历每个boat
for boat in boats:
        # 提取当前boat对应的信息
    match = re.search('^([^\n]*)\n', boat)

    print(boat)
    print('|')
    print(match)
    print('|')
    if match:
        boat_info = match.group(1)
        print(f'Boat: {boat_info}')
        print('|')  # 添加输出语句
    else:
        boat_info = None
        print('boat_infoNone')
        print('|')

    # 提取LWL::、S.A. (reported)::和Fuel::后的数值信息
    lwl_match = re.search('LWL::\s(\d+\.\d+)\n', boat)
    if lwl_match:
        lwl = float(lwl_match.group(1))
        print(f'LWL: {lwl}')  # 添加输出语句
        print('|')
    else:
        lwl = 0
        print('lwl0')
        print('|')

    bm_match = re.search('Beam::\s(\d+\.\d+)\n', boat)
    if bm_match:
        bm = float(bm_match.group(1))
        print(f'Beam: {bm}')  # 添加输出语句
        print('|')
    else:
        bm = 0
        print('bm0')
        print('|')

    sa_match = re.search('S\.A\. \(reported\)::\s(\d+\.\d+)\n', boat)
    if sa_match:
        sa = float(sa_match.group(1))
        print(f'SA: {sa}')  # 添加输出语句
        print('|')
    else:
        sa = 0
        print('sa0')
        print('|')

    fuel_match = re.search('Fuel::\s(\d+\.\d+|\d+)\n', boat)
    if fuel_match:
        fuel = float(fuel_match.group(1))
        print(f'Fuel: {fuel}')  # 添加输出语句
        print('|')
    else:
        fuel = 0
        print('fuel0')
        print('|')


    # 在Excel中查找对应的行，并写入数据
    for row in ws.iter_rows(min_row=2, max_col=20):
        if row[1].value == boat_info:
            row[8].value = lwl
            row[9].value = sa
            row[10].value = fuel
            row[11].value = bm

# 保存Excel文件
wb.save('example.xlsx')
