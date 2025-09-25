import time
from abc import ABC, abstractmethod
from typing import Dict, Tuple, Protocol, List
from datetime import date


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


class CalendarDay:
    def __init__(
        self,
        day: int,
        month: int,
        year: int,
        is_weekend: bool = False,
        is_holiday: bool = False,
        holiday_title: str = "",
    ):
        self.day = day
        self.month = month
        self.year = year
        self.is_weekend = is_weekend
        self.is_holiday = is_holiday
        self.holiday_title = holiday_title
        self.is_current = False

    def get_date_string(self) -> str:
        return f"{self.year}-{self.month:02d}-{self.day:02d}"


class Calendar:
    def __init__(self, year: int, month: int, localization: LocalizationStrategy):
        self.year = year
        self.month = month
        self.localization = localization
        self._month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    def is_leap_year(self, year: int) -> bool:
        return not (year % 4) and (year < 1582 or year % 100 or not (year % 400))

    def get_days_in_month(self) -> int:
        if self.month == 2 and self.is_leap_year(self.year):
            return 29
        return self._month_days[self.month - 1]

    def get_first_weekday(self) -> int:
        days = sum(self._month_days[: self.month - 1])
        if self.month > 2 and self.is_leap_year(self.year):
            days += 1

        a = days + (self.year - 1) * 365
        for i in range(1, self.year):
            if self.is_leap_year(i):
                a += 1

        if self.year > 1582 or (self.year == 1582 and days >= 277):
            a -= 10

        week_start = self.localization.get_week_start()
        offset = 1 if week_start == 1 else 0

        if a:
            a = (a - offset) % 7
        elif offset:
            a += 7 - offset
        return a

    def generate_days(self) -> List[CalendarDay]:
        days = []
        holidays = self.localization.get_holidays()
        current_date = date.today()
        days_in_month = self.get_days_in_month()

        for day in range(1, days_in_month + 1):
            first_weekday = self.get_first_weekday()
            day_of_week = (first_weekday + day - 1) % 7

            if self.localization.get_week_start() == 1:
                is_weekend = day_of_week >= 5
            else:
                is_weekend = day_of_week == 0 or day_of_week == 6

            is_holiday = (day, self.month) in holidays
            holiday_title = holidays.get((day, self.month), "")

            calendar_day = CalendarDay(
                day=day,
                month=self.month,
                year=self.year,
                is_weekend=is_weekend,
                is_holiday=is_holiday,
                holiday_title=holiday_title,
            )

            if (
                current_date.year == self.year
                and current_date.month == self.month
                and current_date.day == day
            ):
                calendar_day.is_current = True

            days.append(calendar_day)

        return days


class CalendarTheme:
    def __init__(self):
        self.title_font = "Arial, Helvetica"
        self.title_size = 12
        self.title_color = "#FFFFFF"
        self.title_bg = "#304B90"

        self.day_font = "Arial, Helvetica"
        self.day_size = 12
        self.day_color = "#000000"
        self.day_bg = "#FFFFFF"

        self.weekend_color = "#FF0000"
        self.weekend_bg = "#FFE0E0"

        self.holiday_color = "#0000FF"
        self.holiday_bg = "#E0E0FF"

        self.border_color = "#304B90"
        self.highlight_color = "#FFFF00"
        self.current_day_border = "red"


class CalendarRenderer(ABC):
    def __init__(self, theme: CalendarTheme):
        self.theme = theme

    @abstractmethod
    def render_header(self, calendar: Calendar) -> str:
        pass

    @abstractmethod
    def render_weekdays(self, calendar: Calendar) -> str:
        pass

    @abstractmethod
    def render_days(self, days: List[CalendarDay], calendar: Calendar) -> str:
        pass

    def render(self, calendar: Calendar) -> str:
        days = calendar.generate_days()

        result = self.render_header(calendar)
        result += self.render_weekdays(calendar)
        result += self.render_days(days, calendar)

        return result


