from django.db import migrations

META = {
    "title": "Главная",
    "meta_title": "ССУ-138 — Строительство объектов федерального уровня",
    "meta_description": "ССУ-138 — строительство, проектирование, спецтехника. Объекты федерального уровня с 2008 года. Москва, Сочи, Крым, Севастополь.",
    "og_title": "ССУ-138 — Строительство объектов федерального уровня",
    "og_description": "ССУ-138 — строительство, проектирование, спецтехника. Объекты федерального уровня с 2008 года. Москва, Сочи, Крым, Севастополь.",
}

CARDS = [
    ("01", "Строительство", "Промышленные, гражданские, военные и социальные объекты под ключ. Опыт работы на объектах федерального значения."),
    ("02", "Проектирование", "Полный цикл проектных работ: рабочая документация, согласования, BIM-моделирование. Соответствие требованиям государственного заказчика."),
    ("03", "Спецтехника", "Аренда спецтехники с экипажем: краны, экскаваторы, бульдозеры. Собственный парк 50+ единиц."),
]

PROJECTS = [
    {
        "title": "Резиденция «Бочаров ручей»", "tag": "ГОСЗАКАЗ",
        "description": "Строительные работы на объекте федерального значения. Заказчик — Управление делами Президента РФ.",
        "static_image": "img/objects/bocharov-ruchey.webp",
        "meta": [
            {"label": "Заказчик", "value": "УДП РФ"},
            {"label": "Локация", "value": "Сочи"},
            {"label": "Тип", "value": "Государственный"},
            {"label": "Статус", "value": "Сдан"},
        ],
    },
    {
        "title": "МДЦ «Артек»", "tag": "МИНПРОСВЕЩЕНИЯ",
        "description": "Реконструкция и строительство объектов МДЦ «Артек». Заказчик — Министерство просвещения РФ.",
        "static_image": "img/objects/artek.jpg",
        "meta": [
            {"label": "Заказчик", "value": "Минпросвещения"},
            {"label": "Локация", "value": "Ялта, Крым"},
            {"label": "Тип", "value": "Социальный"},
            {"label": "Статус", "value": "Сдан"},
        ],
    },
    {
        "title": "Военный госпиталь", "tag": "МИНОБОРОНЫ",
        "description": "Строительство военного госпиталя для Министерства обороны РФ. Полный цикл работ.",
        "static_image": "img/objects/military-hospital.jpg",
        "meta": [
            {"label": "Заказчик", "value": "Минобороны РФ"},
            {"label": "Локация", "value": "Севастополь"},
            {"label": "Тип", "value": "Военный"},
            {"label": "Статус", "value": "Сдан"},
        ],
    },
]

STATS = [
    ("17", "", "17", "лет на рынке"),
    ("100", "+", "100+", "сданных объектов"),
    ("250000", "+", "250 000+", "м² построено"),
    ("50", "+", "50+", "единиц спецтехники"),
]

STAGES = [
    ("01", "Заявка", "Приём обращения, анализ технического задания, оценка"),
    ("02", "Проектирование", "Рабочая документация, BIM-модель, сметный расчёт"),
    ("03", "Согласование", "Государственная экспертиза, разрешения, согласование"),
    ("04", "Строительство", "Производство работ, надзор, контроль качества и сроков"),
    ("05", "Сдача", "Приёмка объекта, документация, гарантийные обязательства"),
]

QUOTE = "«Выражаю Вам благодарность за добросовестный труд, безупречную работу и большой личный вклад в развитие системы жилищно-коммунального хозяйства Запорожской области.»"
ATTR = "Министерство строительства, архитектуры и ЖКХ Запорожской области · И.о. министра В.Н. Завадич · 15 марта 2026 г."


def seed(apps, schema_editor):
    Page = apps.get_model("content", "Page")
    Section = apps.get_model("content", "Section")
    SectionItem = apps.get_model("content", "SectionItem")

    if Page.objects.filter(slug="home").exists():
        return

    page = Page.objects.create(slug="home", is_published=True, **META)

    Section.objects.create(
        page=page, order=0, block_type="hero",
        eyebrow="СПЕЦИАЛИЗИРОВАННОЕ СТРОИТЕЛЬНОЕ УПРАВЛЕНИЕ · С 2008",
        title="Строительство объектов<br>федерального уровня.",
        subtitle="Полный цикл — от проектирования до сдачи под ключ. Государственные подряды, собственный парк техники, контроль качества на каждом этапе.",
    )

    cards = Section.objects.create(
        page=page, order=1, block_type="cards",
        eyebrow="УСЛУГИ", title="Что мы делаем", anchor="services",
    )
    for i, (num, title, desc) in enumerate(CARDS):
        SectionItem.objects.create(section=cards, order=i, number=num, title=title, description=desc)

    projects = Section.objects.create(
        page=page, order=2, block_type="projects",
        eyebrow="РЕАЛИЗОВАННЫЕ ОБЪЕКТЫ", title="Ключевые проекты", anchor="objects",
    )
    for i, p in enumerate(PROJECTS):
        SectionItem.objects.create(
            section=projects, order=i, title=p["title"], tag=p["tag"],
            description=p["description"],
            extra={"static_image": p["static_image"], "meta": p["meta"]},
        )

    stats = Section.objects.create(
        page=page, order=3, block_type="stats", anchor="about",
    )
    for i, (num, suffix, visible, label) in enumerate(STATS):
        SectionItem.objects.create(
            section=stats, order=i, number=num, subtitle=visible, title=label,
            extra={"suffix": suffix},
        )

    Section.objects.create(
        page=page, order=4, block_type="testimonial",
        eyebrow="ДОВЕРИЕ", title="Нам доверяют государственные структуры",
        subtitle=QUOTE, body=ATTR,
        extra={"static_image": "img/gratitude/letter.jpg"},
    )

    stages = Section.objects.create(
        page=page, order=5, block_type="stages",
        eyebrow="ПРОЦЕСС", title="Этапы реализации",
    )
    for i, (num, title, desc) in enumerate(STAGES):
        SectionItem.objects.create(section=stages, order=i, number=num, title=title, description=desc)


def unseed(apps, schema_editor):
    Page = apps.get_model("content", "Page")
    Page.objects.filter(slug="home").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0003_seed_service_pages"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
