from __future__ import annotations

from calendar import monthrange
from datetime import date
from tkinter import filedialog, messagebox
from typing import Dict

import customtkinter as ctk

PRIMARY_COLOR = "#2563eb"
SECONDARY_COLOR = "#38bdf8"
ACCENT_COLOR = "#fb7185"
NEUTRAL_COLOR = "#64748b"
BACKGROUND_COLOR = "#f3f4f6"
SURFACE_COLOR = "#ffffff"
GLASS_COLOR = "#ecf2ff"
DARK_BACKGROUND = "#020617"
LIGHT_TEXT = "#ffffff"
DARK_TEXT = "#0f172a"
BORDER_COLOR = "#dbeafe"
SHADOW_COLOR = "#cbd5f5"
FONT_FAMILY = "Tajawal"

ARABIC_DIGITS_MAP = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")
ARABIC_TO_WESTERN_MAP = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")

RLM = "\u200f"

AR_WEEKDAYS = [
    "الاثنين",
    "الثلاثاء",
    "الأربعاء",
    "الخميس",
    "الجمعة",
    "السبت",
    "الأحد",
]

AR_MONTHS = {
    1: "يناير",
    2: "فبراير",
    3: "مارس",
    4: "أبريل",
    5: "مايو",
    6: "يونيو",
    7: "يوليو",
    8: "أغسطس",
    9: "سبتمبر",
    10: "أكتوبر",
    11: "نوفمبر",
    12: "ديسمبر",
}

GREGORIAN_ZODIAC = [
    {
        "name": "الحمل",
        "start": (3, 21),
        "end": (4, 19),
        "element": "النار",
        "planet": "المريخ",
        "traits": "حيوي، جريء، يعشق التحديات ويقود المبادرات.",
    },
    {
        "name": "الثور",
        "start": (4, 20),
        "end": (5, 20),
        "element": "الأرض",
        "planet": "الزهرة",
        "traits": "صبور، وفيّ، يبحث عن الاستقرار والجمال.",
    },
    {
        "name": "الجوزاء",
        "start": (5, 21),
        "end": (6, 20),
        "element": "الهواء",
        "planet": "عطارد",
        "traits": "اجتماعي، فضولي، سريع التعلّم والتفكير.",
    },
    {
        "name": "السرطان",
        "start": (6, 21),
        "end": (7, 22),
        "element": "الماء",
        "planet": "القمر",
        "traits": "حساس، ودي، يحمي من يحبهم ويعتني بالتفاصيل.",
    },
    {
        "name": "الأسد",
        "start": (7, 23),
        "end": (8, 22),
        "element": "النار",
        "planet": "الشمس",
        "traits": "كاريزمي، قيادي، كريم ويتألق في الأضواء.",
    },
    {
        "name": "العذراء",
        "start": (8, 23),
        "end": (9, 22),
        "element": "الأرض",
        "planet": "عطارد",
        "traits": "منظم، عملي، دقيق ويحب خدمة الآخرين.",
    },
    {
        "name": "الميزان",
        "start": (9, 23),
        "end": (10, 22),
        "element": "الهواء",
        "planet": "الزهرة",
        "traits": "دبلوماسي، متوازن، يسعى للسلام والانسجام.",
    },
    {
        "name": "العقرب",
        "start": (10, 23),
        "end": (11, 21),
        "element": "الماء",
        "planet": "بلوتو",
        "traits": "عميق، شغوف، قوي الإرادة ووفي للغاية.",
    },
    {
        "name": "القوس",
        "start": (11, 22),
        "end": (12, 21),
        "element": "النار",
        "planet": "المشتري",
        "traits": "مغامر، صريح، متفائل ومحب للمعرفة.",
    },
    {
        "name": "الجدي",
        "start": (12, 22),
        "end": (1, 19),
        "element": "الأرض",
        "planet": "زحل",
        "traits": "طموح، مسؤول، منضبط ويخطط للمستقبل.",
    },
    {
        "name": "الدلو",
        "start": (1, 20),
        "end": (2, 18),
        "element": "الهواء",
        "planet": "أورانوس",
        "traits": "مبتكر، إنساني، مستقل ويحب الحرية.",
    },
    {
        "name": "الحوت",
        "start": (2, 19),
        "end": (3, 20),
        "element": "الماء",
        "planet": "نبتون",
        "traits": "خيالي، رحيم، يتواصل مع الآخرين بحدسه العالي.",
    },
]

