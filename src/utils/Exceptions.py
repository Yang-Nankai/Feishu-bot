# -*- coding: utf-8 -*-
# @Time    : 2023/11/29 17:47
# @Comment : All Exceptions


class BaseException(Exception):
    def __init__(self, error_info):
        self.error_info = error_info

    def __str__(self) -> str:
        return "Base: {}".format(self.error_info)

    __repr__ = __str__


class LarkException(BaseException):
    def __init__(self, error_info):
        super().__init__(error_info)
        self.exception_name = "LarkException"

    def __str__(self) -> str:
        return "{}: {}".format(self.exception_name, super().__str__())


class CVEDataException(BaseException):
    def __init__(self, error_info):
        super().__init__(error_info)
        self.exception_name = "CVEDataException"

    def __str__(self) -> str:
        return "{}: {}".format(self.exception_name, super().__str__())


class InvalidEventException(BaseException):
    def __init__(self, error_info):
        super().__init__(error_info)
        self.exception_name = "InvalidEventException"

    def __str__(self) -> str:
        return "{}: {}".format(self.exception_name, super().__str__())


class LeetCodeDailyException(BaseException):
    def __init__(self, error_info):
        super().__init__(error_info)
        self.exception_name = "LeetCodeDailyException"

    def __str__(self) -> str:
        return "{}: {}".format(self.exception_name, super().__str__())


class WeatherDataException(BaseException):
    def __init__(self, error_info):
        super().__init__(error_info)
        self.exception_name = "WeatherDataException"

    def __str__(self) -> str:
        return "{}: {}".format(self.exception_name, super().__str__())


class BilibiliApiException(BaseException):
    def __init__(self, error_info):
        super().__init__(error_info)
        self.exception_name = "BilibiliApiException"

    def __str__(self) -> str:
        return "{}: {}".format(self.exception_name, super().__str__())
