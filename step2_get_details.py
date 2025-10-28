import requests
import json
import time
from bs4 import BeautifulSoup
import os  # Добавим для проверки существования файла


def get_detailed_vacancies(url_list):
    """
    Получает детальную информацию по списку URL вакансий.

    :param url_list: Список ссылок на вакансии.
    :return: Список словарей с детальной информацией о каждой вакансии.
    """
    all_vacancies_data = []
    processed_count = 0
    total_count = len(url_list)

    print(f"Начинаю обработку {total_count} ссылок...")

    for url in url_list:
        try:
            # Извлекаем ID вакансии из URL
            vacancy_id = url.split('/')[-1].split('?')[0]

            # Делаем запрос к API для получения деталей
            api_url = f'https://api.hh.ru/vacancies/{vacancy_id}'
            response = requests.get(api_url)
            response.raise_for_status()
            vacancy_data = response.json()

            # Очищаем описание от HTML-тегов
            raw_html = vacancy_data.get('description', '')
            soup = BeautifulSoup(raw_html, 'html.parser')
            cleaned_description = soup.get_text(separator=' ', strip=True)

            # Собираем нужную нам информацию
            all_vacancies_data.append({
                'id': vacancy_id,
                'url': url,
                'name': vacancy_data.get('name'),
                'company_name': vacancy_data.get('employer', {}).get('name'),
                'salary_from': vacancy_data.get('salary', {}).get('from') if vacancy_data.get('salary') else None,
                'salary_to': vacancy_data.get('salary', {}).get('to') if vacancy_data.get('salary') else None,
                'currency': vacancy_data.get('salary', {}).get('currency') if vacancy_data.get('salary') else None,
                'description': cleaned_description
            })

            processed_count += 1
            # Выводим прогресс, чтобы было не скучно ждать
            print(f"Обработано: {processed_count} / {total_count}")

        except requests.RequestException as e:
            print(f"Ошибка при запросе для URL {url}: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка для URL {url}: {e}")

        # Задержка, чтобы не превысить лимиты API
        time.sleep(0.25)

    print("\nОбработка всех ссылок завершена.")
    return all_vacancies_data


# --- Основной скрипт ---
if __name__ == "__main__":
    input_file = 'vacancy_urls.txt'
    output_file = 'vacancies_data.json'

    if not os.path.exists(input_file):
        print(f"Ошибка: Файл {input_file} не найден. Сначала запустите скрипт из Шага 1.")
    else:
        with open(input_file, 'r', encoding='utf-8') as f:
            urls_to_process = [line.strip() for line in f if line.strip()]

        if urls_to_process:
            detailed_data = get_detailed_vacancies(urls_to_process)

            if detailed_data:
                # Сохраняем результат в JSON файл
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(detailed_data, f, ensure_ascii=False, indent=4)

                print(f"\nВсе данные успешно собраны и сохранены в файл {output_file}")
                print(f"Всего обработано и сохранено вакансий: {len(detailed_data)}")
        else:
            print("Файл с ссылками пуст.")