import pandas as pd
import functions_with_data as fwd
from sklearn.feature_selection import VarianceThreshold
from sklearn.ensemble import RandomForestClassifier
from mlxtend.feature_selection import SequentialFeatureSelector
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


def key_skills_processing(data_train, data_test, top, flag):
    key_skills = fwd.get_uniq_key_skills(data_train, top)
    fwd.dummy_code(data_train, ["key_skills"], uniq_values=key_skills, flag=flag)
    fwd.dummy_code(data_test, ["key_skills"], uniq_values=key_skills, flag=flag)


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
    data_ml['group'] = "many_language"
    data_l = data_l.append(data_ml, sort=False)
    data_new = pd.DataFrame()
    data_new = data_new.append(data_l, sort=False)
    group_to_csv(data_new, path)
    return data_new


def group_to_csv(data, path, word=""):
    data.sort_values(data.columns[0], inplace=True)
    data.to_csv(word + path, sep=';', encoding="utf-8-sig", index=False)


def update_data(train, test, col, columns, tmp1, tmp2):
    col_ind = []
    for i in range(len(columns)):
        col_ind.append(i)
    drop_col = list(set(col_ind) - set(col))
    test = test.drop(test.columns[drop_col], axis=1)
    train = train.drop(train.columns[drop_col], axis=1)
    test['group'] = tmp2
    train['group'] = tmp1
    return train, test


def start_data_pretreatment(train_path, test_path, path, flag, index):
    train = grouping(train_path)
    test = grouping(test_path)
    key_skills_processing(data_train=train, data_test=test, top=100, flag=flag)
    remove_columns = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    train = train.drop(train.columns[remove_columns], axis=1)
    test = test.drop(test.columns[remove_columns], axis=1)
    if index == 3:
        selector = VarianceThreshold(0.009)
        tmp1 = train.group
        train = train.drop(['group'], axis=1)
        tmp2 = test.group
        test = test.drop(['group'], axis=1)
        selector.fit(train)
        col = selector.get_support(True)
        train, test = update_data(train, test, col, train.columns, tmp1, tmp2)
    if index == 4:
        model_rfc = RandomForestClassifier(n_estimators=70)
        selector = SequentialFeatureSelector(model_rfc, k_features=50,
                                             forward=True,
                                             floating=False,
                                             verbose=2,
                                             scoring='accuracy',
                                             cv=0,
                                             n_jobs=-1)
        tmp1 = train.group
        train = train.drop(['group'], axis=1)
        tmp2 = test.group
        test = test.drop(['group'], axis=1)
        selector = selector.fit(train, tmp1)
        col = selector.k_feature_idx_
        train, test = update_data(train, test, col, train.columns, tmp1, tmp2)
    train.to_csv("train_" + str(index) + "_" + path, sep=';', encoding="utf-8-sig", index=False)
    test.to_csv("test_" + str(index) + "_" + path, sep=';', encoding="utf-8-sig", index=False)
    return train, test