CHINESE_ZODIAC = [
    {"name": "الفأر", "traits": "ذكي، ودود، سريع البديهة."},
    {"name": "الثور", "traits": "مثابر، عملي، يعتمد عليه."},
    {"name": "النمر", "traits": "شجاع، ملهم، محب للمغامرة."},
    {"name": "الأرنب", "traits": "لطيف، حذر، دبلوماسي."},
    {"name": "التنين", "traits": "طموح، واثق، يمتلك حضورًا قويًا."},
    {"name": "الثعبان", "traits": "حكيم، متأمل، عميق التفكير."},
    {"name": "الحصان", "traits": "مفعم بالحيوية، محبوب، نشيط."},
    {"name": "الماعز", "traits": "مرهف، فني، متعاطف."},
    {"name": "القرد", "traits": "إبداعي، اجتماعي، مرن."},
    {"name": "الديك", "traits": "منظم، صريح، دقيق."},
    {"name": "الكلب", "traits": "مخلص، أمين، حريص."},
    {"name": "الخنزير", "traits": "كريم، متسامح، محب للحياة."},
]


def to_arabic_digits(value: object) -> str:
    return str(value).translate(ARABIC_DIGITS_MAP)


def format_number(value: int) -> str:
    formatted = f"{value:,}".replace(",", "،")
    return to_arabic_digits(formatted)


def format_date_ar(d: date) -> str:
    weekday = AR_WEEKDAYS[d.weekday()]
    month = AR_MONTHS[d.month]
    return f"{weekday}، {to_arabic_digits(d.day)} {month} {to_arabic_digits(d.year)}م"


def safe_birthdate(year: int, month: int, day: int) -> date:
    last_day = monthrange(year, month)[1]
    return date(year, month, min(day, last_day))


def calculate_age_details(birth_date: date, today: date | None = None) -> Dict[str, int]:
    if today is None:
        today = date.today()
    if birth_date > today:
        raise ValueError("تاريخ الميلاد في المستقبل.")

    years = today.year - birth_date.year
    months = today.month - birth_date.month
    days = today.day - birth_date.day

    if days < 0:
        prev_month = today.month - 1 or 12
        prev_year = today.year if today.month != 1 else today.year - 1
        days += monthrange(prev_year, prev_month)[1]
        months -= 1

    if months < 0:
        years -= 1
        months += 12

    total_days = (today - birth_date).days
    total_weeks = total_days // 7
    total_months = years * 12 + months

    return {
        "years": years,
        "months": months,
        "days": days,
        "total_days": total_days,
        "total_weeks": total_weeks,
        "total_months": total_months,
    }


def get_next_birthday(birth_date: date, today: date | None = None) -> date:
    if today is None:
        today = date.today()
    candidate = safe_birthdate(today.year, birth_date.month, birth_date.day)
    if candidate < today:
        candidate = safe_birthdate(today.year + 1, birth_date.month, birth_date.day)
    return candidate


def get_zodiac_info(birth_date: date) -> dict:
    for record in GREGORIAN_ZODIAC:
        start_month, start_day = record["start"]
        end_month, end_day = record["end"]
        if start_month < end_month or (start_month == end_month and start_day <= end_day):
            in_range = (
                (birth_date.month > start_month or (birth_date.month == start_month and birth_date.day >= start_day))
                and (birth_date.month < end_month or (birth_date.month == end_month and birth_date.day <= end_day))
            )
        else:
            in_range = (
                birth_date.month > start_month
                or (birth_date.month == start_month and birth_date.day >= start_day)
                or birth_date.month < end_month
                or (birth_date.month == end_month and birth_date.day <= end_day)
            )
        if in_range:
            return record
    return GREGORIAN_ZODIAC[0]


def get_chinese_zodiac(year: int) -> dict:
    index = (year - 1900) % 12
    return CHINESE_ZODIAC[index]


def describe_age(age: Dict[str, int]) -> str:
    parts: list[str] = []
    if age["years"]:
        parts.append(f"{format_number(age['years'])}{RLM} سنة")
    if age["months"]:
        parts.append(f"{format_number(age['months'])}{RLM} شهر")
    if age["days"]:
        parts.append(f"{format_number(age['days'])}{RLM} يوم")
    return "، ".join(parts) if parts else "0"


class GlassCard(ctk.CTkFrame):
    def __init__(self, master: ctk.CTkBaseClass, *, corner_radius: int = 24, **kwargs) -> None:
        super().__init__(
            master,
            corner_radius=corner_radius,
            fg_color=GLASS_COLOR,
            border_color=BORDER_COLOR,
            border_width=1,
            **kwargs,
        )


