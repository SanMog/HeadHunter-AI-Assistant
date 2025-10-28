import requests
import time


def get_vacancy_urls(search_params):
    """
    Функция для сбора ссылок на вакансии с HeadHunter по заданным фильтрам.

    :param search_params: Словарь с параметрами для поиска.
    :return: Список ссылок на вакансии.
    """
    base_url = 'https://api.hh.ru/vacancies'
    all_vacancy_urls = []
    page = 0
    max_pages = 1

    print(f"Начинаю поиск с заданными параметрами...")

    while page < max_pages:
        # Копируем основные параметры и добавляем номер страницы
        params = search_params.copy()
        params['page'] = page
        params['per_page'] = 100

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            print(f"Произошла ошибка при запросе: {e}")
            break

        # Получаем ссылки из текущей страницы
        vacancies_on_page = data.get('items', [])
        for vacancy in vacancies_on_page:
            all_vacancy_urls.append(vacancy['alternate_url'])

        # Обновляем общее количество страниц на первой итерации
        if page == 0:
            max_pages = data.get('pages', 1)
            found_total = data.get('found', 0)
            print(f"Найдено всего вакансий: {found_total}. Всего страниц для обработки: {max_pages}")
            if max_pages == 0:
                print("Вакансий по вашему запросу не найдено.")
                break

        print(f"Обработана страница {page + 1} из {max_pages}. Собрано ссылок: {len(all_vacancy_urls)}")

        page += 1
        if page < max_pages:
            time.sleep(0.25)

    print("\nСбор ссылок завершен.")
    return all_vacancy_urls


# --- Пример использования с вашими параметрами ---
if __name__ == "__main__":
    # ПАРАМЕТРЫ, РАСШИФРОВАННЫЕ ИЗ ВАШЕЙ ССЫЛКИ
    my_search_params = {
        'text': 'QA Engineer',
        'area': 113,  # 113 - Россия
        'experience': 'between3And6',  # Опыт от 3 до 6 лет
        'professional_role': 124,  # Роль "Тестировщик"
        'schedule': 'remote',  # Удаленная работа (в API это 'schedule')
        'search_field': ['name', 'company_name', 'description']  # Искать в нескольких полях
    }

    urls = get_vacancy_urls(my_search_params)

    if urls:
        print(f"\nВсего собрано {len(urls)} ссылок на вакансии.")
        print("Первые 5 ссылок:")
        for url in urls[:5]:
            print(url)

        # Сохраняем все ссылки в файл для следующего шага
        with open('vacancy_urls.txt', 'w', encoding='utf-8') as f:
            for url in urls:
                f.write(f"{url}\n")
        print("\nВсе ссылки сохранены в файл vacancy_urls.txt")