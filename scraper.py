import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
import pandas as pd
from bs4 import BeautifulSoup



binary_yandex_driver_file = r'webdriver/yandexdriver.exe'  # path to YandexDriver
options = webdriver.ChromeOptions()
#options.add_argument("--headless")
#options.add_argument("--disable-gpu")
options.page_load_strategy = 'eager'
service = ChromeService(executable_path=binary_yandex_driver_file)
driver_2 = webdriver.Chrome(service=service, options=options)
driver_2.get(f'https://maxidom.ru/catalog/')



lst_index_category = {}
fict_category = ["Ликвидация остатков","Автотовары","Товары для животных","Канцтовары",
                 "Подарочные сертификаты","Кухни", "Коллекции кухонь", "Бренды", ""]

def scrap(ID_REGION, call):
        driver_1 = webdriver.Chrome(service=service, options=options)
        driver_1.get(f'https://maxidom.ru/catalog/?repIDchanged={ID_REGION}')
        category = soup_category(driver_1.page_source, ID_REGION, call)
        value = scrap_value(category, ID_REGION)
        scrap_prod = scrap_product(value, ID_REGION)
        df = pd.DataFrame(scrap_prod)
        df.to_excel("parse.xlsx")
        print("parse.xlsx готов")


def soup_parse_index(src):
        global lst_index_category
        soup_index_catalod= BeautifulSoup(src, "lxml").find("div", class_="content catalog-wrap").find("ul").find_all("a")
        for item in soup_index_catalod:
                if item.text.strip() not in fict_category:
                        lst_index_category[item.text] = item.get("href")
        #return lst_index_category


def soup_category(src, ID_REGION, call):
        category = []
        soup_parse_index(src)
        driver = webdriver.Chrome(service=service, options=options)
        if call != "Все категории":
                for name in lst_index_category.keys():
                        if name.strip() == call:
                                try:
                                        driver.get(f'https://maxidom.ru'+lst_index_category[name]+f"?repIDchanged={ID_REGION}")
                                        time.sleep(5)
                                        soup_catalod = BeautifulSoup(driver.page_source, "lxml").find("div", class_="lvl1__menu").find(
                                                "ul").find_all("a")
                                        for ctg_lnk in soup_catalod:
                                                category.append(ctg_lnk.get("href"))
                                                print(ctg_lnk)
                                except Exception as e:
                                        print(e)
                                finally:
                                        driver.close()
                                        driver.quit()

        else:
                for name in lst_index_category.keys():
                        try:
                                driver.get(f'https://maxidom.ru' + lst_index_category[name] + f"?repIDchanged={ID_REGION}")
                                time.sleep(5)
                                soup_catalod = BeautifulSoup(driver.page_source, "lxml").find("div",
                                                                                              class_="lvl1__menu").find(
                                        "ul").find_all("a")
                                for ctg_lnk in soup_catalod:
                                        category.append(ctg_lnk.get("href"))
                                        print(ctg_lnk)
                        except Exception as e:
                                print(e)
                driver.close()
                driver.quit()

        return category


def scrap_value(category, ID_REGION):
        id_products = []
        driver = webdriver.Chrome(service=service, options=options)
        for cat in category:
                driver.get(f'https://maxidom.ru' + cat + f"?repIDchanged={ID_REGION}")
                time.sleep(5)
                soup_page = BeautifulSoup(driver.page_source, "lxml").find("div", class_="lvl2__content-nav-numbers-number")
                if soup_page is not None:
                        soup_page_num = soup_page.find("ul").find_all("a")[-1].text.strip()
                        for value in range(1, int(soup_page_num)+1):
                                driver.get(f'https://maxidom.ru' + cat + f"?repIDchanged={ID_REGION}&amount=30&PAGEN_2={value}")
                                soup_id = BeautifulSoup(driver.page_source, "lxml").find("div", class_= "lvl1__product-body lvl2 hidden lvl1__product-body-searchresult").find_all("a", itemprop="url")
                                for id in soup_id:
                                        id_products.append(id.get("href"))
                else:
                        driver.get(f'https://maxidom.ru' + cat + f"?repIDchanged={ID_REGION}")
                        soup_id = BeautifulSoup(driver.page_source, "lxml").find("div",
                                                                         class_="lvl1__product-body lvl2 hidden lvl1__product-body-searchresult").find_all(
                                "a", itemprop="url")
                        for id in soup_id:
                                id_products.append(id.get("href"))

        driver.close()
        driver.quit()
        return id_products

