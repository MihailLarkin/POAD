import classification as cl
import pandas as pd

names = ["Исходный", "С проектированными признаками", "С отбором признаков (дисперсия)",
         "С отбором признаков (перебор)"]
info = {"Название": [], "Количество признаков": [], "Точность (Train)": [], "Точность (Test)": []}
for i in range(1, 5):
    if i != 1:
        features_count, score_train, score_test = cl.start_classification(train_path="data.csv",
                                                                          test_path='test_data.csv',
                                                                          path="data.csv", flag=True, index=i)
    else:
        features_count, score_train, score_test = cl.start_classification(train_path="data.csv",
                                                                          test_path='test_data.csv',
                                                                          path="data.csv", flag=False, index=i)
    info["Название"].append(names[i - 1])
    info["Количество признаков"].append(features_count)
    info["Точность (Train)"].append(score_train)
    info["Точность (Test)"].append(score_test)


out = pd.DataFrame().from_dict(info)
out.to_csv("out.csv", sep=';', encoding="utf-8-sig", index=False)
