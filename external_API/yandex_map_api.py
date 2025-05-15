# Здесь через Яндекс карты будем по адресу получать изображение
import requests

GeoCode_Server = "https://geocode-maps.yandex.ru/v1/"
GeoCode_Api_Key = "YOUR_API_GeoCode_Key"

StaticMap_Api_Key = "YOUR_API_StaticMap_Key"
StaticMape_Server = "https://static-maps.yandex.ru/v1"

def get_coord_at_address(address):
    """" Возвращает координаты по адресу (w,h) """

    params = {
        "apikey": GeoCode_Api_Key,
        "geocode": address,
        "format": "json"
    }

    res = requests.get(GeoCode_Server, params=params).json()
    try:
        main = res['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
        coords = main['Point']["pos"].replace(' ', ',')
        return coords
    
    except Exception:
        return None



def get_city_at_address(address):
    """" Возвращает город по адресу """
    params = {
        "apikey": GeoCode_Api_Key,
        "geocode": address,
        "format": "json"
    }

    res = requests.get(GeoCode_Server, params=params).json()
    try:
        main = res['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
        try:
            city = main["metaDataProperty"]['GeocoderMetaData']["AddressDetails"]["Country"]["AdministrativeArea"]["SubAdministrativeArea"]["Locality"]["LocalityName"]
        except Exception:
            city = main["metaDataProperty"]['GeocoderMetaData']["AddressDetails"]["Country"]["AdministrativeArea"]['AdministrativeAreaName']
        return city
    
    except Exception:
        return None



def get_img_at_coord(our_coords=None, bc_marks=None):
    """" Возвращает ссылку на картинку по координатам """
    spn = '0.1,0.1'
    coord = '37.617700,55.755863'
    all_marks = []

    if our_coords:
        coord = our_coords
        all_marks.append(f"{coord},pm2bll")
        spn = "0.002,0.002"

    if bc_marks is not None:
        print('Добавляем метки ByteCraft пунктам')
        for i, m in enumerate(bc_marks):
            bc_marks[i] = f"{m},pm2gnm"
            print(f"Метка : {m}")
        all_marks.extend(bc_marks)

    params = {
        "apikey": StaticMap_Api_Key,
        "ll": coord,
        "spn": spn,
        "format": "json",
        "lang": "ru_RU",
        "size": "600,450",
        "theme": "dark",
        "pt": "~".join(all_marks)
    }
    res = requests.get(StaticMape_Server, params=params).url
    return res
