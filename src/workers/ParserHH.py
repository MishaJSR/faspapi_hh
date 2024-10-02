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
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.brouser = webdriver.Chrome(options=self.chrome_options)
        self.is_run_refresh = False
        self.lst_of_vacancies = []
        self.thread_parsing = threading.Thread(target=self.start_pooling)

    def start_parsing(self) -> bool:
        if not self.thread_parsing.is_alive():
            self.thread_parsing.start()
            return False
        return True

    def start_pooling(self):
        self.brouser.get(self.url)
        time.sleep(10)
        while True:
            div_elements = self.brouser.find_elements(By.XPATH, '//div[contains(@class, "vacancy-info")]')

            links = []
            for div in div_elements[2:7]:
                vacancy_name = div.find_elements(By.TAG_NAME, 'span')[2].text
                span_list = div.find_elements(By.TAG_NAME, 'span')
                div_list_additions = div.find_elements(By.TAG_NAME, 'div')
                add_div = [d for d in div_list_additions if "magritte-tag__label" in d.get_attribute("class")]
                additions = "`".join([el.text for el in add_div if el.text])
                employer = [s.text for s in span_list
                            if "vacancy-serp__vacancy-employer-text" == str(s.get_attribute("data-qa"))][0]
                location = [s.text for s in span_list
                            if "vacancy-serp__vacancy-address" == str(s.get_attribute("data-qa"))][1]
                salary = "Зарплата не указана"
                for el in span_list:
                    if "₽" in el.text:
                        salary = el.text.replace("\u202f", "")
                        break
                url = div.find_elements(By.TAG_NAME, 'a')[0].get_attribute('href').split("?")[0]
                links.append([url, vacancy_name, salary, additions, employer, location])

            # Для примера, выводим найденные ссылки
            for link in links:
                if link not in self.lst_of_vacancies:
                    self.lst_of_vacancies.append(link)
            thread_refresh = threading.Thread(target=self.refresh_browser)
            self.is_run_refresh = True
            thread_refresh.start()
            time.sleep(random.randint(5, 8))
            if thread_refresh.is_alive():
                self.is_run_refresh = False
                self.brouser.close()
                self.brouser = webdriver.Chrome(options=self.chrome_options)
                self.brouser.get(self.url)
            time.sleep(random.randint(5, 8))
            print("working")

    def refresh_browser(self):
        while self.is_run_refresh:
            self.brouser.refresh()
            break
