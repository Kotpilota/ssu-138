"""Модели контента сайта — редактируются из панели /panel/ без деплоя.

Содержит:
- SiteSettings — синглтон с реквизитами компании и настройками сайта.
- Page / Section / SectionItem — блочная структура страниц лендинга и услуг.
"""
from django.db import models

DEFAULT_MAP_EMBED = (
    "https://yandex.ru/map-widget/v1/?ll=33.485610%2C44.581079&z=17"
    "&pt=33.485610%2C44.581079%2Cpm2rdl&l=map&lang=ru_RU"
)


class SiteSettings(models.Model):
    """Общие настройки/реквизиты сайта. Всегда одна запись (pk=1)."""

    phone = models.CharField("Телефон", max_length=32, default="+7 (916) 992-22-24")
    email = models.EmailField("Email", default="info@ssu-138.ru")
    address = models.CharField("Адрес (короткий)", max_length=255, default="г. Москва")

    inn = models.CharField("ИНН", max_length=20, blank=True, default="9111027572")
    ogrn = models.CharField("ОГРН", max_length=20, blank=True, default="1219100000932")
    legal_name = models.CharField(
        "Юр. название", max_length=255, blank=True, default='ООО "ССУ 138"'
    )
    address_legal = models.CharField(
        "Юридический адрес", max_length=255, blank=True,
        default="299053, г. Севастополь, ул. Отрадная, д. 15/1",
    )

    site_url = models.URLField("URL сайта", default="https://ssu-138.ru")
    og_image = models.ImageField(
        "OG-картинка (для соцсетей)", upload_to="site/", blank=True
    )
    map_embed_url = models.URLField(
        "Ссылка на встраиваемую карту", max_length=1000, blank=True,
        default=DEFAULT_MAP_EMBED,
    )

    # Telegram-уведомления (пока читаются из env; поля зарезервированы)
    telegram_enabled = models.BooleanField("Telegram включён", default=False)
    telegram_bot_token = models.CharField("Telegram bot token", max_length=255, blank=True)
    telegram_chat_id = models.CharField("Telegram chat id", max_length=64, blank=True)
    telegram_thread_id = models.CharField("Telegram thread id", max_length=64, blank=True)

    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"

    def __str__(self):
        return "Настройки сайта"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class BlockType(models.TextChoices):
    HERO = "hero", "Hero (главный баннер)"
    SERVICE_HERO = "service_hero", "Hero страницы услуги"
    CARDS = "cards", "Карточки услуг"
    FEATURES = "features", "Фичи (нумерованные)"
    PROJECTS = "projects", "Проекты (объекты)"
    STATS = "stats", "Статистика (счётчики)"
    TESTIMONIAL = "testimonial", "Доверие / отзыв"
    STAGES = "stages", "Этапы"
    CONTACTS = "contacts", "Контакты + форма"
    CTA = "cta", "Призыв к действию"
    NEWS = "news", "Новость (статья + галерея)"
    CUSTOM_HTML = "custom_html", "Произвольный HTML"


class Page(models.Model):
    """Страница сайта: лендинг (home) или страница услуги."""

    slug = models.SlugField("Слаг (URL)", unique=True, max_length=100)
    title = models.CharField("Название (внутреннее)", max_length=200)

    meta_title = models.CharField("SEO title", max_length=300, blank=True)
    meta_description = models.TextField("SEO description", blank=True)
    meta_keywords = models.TextField("SEO keywords", blank=True)
    og_title = models.CharField("OG title", max_length=300, blank=True)
    og_description = models.TextField("OG description", blank=True)
    og_image = models.ImageField("OG image", upload_to="pages/", blank=True)

    is_published = models.BooleanField("Опубликована", default=True)

    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"
        ordering = ["slug"]

    def __str__(self):
        return f"{self.title} (/{self.slug})"


class Section(models.Model):
    """Блок страницы. Тип (block_type) определяет partial для рендера."""

    page = models.ForeignKey(
        Page, on_delete=models.CASCADE, related_name="sections", verbose_name="Страница"
    )
    order = models.PositiveIntegerField("Порядок", default=0, db_index=True)
    block_type = models.CharField(
        "Тип блока", max_length=32, choices=BlockType.choices, default=BlockType.CUSTOM_HTML
    )
    is_visible = models.BooleanField("Показывать", default=True)

    eyebrow = models.CharField("Надзаголовок (mono)", max_length=200, blank=True)
    title = models.CharField("Заголовок", max_length=300, blank=True)
    subtitle = models.TextField("Подзаголовок", blank=True)
    body = models.TextField("Текст / HTML", blank=True)
    image = models.ImageField("Картинка", upload_to="sections/", blank=True)
    anchor = models.SlugField("Якорь (id)", max_length=60, blank=True)
    extra = models.JSONField("Доп. настройки", default=dict, blank=True)

    class Meta:
        verbose_name = "Секция"
        verbose_name_plural = "Секции"
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.get_block_type_display()} — {self.title or self.anchor or self.pk}"

    @property
    def template_name(self):
        return f"landing/blocks/{self.block_type}.html"


class SectionItem(models.Model):
    """Повторяющийся элемент внутри секции (карточка, счётчик, этап и т.д.)."""

    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, related_name="items", verbose_name="Секция"
    )
    order = models.PositiveIntegerField("Порядок", default=0, db_index=True)

    number = models.CharField("Номер / значение", max_length=40, blank=True)
    title = models.CharField("Заголовок", max_length=300, blank=True)
    subtitle = models.CharField("Подзаголовок", max_length=300, blank=True)
    description = models.TextField("Описание", blank=True)
    image = models.ImageField("Картинка", upload_to="items/", blank=True)
    tag = models.CharField("Тег / метка", max_length=100, blank=True)
    link_text = models.CharField("Текст ссылки", max_length=120, blank=True)
    link_url = models.CharField("URL ссылки", max_length=300, blank=True)
    extra = models.JSONField("Доп. поля", default=dict, blank=True)

    class Meta:
        verbose_name = "Элемент секции"
        verbose_name_plural = "Элементы секции"
        ordering = ["order", "id"]

    def __str__(self):
        return self.title or f"Элемент #{self.pk}"
