from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_selection import VarianceThreshold
from mlxtend.feature_selection import SequentialFeatureSelector
import data_pretreatment as dp
import pandas as pd


def label_encoding(data, column):
    label = LabelEncoder()
    dicts = {}
    label.fit(data[column].drop_duplicates())
    dicts[column] = list(label.classes_)
    data[column] = label.transform(data[column])


def start_classification(train_path, test_path, path, flag, index):
    train_data, test_data = dp.start_data_pretreatment(train_path=train_path, test_path=test_path, path=path,
                                                       flag=flag, index=index)
    columns = ["group"]
    for c in columns:
        label_encoding(train_data, c)
        label_encoding(test_data, c)
    y_train = train_data.group
    x_train = train_data.drop(['group'], axis=1)
    y_test = test_data.group
    x_test = test_data.drop(['group'], axis=1)

    model_rfc = RandomForestClassifier(n_estimators=70)
    model_rfc = model_rfc.fit(x_train, y_train)
    return x_train.shape[1], model_rfc.score(x_train, y_train), model_rfc.score(x_test, y_test)
