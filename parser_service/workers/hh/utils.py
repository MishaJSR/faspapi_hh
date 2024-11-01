from selenium.webdriver.common.by import By


def get_data(div_elements) -> list:
    links = []
    for div in div_elements[2:7]:
        is_no_exp = False
        is_remote = False
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
        if "Без опыта" in additions:
            is_no_exp = True
        if "Можно удаленно" in additions:
            is_remote = True
        links.append([url, vacancy_name, salary, is_no_exp, is_remote, employer, location])
    return links