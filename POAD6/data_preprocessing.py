import pandas as pd
import functions_with_data as fwd
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


def key_skills_processing(data, test=False):
    if test:
        data = fwd.dummy_code(data, ["key_skills"], train_key_skills, parse=True)
    else:
        key_skills = fwd.get_uniq_key_skills(data)
        data = fwd.dummy_code(data, ["key_skills"], uniq_values=key_skills, parse=True)
    return data


def grouping(path):
    data = pd.read_csv(path, sep=';')
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
        fwd.fill_nan_value(group, i)
        data_l = data_l.append(group)
    data_ml = data_ml.drop_duplicates()
    fwd.fill_nan_value(data_ml, "any_popular_language")
    # data_ml = discretization_processing(data_ml)
    data_ml['group'] = "many_language"
    data_l = data_l.append(data_ml, sort=False)
    data_other = data[~data["name"].isin(data_l["name"])]
    data_other['group'] = "other"
    fwd.fill_nan_value(data_other, "not_specified")
    # data_other = discretization_processing(data_other)
    data_new = pd.DataFrame()
    data_new = data_new.append(data_l, sort=False)
    data_new = data_new.append(data_other, sort=False)
    group_to_csv(data_new, path)
    return data_new


def dummy_code_key_skills(data_train, data_test):
    key_skills = fwd.get_uniq_key_skills(data_train)
    fwd.dummy_code(data_train, ["key_skills"], uniq_values=key_skills, parse=True)
    fwd.dummy_code(data_test, ["key_skills"], uniq_values=key_skills, parse=True)


def group_to_csv(data, path, word=""):
    data.sort_values(data.columns[0], inplace=True)
    data.to_csv(word + path, sep=';', encoding="utf-8-sig", index=False)


def start_data_preprocessing(train_path, test_path):
    train = grouping(train_path)
    test = grouping(test_path)
    dummy_code_key_skills(train, test)
    remove_columns = [range(0, 15)]  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    train = train.drop(train.columns[remove_columns], axis=1)
    test = test.drop(test.columns[remove_columns], axis=1)
    return train, test
