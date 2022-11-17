import requests
from bs4 import BeautifulSoup
import csv
import datetime
from selenium import webdriver

browser = webdriver.Chrome()
list_gallary_img = []
#Создание файла для cvs
cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")#Получить текущую дату
with open(f"protorg_{cur_time}.csv", "w") as file:#Открыть файл для записи
    writer = csv.writer(file)#Возвращает объект записи, ответственный за преобразование пользовательских данных в строки с разделителями в данном файлоподобном объект

    writer.writerow(#Создать следующие столбцы
        (
            "Название товара или услуги",
            "Название товара в URL",
            "URL",
            "Краткое описание",
            "Полное описание",
            "Картинка анонса",
            "Галлерея",
            "Артикуль",
            "Характеристики",
            "Старая цена",
            "Процент скидки",
            "Цена продажи",
        )
    )

def save_galary(soup_gal, name):
    list_url_img = soup_gal.find_all('img', class_='slide-image')

    iter = 0
    for item_url_img in list_url_img:
        #Получить ответ с картинкой от сервера
        req = requests.get(item_url_img.get('src'), headers=headers)#запрос на сервер
        respons = req.content#Получить контент ответа

        #Сохранить ответ от сервера(картику) в папку
        with open(f"media/items/{name.replace('/', '_')}_{iter}.jpg", "wb") as file:
            file.write(respons)
            list_gallary_img.append(f"media/items/{name.replace('/', '_')}_{iter}.jpg")
        iter += 1


def save_item(soup, url):

    if soup.find_all('li', class_='pagination-item'):
        last_pagen = int(soup.find_all('li', class_='pagination-item')[-2].find('a').text.strip())
    else:
        last_pagen = 1

    for i in range(1, last_pagen + 1):
    #for i in range(1, 2):
        req_cur_page = requests.get(url=f"{url}?page={i}", headers=headers)
        soup_cur_page = BeautifulSoup(req_cur_page.text, "lxml")

        item_container = soup_cur_page.find('div', class_='products-list')
        list_item = item_container.find_all('div', class_='product-card-wrapper')

        for item in list_item:
            detail_url = item.find('a', class_='product-card-photo').get('href')

            browser.get(url=f"{url}{detail_url}")
            #req_detail_page = requests.get(url=f"{url}{detail_url}")
            soup_detail_page = BeautifulSoup(browser.page_source, "lxml")

            #
            soup_galary_container = soup_detail_page.find('div', class_='swiper-wrapper')
            soup_name_item = soup_detail_page.find('h1', class_='page-headding').text.strip()
            save_galary(soup_galary_container,soup_name_item)
            #print(list_gallary_img)

            #Объявление переменных
            #soup_name_item = ''
            soup_name_url = ''
            soup_URL = ''
            soup_smal_description = ''
            soup_full_description = ''
            soup_anons_img_url = ''
            soup_articul = ''
            soup_charakter = ''
            soup_old_price = ''
            soup_discount = ''
            soup_price = ''

            #########
            soup_name_item = soup_name_item
            soup_name_url = detail_url.split('/')[-1]
            soup_URL = f"{url}{detail_url}"
            soup_smal_description = soup_detail_page.find('div', class_='product-introtext').text
            if soup_detail_page.find('div', class_='product-description'):
                soup_full_description = soup_detail_page.find('div', class_='product-description').find('div', class_='tab-block-inner')
            soup_anons_img_url = soup_detail_page.find('div', class_='gallery-main-wrapper').find('a').get('href')
            #soup_gallary_list = list_gallary_img
            if soup_detail_page.find('span', class_='js-product-sku'):
                soup_articul = soup_detail_page.find('span', class_='js-product-sku').text

            if soup_detail_page.find('table'):
                soup_charakter = soup_detail_page.find('table')

            if soup_detail_page.find('div', class_='old-price'):
                soup_old_price = soup_detail_page.find('div', class_='old-price').text.strip().split('\xa0')[0]

            if soup_detail_page.find('span', class_='is-discount'):
                soup_discount = soup_detail_page.find('span', class_='is-discount').text.strip()

            soup_price = soup_detail_page.find('div', class_='price').text.strip().split('\xa0')[0]


            #print(soup_discount)# 
            with open(f"protorg_{cur_time}.csv", "a") as file:
                writer = csv.writer(file)

                writer.writerow(
                    (
                        soup_name_item,
                        soup_name_url,
                        soup_URL,
                        soup_smal_description,
                        soup_full_description,
                        soup_anons_img_url,
                        list_gallary_img,
                        soup_articul,
                        soup_charakter,
                        soup_old_price,
                        soup_discount,
                        soup_price
                    )
                )
                
            
            


        print(i)







url = 'https://www.protorg-msk.ru'#URL главной страницы

headers = {#Заголовки для отправки данных на сайт
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
}
url_subsection = "https://www.protorg-msk.ru/collection/art-9110"#URL детальной страницы подраздела

req_subsection_done = requests.get(url_subsection, headers=headers)#Запрос на получение страницы подраздела 2 уровня
soup_subsection_done = BeautifulSoup(req_subsection_done.text, "lxml")#Получить страницу подраздела 2 уровня в формате soup объекта  need lxml

save_item(soup_subsection_done, url_subsection)

