import education as ed
import get_vacancies as gv

if __name__ == '__main__':
    #gv.download_data_to_csv(city_indexes=[76])
    ed.start_training_and_predict("data.csv", "test_data.csv")