class GradientButton(ctk.CTkButton):
    def __init__(self, master: ctk.CTkBaseClass, *, text: str, command, color: str, hover: str, **kwargs) -> None:
        super().__init__(
            master,
            text=text,
            command=command,
            fg_color=color,
            hover_color=hover,
            corner_radius=18,
            font=ctk.CTkFont(family=FONT_FAMILY, size=16, weight="bold"),
            height=46,
            **kwargs,
        )


class AgeZodiacApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.theme_mode = "light"
        self.title("حاسبة العمر والبرج")
        self.geometry("880x660")
        self.minsize(820, 640)
        self.configure(fg_color=BACKGROUND_COLOR)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.result_order: list[str] = []
        self.result_vars: dict[str, ctk.StringVar] = {}
        self.status_var = ctk.StringVar(value="مرحبا! أدخل تاريخ ميلادك لتحصل على تجربة كاملة.")

        self._build_layout()
        self.bind("<Return>", lambda event: self.calculate())

    def _build_layout(self) -> None:
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=0, column=0, padx=26, pady=24, sticky="nsew")
        container.grid_columnconfigure(0, weight=1)

        header = GlassCard(container, corner_radius=28)
        header.grid(row=0, column=0, sticky="ew", padx=6, pady=(0, 18))
        header.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header,
            text="حاسبة العمر والبرج الفلكي",
            text_color=DARK_TEXT,
            font=ctk.CTkFont(family=FONT_FAMILY, size=28, weight="bold"),
            anchor="e",
            justify="right",
        )
        title.grid(row=0, column=0, padx=24, pady=(22, 4), sticky="e")

        subtitle = ctk.CTkLabel(
            header,
            text="تصميم عصري باللغة العربية لمتابعة عمرك، برجك الغربي والصيني، وكل التفاصيل في لمحة واحدة.",
            text_color=NEUTRAL_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=15),
            wraplength=740,
            justify="right",
            anchor="e",
        )
        subtitle.grid(row=1, column=0, padx=24, pady=(0, 20), sticky="e")

        content = ctk.CTkFrame(container, fg_color="transparent")
        content.grid(row=1, column=0, sticky="nsew")
        content.grid_columnconfigure((0, 1), weight=1)
        content.grid_rowconfigure(0, weight=1)

        input_card = GlassCard(content)
        input_card.grid(row=0, column=1, padx=(12, 0), sticky="nsew")
        input_card.grid_columnconfigure(0, weight=1)

        self._build_inputs(input_card)

        results_card = GlassCard(content)
        results_card.grid(row=0, column=0, padx=(0, 12), sticky="nsew")
        results_card.grid_columnconfigure(0, weight=1)

        self._build_results(results_card)

        footer = ctk.CTkFrame(container, fg_color="transparent")
        footer.grid(row=2, column=0, sticky="ew")
        footer.grid_columnconfigure((0, 1, 2, 3), weight=1)

        GradientButton(
            footer,
            text="حفظ النتائج",
            command=self.save_result,
            color="#22c55e",
            hover="#16a34a",
        ).grid(row=0, column=3, padx=6, pady=(10, 0))

        GradientButton(
            footer,
            text="نسخ النتائج",
            command=self.copy_result,
            color="#14b8a6",
            hover="#0d9488",
        ).grid(row=0, column=2, padx=6, pady=(10, 0))

        GradientButton(
            footer,
            text="الوضع الليلي",
            command=self.toggle_theme,
            color=PRIMARY_COLOR,
            hover=SECONDARY_COLOR,
        ).grid(row=0, column=1, padx=6, pady=(10, 0))

        GradientButton(
            footer,
            text="مركز المساعدة",
            command=self.show_help,
            color=ACCENT_COLOR,
            hover="#f43f5e",
        ).grid(row=0, column=0, padx=6, pady=(10, 0))

        self.status_label = ctk.CTkLabel(
            container,
            textvariable=self.status_var,
            text_color=PRIMARY_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
            anchor="e",
            justify="right",
        )
        self.status_label.grid(row=3, column=0, padx=12, pady=(18, 0), sticky="e")

    def _build_inputs(self, card: ctk.CTkFrame) -> None:
        card.grid_rowconfigure((0, 1, 2, 3, 4), weight=0)
        card.grid_rowconfigure(5, weight=1)

        header = ctk.CTkLabel(
            card,
            text="تفاصيل الميلاد",
            text_color=DARK_TEXT,
            font=ctk.CTkFont(family=FONT_FAMILY, size=20, weight="bold"),
            anchor="e",
            justify="right",
        )
        header.grid(row=0, column=0, padx=22, pady=(24, 10), sticky="e")

        helper = ctk.CTkLabel(
            card,
            text="أدخل تاريخ ميلادك بدقة. يدعم التطبيق الأرقام العربية والهندية.",
            text_color=NEUTRAL_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            wraplength=320,
            justify="right",
            anchor="e",
        )
        helper.grid(row=1, column=0, padx=22, pady=(0, 18), sticky="e")

        self.year_entry = self._create_input_field(card, "السنة", placeholder="مثال: 1995", row=2)
        self.month_entry = self._create_input_field(card, "الشهر", placeholder="مثال: 5", row=3)
        self.day_entry = self._create_input_field(card, "اليوم", placeholder="مثال: 15", row=4)

        action_area = ctk.CTkFrame(card, fg_color="transparent")
        action_area.grid(row=5, column=0, padx=18, pady=(12, 24), sticky="ew")
        action_area.grid_columnconfigure((0, 1, 2), weight=1)

        GradientButton(
            action_area,
            text="استخدام تاريخ اليوم",
            command=self.fill_today,
            color="#6366f1",
            hover="#4f46e5",
        ).grid(row=0, column=2, padx=6, pady=6)

        GradientButton(
            action_area,
            text="مسح",
            command=self.clear_inputs,
            color="#f97316",
            hover="#ea580c",
        ).grid(row=0, column=1, padx=6, pady=6)

        GradientButton(
            action_area,
            text="احسب الآن",
            command=self.calculate,
            color=PRIMARY_COLOR,
            hover=SECONDARY_COLOR,
        ).grid(row=0, column=0, padx=6, pady=6)

    def _build_results(self, card: ctk.CTkFrame) -> None:
        card.grid_rowconfigure(0, weight=0)
        card.grid_rowconfigure(1, weight=1)

        header = ctk.CTkLabel(
            card,
            text="نتائجك الشخصية",
            text_color=DARK_TEXT,
            font=ctk.CTkFont(family=FONT_FAMILY, size=20, weight="bold"),
            anchor="e",
            justify="right",
        )
        header.grid(row=0, column=0, padx=22, pady=(24, 10), sticky="e")

        description = ctk.CTkLabel(
            card,
            text="يتم عرض كل التفاصيل بشكل متناسق بدون تمرير أو اقتطاع.",
            text_color=NEUTRAL_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            wraplength=320,
            justify="right",
            anchor="e",
        )
        description.grid(row=1, column=0, padx=22, pady=(0, 18), sticky="e")

        results_frame = ctk.CTkFrame(card, fg_color=SURFACE_COLOR, corner_radius=18)
        results_frame.grid(row=2, column=0, padx=18, pady=(0, 24), sticky="nsew")
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_columnconfigure(1, weight=0)

        self._add_result_row(results_frame, 0, "تفاصيل العمر", "age_details", multiline=True)
        self._add_result_row(results_frame, 1, "إجمالي الأشهر", "age_months")
        self._add_result_row(results_frame, 2, "إجمالي الأيام", "age_days")
        self._add_result_row(results_frame, 3, "إجمالي الأسابيع", "age_weeks")
        self._add_result_row(results_frame, 4, "تاريخ الميلاد", "birth_date")
        self._add_result_row(results_frame, 5, "يوم الميلاد", "birth_day_name")
        self._add_result_row(results_frame, 6, "البرج الغربي", "zodiac")
        self._add_result_row(results_frame, 7, "وصف البرج", "zodiac_traits", multiline=True)
        self._add_result_row(results_frame, 8, "البرج الصيني", "chinese")
        self._add_result_row(results_frame, 9, "عيد الميلاد القادم", "next_birthday", multiline=True)

    def _create_input_field(self, card: ctk.CTkFrame, label: str, *, placeholder: str, row: int) -> ctk.CTkEntry:
        wrapper = ctk.CTkFrame(card, fg_color=SURFACE_COLOR, corner_radius=18)
        wrapper.grid(row=row, column=0, padx=18, pady=8, sticky="ew")
        wrapper.grid_columnconfigure(0, weight=1)

        caption = ctk.CTkLabel(
            wrapper,
            text=f"{label}:",
            text_color=DARK_TEXT,
            font=ctk.CTkFont(family=FONT_FAMILY, size=15, weight="bold"),
            anchor="e",
            justify="right",
        )
        caption.grid(row=0, column=0, padx=16, pady=(12, 4), sticky="e")

        entry = ctk.CTkEntry(
            wrapper,
            height=44,
            justify="right",
            font=ctk.CTkFont(family=FONT_FAMILY, size=16),
            placeholder_text=placeholder,
        )
        entry.grid(row=1, column=0, padx=16, pady=(0, 12), sticky="ew")
        return entry

    def _add_result_row(self, frame: ctk.CTkFrame, row: int, title: str, key: str, *, multiline: bool = False) -> None:
        value_var = ctk.StringVar(value="")
        value_label = ctk.CTkLabel(
            frame,
            textvariable=value_var,
            text_color=DARK_TEXT,
            font=ctk.CTkFont(family=FONT_FAMILY, size=16, weight="bold"),
            anchor="e",
            justify="right",
            wraplength=560 if multiline else 520,
        )
        value_label.grid(row=row, column=0, padx=(18, 12), pady=6, sticky="ew")

        title_label = ctk.CTkLabel(
            frame,
            text=title,
            text_color=NEUTRAL_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=14),
            anchor="e",
            justify="right",
        )
        title_label.grid(row=row, column=1, padx=(10, 18), pady=6, sticky="e")

        self.result_vars[key] = value_var
        self.result_order.append(key)

    def calculate(self) -> None:
        day_text = self.day_entry.get().strip().translate(ARABIC_TO_WESTERN_MAP)
        month_text = self.month_entry.get().strip().translate(ARABIC_TO_WESTERN_MAP)
        year_text = self.year_entry.get().strip().translate(ARABIC_TO_WESTERN_MAP)

        if not day_text or not month_text or not year_text:
            self._show_error("الرجاء إدخال اليوم والشهر والسنة بالكامل.")
            return

        try:
            day = int(day_text)
            month = int(month_text)
            year = int(year_text)
        except ValueError:
            self._show_error("يجب أن تكون القيم المدخلة أرقامًا صحيحة.")
            return

        today = date.today()
        if not (1 <= month <= 12):
            self._show_error("الشهر يجب أن يكون بين ١ و١٢.")
            return
        if not (1 <= day <= 31):
            self._show_error("اليوم خارج النطاق المسموح.")
            return
        if year < 1900 or year > today.year + 1:
            self._show_error("يرجى إدخال سنة من ١٩٠٠ وحتى العام القادم.")
            return

        try:
            birth_date = safe_birthdate(year, month, day)
        except ValueError:
            self._show_error("التاريخ غير صالح. تحقق من عدد أيام الشهر الذي اخترته.")
            return

        if birth_date > today:
            self._show_error("تاريخ الميلاد لا يمكن أن يكون في المستقبل.")
            return

        age = calculate_age_details(birth_date, today)
        next_birthday = get_next_birthday(birth_date, today)
        zodiac = get_zodiac_info(birth_date)
        chinese = get_chinese_zodiac(year)

        age_details = describe_age(age)
        age_months = f"{format_number(age['total_months'])}{RLM} شهر"
        age_days = f"{format_number(age['total_days'])}{RLM} يوم منذ الولادة"
        age_weeks = f"{format_number(age['total_weeks'])}{RLM} أسبوع"
        birth_date_text = format_date_ar(birth_date)
        birth_day_name = f"كان يوم {AR_WEEKDAYS[birth_date.weekday()]}"
        zodiac_text = f"{zodiac['name']} — العنصر: {zodiac['element']}، الكوكب الحاكم: {zodiac['planet']}"
        zodiac_traits = zodiac["traits"]
        chinese_text = f"برجك الصيني: {chinese['name']} — {chinese['traits']}"

        days_until = (next_birthday - today).days
        if days_until == 0:
            next_birthday_text = (
                f"اليوم هو عيد ميلادك! 🎉 تكمل {format_number(age['years'])} سنة"
            )
        else:
            upcoming_age = age["years"] + 1
            approx_weeks = max(1, days_until // 7)
            next_birthday_text = (
                f"عيدك القادم: {format_date_ar(next_birthday)} — متبقٍ {format_number(days_until)} يوم"
                f" (حوالي {format_number(approx_weeks)} أسبوع). ستبلغ {format_number(upcoming_age)} سنة."
            )

        self.result_vars["age_details"].set(age_details)
        self.result_vars["age_months"].set(age_months)
        self.result_vars["age_days"].set(age_days)
        self.result_vars["age_weeks"].set(age_weeks)
        self.result_vars["birth_date"].set(birth_date_text)
        self.result_vars["birth_day_name"].set(birth_day_name)
        self.result_vars["zodiac"].set(zodiac_text)
        self.result_vars["zodiac_traits"].set(zodiac_traits)
        self.result_vars["chinese"].set(chinese_text)
        self.result_vars["next_birthday"].set(next_birthday_text)

        self._set_status("تم الحساب بنجاح. استمتع بتفاصيلك المميزة!", success=True)

    def save_result(self) -> None:
        lines = [self.result_vars[key].get() for key in self.result_order if self.result_vars[key].get()]
        if not lines:
            self._show_error("لا توجد نتائج محفوظة. قم بالحساب أولًا.")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("ملف نصي", "*.txt"), ("كل الملفات", "*.*")],
            initialfile="نتيجة_العمر_والبرج.txt",
            title="حفظ النتائج",
        )
        if not filepath:
            self._set_status("تم إلغاء عملية الحفظ.")
            return

        try:
            with open(filepath, "w", encoding="utf-8") as output_file:
                output_file.write("\n".join(lines))
        except OSError:
            self._show_error("تعذر حفظ الملف. تأكد من صلاحيات الكتابة والمسار المختار.")
            return

        self._set_status("تم حفظ النتائج بنجاح.", success=True)

    def copy_result(self) -> None:
        lines = [self.result_vars[key].get() for key in self.result_order if self.result_vars[key].get()]
        if not lines:
            self._show_error("لا توجد نتائج لنسخها. قم بالحساب أولًا.")
            return

        joined_text = "\n".join(lines)
        self.clipboard_clear()
        self.clipboard_append(joined_text)
        self._set_status("تم نسخ النتائج إلى الحافظة.", info=True)

    def clear_inputs(self) -> None:
        self.day_entry.delete(0, "end")
        self.month_entry.delete(0, "end")
        self.year_entry.delete(0, "end")
        for key in self.result_vars:
            self.result_vars[key].set("")
        self._set_status("تمت إعادة التهيئة. أدخل تاريخ ميلاد جديد.")

    def fill_today(self) -> None:
        today = date.today()
        self.day_entry.delete(0, "end")
        self.day_entry.insert(0, str(today.day))
        self.month_entry.delete(0, "end")
        self.month_entry.insert(0, str(today.month))
        self.year_entry.delete(0, "end")
        self.year_entry.insert(0, str(today.year))
        self._set_status("تم إدخال تاريخ اليوم. يمكنك التعديل أو الحساب مباشرة.")

    def toggle_theme(self) -> None:
        if self.theme_mode == "light":
            self.theme_mode = "dark"
            ctk.set_appearance_mode("dark")
            self.configure(fg_color=DARK_BACKGROUND)
            self.status_label.configure(text_color=SECONDARY_COLOR)
            self._set_status("تم تفعيل الوضع الليلي.", info=True)
        else:
            self.theme_mode = "light"
            ctk.set_appearance_mode("light")
            self.configure(fg_color=BACKGROUND_COLOR)
            self.status_label.configure(text_color=PRIMARY_COLOR)
            self._set_status("تم تفعيل الوضع النهاري.", info=True)

    def show_help(self) -> None:
        messagebox.showinfo(
            "مركز المساعدة",
            "١. أدخل تاريخ ميلادك بالأرقام العربية أو الهندية.\n"
            "٢. اضغط على \"احسب الآن\" لعرض التفاصيل بالكامل.\n"
            "٣. يمكنك حفظ النتائج أو نسخها للمشاركة.\n"
            "٤. جرّب الوضع الليلي واستمتع بالواجهة العصرية!",
        )

    def _show_error(self, message: str) -> None:
        messagebox.showerror("خطأ", message)
        self._set_status(message, error=True)

    def _set_status(self, message: str, *, success: bool = False, error: bool = False, info: bool = False) -> None:
        self.status_var.set(message)
        if success:
            color = "#16a34a"
        elif error:
            color = "#ef4444"
        elif info:
            color = SECONDARY_COLOR if self.theme_mode == "light" else "#60a5fa"
        else:
            color = PRIMARY_COLOR
        self.status_label.configure(text_color=color)


def main() -> None:
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    app = AgeZodiacApp()
    app.mainloop()


if __name__ == "__main__":
    main()
