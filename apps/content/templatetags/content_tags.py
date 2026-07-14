from django import template
from django.template.loader import select_template

register = template.Library()


@register.simple_tag(takes_context=True)
def render_section(context, section):
    """Рендерит секцию через partial landing/blocks/<block_type>.html.

    Фолбэк на custom_html, если partial для типа не найден (например, тип
    сохранён, но шаблон ещё не создан)."""
    tpl = select_template([
        f"landing/blocks/{section.block_type}.html",
        "landing/blocks/custom_html.html",
    ])
    ctx = context.flatten()
    ctx["section"] = section
    ctx["items"] = section.items.all()
    return tpl.render(ctx)
