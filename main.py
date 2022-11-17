import requests
from bs4 import BeautifulSoup
import csv
import datetime
from selenium import webdriver
import time

#глобальные переменные для итоговой работы и записи в файл
browser = webdriver.Chrome()
#list_gallary_img = []
catalog = []#Готовый каталог
#section = []#Раздел каталога                            //1 lvl
#subsection = []#Подраздел каталога                      //2 lvl
#subsection_2 = []#Подраздел каталога 2 уровня           //3 lvl

def log():
    pass

def save_img_sections(url, name):
    #Получить ответ с картинкой от сервера
    req = requests.get(url, headers=headers)#запрос на сервер
    respons = req.content#Получить контент ответа

    #Сохранить ответ от сервера(картику) в папку
    with open(f"media/sections/{name.replace('/', '_')}.jpg", "wb") as file:
        file.write(respons)

def save_galary(soup_gal, name):
    list_url_img = soup_gal.find_all('img', class_='slide-image')
    list_gallary_img = []
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
    return list_gallary_img


def save_item(soup, url):

    if soup.find_all('li', class_='pagination-item'):
        last_pagen = int(soup.find_all('li', class_='pagination-item')[-2].find('a').text.strip())
        #last_pagen = 2
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
            time.sleep(1)
            #req_detail_page = requests.get(url=f"{url}{detail_url}")
            soup_detail_page = BeautifulSoup(browser.page_source, "lxml")

            #
            soup_galary_container = soup_detail_page.find('div', class_='swiper-wrapper')
            if  soup_detail_page.find('h1', class_='page-headding'):
                soup_name_item = soup_detail_page.find('h1', class_='page-headding').text.strip()
            else:
                soup_name_item = 'Не удалось найти название'
            
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
            if soup_detail_page.find('div', class_='product-introtext'):
                soup_smal_description = soup_detail_page.find('div', class_='product-introtext').text
            if soup_detail_page.find('div', class_='product-description'):
                soup_full_description = soup_detail_page.find('div', class_='product-description').find('div', class_='tab-block-inner')
            if soup_detail_page.find('div', class_='gallery-main-wrapper').find('a'):
                soup_anons_img_url = soup_detail_page.find('div', class_='gallery-main-wrapper').find('a').get('href')
            soup_gallary_list = save_galary(soup_galary_container,soup_name_item)
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
                        soup_gallary_list,
                        soup_articul,
                        soup_charakter,
                        soup_old_price,
                        soup_discount,
                        soup_price,
                        name_section,
                        name_subsection,
                        name_subsection_2
                    )
                )
            soup_gallary_list = []
            #log(url_section, url_subsection, )

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
            "Раздел 1 уровня",
            "Раздел 2 уровня",
            "Раздел 3 уровня",
        )
    )

headers = {#Заголовки для отправки данных на сайт
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
}
url = 'https://www.protorg-msk.ru'#URL главной страницы

browser.get(url)#URL главной страницы
soup_home = BeautifulSoup(browser.page_source, "lxml")#Получить HTML главной страницы  need lxml

#Работа на формирование главных разделов
home_catigories_container = soup_home.find('div', class_='special-categories')#Получить контейнер в котором храняться раделы первого уровня
list_categories_home = home_catigories_container.find_all('div', class_='special-category')#Список контейнеров 

#Пройтись по разделам каталога верхнего уровня
for section in list_categories_home[0:1]:
    name_section = section.find('div', class_='category-caption').text.strip()#Название раздела
    url_pictures_section = section.find('picture', class_='category-image').find('img').get('src')#URL картинки раздела
    url_section = f"{url}{section.find('a', class_='category-inner').get('href')}"#URL детальной страницы раздела

    save_img_sections(url_pictures_section, name_section)#функция сохранения картики разделов

    #Зайти внутрь разделов верхнего уровня
    browser.get(url_section)#Запрос на получение страницы раздела верхнего уровня
    soup_subsection = BeautifulSoup(browser.page_source, "lxml")#Получить страницу раздела врехнего уровня в формате soup объекта  need lxml

    subsections_container = soup_subsection.find('div', class_='categories-subcollections')#Получить контейнер с подкатегориями
    list_subsections = subsections_container.find_all('div', class_='category-subcollections')#Получить список подкатегорий

    #Пройтись по списку подкатегорий
    for subsection in list_subsections:
        name_subsection = subsection.find('div', class_='category-caption').text.strip()#Название подраздела
        url_pictures_subsection = subsection.find('picture', class_='category-image').find('img').get('src')#URL картинки подраздела
        url_subsection = f"{url}{subsection.find('a', class_='category-inner').get('href')}"#URL детальной страницы подраздела

        save_img_sections(url_pictures_subsection, name_subsection)#функция сохранения картики разделов

        #Зайти внутрь подразделов
        browser.get(url_subsection)#Запрос на получение страницы подраздела
        soup_subsection_2 = BeautifulSoup(browser.page_source, "lxml")#Получить страницу подраздела в формате soup объекта  need lxml

        subsections_2_container = soup_subsection_2.find('div', class_='categories-subcollections-cus')#Получить контейнер с подкатегориями 2 уровня
        if subsections_2_container == None:
            name_subsection_2 = ''
            save_item(soup_subsection_2, url_subsection)
            print('Заглушка')
        else:
            list_subsections_2 = subsections_2_container.find_all('div', class_='category-subcollections')#Получить список подкатегорий

            #Пройтись по списку подкатегорий 2 уровня
            for subsections_2 in list_subsections_2:
                name_subsection_2 = subsections_2.find('div', class_='category-caption').text.strip()#Название подраздела 2 уровня
                url_pictures_subsection_2 = subsections_2.find('picture', class_='category-image').find('img').get('src')#URL картинки подраздела 2 уровня
                url_subsection_2 = f"{url}{subsections_2.find('a', class_='category-inner').get('href')}"#URL детальной страницы подраздела 2 уровня

                save_img_sections(url_pictures_subsection, name_subsection_2)#функция сохранения картики разделов

                #Зайти внутрь подразделов 2 уровня
                browser.get(url_subsection_2)#Запрос на получение детальной страницы
                soup_subsection_done = BeautifulSoup(browser.page_source, "lxml")#Получить детальную страницу в формате soup объекта  need lxml

                save_item(soup_subsection_done, url_subsection_2)




#print(list_categories_home)df







# with open(f"labirint_{cur_time}.csv", "a") as file:
#     writer = csv.writer(file)

#     writer.writerow(
#         (
#             book_title,
#             book_author,
#             book_publishing,
#             book_new_price,
#             book_old_price,
#             book_sale,
#             book_status
#         )
#     )




# img_list = []
#     for i in range(1, 49):
#         url = f"https://www.recordpower.co.uk/flip/Winter2020/files/mobile/{i}.jpg"
#         req = requests.get(url=url, headers=headers)
#         response = req.content

#         with open(f"media/{i}.jpg", "wb") as file:
#             file.write(response)
#             img_list.append(f"media/{i}.jpg")
#             print(f"Downloaded {i} of 48")

#     print("#" * 20)
#     print(img_list)