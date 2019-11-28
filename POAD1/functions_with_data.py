import pandas as pd


def groups_to_csv(data):
    no_nan_data = data.fillna('nan_value')
    unique_field_value = pd.unique(no_nan_data['building_class_category'].values)
    for field_value in unique_field_value:
        no_nan_data[no_nan_data['building_class_category'] == field_value].to_csv('./csv_files/' + field_value + '.csv')


def describe_table_to_csv(data):
    nan_sum_data = data.isnull().sum().to_frame()
    df_desc = data.describe(include='all')
    df_desc.drop(df_desc.index[[1, 2, 3, 5, 7, 9]]).transpose().join(nan_sum_data).\
        rename(columns={'50%': 'median', 0: 'nan_count'}).\
        to_csv('./describe_table.csv', sep=';')


def percents_building_class_category_to_csv(data):
    percent_data = data.groupby('building_class_category').size() / len(data['building_class_category'])
    percent_data.to_csv('./percent_building_class_category.csv', sep=';', header=False)


def normalize_numeric_data_to_csv(data):
    numeric_columns = [c for c in data.columns if data[c].dtype.name != 'object']
    numeric_data = data[numeric_columns].fillna(0)
    normalized_numeric_data = (numeric_data-numeric_data.min())/(numeric_data.max() - numeric_data.min()).fillna(0)
    data[numeric_columns] = normalized_numeric_data
    data.to_csv('./normalized_numeric_data.csv', sep=';')
