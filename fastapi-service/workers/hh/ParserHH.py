import logging
import threading
import time
import random
from threading import Lock
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from vacancy.utils import hh_pusher_to_db
from subscriber.utils import send_first_matches_by_sub
from workers.Reporter import Reporter
from workers.hh.Observer import Observer, Subject
from workers.hh.utils import get_data





class ParserHH(Subject):
    url: str = 'https://hh.ru/search/vacancy?area=1&ored_clusters=true&order_by=publication_time'

    def __init__(self, reporter: Reporter) -> None:
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.brouser = webdriver.Chrome(options=self.chrome_options)
        self.is_run_refresh = False
        self.lst_of_vacancies = []
        self._observers: list[Observer] = []
        self.new_links = []
        self.attach(reporter)

    def attach(self, reporter: Reporter) -> None:
        self._observers.append(reporter)
        logging.info(f"Attached an observer. {reporter}")

    def detach(self, reporter: Reporter) -> None:
        self._observers.remove(reporter)

    async def notify(self) -> None:
        logging.info("Notifying observers...")
        for observer in self._observers:
            await observer.update(self)

    async def start_pooling(self) -> None:
        logging.info("Start Parser HH")
        self.brouser.get(self.url)
        time.sleep(10)
        while True:
            logging.info("Start circle Parser HH")
            div_elements = self.brouser.find_elements(By.XPATH, '//div[contains(@class, "vacancy-info")]')
            links = get_data(div_elements)
            self.new_links = []
            for link in links:
                if link not in self.lst_of_vacancies:
                    self.lst_of_vacancies.append(link)
                    self.new_links.append(link)
            if self.new_links:
                await self.notify()
            thread_refresh = threading.Thread(target=self.refresh_browser)
            self.is_run_refresh = True
            thread_refresh.start()
            time.sleep(random.randint(5, 8))
            self.restart_brouser(thread_refresh)
            if len(self.lst_of_vacancies) > 20:
                self.lst_of_vacancies = []
                logging.info("HH Clear vac list")

    def refresh_browser(self) -> None:
        while self.is_run_refresh:
            self.brouser.refresh()
            break

    def restart_brouser(self, thread_refresh) -> None:
        if thread_refresh.is_alive():
            self.is_run_refresh = False
            self.brouser.close()
            self.brouser = webdriver.Chrome(options=self.chrome_options)
            self.brouser.get(self.url)

    @staticmethod
    async def update_db(new_links) -> None:
        for link in new_links:
            is_new = await hh_pusher_to_db(new_vac=link)
            if is_new:
                await send_first_matches_by_sub(link=link)
