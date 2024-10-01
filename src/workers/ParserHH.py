import threading
import time
import random
from threading import Lock, Thread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class ParserMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class ParserHH(metaclass=ParserMeta):
    url = 'https://hh.ru/search/vacancy?area=1&ored_clusters=true&order_by=publication_time'

    def __init__(self) -> None:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.brouser = webdriver.Chrome()
        self.is_run_refresh = False
        self.lst_of_vacancies = []

    def start_parsing(self):
        thread_parsing = threading.Thread(target=self.start_pooling)
        thread_parsing.start()

    def start_pooling(self):
        self.brouser.get(self.url)
        time.sleep(10)
        while True:
            div_elements = self.brouser.find_elements(By.XPATH, '//div[contains(@class, "vacancy-info")]')

            links = []
            for div in div_elements[2:7]:
                vacancy_name = div.find_elements(By.TAG_NAME, 'span')[2].text
                span_list = div.find_elements(By.TAG_NAME, 'span')
                salary = "Зарплата не указана"
                for el in span_list:
                    if "₽" in el.text:
                        salary = el.text.replace("\u202f", "")
                a_elements = div.find_elements(By.TAG_NAME, 'a')
                links.append([a_elements[0].get_attribute('href'), vacancy_name, salary])

            # Для примера, выводим найденные ссылки
            for link in links:

                res = link[0].split("?")[0]
                vac = [res, link[1], link[2]]
                if vac not in self.lst_of_vacancies:
                    self.lst_of_vacancies.append(vac)
                    print(self.lst_of_vacancies)
                    # send
            thread_refresh = threading.Thread(target=self.refresh_browser)
            self.is_run_refresh = True
            thread_refresh.start()
            time.sleep(random.randint(5, 8))
            if thread_refresh.is_alive():
                self.is_run_refresh = False
                self.brouser.close()
                self.brouser = webdriver.Chrome()
                self.brouser.get(self.url)

            time.sleep(random.randint(5, 8))
            print("working")

    def refresh_browser(self):
        while self.is_run_refresh:
            self.brouser.refresh()
            break
