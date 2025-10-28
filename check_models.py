import google.generativeai as genai
import os

print("--- Запускаю диагностику моделей Gemini ---")

try:
    # Пытаемся получить ключ из окружения
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("\nОШИБКА: API-ключ не найден в переменных окружения.")
        print("Перед запуском выполните команду:")
        print('$env:GOOGLE_API_KEY = "ВАШ_КЛЮЧ"')
        exit()  # Выходим из скрипта

    genai.configure(api_key=api_key)
    print("\nAPI-ключ успешно подхвачен. Запрашиваю список моделей у Google...")

    # Получаем и выводим список всех доступных моделей
    print("\n--- СПИСОК ДОСТУПНЫХ МОДЕЛЕЙ ---")
    model_found = False
    for model in genai.list_models():
        # Нас интересуют модели, которые умеют генерировать контент
        if 'generateContent' in model.supported_generation_methods:
            print(f"  - Имя модели: {model.name}")
            print(f"    Поддерживаемые методы: {model.supported_generation_methods}\n")
            model_found = True

    if not model_found:
        print("Не найдено ни одной модели, поддерживающей 'generateContent'.")

    print("--- Диагностика завершена ---")


except Exception as e:
    print(f"\n!!! Произошла критическая ошибка при выполнении диагностики: {e}")