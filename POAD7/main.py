import clustering as cl
import my_groups as mg
import collections
import os
import warnings

warnings.filterwarnings("ignore")


def dict_to_str(d):
    output_str = ""
    for i in d:
        output_str += str(i) + ": " + str(d[i]) + "\n"
    return output_str.strip()


def feature_counter(data, col):
    counter = collections.Counter()
    for val in data[col]:
        counter[val] += 1
    counter_dict = dict(counter)
    return counter_dict


def get_values(d, val):
    search_item = 0
    for i in d:
        if d[i] == val:
            search_item = i
    return search_item


def get_all_info(data, group, path):
    output_str = ""
    os.remove(path)
    for i in range(10):
        df = data[data[group] == i]
        output_str += "Кластер " + str(i + 1) + "\n" + "Количество объектов: " + str(len(df)) + "\n"
        output_str += dict_to_str(feature_counter(df, "my_group")) + "\n\n"
        f = open(path, 'a')
        f.write(output_str)
        output_str = ""
        f.close()


if __name__ == "__main__":
    dt = cl.start_clustering("data.csv")
    dt["my_group"] = mg.grouping("data.csv")
    get_all_info(dt, "k_means_group", "diff.txt")