def scrap_product(value, ID_REGION):
        cod = []
        name = []
        price = []
        old_price = []
        if ID_REGION == 2:
                mag_1 = []
                mag_2 = []
                mag_3 = []
                mag_4 = []
                mag_5 = []
                mag_6 = []
                mag_7 = []
                mag_8 = []
                mag_9 = []
                mag_10 = []
                mag_11 = []
                mag_12 = []
                dict_product = {"Код": cod, "Наименование": name, "Цена": old_price,"Цена со скидкой": price,
                                "Гражданский пр-т, д. 18А": mag_1, "Московский пр-т, д. 131": mag_2,
                                "Ленинский пр-т, д. 103": mag_3, "Богатырский пр-т, д. 15": mag_4,
                                "Выборгское ш., д. 503, к. 2": mag_5, "Дунайский пр-т, д. 64": mag_6,
                                "ул. Тельмана д. 31": mag_7, "ул. Передовиков д.18 к 2": mag_8,
                                "пр. Энгельса, д. 154": mag_9, "ул. Уральская, д. 1": mag_10,
                                "Пулковское шоссе, д. 17": mag_11, "Дальневосточный пр-т, д.16 к 2": mag_12}
        elif ID_REGION == 9:
                mag_1 = []
                mag_2 = []
                mag_3 = []
                mag_4 = []
                dict_product = {"Код": cod, "Наименование": name, "Цена": old_price,"Цена со скидкой": price,
                                "Котельники, Белая Дача, 1-й Покровский проезд, д.2" : mag_1,
                                "Электросталь, пос. Случайный, тер. массив 1, 12" : mag_2,
                                "Одинцово, ул.Восточная, 19" : mag_3, "Щербинка, ул. Восточная, д. 80" : mag_4}
        driver = webdriver.Chrome(service=service, options=options)
        k = 1
        for product_link in value:
                driver.get(f'https://maxidom.ru' + product_link + f"?repIDchanged={ID_REGION}")
                soup_stock = BeautifulSoup(driver.page_source, "lxml").find_all(class_="flypage__product-essence-available-adress-howmuch")
                soup = BeautifulSoup(driver.page_source, "lxml")
                with open("index.html", "w") as file:
                        file.write(driver.page_source)
                if soup is None:
                        break
                if ID_REGION == 2:
                        print(str(k) + " " + soup.find(class_="flypage__header-mobile").find("p").text)
                        cod.append(soup.find(class_="flypage__lineinfo-code").find("span").text)
                        name.append(soup.find(class_ ="flypage__header-mobile").find("p").text)
                        mag_1.append((soup_stock[0].text))
                        mag_2.append((soup_stock[0].text))
                        mag_3.append((soup_stock[1].text))
                        mag_4.append((soup_stock[2].text))
                        mag_5.append((soup_stock[3].text))
                        mag_6.append((soup_stock[0].text))
                        mag_7.append((soup_stock[1].text))
                        mag_8.append((soup_stock[2].text))
                        mag_9.append((soup_stock[3].text))
                        mag_10.append((soup_stock[3].text))
                        mag_11.append((soup_stock[3].text))
                        mag_12.append((soup_stock[3].text))
                        old_price_soup = soup.find(class_="lvl1__product-body-buy-price-discount-old")
                        print(old_price_soup)
                        if old_price_soup is  None:
                                old_price.append(soup.find(class_="lvl1__product-body-buy-price-base").find("span").text)
                                price.append("-")
                        else:
                                old_price.append(soup.find(class_="lvl1__product-body-buy-price-base").find("span").text)
                                price.append(old_price_soup.find("span").text)


                else:
                        print(str(k) + " " + soup.find(class_="flypage__header-mobile").find("p").text)
                        cod.append(soup.find(class_="flypage__lineinfo-code").find("span").text)
                        name.append(soup.find(class_="flypage__header-mobile").find("p").text)
                        price.append(soup.find(class_="lvl1__product-body-buy-price-base").find("span").text)
                        mag_1.append((soup_stock[0].text))
                        mag_2.append((soup_stock[1].text))
                        mag_3.append((soup_stock[2].text))
                        mag_4.append((soup_stock[3].text))
                        old_price_soup = soup.find(class_="lvl1__product-body-buy-price-discount-old")
                        if old_price_soup is None:
                                old_price.append(soup.find(class_="lvl1__product-body-buy-price-base").find("span").text)
                                price.append("-")
                        else:
                                old_price.append(old_price_soup.find("span").text)
                                price.append(soup.find(class_="lvl1__product-body-buy-price-base").find("span").text)

                k+=1

        driver.quit()
        return dict_product


soup_parse_index(driver_2.page_source)

driver_2.quit()
