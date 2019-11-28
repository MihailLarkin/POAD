import pandas as pd
import preliminary_processing as pp
import warnings
warnings.filterwarnings("ignore")

popular_vacancies_regex = {"1C": "1[ ]*[СсCc](?!.битрикс|.bitrix)",
                           "1C Bitrix": "(1[СсCc])?.(битрикс|.bitrix)",
                           "C#": "([cс]#)|(net)|(asp)|(core)",
                           "C++": "([сc][ ]*[+][ ]*[+])",
                           "JavaScript": "(front[ ]*[-]?[ ]*end)|(js)|(node)|(javascript)|(фронт[ ]*[-]?[ ]*енд)|("
                                         "react)|(angular)|(vue)",
                           "PHP": "(php)|(пхп)",
                           "Java": "(\\bjava\\b)",
                           "IOS": "(ios)",
                           "SQL": "(sql)|(oracle)|(postgres)",
                           "Android_Java": "(android)|(андроид)",
                           "Python": "(python)|(питон)|(django)",
                           "Golang": "(\\bgo\\b)|(golang)",
                           "Delphi": "(delphi)",
                           "Ruby": "(ruby)",
                           "Unity": "(unity)"
                           }


def other_groups_separation(df, group_with_language):
    regex_web_none_language = "(web)|(веб)"
    regex_backend_none_language = "(back[ ]*[-]?[ ]*end)"
    other = df[~df["name"].isin(group_with_language["name"])]
    web = other[other["name"].str.lower().str.contains(regex_web_none_language, regex=True)]
    other = other.drop(web.index)
    back = other[other["name"].str.lower().str.contains(regex_backend_none_language, regex=True)]
    other = other.drop(back.index)
    pp.fill_nan_value(web, "WEB")
    pp.fill_nan_value(back, "Backend")
    pp.fill_nan_value(other, "Not specified")
    web = key_skills_processing(web)
    back = key_skills_processing(back)
    other = key_skills_processing(other)
    web = discretization_processing(web)
    back = discretization_processing(back)
    other = discretization_processing(other)
    web.to_csv("./groups/Web_none_language.csv", sep=';', encoding="utf-8-sig", index=False)
    back.to_csv("./groups/Backend_none_language.csv", sep=';', encoding="utf-8-sig", index=False)
    other.to_csv("./groups/Other.csv", sep=';', encoding="utf-8-sig", index=False)


def key_skills_processing(data):
    key_skills = pp.get_uniq_key_skills(data)
    data = pp.dummy_code(data, ["key_skills"], uniq_values=key_skills, parse=True)
    return data


def discretization_processing(data):
    data["max_salary"] = pp.discretization_salary(data["max_salary"])
    data["min_salary"] = pp.discretization_salary(data["min_salary"])
    return data


def popular_groups_separation(path):
    df = pd.read_csv(path, sep=';')
    df['days_count'] = pp.normalization(df['days_count'])[0]
    df = pp.dummy_code(df, ["area", "experience", "employment", "schedule"])
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
        pp.fill_nan_value(group_df, i)
        group_df = key_skills_processing(group_df)
        group_df = discretization_processing(group_df)
        group_df.to_csv("./groups/" + i + ".csv", sep=';', encoding="utf-8-sig", index=False)
    many_language = many_language.drop_duplicates()
    pp.fill_nan_value(many_language, "Any_popular_language")
    many_language = key_skills_processing(many_language)
    many_language = discretization_processing(many_language)
    group_with_language = group_with_language.append(many_language, sort=True)
    other_groups_separation(df, group_with_language=group_with_language)
    many_language.to_csv("./groups/ManyLanguage.csv", sep=';', encoding="utf-8-sig", index=False)
