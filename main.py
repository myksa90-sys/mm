import flet as ft
from datetime import date
from calendar import monthrange

PRIMARY_COLOR = "#2563eb"
SECONDARY_COLOR = "#38bdf8"
ACCENT_COLOR = "#fb7185"
NEUTRAL_COLOR = "#64748b"

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
    return str(value).translate(str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩"))

def format_date_ar(d: date) -> str:
    weekday = AR_WEEKDAYS[d.weekday()]
    month = AR_MONTHS[d.month]
    return f"{weekday}، {to_arabic_digits(d.day)} {month} {to_arabic_digits(d.year)}م"

def safe_birthdate(year: int, month: int, day: int) -> date:
    last_day = monthrange(year, month)[1]
    return date(year, month, min(day, last_day))

def calculate_age_details(birth_date: date, today: date | None = None):
    if today is None:
        today = date.today()
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

def describe_age(age):
    parts = []
    if age["years"]:
        parts.append(f'{to_arabic_digits(age["years"])} سنة')
    if age["months"]:
        parts.append(f'{to_arabic_digits(age["months"])} شهر')
    if age["days"]:
        parts.append(f'{to_arabic_digits(age["days"])} يوم')
    return "، ".join(parts) if parts else "0"

def main(page: ft.Page):
    page.title = "حاسبة العمر والبرج الفلكي"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 480
    page.window_height = 850
    page.bgcolor = "#f3f4f6"

    year = ft.TextField(label="السنة", text_align=ft.TextAlign.RIGHT, autofocus=True)
    month = ft.TextField(label="الشهر", text_align=ft.TextAlign.RIGHT)
    day = ft.TextField(label="اليوم", text_align=ft.TextAlign.RIGHT)
    result = ft.Column()

    def calculate(e):
        result.controls.clear()
        try:
            y = int(year.value)
            m = int(month.value)
            d = int(day.value)
            today = date.today()
            birth_date = safe_birthdate(y, m, d)
            if birth_date > today:
                raise Exception("تاريخ الميلاد لا يمكن أن يكون في المستقبل.")
            age = calculate_age_details(birth_date, today)
            next_birthday = get_next_birthday(birth_date, today)
            zodiac = get_zodiac_info(birth_date)
            chinese = get_chinese_zodiac(y)

            age_details = describe_age(age)
            age_months = f"{to_arabic_digits(age['total_months'])} شهر"
            age_days = f"{to_arabic_digits(age['total_days'])} يوم منذ الولادة"
            age_weeks = f"{to_arabic_digits(age['total_weeks'])} أسبوع"
            birth_date_text = format_date_ar(birth_date)
            birth_day_name = f"كان يوم {AR_WEEKDAYS[birth_date.weekday()]}"
            zodiac_text = f"{zodiac['name']} — العنصر: {zodiac['element']}، الكوكب الحاكم: {zodiac['planet']}"
            zodiac_traits = zodiac["traits"]
            chinese_text = f"برجك الصيني: {chinese['name']} — {chinese['traits']}"
            days_until = (next_birthday - today).days
            if days_until == 0:
                next_birthday_text = (
                    f"اليوم هو عيد ميلادك! 🎉 تكمل {to_arabic_digits(age['years'])} سنة"
                )
            else:
                upcoming_age = age["years"] + 1
                approx_weeks = max(1, days_until // 7)
                next_birthday_text = (
                    f"عيدك القادم: {format_date_ar(next_birthday)} — متبقٍ "
                    f"{to_arabic_digits(days_until)} يوم (حوالي {to_arabic_digits(approx_weeks)} أسبوع). "
                    f"ستبلغ {to_arabic_digits(upcoming_age)} سنة."
                )

            items = [
                ft.Text("نتائجك الشخصية", size=26, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.RIGHT),
                ft.Divider(),
                ft.Text(f"تفاصيل العمر: {age_details}", text_align=ft.TextAlign.RIGHT),
                ft.Text(f"إجمالي الأشهر: {age_months}", text_align=ft.TextAlign.RIGHT),
                ft.Text(f"إجمالي الأيام: {age_days}", text_align=ft.TextAlign.RIGHT),
                ft.Text(f"إجمالي الأسابيع: {age_weeks}", text_align=ft.TextAlign.RIGHT),
                ft.Text(f"تاريخ الميلاد: {birth_date_text}", text_align=ft.TextAlign.RIGHT),
                ft.Text(f"{birth_day_name}", text_align=ft.TextAlign.RIGHT),
                ft.Text(f"البرج الغربي: {zodiac_text}", text_align=ft.TextAlign.RIGHT),
                ft.Text(f"وصف البرج: {zodiac_traits}", text_align=ft.TextAlign.RIGHT),
                ft.Text(f"{chinese_text}", text_align=ft.TextAlign.RIGHT),
                ft.Text(f"{next_birthday_text}", text_align=ft.TextAlign.RIGHT),
            ]
            result.controls.extend(items)
        except Exception as ex:
            result.controls.append(ft.Text(f"خطأ في البيانات: {ex}", color="red", text_align=ft.TextAlign.RIGHT))
        page.update()

    btn = ft.ElevatedButton(text="احسب الآن", bgcolor=PRIMARY_COLOR, color="white", on_click=calculate)
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("حاسبة العمر والبرج الفلكي", size=32, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.RIGHT),
                ft.Text(
                    "أدخل تاريخ ميلادك وسيتم عرض عمرك وجميع التفاصيل الفلكية مباشرة.",
                    size=15, text_align=ft.TextAlign.RIGHT),
                year,
                month,
                day,
                btn,
                ft.Divider(thickness=2),
                result,
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.END),
            padding=26,
            border_radius=ft.border_radius.all(16),
            bgcolor="#ecf2ff"
        )
    )

ft.app(target=main)
