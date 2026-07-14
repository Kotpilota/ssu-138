from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django.utils import timezone




def index(request):
    from apps.content.models import Page

    page = get_object_or_404(
        Page.objects.prefetch_related("sections__items"),
        slug="home", is_published=True,
    )
    sections = [s for s in page.sections.all() if s.is_visible]
    return render(request, "landing/index.html", {"page": page, "sections": sections})


def service_page(request, slug):
    from apps.content.models import Page

    page = get_object_or_404(
        Page.objects.prefetch_related("sections__items"),
        slug=slug, is_published=True,
    )
    sections = [s for s in page.sections.all() if s.is_visible]
    hero = next(
        (s for s in page.sections.all() if s.block_type == "service_hero"), None
    )
    return render(request, "landing/service_page.html", {
        "page": page, "slug": slug, "sections": sections, "hero": hero,
    })


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
