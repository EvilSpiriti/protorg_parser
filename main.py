import requests
from bs4 import BeautifulSoup
import csv
import datetime

#глобальные переменные для итоговой работы и записи в файл
catalog = []#Готовый каталог
#section = []#Раздел каталога                            //1 lvl
#subsection = []#Подраздел каталога                      //2 lvl
#subsection_2 = []#Подраздел каталога 2 уровня           //3 lvl

def save_img_sections(url, name):
    #Получить ответ с картинкой от сервера
    req = requests.get(url, headers=headers)#запрос на сервер
    respons = req.content#Получить контент ответа

    #Сохранить ответ от сервера(картику) в папку
    with open(f"media/sections/{name}.jpg", "wb") as file:
        file.write(respons)


def save_item(soup, url):

    item_container = soup.find('div', class_='products-list')
    list_item = item_container.find_all('div', class_='product-card-wrapper')

#Создание файла для cvs
#cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")#Получить текущую дату
# with open(f"protorg_{cur_time}.csv", "w") as file:#Открыть файл для записи
#     writer = csv.writer(file)#Возвращает объект записи, ответственный за преобразование пользовательских данных в строки с разделителями в данном файлоподобном объект

#     writer.writerow(#Создать следующие столбцы
#         (
#             "Название товара или услуги",
#             "Название товара в URL",
#             "URL",
#             "Краткое описание",
#             "Полное описание",
#             "Картинка анонса",
#             "Галлерея",
#             "Артикуль",
#             "Параметр: Стандарт",
#             "Параметр: Тип головки",
#             "Параметр: Диаметр, мм",
#             "Параметр: Длина, мм",
#             "Вид покрытия",
#             "Старая цена",
#             "Процент скидки",
#             "Цена продажи",
#             "Раздел 1 уровня",
#             "Раздел 2 уровня",
#             "Раздел 3 уровня",
#         )
#     )

headers = {#Заголовки для отправки данных на сайт
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
}
url = 'https://www.protorg-msk.ru'#URL главной страницы

req_home = requests.get(url, headers=headers)#URL главной страницы
soup_home = BeautifulSoup(req_home.text)#Получить HTML главной страницы  need lxml

#Работа на формирование главных разделов
home_catigories_container = soup_home.find('div', class_='special-categories')#Получить контейнер в котором храняться раделы первого уровня
list_categories_home = home_catigories_container.find_all('div', class_='special-category')#Список контейнеров 

#Пройтись по разделам каталога верхнего уровня
for section in list_categories_home[0:1]:
    name_section = section.find('div', class_='category-caption').text.strip()#Название раздела
    url_pictures_section = section.find('picture', class_='category-image').find('img').get('src')#URL картинки раздела
    url_section = f"{url}{section.find('a', class_='category-inner').get('href')}"#URL детальной страницы раздела

    #save_img_sections(url_pictures_section, name_section)#функция сохранения картики разделов

    #Зайти внутрь разделов верхнего уровня
    req_subsection = requests.get(url_section, headers=headers)#Запрос на получение страницы раздела верхнего уровня
    soup_subsection = BeautifulSoup(req_subsection.text)#Получить страницу раздела врехнего уровня в формате soup объекта  need lxml

    subsections_container = soup_subsection.find('div', class_='categories-subcollections')#Получить контейнер с подкатегориями
    list_subsections = subsections_container.find_all('div', class_='categories-subcollections-cus')#Получить список подкатегорий

    #Пройтись по списку подкатегорий
    for subsection in list_subsections[0:1]:
        name_subsection = subsection.find('div', class_='category-caption').text.strip()#Название подраздела
        url_pictures_subsection = subsection.find('picture', class_='category-image').find('img').get('src')#URL картинки подраздела
        url_subsection = f"{url}{subsection.find('a', class_='category-inner').get('href')}"#URL детальной страницы подраздела

        #save_img_sections(url_pictures_subsection, name_subsection)#функция сохранения картики разделов

        #Зайти внутрь подразделов
        req_subsection_2 = requests.get(url_subsection, headers=headers)#Запрос на получение страницы подраздела
        soup_subsection_2 = BeautifulSoup(req_subsection_2.text)#Получить страницу подраздела в формате soup объекта  need lxml

        subsections_2_container = soup_subsection_2.find('div', class_='categories-subcollections-cus')#Получить контейнер с подкатегориями 2 уровня
        if subsections_2_container == None:
            #save_item()
            print('Заглушка')
        else:
            list_subsections_2 = subsections_2_container.find_all('div', class_='category-subcollections')#Получить список подкатегорий

            #Пройтись по списку подкатегорий 2 уровня
            for subsections_2 in list_subsections_2[0:1]:
                name_subsection_2 = subsections_2.find('div', class_='category-caption').text.strip()#Название подраздела 2 уровня
                url_pictures_subsection_2 = subsections_2.find('picture', class_='category-image').find('img').get('src')#URL картинки подраздела 2 уровня
                url_subsection_2 = f"{url}{subsections_2.find('a', class_='category-inner').get('href')}"#URL детальной страницы подраздела 2 уровня

                #save_img_sections(url_pictures_subsection, name_subsection)#функция сохранения картики разделов

                #Зайти внутрь подразделов 2 уровня
                req_subsection_done = requests.get(url_subsection_2, headers=headers)#Запрос на получение детальной страницы
                soup_subsection_done = BeautifulSoup(req_subsection_done.text)#Получить детальную страницу в формате soup объекта  need lxml

                save_item(soup_subsection_done, url_subsection_2)







                print(name_subsection_2)
                print(url_pictures_subsection_2)
                print(url_subsection_2)

#print(list_categories_home)








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