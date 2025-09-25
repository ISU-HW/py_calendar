from abc import ABC, abstractmethod
from datetime import datetime, date
from typing import Dict, Tuple, Optional, Protocol, List
import time


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
            (7, 1): "Рождество",
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
        self.is_empty = False

    def get_date_string(self) -> str:
        return f"{self.year}-{self.month:02d}-{self.day:02d}"

    def get_display_text(self) -> str:
        return str(self.day) if not self.is_empty else "&nbsp;"


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

    def generate_calendar_grid(self) -> List[List[CalendarDay]]:
        weeks = []
        holidays = self.localization.get_holidays()
        current_date = date.today()
        days_in_month = self.get_days_in_month()
        first_weekday = self.get_first_weekday()

        current_week = []

        for i in range(first_weekday):
            empty_day = CalendarDay(0, self.month, self.year)
            empty_day.is_empty = True
            current_week.append(empty_day)

        for day in range(1, days_in_month + 1):
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

            current_week.append(calendar_day)

            if len(current_week) == 7:
                weeks.append(current_week)
                current_week = []

        while len(current_week) < 7:
            empty_day = CalendarDay(0, self.month, self.year)
            empty_day.is_empty = True
            current_week.append(empty_day)

        if current_week:
            weeks.append(current_week)

        return weeks

    def get_title(self) -> str:
        month_name = self.localization.get_months()[self.month - 1]
        return f"{month_name} {self.year}"


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
    def render(self, calendar: Calendar) -> str:
        pass


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
    text-align: center;
    padding: 8px;
}}
.calendar-weekday-{self._style_id} {{
    font-family: {self.theme.title_font};
    font-size: {self.theme.title_size}px;
    color: {self.theme.title_color};
    background-color: {self.theme.title_bg};
    text-align: center;
    padding: 5px;
}}
.calendar-day-{self._style_id} {{
    font-family: {self.theme.day_font};
    font-size: {self.theme.day_size}px;
    color: {self.theme.day_color};
    background-color: {self.theme.day_bg};
    text-align: center;
    padding: 8px;
    width: 40px;
    height: 30px;
}}
.calendar-weekend-{self._style_id} {{
    font-family: {self.theme.day_font};
    font-size: {self.theme.day_size}px;
    color: {self.theme.weekend_color};
    background-color: {self.theme.weekend_bg};
    text-align: center;
    padding: 8px;
    width: 40px;
    height: 30px;
}}
.calendar-holiday-{self._style_id} {{
    font-family: {self.theme.day_font};
    font-size: {self.theme.day_size}px;
    color: {self.theme.holiday_color};
    background-color: {self.theme.holiday_bg};
    text-align: center;
    padding: 8px;
    width: 40px;
    height: 30px;
}}
.calendar-current-{self._style_id} {{
    border: 3px solid {self.theme.current_day_border} !important;
    padding: 5px !important;
}}
</style>"""

    def render(self, calendar: Calendar) -> str:
        styles = self._generate_styles()
        calendar_grid = calendar.generate_calendar_grid()
        weekdays = calendar.localization.get_weekdays()

        html = styles
        html += f'<table border="1" cellspacing="0" cellpadding="0" style="border-color: {self.theme.border_color};">'
        html += f'<tr><td style="background-color: {self.theme.border_color};">'
        html += '<table border="0" cellspacing="1" cellpadding="0">'

        html += f'<tr><td colspan="7" class="calendar-title-{self._style_id}"><b>{calendar.get_title()}</b></td></tr>'

        html += "<tr>"
        for weekday in weekdays:
            html += f'<td class="calendar-weekday-{self._style_id}">{weekday}</td>'
        html += "</tr>"

        for week in calendar_grid:
            html += "<tr>"
            for day in week:
                css_class = self._get_day_css_class(day)
                title_attr = (
                    f' title="{day.holiday_title}"' if day.holiday_title else ""
                )
                current_class = (
                    f" calendar-current-{self._style_id}" if day.is_current else ""
                )

                html += f'<td class="{css_class}{current_class}"{title_attr}>{day.get_display_text()}</td>'
            html += "</tr>"

        html += "</table></td></tr></table>"
        return html

    def _get_day_css_class(self, day: CalendarDay) -> str:
        if day.is_holiday:
            return f"calendar-holiday-{self._style_id}"
        elif day.is_weekend:
            return f"calendar-weekend-{self._style_id}"
        else:
            return f"calendar-day-{self._style_id}"


class HTMLDocumentBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        self._title = ""
        self._body = ""
        self._charset = "utf-8"
        self._meta_tags = []
        return self

    def set_title(self, title: str):
        self._title = title
        return self

    def set_body(self, body: str):
        self._body = body
        return self

    def set_charset(self, charset: str):
        self._charset = charset
        return self

    def add_meta_tag(self, name: str, content: str):
        self._meta_tags.append(f'<meta name="{name}" content="{content}">')
        return self

    def build(self) -> str:
        meta_section = f'<meta charset="{self._charset}">'
        if self._meta_tags:
            meta_section += "\n    " + "\n    ".join(self._meta_tags)

        return f"""<!DOCTYPE html>
<html>
<head>
    {meta_section}
    <title>{self._title}</title>
</head>
<body>
    {self._body}
</body>
</html>"""


class CalendarFileManager:
    @staticmethod
    def save_to_file(content: str, filename: str, encoding: str = "utf-8"):
        with open(filename, "w", encoding=encoding) as f:
            f.write(content)


class CalendarGenerator:
    def __init__(self, theme: Optional[CalendarTheme] = None):
        self.theme = theme or CalendarTheme()

    def generate_html_calendar(
        self, year: int, month: int, lang: str = "ru", filename: Optional[str] = None
    ) -> str:
        localization = LocalizationFactory.create(lang)
        calendar = Calendar(year, month, localization)
        renderer = HTMLCalendarRenderer(self.theme)

        calendar_html = renderer.render(calendar)

        document = (
            HTMLDocumentBuilder()
            .set_title(f"Календарь - {calendar.get_title()}")
            .add_meta_tag("viewport", "width=device-width, initial-scale=1.0")
            .add_meta_tag("description", f"Календарь на {calendar.get_title()}")
            .set_body(calendar_html)
            .build()
        )

        if filename:
            CalendarFileManager.save_to_file(document, filename)

        return document

    def generate_current_month(
        self, lang: str = "ru", filename: Optional[str] = None
    ) -> str:
        current_time = time.localtime()
        return self.generate_html_calendar(
            current_time.tm_year, current_time.tm_mon, lang, filename
        )

    def generate_multiple_calendars(
        self, year: int, month: int, languages: Optional[List[str]] = None
    ) -> Dict[str, str]:
        if languages is None:
            languages = LocalizationFactory.get_supported_languages()

        results = {}
        for lang in languages:
            filename = f"calendar_{lang}_{year}_{month:02d}.html"
            document = self.generate_html_calendar(year, month, lang, filename)
            results[lang] = filename

        return results


if __name__ == "__main__":
    generator = CalendarGenerator()

    current_time = time.localtime()
    current_year = current_time.tm_year
    current_month = current_time.tm_mon

    generated_files = generator.generate_multiple_calendars(
        year=current_year, month=current_month
    )

    for lang, filename in generated_files.items():
        localization = LocalizationFactory.create(lang)
        month_name = localization.get_months()[current_month - 1]
        print(f"- {filename} ({month_name} {current_year} на {lang})")

    print(f"\nПоддерживаемые языки: {LocalizationFactory.get_supported_languages()}")

    special_calendar = generator.generate_html_calendar(
        year=2025, month=1, lang="ru", filename="december_2025.html"
    )