class HTMLCalendarRenderer(CalendarRenderer):
    def __init__(self, theme: CalendarTheme):
        super().__init__(theme)
        self._style_id = id(self)

    def _generate_styles(self) -> str:
        return f"""<style>
.calendar-title-{self._style_id} {{
    font-family: {self.theme.title_font};
    font-size: {self.theme.title_size}px;
    color: {self.theme.title_color};
    background-color: {self.theme.title_bg};
}}
.calendar-day-{self._style_id} {{
    font-family: {self.theme.day_font};
    font-size: {self.theme.day_size}px;
    color: {self.theme.day_color};
    background-color: {self.theme.day_bg};
}}
.calendar-weekend-{self._style_id} {{
    font-family: {self.theme.day_font};
    font-size: {self.theme.day_size}px;
    color: {self.theme.weekend_color};
    background-color: {self.theme.weekend_bg};
}}
.calendar-holiday-{self._style_id} {{
    font-family: {self.theme.day_font};
    font-size: {self.theme.day_size}px;
    color: {self.theme.holiday_color};
    background-color: {self.theme.holiday_bg};
}}
</style>"""

    def render_header(self, calendar: Calendar) -> str:
        month_name = calendar.localization.get_months()[calendar.month - 1]
        title = f"{month_name} {calendar.year}"

        styles = self._generate_styles()

        return f"""{styles}
<table border="1" cellspacing="0" cellpadding="0">
<tr><td bgcolor="{self.theme.border_color}">
<table border="0" cellspacing="1" cellpadding="3">
<tr><td colspan="7" class="calendar-title-{self._style_id}" align="center">
<b>{title}</b>
</td></tr>"""

    def render_weekdays(self, calendar: Calendar) -> str:
        weekdays = calendar.localization.get_weekdays()
        html = "<tr>"

        for weekday in weekdays:
            html += f'<td class="calendar-title-{self._style_id}" align="center">{weekday}</td>'

        html += "</tr>"
        return html

    def render_days(self, days: List[CalendarDay], calendar: Calendar) -> str:
        html = ""
        first_weekday = calendar.get_first_weekday()

        html += "<tr>"
        for i in range(first_weekday):
            html += (
                f'<td class="calendar-day-{self._style_id}" align="center">&nbsp;</td>'
            )

        current_weekday = first_weekday

        for day in days:
            if current_weekday == 7:
                html += "</tr><tr>"
                current_weekday = 0

            css_class = f"calendar-day-{self._style_id}"
            style = ""
            title_attr = ""

            if day.is_holiday:
                css_class = f"calendar-holiday-{self._style_id}"
                if day.holiday_title:
                    title_attr = f' title="{day.holiday_title}"'
            elif day.is_weekend:
                css_class = f"calendar-weekend-{self._style_id}"

            if day.is_current:
                style = f' style="border: 3px solid {self.theme.current_day_border};"'

            html += f'<td class="{css_class}" align="center"{title_attr}{style}>{day.day}</td>'
            current_weekday += 1

        while current_weekday < 7:
            html += (
                f'<td class="calendar-day-{self._style_id}" align="center">&nbsp;</td>'
            )
            current_weekday += 1

        html += "</tr></table></td></tr></table>"
        return html


if __name__ == "__main__":
    theme = CalendarTheme()

    for lang in LocalizationFactory.get_supported_languages():
        localization = LocalizationFactory.create(lang)
        calendar = Calendar(2025, 9, localization)
        renderer = HTMLCalendarRenderer(theme)

        calendar_html = renderer.render(calendar)
        html = f"<!DOCTYPE html><html><head><meta charset='utf-8'></head><body>{calendar_html}</body></html>"

        with open(f"calendar_{lang}.html", "w", encoding="utf-8") as file:
            file.write(html)

    print(
        f"Календари созданы для языков: {LocalizationFactory.get_supported_languages()}"
    )
