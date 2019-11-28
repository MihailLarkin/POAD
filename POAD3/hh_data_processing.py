import hh_parse_vacancies as hh
import pandas as pd
import numpy as np
import datetime as dt
import regex as re

path = 'files\\'


def get_uniq_key_skills(df, groups_count):
    uniq_key_skills = {}
    key_skills = [c for c in df["key_skills"].str.split(";")]
    for j in range(len(key_skills)):
        if key_skills[j] is not None:
            if len(key_skills[j]) > 0:
                for k in range(len(key_skills[j])):
                    if not key_skills[j][k] in uniq_key_skills:
                        uniq_key_skills[key_skills[j][k]] = [None] * groups_count
    return uniq_key_skills


def get_unique_min_salary(df):
    return df[df["min_salary"].notna()]["min_salary"].unique()


def get_unique_max_salary(df):
    return df[df["max_salary"].notna()]["max_salary"].unique()


def input_unique_count(uniques_values_dict, uniques_dict, index, value, data, length=11):
    not_nan_data = data[data[value].notna()]
    for s in range(len(uniques_dict)):
        if uniques_dict[s] is not None:
            if not uniques_dict[s] in uniques_values_dict:
                uniques_values_dict[uniques_dict[s]] = [None] * length
            uniques_values_dict[uniques_dict[s]][index] = len(
                not_nan_data[not_nan_data[value] == uniques_dict[s]][value])


def sort_data(df):
    df = df.sort_values(['max_salary', 'min_salary'], ascending=[True, True])
    df.to_csv(path + "sorted_by_salary.csv", sep=";", encoding="utf-8-sig")


def hh_information_to_csv_salary(df):
    uniq_names_dict = {}
    uniq_experience_dict = {}
    uniq_employment_dict = {}
    uniq_schedule_dict = {}

    unique_names = df["name"].unique()
    groups_count = 11
    aggregate_date_dict = {
        "min_days": [None] * groups_count,
        "avg_days": [None] * groups_count,
        "max_days": [None] * groups_count,
    }
    unique_experiences = df["experience"].unique()
    unique_employments = df["employment"].unique()
    unique_schedules = df["schedule"].unique()
    min_salary = df["max_salary"].min()
    max_salary = df["max_salary"].max()
    uniq_key_skills = get_uniq_key_skills(df=df, groups_count=groups_count)
    h = (max_salary - min_salary) / 10
    for i in range(0, 10):
        if i == 0:
            group = df[np.logical_and(df["max_salary"] >= min_salary, df["max_salary"] <= min_salary + h)]
            group.to_csv(path + "salary_groups\\salary_group: " +
                         str(min_salary + h * i) + "-" + str( min_salary + h * (i + 1)) +
                         ".csv",sep=";", encoding="utf-8-sig")
            df_empty_group = df[df["max_salary"].isna()]
            df_empty_group.to_csv(path + "salary_groups\\empty_salary.csv", sep=";", encoding="utf-8-sig")

            input_unique_count(uniq_names_dict, unique_names, 10, "name", df_empty_group)
            input_unique_count(uniq_experience_dict, unique_experiences, 10, "experience", df_empty_group)
            input_unique_count(uniq_employment_dict, unique_employments, 10, "employment", df_empty_group)
            input_unique_count(uniq_schedule_dict, unique_schedules, 10, "schedule", df_empty_group)
        else:
            group = df[np.logical_and(df["max_salary"] > min_salary + h * i,
                                      df["max_salary"] <= min_salary + h * (i + 1))]
            group.to_csv(
                path + "salary_groups\\group " + str(min_salary + h * i) + "-" + str(
                    min_salary + h * (i + 1)) + ".csv",
                sep=";", encoding="utf-8-sig")

            aggregate_date_dict["min_days"][i] = group["days_from_today"].min()
            aggregate_date_dict["max_days"][i] = group["days_from_today"].max()
            aggregate_date_dict["avg_days"][i] = group["days_from_today"].mean()

            input_unique_count(uniq_names_dict, unique_names, i, "name", group)
            input_unique_count(uniq_experience_dict, unique_experiences, i, "experience", group)
            input_unique_count(uniq_employment_dict, unique_employments, i, "employment", group)
            input_unique_count(uniq_schedule_dict, unique_schedules, i, "schedule", group)

            not_nan_data = group[group["key_skills"].notna()]
            for key in uniq_key_skills:
                uniq_key_skills[key][i] = len(not_nan_data[not_nan_data["key_skills"].str.find(key) >= 0])

        uniq_names_df = pd.DataFrame(uniq_names_dict)
        uniq_names_df.to_csv(path + "salary_groups\\unique_names.csv", sep=";", encoding="utf-8-sig")

        uniq_experience_df = pd.DataFrame(uniq_experience_dict)
        uniq_experience_df.to_csv(path + "salary_groups\\uniq_experience.csv", sep=";", encoding="utf-8-sig")

        uniq_employment_df = pd.DataFrame(uniq_employment_dict)
        uniq_employment_df.to_csv(path + "salary_groups\\uniq_employment.csv", sep=";", encoding="utf-8-sig")

        uniq_schedule_df = pd.DataFrame(uniq_schedule_dict)
        uniq_schedule_df.to_csv(path + "salary_groups\\uniq_schedule.csv", sep=";", encoding="utf-8-sig")

        days_df = pd.DataFrame(aggregate_date_dict)
        days_df.to_csv(path + "salary_groups\\days_info.csv", sep=";", encoding="utf-8-sig")

        key_skills_df = pd.DataFrame(uniq_key_skills)
        key_skills_df.to_csv(path + "salary_groups\\key_skills.csv", sep=";", encoding="utf-8-sig")


