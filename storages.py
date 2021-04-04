import logging
import csv
import json

from abc import abstractmethod


class Repository:
    @abstractmethod
    def insert(self, friends):
        pass

    @abstractmethod
    def delete(self, friends):
        pass

    @abstractmethod
    def update(self, friends):
        pass

class CSVRepository(Repository):
    def __init__(self, config):
        self.__path_to_file = config["Repository"]["PATH_TO_CSV_FILE"]

    def insert(self, friends):
        logging.info("start insert in csv")
        with open(self.__path_to_file, "w") as csv_file:
            writer = csv.writer(csv_file, delimiter='\t')
            for friend in friends:
                writer.writerow(friend)
                logging.debug("insert new row, row: {0}".format(friend))


class JSONRepository(Repository):
    def __init__(self, config):
        self.__path_to_file = config["Repository"]["PATH_TO_JSON_FILE"]

    def insert(self, friends):
        logging.info("start insert in json")
        with open(self.__path_to_file, "w", encoding='utf-8') as json_file:
            json.dump(friends, json_file, ensure_ascii=False, indent=3)
            logging.debug("insert data in json")