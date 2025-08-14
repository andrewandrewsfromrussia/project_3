# main.py

import os
from dotenv import load_dotenv
from src.db import create_database, create_tables
from src.data_loader import load_data
from src.db_manager import DBManager

# Загрузка переменных окружения из .env
load_dotenv()

# 1. Создание БД (один раз)
create_database(
    db_name=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

# 2. Создание таблиц (один раз)
create_tables()
print("✅ Создание таблиц успешно")

# 3. Загрузка данных (один раз)
load_data()
print("✅ Данные успешно загружены в базу данных")

# 4. Работа с пользователем
db = DBManager()


def show_menu():
    """Выводит текстовое меню"""
    print("\nВыберите действие:")
    print("1 — Компании и количество вакансий")
    print("2 — Все вакансии")
    print("3 — Средняя зарплата")
    print("4 — Вакансии с зарплатой выше средней")
    print("5 — Поиск вакансий по ключевому слову")
    print("0 — Выход")


while True:
    show_menu()
    choice = input("Введите номер команды: ")

    if choice == "1":
        data = db.get_companies_and_vacancies_count()
        print("\nКомпании и количество вакансий:")
        for name, count in data:
            print(f"- {name}: {count} вакансий")

    elif choice == "2":
        data = db.get_all_vacancies()
        print("\nВсе вакансии:")
        for name, title, s_from, s_to, url in data:
            salary_str = f"{s_from or '–'}–{s_to or '–'}"
            print(f"- {name} | {title} | {salary_str} | {url}")

    elif choice == "3":
        avg = db.get_avg_salary()
        print(f"\nСредняя зарплата по всем вакансиям: {avg:.2f}")

    elif choice == "4":
        data = db.get_vacancies_with_higher_salary()
        print("\nВакансии с зарплатой выше средней:")
        for name, title, s_from, s_to in data:
            salary_str = f"{s_from or '–'}–{s_to or '–'}"
            print(f"- {name} | {title} | {salary_str}")

    elif choice == "5":
        keyword = input("Введите ключевое слово: ").strip()
        data = db.get_vacancies_with_keyword(keyword)
        print(f"\nВакансии с ключевым словом '{keyword}':")
        for name, title, url in data:
            print(f"- {name} | {title} | {url}")

    elif choice == "0":
        print("👋 До свидания!")
        db.close()
        break

    else:
        print("⚠️ Неверная команда. Попробуйте снова.")