def hh_information_to_csv_names(df):
    df_g = df.sort_values(['name'])
    df_g.to_csv(path+"names_group_one_file.csv", sep=";", encoding="utf-8-sig")
    uniq_experience_dict = {}
    uniq_min_salary_dict = {}
    uniq_max_salary_dict = {}
    uniq_employment_dict = {}
    uniq_schedule_dict = {}
    unique_names = df["name"].unique()
    groups_count = len(unique_names)
    aggregate_date_dict = {
        "min_days": [None] * groups_count,
        "avg_days": [None] * groups_count,
        "max_days": [None] * groups_count,
    }
    unique_min_salary = get_unique_min_salary(df)
    unique_max_salary = get_unique_max_salary(df)
    unique_experiences = df["experience"].unique()
    unique_employments = df["employment"].unique()
    unique_schedules = df["schedule"].unique()
    min_salary = df["max_salary"].min()
    max_salary = df["max_salary"].max()
    uniq_key_skills = get_uniq_key_skills(df=df, groups_count=groups_count)
    step = (max_salary - min_salary) / 10
    for i in range(len(unique_names)):
        df_group = df[df["name"] == unique_names[i]]
        df_group.to_csv(
            path + "name_groups\\group_name " + unique_names[i].replace('/', ';').replace('\\', ';')
            .replace('"', "").replace('|', '') + "(" + str(
                i) + ").csv",
            sep=";", encoding="utf-8-sig")

        aggregate_date_dict["min_days"][i] = df_group["days_from_today"].min()
        aggregate_date_dict["max_days"][i] = df_group["days_from_today"].max()
        aggregate_date_dict["avg_days"][i] = df_group["days_from_today"].mean()

        input_unique_count(uniq_min_salary_dict, unique_min_salary, i, "min_salary", df_group, groups_count)
        input_unique_count(uniq_max_salary_dict, unique_max_salary, i, "max_salary", df_group, groups_count)
        input_unique_count(uniq_experience_dict, unique_experiences, i, "experience", df_group, groups_count)
        input_unique_count(uniq_employment_dict, unique_employments, i, "employment", df_group, groups_count)
        input_unique_count(uniq_schedule_dict, unique_schedules, i, "schedule", df_group, groups_count)

        not_nan_ks = df_group[df_group["key_skills"].notna()]
        for key in uniq_key_skills:
            uniq_key_skills[key][i] = len(not_nan_ks[not_nan_ks["key_skills"].str.find(key) >= 0])

    uniq_min_salary_df = pd.DataFrame(uniq_min_salary_dict)
    uniq_min_salary_df.to_csv(path + "name_groups\\unique_min_salary.csv", sep=";", encoding="utf-8-sig")

    uniq_max_salary_df = pd.DataFrame(uniq_max_salary_dict)
    uniq_max_salary_df.to_csv(path + "name_groups\\unique_max_salary.csv", sep=";", encoding="utf-8-sig")

    uniq_experience_df = pd.DataFrame(uniq_experience_dict)
    uniq_experience_df.to_csv(path + "name_groups\\uniq_experience.csv", sep=";", encoding="utf-8-sig")

    uniq_employment_df = pd.DataFrame(uniq_employment_dict)
    uniq_employment_df.to_csv(path + "name_groups\\uniq_employment.csv", sep=";", encoding="utf-8-sig")

    uniq_schedule_df = pd.DataFrame(uniq_schedule_dict)
    uniq_schedule_df.to_csv(path + "name_groups\\uniq_schedule.csv", sep=";", encoding="utf-8-sig")

    days_df = pd.DataFrame(aggregate_date_dict)
    days_df.to_csv(path + "name_groups\\days_info.csv", sep=";", encoding="utf-8-sig")

    key_skills_df = pd.DataFrame(uniq_key_skills)
    key_skills_df.to_csv(path + "name_groups\\key_skills.csv", sep=";", encoding="utf-8-sig")


def start_processing():
    path = 'files\\'
    hh_dict = hh.get_vacancies()
    df = pd.DataFrame(hh_dict)
    df['description'] = df['description'].apply(lambda x: (re.sub(r'<.*?>', '', str(x))))
    df['created_at'] = df['created_at'].apply(lambda x: (
        re.sub(r'(?<date>\d{4}-\d{2}-\d{2}).*', re.match("(?<date>\d{4}-\d{2}-\d{2}).*", str(x))["date"], str(x))))
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["days_from_today"] = pd.Series([(dt.datetime.today() - c).days for c in df["created_at"]])
    df.to_csv(path + 'hh_vacancies.csv', sep=";", encoding="utf-8-sig")

    df = df.sort_values(['max_salary', 'min_salary'], ascending=[True, True])
    df.to_csv(path + "sorted_by_salary.csv", sep=";", encoding="utf-8-sig")
    hh_information_to_csv_names(df)
    hh_information_to_csv_salary(df)


start_processing()

