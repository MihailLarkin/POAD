import pandas as pd


def fill_nan_value(data, skills):
    mean_max = round(data["max_salary"].mean(skipna=True), 0)
    mean_min = round(data["min_salary"].mean(skipna=True), 0)
    min_min = round(data["min_salary"].min(skipna=True), 0)
    data["max_salary"] = data["max_salary"].fillna(mean_max)
    if mean_min > mean_max:
        data["min_salary"] = data["min_salary"].fillna(min_min)
    else:
        data["min_salary"] = data["min_salary"].fillna(mean_min)
    data["key_skills"] = data["key_skills"].fillna(skills)
    data["conditions"] = data["conditions"].fillna("Не указан")


df = pd.read_csv("sorted_by_salary.csv", sep=';')

popular_vacancies_regex = {"1C": "1[ ]*[СсCc](?!.битрикс|.bitrix)",
                           "1C Bitrix": "(1[СсCc])?.(битрикс|.bitrix)",
                           "C#": "([cс]#)|(net)|(asp)|(core)",
                           "C++": "([сc][ ]*[+][ ]*[+])",
                           "JavaScript": "(front[ ]*[-]?[ ]*end)|(js)|(node)|(javascript)|(фронт[ ]*[-]?[ ]*енд)|("
                                         "react)|(angular)|(vue)",
                           "PHP": "(php)|(пхп)",
                           "JAVA": "(\\bjava\\b)",
                           "IOS": "(ios)",
                           "SQL": "(sql)|(oracle)|(postgres)",
                           "Android_JAVA": "(android)|(андроид)",
                           "Python": "(python)|(питон)|(django)",
                           "GO": "(\\bgo\\b)|(golang)",
                           "Delphi": "(delphi)",
                           "Ruby": "(ruby)",
                           "Unity": "(unity)"
                           }
regex_web_none_language = "(web)|(веб)"
regex_backend_none_language = "(back[ ]*[-]?[ ]*end)"
many_language = pd.DataFrame()
group_with_language = pd.DataFrame()
for i in popular_vacancies_regex:
    group_df = df[df["name"].str.lower().str.contains(popular_vacancies_regex[i], regex=True)]
    for j in popular_vacancies_regex:
        if i != j:
            tmp = group_df[group_df["name"].str.lower().str.contains(popular_vacancies_regex[j], regex=True)]
            many_language = many_language.append(tmp)
            group_df = group_df.drop(tmp.index)
    group_with_language = group_with_language.append(group_df)
    fill_nan_value(group_df, i)
    group_df.to_csv("./groups/" + i + ".csv", sep=';', encoding="utf-8-sig", index=False)
many_language = many_language.drop_duplicates()
group_with_language = group_with_language.append(many_language)
other = df[~df["name"].isin(group_with_language["name"])]
web = other[other["name"].str.lower().str.contains(regex_web_none_language, regex=True)]
other = other.drop(web.index)
back = other[other["name"].str.lower().str.contains(regex_backend_none_language, regex=True)]
other = other.drop(back.index)
fill_nan_value(web, "Веб технологии")
fill_nan_value(back, "Backend разработка")
fill_nan_value(other, "Не указан")
fill_nan_value(many_language, "Знание любого языка программирования")
web.to_csv("./groups/Web_none_language.csv", sep=';', encoding="utf-8-sig", index=False)
back.to_csv("./groups/Backend_none_language.csv", sep=';', encoding="utf-8-sig", index=False)
other.to_csv("./groups/Other.csv", sep=';', encoding="utf-8-sig", index=False)
many_language.to_csv("./groups/ManyLanguage.csv", sep=';', encoding="utf-8-sig", index=False)
