import os
import psycopg2
from dotenv import load_dotenv
from src.api import get_employers, get_vacancies

load_dotenv()

company_ids = [1740, 3529, 78638, 15478, 2180, 80, 3776, 2748, 1122462]


def load_data():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )
    cur = conn.cursor()

    # Получаем работодателей
    employers = get_employers(company_ids)

    for emp in employers:
        cur.execute(
            """
            INSERT INTO companies (id, name, description, site_url, open_vacancies)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
            """,
            (
                emp.get("id"),
                emp.get("name"),
                emp.get("description"),
                emp.get("site_url"),
                emp.get("open_vacancies"),
            )
        )

        # Получаем вакансии работодателя
        vacancies = get_vacancies(emp["id"])
        for vac in vacancies:
            salary = vac.get("salary") or {}
            cur.execute(
                """
                INSERT INTO vacancies (name, salary_from, salary_to, currency, vacancy_url, employer_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    vac.get("name"),
                    salary.get("from"),
                    salary.get("to"),
                    salary.get("currency"),
                    vac.get("alternate_url"),
                    emp.get("id")
                )
            )

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Данные успешно загружены в БД")
