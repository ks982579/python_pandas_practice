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

    def __init__(self, csv_file: str, exceptions: list[str]) -> None:
        self.__exceptions = exceptions  # TODO: pass through functions
        self.__controller = ParserController(csv_file)


class ParserController:
    """Class to interact with and manipulate data to perform analysis."""

    def __init__(self, csv_file: str):
        self.__data = ParserData(csv_file)


class ParserData:
    """
    Designed to store and manipulate data for analysis.
    """

    def __init__(self, csv_file_path):
        self.__dataframe = self.__modify_df(csv_file_path)

    @staticmethod
    def __correct_path_format(url_series):
        """Method for correcting url path format to keep standard"""

        def slash_checker(url: str):
            url = url.strip()
            if not (url.startswith("/")):
                url = "/" + url

            if not (url.endswith("/")):
                url = url + "/"

            return url

        return url_series.apply(slash_checker)

    @staticmethod
    def __correct_datetime_format(datetime_series):
        """Method for transforming string-datetime series into datetime data type."""
        return pd.to_datetime(
            datetime_series, errors="raise", format="%Y-%m-%d %H:%M:%S"
        )

    @staticmethod
    def __split_datetime_to_date_time(datetime_series):
        """Method to split datetime series into a date series and time series."""
        _date_ser = datetime_series.dt.date
        _time_ser = datetime_series.dt.time
        return (_date_ser, _time_ser)

    def __modify_df(self, path):
        """Method to modify dataframe for easy use going forward."""
        _df = pd.read_csv(path)
        _path_ser = self.__correct_path_format(_df["path"])
        _date_series = self.__correct_datetime_format(_df["date"])
        _d, _t = self.__split_datetime_to_date_time(_date_series)
        _df = pd.DataFrame({"path": _path_ser, "date": _d, "time": _t})
        return _df

    dataframe = property(
        fget=lambda self: self.__dataframe,
        doc="Providing restricted access to Dataframe.",
    )
