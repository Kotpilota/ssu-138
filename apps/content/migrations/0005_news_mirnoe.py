"""Наполнение прода объектом «пгт Мирное» (ремонт кровель):
- карточка в блок «Ключевые проекты» на главной;
- блок-новость «Возрождение двух домов в Мирном» с галереей.

Контент дальше редактируется из /panel/ → Страницы → Главная.
"""
from django.db import migrations

CARD = {
    "title": "Ремонт кровель, пгт Мирное",
    "tag": "КАПРЕМОНТ · ФКР",
    "description": (
        "Капитальный ремонт кровель двух домов 1950-х годов постройки "
        "по ул. Школьной, 3 и 5. Новые стропила, перекрытия и профнастил."
    ),
    "static_image": "img/objects/mirnoe.jpg",
    "meta": [
        {"label": "Заказчик", "value": "ФКР Запорожской обл."},
        {"label": "Локация", "value": "пгт Мирное"},
        {"label": "Площадь", "value": "1 718 м²"},
        {"label": "Статус", "value": "В работе"},
    ],
}

NEWS_TITLE = "Возрождение двух домов в Мирном"
NEWS_DATE = "Июль 2026"
NEWS_LEAD = (
    "В посёлке городского типа Мирное Запорожской области бригада ООО «ССУ 138» "
    "завершает капитальный ремонт кровель двух домов, построенных ещё в 1950-х годах. "
    "Эти здания не знали такого обновления с самого возведения."
)
NEWS_PARAGRAPHS = [
    "Дома по улице Школьной, 3 и 5, — ровесники послевоенного восстановления региона. "
    "Их кровли, сложенные из глиняной черепицы, отслужили почти 70 лет: за это время "
    "капитальный ремонт здесь не проводился ни разу. Естественный износ, перепады "
    "температур и осадки сделали своё дело — старые перекрытия прогнили, а утеплитель "
    "из шлака давно перестал выполнять свои функции. Общая площадь отремонтированной "
    "кровли составила более 1 700 квадратных метров: 880 м² на доме №3 и 838 м² на доме №5.",
    "Подрядчик ООО «ССУ 138» провёл комплексную реконструкцию кровельной системы. "
    "Работы начались в апреле и уже к концу июля выходят на финишную прямую. Вместо "
    "прогнивших конструкций смонтированы новые деревянные стропила и чердачные "
    "перекрытия. Все деревянные элементы обработаны огнезащитными и антисептическими "
    "составами, предотвращающими появление плесени и грибка. Старый шлаковый утеплитель "
    "заменяется на современный, а вместо ветхой черепицы кровельщики укладывают "
    "надёжный и долговечный профнастил.",
    "Замена кровли — один из ключевых этапов в поддержании технического состояния "
    "многоквартирных домов. Работы в пгт Мирное ведутся в рамках поручения губернатора "
    "Запорожской области Евгения Балицкого и под контролем Фонда капитального ремонта "
    "многоквартирных домов Запорожской области.",
]
NEWS_BODY = "".join(f"<p>{p}</p>" for p in NEWS_PARAGRAPHS)

GALLERY = [
    {"image": "img/news/mirnoe/panorama.jpg", "caption": "Дом по ул. Школьной после замены кровли"},
    {"image": "img/news/mirnoe/kran.jpg", "caption": "Монтаж кровли — автокран на объекте"},
    {"image": "img/news/mirnoe/kontejnery.jpg", "caption": "Демонтаж старой черепицы и вывоз строительного мусора"},
    {"image": "img/news/mirnoe/dom.jpg", "caption": "Новый профнастил вместо ветхой черепицы"},
    {"image": "img/news/mirnoe/uteplitel.jpg", "caption": "Современный утеплитель на смену шлаковому"},
]

ANCHOR = "news-mirnoe"


def seed(apps, schema_editor):
    Page = apps.get_model("content", "Page")
    Section = apps.get_model("content", "Section")
    SectionItem = apps.get_model("content", "SectionItem")

    try:
        page = Page.objects.get(slug="home")
    except Page.DoesNotExist:
        return

    projects = page.sections.filter(block_type="projects").order_by("order").first()

    # 1. Карточка объекта в «Ключевые проекты»
    if projects and not projects.items.filter(title__icontains="Мирн").exists():
        last = projects.items.order_by("-order").first()
        next_order = (last.order + 1) if last else 0
        SectionItem.objects.create(
            section=projects, order=next_order,
            title=CARD["title"], tag=CARD["tag"], description=CARD["description"],
            extra={"static_image": CARD["static_image"], "meta": CARD["meta"]},
        )

    # 2. Блок-новость сразу после блока проектов
    if page.sections.filter(anchor=ANCHOR).exists():
        return

    insert_after = projects.order if projects else 1
    for s in page.sections.filter(order__gt=insert_after).order_by("-order"):
        s.order += 1
        s.save(update_fields=["order"])

    news = Section.objects.create(
        page=page, order=insert_after + 1, block_type="news",
        eyebrow="НОВОСТИ", title=NEWS_TITLE, subtitle=NEWS_LEAD, body=NEWS_BODY,
        anchor=ANCHOR, extra={"date": NEWS_DATE},
    )
    for i, g in enumerate(GALLERY):
        SectionItem.objects.create(
            section=news, order=i, title=g["caption"],
            extra={"static_image": g["image"]},
        )


def unseed(apps, schema_editor):
    Page = apps.get_model("content", "Page")
    Section = apps.get_model("content", "Section")

    try:
        page = Page.objects.get(slug="home")
    except Page.DoesNotExist:
        return

    Section.objects.filter(page=page, anchor=ANCHOR).delete()
    projects = page.sections.filter(block_type="projects").first()
    if projects:
        projects.items.filter(title__icontains="Мирн").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0004_seed_home"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
