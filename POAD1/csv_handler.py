import functions_with_data as fdf

data = fdf.pd.read_csv('./brooklyn_sales_map.csv', sep=',', low_memory=False)
data['building_class_category'] = data['building_class_category'].str.replace('  ', ' ').str.replace('/', '_')
fdf.groups_to_csv(data)
fdf.describe_table_to_csv(data)
fdf.percents_building_class_category_to_csv(data)
fdf.normalize_numeric_data_to_csv(data)
