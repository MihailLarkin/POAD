import warnings

import pandas as pd

warnings.filterwarnings("ignore")


def get_uniq_key_skills(df, top):
    uniq_key_skills = {}
    key_skills = pd.Series([c for c in df["key_skills"].str.split(";")]).dropna()
    for array in key_skills:
        if len(array) > 0:
            for key_skill in array:
                if key_skill != "":
                    if not key_skill in uniq_key_skills:
                        uniq_key_skills[key_skill] = 1
                    else:
                        uniq_key_skills[key_skill] += 1
    uniq_key_skills_df = pd.DataFrame(uniq_key_skills, index=["size"]).transpose()
    uniq_key_skills_df = uniq_key_skills_df.sort_values("size", ascending=False)
    return uniq_key_skills_df.head(top).transpose().columns.values


def normalization(series, f_min=0, f_max=1):
    d_min, d_max = series.min(), series.max()
    factor = (f_max - f_min) / (d_max - d_min)
    normalized = f_min + (series - d_min) * factor
    return normalized, factor


def dummy_code(data, columns, uniq_values=None, flag=False):
    get_uniq = False
    if flag:
        data["Frontend-developer"] = data['key_skills'].apply(
            lambda x: 1 if set(x.split(';')) >= {'CSS', 'HTML'} or
                           set(x.split(';')) >= {'CSS3',
                                                 'HTML5'}
            else 0)

        data["C#-developer"] = data['key_skills'].apply(
            lambda x: 1 if set(x.split(';')) >= {'C#', '.NET Framework'} else 0)
        data["PostgreSQL/MySQL-developer"] = data['key_skills'].apply(
            lambda x: 1 if set(x.split(';')) >= {'PostgreSQL', 'MySQL'} else 0)
        data["Android-developer"] = data['key_skills'].apply(
            lambda x: 1 if set(x.split(';')) >= {'Java', 'Android'} else 0)
        data["PHP/Laravel-developer"] = data['key_skills'].apply(
            lambda x: 1 if set(x.split(';')) >= {'PHP', 'Laravel'} else 0)
    for column in columns:
        if uniq_values is None:
            uniq_values = data[column].unique()
            get_uniq = True
        for i in range(len(uniq_values)):
            data[uniq_values[i]] = data[column].apply(
                lambda x: 1 if x.find(uniq_values[i]) > -1 else 0)
        data["Other"] = data[column].apply(
            lambda x: 1 if len(list(set(x.split(';')) - set(uniq_values))) > 0 else 0)
        if get_uniq:
            uniq_values = None
    data = data.drop(columns=columns)
    return data


def fill_nan_value(data, skills):
    data["key_skills"] = data["key_skills"].fillna(skills)


def sampling_salary(column):
    column_min = column.min()
    column_max = column.max()
    step = (column_max - column_min) / 10
    for i in range(10):
        salary_group = (column >= column_min + step * i) & (column < column_min + step * (i + 1))
        if i == 9:
            salary_group = (column >= column_min + step * i) & (column <= column_min + step * (i + 1))
        column[salary_group] = column[salary_group].apply(lambda x: (i + 1))
    return column
