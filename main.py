import time
from typing import Dict, Tuple, Protocol

cal_ID = 0


class LocalizationStrategy(Protocol):
    def get_weekdays(self) -> Tuple[str, ...]: ...

    def get_months(self) -> Tuple[str, ...]: ...

    def get_week_start(self) -> int: ...

    def get_holidays(self) -> Dict[Tuple[int, int], str]: ...


class RussianLocalization:
    def get_weekdays(self) -> Tuple[str, ...]:
        return ("Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс")

    def get_months(self) -> Tuple[str, ...]:
        return (
            "Январь",
            "Февраль",
            "Март",
            "Апрель",
            "Май",
            "Июнь",
            "Июль",
            "Август",
            "Сентябрь",
            "Октябрь",
            "Ноябрь",
            "Декабрь",
        )

    def get_week_start(self) -> int:
        return 1

    def get_holidays(self) -> Dict[Tuple[int, int], str]:
        return {
            (1, 1): "Новый год",
            (23, 2): "День защитника Отечества",
            (8, 3): "Международный женский день",
            (1, 5): "Праздник Весны и Труда",
            (9, 5): "День Победы",
            (12, 6): "День России",
            (4, 11): "День народного единства",
        }


class EnglishLocalization:
    def get_weekdays(self) -> Tuple[str, ...]:
        return ("Su", "Mo", "Tu", "We", "Th", "Fr", "Sa")

    def get_months(self) -> Tuple[str, ...]:
        return (
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        )

    def get_week_start(self) -> int:
        return 0

    def get_holidays(self) -> Dict[Tuple[int, int], str]:
        return {
            (1, 1): "New Year's Day",
            (25, 12): "Christmas Day",
        }


class GermanLocalization:
    def get_weekdays(self) -> Tuple[str, ...]:
        return ("Mo", "Di", "Mi", "Do", "Fr", "Sa", "So")

    def get_months(self) -> Tuple[str, ...]:
        return (
            "Januar",
            "Februar",
            "März",
            "April",
            "Mai",
            "Juni",
            "Juli",
            "August",
            "September",
            "Oktober",
            "November",
            "Dezember",
        )

    def get_week_start(self) -> int:
        return 1

    def get_holidays(self) -> Dict[Tuple[int, int], str]:
        return {
            (1, 1): "Neujahr",
            (6, 1): "Heilige Drei Könige",
            (25, 12): "Weihnachten",
            (26, 12): "Zweiter Weihnachtstag",
        }


class LocalizationFactory:
    _strategies = {
        "ru": RussianLocalization,
        "en": EnglishLocalization,
        "ge": GermanLocalization,
    }

    @classmethod
    def create(cls, lang: str) -> LocalizationStrategy:
        if lang not in cls._strategies:
            raise ValueError(f"Unsupported language: {lang}")
        return cls._strategies[lang]()

    @classmethod
    def register_language(cls, lang: str, strategy_class):
        cls._strategies[lang] = strategy_class

    @classmethod
    def get_supported_languages(cls):
        return list(cls._strategies.keys())


