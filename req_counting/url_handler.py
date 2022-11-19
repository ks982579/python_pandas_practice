"""
Small module to handle counting
Working on Facade-like Design pattern.
The 'ParserInterface' is what will be used in the notebook.
Through composition, it will use the controller and data.
"""

import pandas as pd
import numpy as np


class ParserInterface:
    """Class to run simple commands on data."""

    def __init__(self, csv_file: str) -> None:
        self.__controller = ParserController(csv_file)


class ParserController:
    """Class to interact with and manipulate data to perform analysis."""

    def __init__(self, csv_file: str):
        self.__data = ParserData(csv_file)


class ParserData:
    """Designed to store and manipulate data for analysis."""

    def __init__(self, csv_file_path):
        self.__dataframe = pd.read_csv(csv_file_path)

    def testMe(self, path):
        return self.__modify_df(path)

    @staticmethod
    def __correct_datetime_format(datetime_series):
        return pd.to_datetime(
            datetime_series, 
            errors="raise",
            format="%Y-%m-%d %H:%M:%S"
        )
    
    @staticmethod
    def __split_datetime_to_date_time(datetime_series):
        pass

    def __modify_df(self, path):
        _df = pd.read_csv(path)
        _date_series = self.__correct_datetime_format(_df["date"])
        date_ser, time_ser = "TODO: This Here!"

        return _date_series

    dataframe = property(
        fget=lambda self: self.__dataframe,
        doc="Providing restricted access to Dataframe.",
    )
