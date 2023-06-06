import requests

# Store the area names and data
sarea_list = None
data_list = None


def getInfo() -> None:
    global sarea_list, data_list
    # Get data from TCGB website
    url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
    response = requests.get(url)
    if response.status_code == 200:
        print("下載成功")
    
    data_list = response.json()
    # Get all available areas
    sarea_temp = set()
    for item in data_list:
        sarea_temp.add(item["sarea"])
    sarea_list = sorted(list(sarea_temp))
    

def getInfoFromArea(areaName, keyword="") -> list:
    '''
    filter_data = []
    for data in data_list:
        if data["sarea"] == areaName:
            if (keyword == None) or (keyword in data["sna"]):
                filter_data.append(data)
    '''
    # filter_data = filter(lambda data: data["sarea"] == areaName, data_list)
    filter_data = filter(lambda data: (data["sarea"] == areaName) and (keyword in data["sna"]), data_list)
    return list(filter_data)

def filter_sbi_warning_data(area_data, numbers) -> list:
    filter_data = filter(lambda n: n['sbi'] <= numbers, area_data)
    return list(filter_data)


def filter_bemp_warning_data(area_data, numbers) -> list:
    filter_data = filter(lambda n: n['bemp'] <= numbers, area_data)
    return list(filter_data)


getInfo()