class MonthlyCalendar:
    def __init__(self, year=None, month=None, lang="ru"):
        self.localization = LocalizationFactory.create(lang)

        # Обновляем цветовую схему согласно требованиям
        self.saFontColor = "#FF0000"  # Ярко красный для субботы
        self.saBGColor = "#FFE0E0"  # Светло красный фон для субботы
        self.suFontColor = "#FF0000"  # Ярко красный для воскресенья
        self.suBGColor = "#FFE0E0"  # Светло красный фон для воскресенья

        # Синий цвет для праздников согласно требованиям
        self.holidayFontColor = "#0000FF"  # Синий цвет текста
        self.holidayBGColor = "#E0E0FF"  # Светло синий фон

        self.tFontFace = "Arial, Helvetica"
        self.tFontSize = 12
        self.tFontColor = "#FFFFFF"
        self.tBGColor = "#304B90"

        self.hFontFace = "Arial, Helvetica"
        self.hFontSize = 10
        self.hFontColor = "#FFFFFF"
        self.hBGColor = "#304B90"

        self.dFontFace = "Arial, Helvetica"
        self.dFontSize = 12
        self.dFontColor = "#000000"
        self.dBGColor = "#FFFFFF"

        self.saFontColor = "#FF0000"
        self.saBGColor = "#FFE0E0"
        self.suFontColor = "#FF0000"
        self.suBGColor = "#FFE0E0"

        self.holidayFontColor = "#0000FF"
        self.holidayBGColor = "#E0E0FF"

        self.tdBorderColor = "red"
        self.borderColor = "#304B90"
        self.hilightColor = "#FFFF00"

        self.link = ""

        if year is None and month is None:
            year = time.localtime().tm_year
            month = time.localtime().tm_mon
        elif year is None and month is not None:
            year = time.localtime().tm_year
        elif month is None:
            month = 1
        self.year = int(year)
        self.month = int(month)
        self.specDays = {}

    __size = 0
    __mDays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    def set_styles(self):
        globals()["cal_ID"] += 1
        html = "<style> .cssTitle" + str(globals()["cal_ID"]) + " { "
        if self.tFontFace:
            html += "font-family: " + self.tFontFace + "; "
        if self.tFontSize:
            html += "font-size: " + str(self.tFontSize) + "px; "
        if self.tFontColor:
            html += "color: " + self.tFontColor + "; "
        if self.tBGColor:
            html += "background-color: " + self.tBGColor + "; "
        html += "} .cssHeading" + str(globals()["cal_ID"]) + " { "
        if self.hFontFace:
            html += "font-family: " + self.hFontFace + "; "
        if self.hFontSize:
            html += "font-size: " + str(self.hFontSize) + "px; "
        if self.hFontColor:
            html += "color: " + self.hFontColor + "; "
        if self.hBGColor:
            html += "background-color: " + self.hBGColor + "; "
        html += "} .cssDays" + str(globals()["cal_ID"]) + " { "
        if self.dFontFace:
            html += "font-family: " + self.dFontFace + "; "
        if self.dFontSize:
            html += "font-size: " + str(self.dFontSize) + "px; "
        if self.dFontColor:
            html += "color: " + self.dFontColor + "; "
        if self.dBGColor:
            html += "background-color: " + self.dBGColor + "; "
        html += "} .cssSaturdays" + str(globals()["cal_ID"]) + " { "
        if self.dFontFace:
            html += "font-family: " + self.dFontFace + "; "
        if self.dFontSize:
            html += "font-size: " + str(self.dFontSize) + "px; "
        if self.saFontColor:
            html += "color: " + self.saFontColor + "; "
        if self.saBGColor:
            html += "background-color: " + self.saBGColor + "; "
        html += "} .cssSundays" + str(globals()["cal_ID"]) + " { "
        if self.dFontFace:
            html += "font-family: " + self.dFontFace + "; "
        if self.dFontSize:
            html += "font-size: " + str(self.dFontSize) + "px; "
        if self.suFontColor:
            html += "color: " + self.suFontColor + "; "
        if self.suBGColor:
            html += "background-color: " + self.suBGColor + "; "
        html += "} .cssHolidays" + str(globals()["cal_ID"]) + " { "
        if self.dFontFace:
            html += "font-family: " + self.dFontFace + "; "
        if self.dFontSize:
            html += "font-size: " + str(self.dFontSize) + "px; "
        if self.holidayFontColor:
            html += "color: " + self.holidayFontColor + "; "
        if self.holidayBGColor:
            html += "background-color: " + self.holidayBGColor + "; "
        html += "} .cssHilight" + str(globals()["cal_ID"]) + " { "
        if self.dFontFace:
            html += "font-family: " + self.dFontFace + "; "
        if self.dFontSize:
            html += "font-size: " + str(self.dFontSize) + "px; "
        if self.dFontColor:
            html += "color: " + self.dFontColor + "; "
        if self.hilightColor:
            html += "background-color: " + self.hilightColor + "; "
        html += "cursor: default; "
        html += "} </style>"
        return html

    def leap_year(self, year):
        return not (year % 4) and (year < 1582 or year % 100 or not (year % 400))

    def get_weekday(self, year, days):
        a = days
        if year:
            a += (year - 1) * 365
        for i in range(1, year):
            if self.leap_year(i):
                a += 1
        if year > 1582 or (year == 1582 and days >= 277):
            a -= 10

        offset = 1 if self.localization.get_week_start() == 1 else 0

        if a:
            a = (a - offset) % 7
        elif offset:
            a += 7 - offset
        return a

    def is_holiday(self, day):
        return (day, self.month) in self.localization.get_holidays()

    def get_holiday_title(self, day):
        return self.localization.get_holidays().get((day, self.month), "")

    def table_cell(self, content, cls, date="", style=""):
        size = int(round(self.__size * 1.5))
        html = "<td align=center width=" + str(size) + ' class="' + cls + '"'

        if content != "&nbsp;" and cls.lower().find("day") != -1:
            link = self.link

            if len(self.specDays) > 0 and content in self.specDays:
                if self.specDays[content][0]:
                    style += "background-color:" + self.specDays[content][0] + ";"
                if self.specDays[content][1]:
                    html += ' title="' + self.specDays[content][1] + '"'
                if self.specDays[content][2]:
                    link = self.specDays[content][2]
                    style += "cursor:pointer" + ";"
                else:
                    link = "brak"
                    style += "cursor:pointer" + ";"

            if link == "brak":
                html += (
                    " onMouseOver=\"this.className='cssHilight"
                    + str(globals()["cal_ID"])
                    + "'\""
                )
                html += " onMouseOut=\"this.className='" + cls + "'\""
                html += " onClick=\"document.location.href='" + "?date=" + date + "'\""

            if link and link != "brak":
                html += (
                    " onMouseOver=\"this.className='cssHilight"
                    + str(globals()["cal_ID"])
                    + "'\""
                )
                html += " onMouseOut=\"this.className='" + cls + "'\""
                html += (
                    " onClick=\"document.location.href='"
                    + link
                    + "?date="
                    + date
                    + "'\""
                )
        if style:
            html += ' style="' + style + '"'
        html += ">" + content + "</td>"
        return html

    def table_head(self, content):
        html = (
            "<tr><td colspan=7"
            + ' class="cssTitle'
            + str(globals()["cal_ID"])
            + '" align=center><b>'
            + content
            + "</b></td></tr><tr>"
        )

        weekdays = self.localization.get_weekdays()
        for i in range(7):
            if self.localization.get_week_start() == 1:
                day_index = i
            else:
                day_index = (i + 6) % 7

            wDay = weekdays[day_index]
            html += self.table_cell(wDay, "cssHeading" + str(globals()["cal_ID"]))

        html += "</tr>"
        return html

    def create(self):
        self.__size = (
            (self.hFontSize > self.dFontSize) and self.hFontSize or self.dFontSize
        )

        date = time.strftime("%Y-%m-%d", time.localtime())
        (curYear, curMonth, curDay) = [int(v) for v in date.split("-")]

        if self.year < 1 or self.year > 3999:
            html = "<b>Год должен быть от 1 до 3999!</b>"
        elif self.month < 1 or self.month > 12:
            html = "<b>Месяц должен быть от 1 до 12!</b>"
        else:
            if self.leap_year(self.year):
                self.__mDays[1] = 29
            days = 0
            for i in range(self.month - 1):
                days += self.__mDays[i]

            start = self.get_weekday(self.year, days)
            stop = self.__mDays[self.month - 1]

            html = self.set_styles()
            html += "<table border=1 cellspacing=0 cellpadding=0><tr>"
            html += "<td" + (self.borderColor and " bgcolor=" + self.borderColor) + ">"
            html += "<table border=0 cellspacing=1 cellpadding=3>"
            title = (
                self.localization.get_months()[self.month - 1] + " " + str(self.year)
            )
            html += self.table_head(title)
            daycount = 1

            if self.year == curYear and self.month == curMonth:
                inThisMonth = 1
            else:
                inThisMonth = 0

            while daycount <= stop:
                html += "<tr>"

                for i in range(7):
                    if self.localization.get_week_start() == 1:
                        day_of_week = i
                    else:
                        day_of_week = (i + 6) % 7

                    if (
                        daycount <= stop
                        and daycount > 0
                        and (daycount != 1 or i >= start)
                        and self.is_holiday(daycount)
                    ):
                        cls = "cssHolidays"
                    elif day_of_week == 5:
                        cls = "cssSaturdays"
                    elif day_of_week == 6:
                        cls = "cssSundays"
                    else:
                        cls = "cssDays"

                    style = ""
                    date = (
                        "%s-%02d-%02d" % (self.year, self.month, daycount)
                        if daycount <= stop
                        else ""
                    )

                    if (daycount == 1 and i < start) or daycount > stop:
                        content = "&nbsp;"
                    else:
                        content = str(daycount)

                        if self.is_holiday(daycount):
                            holiday_title = self.get_holiday_title(daycount)
                            if holiday_title:
                                style += f'cursor:help;" title="{holiday_title}'

                        if inThisMonth and daycount == curDay:
                            style = (
                                "padding:0px;border:3px solid "
                                + self.tdBorderColor
                                + ";"
                            )
                        elif self.year == 1582 and self.month == 10 and daycount == 4:
                            daycount = 14
                        daycount += 1

                    html += self.table_cell(
                        content, cls + str(globals()["cal_ID"]), date, style
                    )

                html += "</tr>"
            html += "</table></td></tr></table>"
        return html


if __name__ == "__main__":
    for lang in LocalizationFactory.get_supported_languages():
        calendar = MonthlyCalendar(2025, 9, lang)
        body = calendar.create()
        html = f"<!DOCTYPE html><html><head><meta charset='utf-8'></head><body>{body}</body></html>"

        with open(f"calendar_{lang}.html", "w", encoding="utf-8") as file:
            file.write(html)

    print(
        f"Календари созданы для языков: {LocalizationFactory.get_supported_languages()}"
    )
