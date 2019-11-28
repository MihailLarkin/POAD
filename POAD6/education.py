from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score, KFold
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import data_preprocessing as dt
import pandas as pd


def label_encoding(data, column):
    label = LabelEncoder()
    dicts = {}
    label.fit(data[column].drop_duplicates())
    dicts[column] = list(label.classes_)
    data[column] = label.transform(data[column])


def models_analysis(data):
    target = data.group
    train = data.drop(['group'], axis=1)
    itog_val = {}
    model_rfc = RandomForestClassifier(n_estimators=70)
    model_knc = KNeighborsClassifier(n_neighbors=18)
    model_svc = svm.SVC()
    kf = KFold(n_splits=5, shuffle=True, random_state=1)
    scores = cross_val_score(model_rfc, train, target, cv=kf)
    itog_val['RandomForestClassifier'] = scores.mean()
    scores = cross_val_score(model_knc, train, target, cv=kf)
    itog_val['KNeighborsClassifier'] = scores.mean()
    scores = cross_val_score(model_svc, train, target, cv=kf)
    itog_val['SVC'] = scores.mean()
    pd.DataFrame.from_dict(data=itog_val, orient='index').plot(kind='bar', legend=False)
    plt.show()
    print(model_rfc.score(train, target))


def start_training_and_predict(training_path, test_path):
    training_data, test_data = dt.start_data_preprocessing(train_path=training_path, test_path=test_path)
    columns = ["group"]
    for c in columns:
        label_encoding(training_data, c)
        label_encoding(test_data, c)
    # models_analysis(training_data)
    y_train = training_data.group
    x_train = training_data.drop(['group'], axis=1)
    y_test = test_data.group
    x_test = test_data.drop(['group'], axis=1)
    model_rfc = RandomForestClassifier(n_estimators=70)
    model_rfc = model_rfc.fit(x_train, y_train)
    print(model_rfc.score(x_train, y_train))
    print(model_rfc.score(x_test, y_test))
    result_columns = ["predict_group", "alg_group", "features"]
    result = pd.DataFrame(columns=result_columns)
    result["predict_group"] = model_rfc.predict(x_test)
    result["alg_group"] = y_test.reset_index(drop=True)
    key_skills = ' '.join([str(elem) for elem in x_test.columns])
    result["features"][0] = key_skills
    result.to_csv("result.csv", sep=';', encoding="utf-8-sig", index=False)
