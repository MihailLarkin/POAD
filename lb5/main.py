import parse_vacancies as hh
import pandas as pd
from tqdm import tqdm
import datetime as dt
import regex as re
import data_separation as ds


def download_data_to_csv():
    df = pd.DataFrame()
    cities = [1, 2, 3, 4, 66]
    for i in tqdm(cities):
        df = df.append(pd.DataFrame(hh.get_vacancies(i)))
    df = df.reset_index(drop=True)
    df = df[df['created_at'].notna()]
    df['description'] = df['description'].apply(lambda x: (re.sub(r'<.*?>', '', str(x))))
    df['created_at'] = df['created_at'].apply(lambda x: (
        re.sub(r'(?<date>\d{4}-\d{2}-\d{2}).*', re.match("(?<date>\d{4}-\d{2}-\d{2}).*", str(x))["date"],
               str(x))))
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["days_count"] = pd.Series([(dt.datetime.today() - c).days for c in df["created_at"]])
    df.to_csv("data.csv", sep=";", encoding="utf-8-sig")


if __name__ == "__main__":
    # download_data_to_csv()
    ds.popular_groups_separation("data.csv")
