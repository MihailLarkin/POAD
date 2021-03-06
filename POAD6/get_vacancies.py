import pandas as pd
import requests
import datetime as dt
import regex as re


def get_vacancies(city):
    url_vacancies = 'https://api.hh.ru/vacancies?'
    params = {'area': city, 'text': 'Программист', "per_page": 100}
    url_vacancy = 'https://api.hh.ru/vacancies/'
    vac_count = requests.get(url_vacancies, params).json()["found"]
    vac_pages = requests.get(url_vacancies, params).json()["pages"]
    found = vac_count if vac_count < 1000 else 1000
    pages = vac_pages if vac_pages < 10 else 10
    hh_vacancies_dict = {
        "name": [None] * found,
        "area": [None] * found,
        "min_salary": [None] * found,
        "max_salary": [None] * found,
        "employer": [None] * found,
        "created_at": [None] * found,
        "experience": [None] * found,
        "employment": [None] * found,
        "schedule": [None] * found,
        "description": [None] * found,
        "responsibility": [None] * found,
        "requirement": [None] * found,
        "key_skills": [None] * found,
        "days_count": [None] * found,
    }
    count = 0

    for i in range(pages):
        params["page"] = i
        vacancies = requests.get(url_vacancies, params).json()["items"]
        for j in range(len(vacancies)):
            vacancy = requests.get(url_vacancy + vacancies[j]["id"]).json()
            hh_vacancies_dict["name"][count] = vacancy["name"]
            hh_vacancies_dict["area"][count] = vacancy["area"]["name"]
            if vacancy["salary"] is not None:
                hh_vacancies_dict["min_salary"][count] = vacancy["salary"]["from"]
                hh_vacancies_dict["max_salary"][count] = vacancy["salary"]["to"]
            hh_vacancies_dict["employer"][count] = vacancy["employer"]["name"]
            hh_vacancies_dict["created_at"][count] = vacancy["created_at"]
            hh_vacancies_dict["experience"][count] = vacancy["experience"]["name"]
            hh_vacancies_dict["employment"][count] = vacancy["employment"]["name"]
            hh_vacancies_dict["schedule"][count] = vacancy["schedule"]["name"]
            hh_vacancies_dict["description"][count] = vacancy["description"]
            hh_vacancies_dict["responsibility"][count] = vacancies[j]["snippet"]["responsibility"]
            hh_vacancies_dict["requirement"][count] = vacancies[j]["snippet"]["requirement"]
            if len(vacancy["key_skills"]) > 0:
                hh_vacancies_dict["key_skills"][count] = vacancy["key_skills"][0]["name"]
                for k in range(1, len(vacancy["key_skills"])):
                    hh_vacancies_dict["key_skills"][count] += ";" + vacancy["key_skills"][k]["name"]
            count += 1
    return hh_vacancies_dict


def download_data_to_csv(city_indexes):
    df = pd.DataFrame()
    cities = city_indexes
    for i in cities:
        df = df.append(pd.DataFrame(get_vacancies(i)))
    df = df.reset_index(drop=True)
    df = df[df['created_at'].notna()]
    df['description'] = df['description'].apply(lambda x: (re.sub(r'<.*?>', '', str(x))))
    df['created_at'] = df['created_at'].apply(lambda x: (
        re.sub(r'(?<date>\d{4}-\d{2}-\d{2}).*', re.match("(?<date>\d{4}-\d{2}-\d{2}).*", str(x))["date"],
               str(x))))
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["days_count"] = pd.Series([(dt.datetime.today() - c).days for c in df["created_at"]])
    df.to_csv("test_data.csv", sep=';', encoding="utf-8-sig")
