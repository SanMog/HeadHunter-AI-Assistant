import json
import re
import os

# --- БАЗА ЗНАНИЙ НА ОСНОВЕ ВАШЕГО РЕЗЮМЕ И СТРАТЕГИИ ---

# 1. Ключевые навыки с "весами" (чем важнее, тем больше балл)
SKILLS_KEYWORDS = {
    # Основной стек автоматизации
    'python': 20, 'selenium': 20, 'pytest': 20, 'postman': 15, 'api': 15,
    'автоматизированное тестирование': 20, 'автотест': 20,
    # Инструменты и технологии
    'sql': 10, 'mysql': 10, 'postgresql': 10, 'git': 10, 'jenkins': 15, 'ci/cd': 15,
    'jira': 5, 'testit': 5, 'zephyr': 5, 'confluence': 5,
    'kibana': 10, 'docker': 10, 'linux': 5,
    # Уникальное преимущество
    'desktop': 25, 'winium': 30,  # Очень ценно, так как редкость
    # Методологии и процессы
    'agile': 5, 'scrum': 5, 'тест-дизайн': 10, 'нагрузочное тестирование': 10, 'jmeter': 10,
    'регрессионное тестирование': 5, 'функциональное тестирование': 5,
    # Домены
    'fintech': 15, 'финтех': 15, 'govtech': 15, 'гостех': 15, 'medtech': 15, 'медтех': 15
}

# 2. "Золотые" фразы, которые указывают на идеальную вакансию
GOLDEN_KEYWORDS = {
    'с нуля': 50,
    'единственный qa': 50, 'единственным тестировщиком': 50,
    'выстроить процессы': 50, 'построение процессов': 50,
    'оптимизация процессов': 40, 'улучшение qa': 40,
    'проактивный': 30, 'продуктовое мышление': 30
}

# 3. "Штрафные" слова. Теперь они не отбрасывают, а сильно понижают рейтинг
### ИЗМЕНЕНИЕ: RED_FLAG_KEYWORDS превратились в PENALTY_KEYWORDS с весами штрафов ###
PENALTY_KEYWORDS = {
    # Чужой основной стек
    'java': 200, 'c#': 200, 'typescript': 150, 'javascript': 100,
    # Явные руководящие роли
    'lead': 250, 'head of': 250, 'руководитель': 250, 'teamlead': 250, 'тимлид': 250,
    # Нерелевантные домены
    '1с': 300, 'gamedev': 300, 'hardware': 300
}


# --- ОСНОВНАЯ ЛОГИКА АНАЛИЗА ---

def analyze_vacancies(vacancies_data):
    all_analyzed_vacancies = []

    for vacancy in vacancies_data:
        description_text = (vacancy.get('name', '') + ' ' + vacancy.get('description', '')).lower()

        score = 0
        found_reasons = []

        # 1. Начисляем баллы за "золотые" слова
        for keyword, points in GOLDEN_KEYWORDS.items():
            if keyword in description_text:
                score += points
                found_reasons.append(f"+{points} (золотое слово: {keyword})")

        # 2. Начисляем баллы за навыки
        for keyword, points in SKILLS_KEYWORDS.items():
            if re.search(r'\b' + keyword + r'\b', description_text):
                score += points
                found_reasons.append(f"+{points} (навык: {keyword})")

        # 3. Вычитаем штрафные баллы
        for keyword, penalty_points in PENALTY_KEYWORDS.items():
            # ### ИЗМЕНЕНИЕ: Специальная проверка для C# ###
            # Для C# и 1С ищем простое вхождение, т.к. re.search их плохо обрабатывает
            if keyword in ['c#', '1с']:
                if keyword in description_text:
                    score -= penalty_points
                    found_reasons.append(f"-{penalty_points} (штраф: {keyword})")
            else:  # Для остальных слов используем re.search, чтобы избежать ложных срабатываний (например, 'java' в 'javascript')
                if re.search(r'\b' + keyword + r'\b', description_text):
                    score -= penalty_points
                    found_reasons.append(f"-{penalty_points} (штраф: {keyword})")

        vacancy['score'] = score
        vacancy['reasons'] = list(set(found_reasons))
        all_analyzed_vacancies.append(vacancy)

    # Сортируем ВСЕ вакансии по убыванию балла
    all_analyzed_vacancies.sort(key=lambda x: x['score'], reverse=True)

    # Разделяем на подходящие и отклоненные
    ranked_vacancies = [v for v in all_analyzed_vacancies if v['score'] >= -50]  # ### ИЗМЕНЕНИЕ: Расширяем порог ###
    rejected_vacancies = [v for v in all_analyzed_vacancies if v['score'] < -50]

    return ranked_vacancies, rejected_vacancies


# --- Основной скрипт ---
if __name__ == "__main__":
    input_file = 'vacancies_data.json'
    ranked_output_file = 'ranked_vacancies.json'
    rejected_output_file = 'rejected_vacancies.json'

    if not os.path.exists(input_file):
        print(f"Ошибка: Файл {input_file} не найден. Сначала запустите скрипт из Шага 2.")
    else:
        with open(input_file, 'r', encoding='utf-8') as f:
            all_vacancies = json.load(f)

        ranked, rejected = analyze_vacancies(all_vacancies)

        # Сохраняем результаты
        with open(ranked_output_file, 'w', encoding='utf-8') as f:
            json.dump(ranked, f, ensure_ascii=False, indent=4)

        with open(rejected_output_file, 'w', encoding='utf-8') as f:
            json.dump(rejected, f, ensure_ascii=False, indent=4)

        print("Улучшенный анализ завершен!")
        print(f"Найдено подходящих вакансий (score > 0): {len(ranked)}. Результаты в файле {ranked_output_file}")
        print(f"Отклонено вакансий (score <= 0): {len(rejected)}. Результаты в файле {rejected_output_file}")

        if ranked:
            print("\n--- ТОП-10 НАИБОЛЕЕ ПОДХОДЯЩИХ ВАКАНСИЙ (новая версия) ---")
            for vacancy in ranked[:10]:
                print(f"Score: {vacancy['score']:<5} | {vacancy['name']} | {vacancy['url']}")