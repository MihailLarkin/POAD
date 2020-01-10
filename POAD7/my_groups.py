import pandas as pd
import warnings

warnings.filterwarnings("ignore")

popular_vacancies_regex = {"1C": "1[ ]*[СсCc](?!.битрикс|.bitrix)",
                           "1C Bitrix": "(1[СсCc])?.(битрикс|.bitrix)",
                           "C#": "([cс]#)|(net)|(asp)|(core)",
                           "C++": "([сc][ ]*[+][ ]*[+])",
                           "JavaScript": "(front[ ]*[-]?[ ]*end)|(js)|(node)|(javascript)|(фронт[ ]*[-]?[ ]*енд)|("
                                         "react)|(angular)|(vue)",
                           "PHP": "(php)|(пхп)",
                           "Java": "(\\bjava\\b)|(android)|(андроид)",
                           "SQL": "(sql)|(oracle)|(postgres)",
                           "Python": "(python)|(питон)|(django)",
                           "Delphi": "(delphi)",
                           "Ruby": "(ruby)",
                           "Unity": "(unity)"
                           }


def grouping(path):
    data = pd.read_csv(path, sep=';')
    data['min_salary'].fillna(data['min_salary'].mode().iloc[0], inplace=True)
    data['max_salary'].fillna(data['max_salary'].max(), inplace=True)
    data = data[data['min_salary'] <= data['max_salary']]
    data = data[~data['key_skills'].isna()]
    data_ml = pd.DataFrame()
    data_l = pd.DataFrame()
    for i in popular_vacancies_regex:
        group = data[data["name"].str.lower().str.contains(popular_vacancies_regex[i], regex=True)]
        group["group"] = i
        for j in popular_vacancies_regex:
            if i != j:
                tmp = group[group["name"].str.lower().str.contains(popular_vacancies_regex[j], regex=True)]
                data_ml = data_ml.append(tmp)
                group = group.drop(tmp.index)
        data_l = data_l.append(group)
    data_ml = data_ml.drop_duplicates()
    data_ml['group'] = "many_language"
    data_l = data_l.append(data_ml, sort=False)
    data_other = data[~data["name"].isin(data_l["name"])]
    data_other['group'] = "other"
    data_new = pd.DataFrame()
    data_new = data_new.append(data_l, sort=False)
    data_new = data_new.append(data_other, sort=False)
    data_new.sort_index(inplace=True)
    data_new.drop_duplicates(inplace=True)
    data_new.reset_index(drop=True, inplace=True)
    data_new.to_csv("my_group.csv", sep=';', encoding="utf-8-sig")
    return data_new["group"]
