import pandas as pd
from sklearn.preprocessing import LabelEncoder

label_dict = {}


def normalization(series, f_min=0, f_max=1):
    d_min, d_max = series.min(), series.max()
    factor = (f_max - f_min) / (d_max - d_min)
    normalized = f_min + (series - d_min) * factor
    return normalized, factor


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


def label_encoding(data, column):
    label = LabelEncoder()
    dicts = {}
    label.fit(data[column].drop_duplicates())
    dicts[column] = list(label.classes_)
    label_dict[column] = {}
    code = label.transform(label.classes_)
    data[column] = label.transform(data[column])
    return label.classes_, code


def dummy_code(data, columns, uniq_values=None):
    get_uniq = False
    for column in columns:
        if uniq_values is None:
            uniq_values = data[column].unique()
            get_uniq = True
        for i in range(len(uniq_values)):
            data[uniq_values[i]] = data[column].apply(
                lambda x: 1 if x.find(uniq_values[i]) > -1 else 0)
        if get_uniq:
            uniq_values = None
    data = data.drop(columns=columns)
    return data


def start_preprocessing(path):
    data = pd.read_csv(path, sep=';')
    data.reset_index(drop=True, inplace=True)
    data['min_salary'].fillna(data['min_salary'].mode().iloc[0], inplace=True)
    data['max_salary'].fillna(data['max_salary'].max(), inplace=True)
    data = data[data['min_salary'] <= data['max_salary']]
    data = data[~data['key_skills'].isna()]
    tmp = data['name']
    remove_columns = ['area', 'key_skills', 'name', 'employer', 'created_at', 'description', 'responsibility',
                      'Unnamed: 0',
                      'requirement']
    columns = ['experience', 'employment', 'schedule']

    data['days_count'] = normalization(data['days_count'])[0]
    key_skills = get_uniq_key_skills(data, 10)
    dummy_code(data, ["key_skills"], key_skills)
    for c in columns:
        a, b = label_encoding(data, c)
        j = 0
        for i in a:
            label_dict[c][i] = b[j]
            j += 1
    data.drop(remove_columns, axis=1, inplace=True)
    #data.to_csv("new_data.csv", sep=';', encoding="utf-8-sig")
    data.reset_index(drop=True, inplace=True)
    return data, tmp
