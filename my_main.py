import time, math


cal_ID = 0


class Localization:
    def __init__(self, lang="ru"):
        self._languages = ("ru", "ge", "en")
        self._lang = lang

        self._weekdays_locals = {
            "ru": ("Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"),
            "ge": ("Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"),
            "en": ("Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"),
        }

        self._months_locals = {
            "ru": (
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
            ),
            "ge": (
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
            ),
            "en": (
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
            ),
        }

        self._error_locals = {
            "ru": ("Год должен быть от 1 до 3999!", "Месяц должен быть от 1 до 12!"),
            "ge": (
                "Jahr muss zwischen 1 und 3999 liegen!",
                "Monat muss zwischen 1 und 12 liegen!",
            ),
            "en": ("Year must be 1 - 3999!", "Month must be 1 - 12!"),
        }

        self._week_start = {"ru": 1, "ge": 0, "en": 0}

    @property
    def languages(self):
        return self._languages

    @property
    def lang(self):
        return self._lang

    @lang.setter
    def lang(self, val):
        if val in self._languages:
            self._lang = val

    def set_lang(self, val):
        if val in self._languages:
            self._lang = val

    @property
    def weekdays_locals(self):
        return self._weekdays_locals

    @weekdays_locals.setter
    def weekdays_locals(self, val):
        self._weekdays_locals = val

    def set_weekdays_local(self, lang, new_val):
        self._weekdays_locals[lang] = new_val

    @property
    def months_locals(self):
        return self._months_locals

    @months_locals.setter
    def months_locals(self, val):
        self._months_locals = val

    def set_months_locals(self, lang, new_val):
        self._months_locals[lang] = new_val

    @property
    def error_locals(self):
        return self._error_locals

    def set_error_locals(self, lang, new_val):
        self._error_locals[lang] = new_val

    @property
    def week_start(self):
        return self._week_start.get(self._lang, 1)

    def set_week_start(self, lang, start_day):
        if start_day in (0, 1):
            self._week_start[lang] = start_day

    def add_language(self, new_lang):
        if new_lang not in self._languages:
            self._languages = self._languages + (new_lang,)

    def remove_language(self, lang_to_remove):
        if lang_to_remove not in self._languages:
            raise ValueError(
                f"Язык '{lang_to_remove}' не найден в списке поддерживаемых"
            )

        languages_list = list(self._languages)
        languages_list.remove(lang_to_remove)
        self._languages = tuple(languages_list)

        if lang_to_remove in self._weekdays_locals:
            del self._weekdays_locals[lang_to_remove]
        if lang_to_remove in self._months_locals:
            del self._months_locals[lang_to_remove]
        if lang_to_remove in self._error_locals:
            del self._error_locals[lang_to_remove]
        if lang_to_remove in self._week_start:
            del self._week_start[lang_to_remove]

        if self._lang == lang_to_remove and self._languages:
            self._lang = self._languages[0]

    @property
    def months(self):
        return self._months_locals.get(self._lang, self._months_locals["en"])

    @property
    def weekdays(self):
        return self._weekdays_locals.get(self._lang, self._weekdays_locals["en"])

    @property
    def error_messages(self):
        return self._error_locals.get(self._lang, self._error_locals["en"])

    def add_weekdays_local(self, lang, weekdays_tuple):
        if len(weekdays_tuple) == 7:
            self._weekdays_locals[lang] = weekdays_tuple
        else:
            raise ValueError("Должно быть ровно 7 дней недели")

    def remove_weekdays_local(self, lang):
        if lang in self._weekdays_locals:
            del self._weekdays_locals[lang]

    def add_months_local(self, lang, months_tuple):
        if len(months_tuple) == 12:
            self._months_locals[lang] = months_tuple
        else:
            raise ValueError("Должно быть ровно 12 месяцев")

    def remove_months_local(self, lang):
        if lang in self._months_locals:
            del self._months_locals[lang]


class MonthlyCalendar:
    def __init__(self, year=None, month=None, lang="ru"):
        self.loc = Localization(lang)

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

        self.wFontFace = "Arial, Helvetica"
        self.wFontSize = 10
        self.wFontColor = "#FFFFFF"
        self.wBGColor = "#304B90"

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

        self.holidays = {
            "ru": {
                (1, 1): "Новый год",
                (7, 1): "Рождество",
                (23, 2): "День защитника Отечества",
                (8, 3): "Международный женский день",
                (1, 5): "Праздник Весны и Труда",
                (9, 5): "День Победы",
                (12, 6): "День России",
                (4, 11): "День народного единства",
            },
            "ge": {
                (1, 1): "Neujahr",
                (6, 1): "Heilige Drei Könige",
                (25, 12): "Weihnachten",
                (26, 12): "Zweiter Weihnachtstag",
            },
            "en": {(1, 1): "New Year's Day", (25, 12): "Christmas Day"},
        }

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

    def set_language(self, lang):
        self.loc.set_lang(lang)

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

        offset = 1 if self.loc.week_start == 1 else 0

        if a:
            a = (a - offset) % 7
        elif offset:
            a += 7 - offset
        return a

    def is_holiday(self, day):
        current_holidays = self.holidays.get(self.loc.lang, {})
        return (day, self.month) in current_holidays

    def get_holiday_title(self, day):
        current_holidays = self.holidays.get(self.loc.lang, {})
        return current_holidays.get((day, self.month), "")

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

        for i in range(7):
            if self.loc.week_start == 1:
                day_index = i
            else:
                day_index = (i + 6) % 7

            wDay = self.loc.weekdays[day_index]
            html += self.table_cell(wDay, "cssHeading" + str(globals()["cal_ID"]))

        html += "</tr>"
        return html

    def viewEvent(self, start, end, color, title, link=""):
        if start > end:
            return
        if start < 1 or start > 31:
            return
        if end < 1 or end > 31:
            return
        while start <= end:
            self.specDays[str(start)] = [color, title, link]
            start += 1

    def create(self):
        self.__size = (
            (self.hFontSize > self.dFontSize) and self.hFontSize or self.dFontSize
        )

        date = time.strftime("%Y-%m-%d", time.localtime())
        (curYear, curMonth, curDay) = [int(v) for v in date.split("-")]

        if self.year < 1 or self.year > 3999:
            html = "<b>" + self.loc.error_messages[0] + "</b>"
        elif self.month < 1 or self.month > 12:
            html = "<b>" + self.loc.error_messages[1] + "</b>"
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
            title = self.loc.months[self.month - 1] + " " + str(self.year)
            html += self.table_head(title)
            daycount = 1

            if self.year == curYear and self.month == curMonth:
                inThisMonth = 1
            else:
                inThisMonth = 0

            while daycount <= stop:
                html += "<tr>"

                for i in range(7):
                    if self.loc.week_start == 1:
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


class CalendarHTMLGenerator:
    def __init__(self, filename=None):
        self.filename = filename or "calendar"

    def generate(self, year=None, month=None, lang="ru"):
        calendar = MonthlyCalendar(year, month, lang)
        body = calendar.create()

        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8'>
    <title>Календарь - {calendar.loc.months[calendar.month - 1]} {calendar.year}</title>
</head>
<body>
    {body}
</body>
</html>"""

        filename = self.filename
        if not filename.lower().endswith(".html"):
            filename += ".html"

        with open(filename, "w", encoding="utf-8") as file:
            file.write(html)

        return filename


if __name__ == "__main__":
    generator = CalendarHTMLGenerator("calendar_ru")

    filename_ru = generator.generate(2025, 9, "ru")
    print(f"{filename_ru}")
