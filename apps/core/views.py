from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.conf import settings
from django.utils import timezone


SERVICE_PAGES = {
    "stroitelstvo": {
        "meta_title": "Строительство под ключ в Москве — Генподрядчик ССУ-138",
        "meta_description": "Генподрядчик ССУ-138: промышленное, гражданское, военное и социальное строительство под ключ. Госзаказы с 2008 г. 100+ объектов. Москва, Сочи, Крым, Севастополь.",
        "meta_keywords": "строительство под ключ Москва, промышленное строительство Москва, генподрядчик строительство, строительство промышленных объектов, военное строительство, государственные объекты строительство, ССУ-138",
        "og_title": "Строительство под ключ в Москве — ССУ-138",
        "og_description": "Промышленное, гражданское и военное строительство. Госзаказы с 2008 г. 100+ объектов.",
        "label": "СТРОИТЕЛЬСТВО",
        "h1": "Строительство под ключ в Москве",
        "subtitle": "Промышленные, гражданские, военные и социальные объекты федерального уровня. Полный цикл от проектирования до сдачи.",
        "features": [
            {"num": "01", "title": "Промышленные объекты", "desc": "Заводы, производственные корпуса, склады, технические сооружения любой сложности."},
            {"num": "02", "title": "Гражданское строительство", "desc": "Административные здания, жилые комплексы, объекты коммерческой недвижимости."},
            {"num": "03", "title": "Военные объекты", "desc": "Строительство для Министерства обороны РФ. Опыт работы на объектах федерального значения."},
            {"num": "04", "title": "Социальные объекты", "desc": "Больницы, учебные заведения, детские лагеря, спортивные и культурные центры."},
        ],
        "service_name_ld": "Строительство под ключ",
        "service_desc_ld": "Промышленные, гражданские, военные и социальные объекты. Полный цикл работ от проектирования до сдачи.",
    },
    "proektirovanie": {
        "meta_title": "Проектирование зданий в Москве — ССУ-138",
        "meta_description": "ССУ-138: полный цикл проектных работ, BIM-моделирование, рабочая документация, государственная экспертиза. Проектирование в Москве с 2008 года.",
        "meta_keywords": "проектирование зданий Москва, BIM проектирование, рабочая документация строительство, государственная экспертиза, проектная организация Москва, ССУ-138",
        "og_title": "Проектирование зданий и сооружений — ССУ-138",
        "og_description": "Полный цикл проектных работ: рабочая документация, BIM-моделирование, госэкспертиза. Москва.",
        "label": "ПРОЕКТИРОВАНИЕ",
        "h1": "Проектирование зданий и сооружений в Москве",
        "subtitle": "Полный цикл проектных работ: рабочая документация, BIM-моделирование, согласования и государственная экспертиза.",
        "features": [
            {"num": "01", "title": "Рабочая документация", "desc": "Полный комплект проектной и рабочей документации в соответствии с нормами РФ."},
            {"num": "02", "title": "BIM-моделирование", "desc": "Информационное моделирование зданий для государственных и коммерческих заказчиков."},
            {"num": "03", "title": "Государственная экспертиза", "desc": "Прохождение Главгосэкспертизы, региональных экспертиз и согласований в госорганах."},
            {"num": "04", "title": "Сметный расчёт", "desc": "Разработка сметной документации, расчёт стоимости строительства по ГЭСН и ФЕР."},
        ],
        "service_name_ld": "Проектирование зданий и сооружений",
        "service_desc_ld": "Полный цикл проектных работ: рабочая документация, BIM-моделирование, государственная экспертиза.",
    },
    "spetstehnika": {
        "meta_title": "Аренда спецтехники в Москве — ССУ-138 | Краны, Экскаваторы",
        "meta_description": "Аренда спецтехники от ССУ-138: краны, экскаваторы, бульдозеры с экипажем. Собственный парк 50+ единиц. Москва, Сочи, Крым, Севастополь.",
        "meta_keywords": "аренда спецтехники Москва, аренда крана Москва, аренда экскаватора Москва, аренда бульдозера Москва, спецтехника с экипажем, строительная техника аренда",
        "og_title": "Аренда спецтехники с экипажем — ССУ-138",
        "og_description": "Краны, экскаваторы, бульдозеры. Собственный парк 50+ единиц. Москва, Сочи, Крым.",
        "label": "СПЕЦТЕХНИКА",
        "h1": "Аренда спецтехники с экипажем в Москве",
        "subtitle": "Собственный парк 50+ единиц: краны, экскаваторы, бульдозеры. Опытные машинисты, оперативная подача на объект.",
        "features": [
            {"num": "01", "title": "Краны", "desc": "Автокраны и башенные краны различной грузоподъёмности с опытными операторами."},
            {"num": "02", "title": "Экскаваторы", "desc": "Гусеничные и колёсные экскаваторы для земляных, демонтажных и планировочных работ."},
            {"num": "03", "title": "Бульдозеры", "desc": "Бульдозеры для планировки территории, вертикальной планировки, рекультивации."},
            {"num": "04", "title": "Прочая техника", "desc": "Погрузчики, самосвалы, компрессоры и другая строительная и вспомогательная техника."},
        ],
        "service_name_ld": "Аренда спецтехники с экипажем",
        "service_desc_ld": "Аренда строительной техники: краны, экскаваторы, бульдозеры. Собственный парк 50+ единиц.",
    },
}


def index(request):
    return render(request, "landing/index.html")


def service_page(request, slug):
    data = SERVICE_PAGES.get(slug)
    if data is None:
        raise Http404
    return render(request, "landing/service_page.html", {"service": data, "slug": slug})


def privacy(request):
    return render(request, "landing/privacy.html")


def healthz(request):
    return HttpResponse("ok", content_type="text/plain")


def robots_txt(request):
    site_url = getattr(settings, "SITE_URL", "https://ssu-138.ru")
    content = f"""User-agent: *
Allow: /
Disallow: /panel/
Disallow: /admin/
Disallow: /api/

Sitemap: {site_url}/sitemap.xml
"""
    return HttpResponse(content, content_type="text/plain; charset=utf-8")


def sitemap_xml(request):
    site_url = getattr(settings, "SITE_URL", "https://ssu-138.ru")
    today = timezone.now().date().isoformat()
    content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{site_url}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>{site_url}/stroitelstvo/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>{site_url}/proektirovanie/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>{site_url}/spetstehnika/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>{site_url}/privacy/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>yearly</changefreq>
    <priority>0.3</priority>
  </url>
</urlset>"""
    return HttpResponse(content, content_type="application/xml; charset=utf-8")


def handler404(request, exception):
    return render(request, "404.html", status=404)


def handler500(request):
    return render(request, "500.html", status=500)
