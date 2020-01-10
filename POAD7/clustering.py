from sklearn.cluster import KMeans, SpectralClustering
import data_preprocessing as dp
import numpy as np
import collections
import os
import warnings

warnings.filterwarnings("ignore")


def get_center_cluster_by_func(data, group):
    centres = []
    for i in range(0, 10):
        dt = data[data[group] == i]
        dt.drop(["k_means_group"], axis=1, inplace=True)
        tmp = []
        for j in dt.columns:
            if j != "spectral_clustering_group":
                tmp.append(dt[j].mean())
        centres.append(tmp)
    return centres


def dict_to_str(d):
    output_str = ""
    for i in d:
        output_str += str(i) + ": " + str(d[i]) + "  "
    return output_str.strip()


def get_values(d, val):
    search_item = 0
    for i in d:
        if d[i] == val:
            search_item = i
    return search_item


def get_salary_info(data):
    return {"max_mean": data['max_salary'].mean(), "min_mean": data['min_salary'].mean()}


def feature_counter(data, col):
    counter = collections.Counter()
    for val in data[col]:
        counter[val] += 1
    counter_dict = dict(counter)
    decoder_dict = {}
    for i in counter_dict:
        new_key = get_values(dp.label_dict[col], i)
        decoder_dict[new_key] = counter_dict[i]
    return decoder_dict


def get_key_skills(data):
    columns_sum = {}
    dt = data.drop(["spectral_clustering_group", "k_means_group",'name'], axis=1)
    for i in range(6, len(dt.columns)):
        columns_sum[dt.columns[i]] = dt[dt.columns[i]].sum()
    sorted_sum = [(k, columns_sum[k]) for k in sorted(columns_sum.keys(), key=columns_sum.get, reverse=True)][:5]
    keys_dict = {}
    for i in sorted_sum:
        keys_dict[i[0]] = i[1]
    return keys_dict


def get_all_info(data, center, path, group):
    output_str = ""
    os.remove(path)
    for i in range(0, 10):
        dt = data[data[group] == i]
        dt.reset_index(drop=True, inplace=True)
        output_str += "Кластер " + str(i + 1) + "\n" + "Количество объектов: " + str(
            len(dt)) + "\n" + "Центр: " + "\n"
        output_str += dict_to_str(get_center_cluster(dt, center[i])) + "\n" + "Топ 5 key skills: " + dict_to_str(
            get_key_skills(dt)) + "\n"
        output_str += dict_to_str(get_salary_info(dt)) + "\n"
        columns = ['experience', 'employment', 'schedule']
        for c in columns:
            output_str += c + ": " + dict_to_str(feature_counter(dt, c)) + "\n"
        output_str += "\n\n"
        f = open(path, 'a')
        f.write(output_str)
        output_str = ""
        f.close()


def get_center_cluster(data, center):
    name = data['name']
    df = data.drop(["k_means_group", "spectral_clustering_group",'name'], axis=1)
    min = np.linalg.norm(df.iloc[0].to_numpy() - center)
    index = 0
    for i in df.index:
        tmp = np.linalg.norm(df.iloc[i].to_numpy() - center)
        if tmp < min:
            min = tmp
            index = i
    searching_center = df.iloc[index].to_dict()
    searching_center['name'] = name[index]
    return searching_center


def start_clustering(path):
    data, name = dp.start_preprocessing(path)
    name.reset_index(drop=True,inplace=True)
    k_means_clustering = KMeans(n_clusters=10).fit(data)
    spectral_clustering = SpectralClustering(n_clusters=10, random_state=1,
                                             affinity='nearest_neighbors')

    data['k_means_group'] = k_means_clustering.predict(data)
    data['spectral_clustering_group'] = spectral_clustering.fit_predict(data, data)

    spectral_clustering_centres = get_center_cluster_by_func(data, "spectral_clustering_group")
    k_means_centres = k_means_clustering.cluster_centers_
    data.reset_index(drop=True, inplace=True)
    data['name'] = name
    get_all_info(data, k_means_centres, "KMeans.txt", "k_means_group")
    get_all_info(data, spectral_clustering_centres, "SpectralClustering.txt", "spectral_clustering_group")
    dt = data.drop(['spectral_clustering_group'], axis=1)
    return dt
