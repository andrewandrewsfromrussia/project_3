import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv


load_dotenv()


def create_database(db_name: str, user: str, password: str, host: str, port: str) -> None:
    """
    Создание БД, если её нет
    """
    conn = psycopg2.connect(dbname="postgres", user=user, password=password, host=host, port=port)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
    exists = cur.fetchone()

    if not exists:
        cur.execute(f"CREATE DATABASE {db_name}")
        print(f"✅ База данных '{db_name}' успешно создана")
    else:
        print(f"ℹ️ База данных '{db_name}' уже существует")

    cur.close()
    conn.close()


def create_tables():
    """
    Создание таблиц companies и vacancies
    """
    db_name = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")

    conn = psycopg2.connect(dbname=db_name, user=user, password=password, host=host, port=port)
    cur = conn.cursor()

    # Создание таблиц
    cur.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            site_url TEXT,
            open_vacancies INTEGER
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS vacancies (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            salary_from INTEGER,
            salary_to INTEGER,
            currency TEXT,
            vacancy_url TEXT,
            employer_id INTEGER REFERENCES companies(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Таблицы успешно созданы")
