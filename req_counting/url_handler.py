"""
Small module to handle counting
Working on Facade-like Design pattern.
The 'ParserInterface' is what will be used in the notebook.
Through composition, it will use the controller and data.
"""

import pandas as pd
import numpy as np
from datetime import datetime as dt
from datetime import timedelta as td
from typing import Optional


class ParserInterface:
    """Class to run simple commands on data."""

    def __init__(self, csv_file: str, exceptions: list[str]) -> None:
        self.__exceptions = exceptions  # TODO: pass through functions
        self.__controller = ParserController(csv_file)

    def show_usage_flags(self, quan_dict: dict[str, int]) -> pd.DataFrame:
        """To display a dataframe of counts and labeled usages"""
        # -- Get The grouped data
        count_ser = self.__controller.group_by_path()

        # -- Should show histogram

        # -- Get quantiles
        quants = self.__controller.get_quants_df(count_ser, quan_dict, self.__exceptions)

        return quants
    
    def show_monthly_counts(self, months: Optional[int]= None) -> pd.DataFrame:
        self.__controller.monthly_group(months)
        return 0


class ParserController:
    """Class to interact with and manipulate data to perform analysis."""

    def __init__(self, csv_file: str, urls_file: str):
        self.__data = ParserData(csv_file, urls_file)

    def testMe(self, _dy, _ex):
        _ser = self.group_by_path()
        return self.get_quants_df(_ser, _dy, _ex)
    
    @staticmethod
    def __apply_exclusion(series: pd.Series, exclusion: list[str]) -> pd.Series:
        """Excluding rows based on index values"""
        _filter = pd.Series(series.index, index=series.index).isin(exclusion)
        return series.loc[~_filter]
    
    @staticmethod
    def __apply_label(labels_dataframe, count):
        """For use within apply() method"""
        for _i in range(len(labels_dataframe)):
            # get row
            _r = labels_dataframe.iloc[_i]
            if count <= _r["quant_val"]:
                return _r["labels"]

        # Should not make it to this return value
        return np.NAN

    @staticmethod
    def __get_root(url: str) -> str:
        """Remove beginning and ending forward slashes"""
        return url[1:url.find("/", 1)]

    # --- Groupint Data ---
    def group_by_path(self) -> pd.Series:
        """Creates a series, indexed by path, displaying count for each path"""
        _gdf = self.__data.dataframe.groupby(by="path")
        _ser = _gdf.count()["date"]
        _ser.name = "requests"
        return _ser
    
    def monthly_groups(self, months):
        
        # return self.__data.dataframe["date-time"].dt.isocalendar()
        #return self.__data.dataframe["date-time"].dt.month
        _now = dt.now()
        _then = dt(_now.year, (_now.month - months)%12, _now.day)
        return _then
    
    # --- Providing new dataframes ---
    def get_quants_df(self, series, percent_dict, exceptions):
        """Given a series of counts for endpoints, returns labeled quantile thresholds."""
        # Create quantile Dataframe
        _dict = {
            "labels": percent_dict.keys(),
            "quantile": percent_dict.values(),
        }
        quantDF = pd.DataFrame(_dict)

        ## FILTER OUT EXCEPTIONS
        ### the .filter() method keeps index in list, we want to exclude
        series = self.__apply_exclusion(series, exceptions)

        # Adding thresholds
        quantDF["quant_val"] = quantDF["quantile"].apply(lambda x: series.quantile(q=(x/100)))

        # Do we have 'no-use'?
        if not (0 in quantDF["quantile"].array):
            # add on to last row
            quantDF.loc[len(quantDF)] = {"labels": "none", "quantile": 0, "quant_val": 0}
        
        # ensure sorted
        quantDF.sort_values("quantile", inplace=True)
        quantDF.reset_index(drop=True, inplace=True)

        ## reindex series to include 0 values
        series = series.reindex(self.__data.possible_urls, fill_value=0)
        
        # Reapply exclusion
        series = self.__apply_exclusion(series, exceptions)

        # Create DataFrame
        usage_series = series.apply(lambda x: self.__apply_label(quantDF, x))
        usage_series.name = "usage"

        # Get Root
        _root_ser = pd.Series(series.index, index=series.index, name="root")
        _root_ser= _root_ser.apply(self.__get_root)

        _df = pd.DataFrame({
            series.name: series,
            usage_series.name: usage_series,
            _root_ser.name: _root_ser,
        })

        return _df


class ParserData:
    """
    Designed to store and manipulate data for analysis.
    """

    def __init__(self, csv_file_path, possible_urls_path):
        self.__dataframe = self.__modify_df(csv_file_path)
        self.__url_paths = self.__save_urls(possible_urls_path)

    def testme(self, _p):
        return self.__save_urls(_p)

    @staticmethod
    def __correct_path_format(url_series):
        """Method for correcting url path format to keep standard"""

        def slash_checker(url: str):
            """Inner function for .apply() method to add missing slashes to url paths."""
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
        _dt = self.__correct_datetime_format(_df["date"])
        _d, _t = self.__split_datetime_to_date_time(_dt)
        _df = pd.DataFrame({"path": _path_ser, "date-time": _dt, "date": _d, "time": _t})
        return _df

    dataframe = property(
        fget=lambda self: self.__dataframe,
        doc="Providing restricted access to Dataframe.",
    )

    def __save_urls(self, txt_file_path):
        """Take in urls from *.txt file and save them to a series."""
        _urls = []
        with open(txt_file_path, mode="r") as _f:
            for _e in _f:
                if _e.endswith(("\n", "\r")):
                    _e = _e[:-1]
                _urls.append(_e)

        return self.__correct_path_format(pd.Series(_urls, name="urls"))

    possible_urls = property(
        fget=lambda self: self.__url_paths,
        doc="Providing restricted access to possible urls Series"
    )
