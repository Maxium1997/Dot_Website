from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.urls import NoReverseMatch, reverse
from django.views.generic import TemplateView, ListView

# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'


def robots_txt(request):
    return TemplateResponse(request, "robots.txt", content_type="text/plain")


def sitemap_xml(request):
    url_names = [
        "index",
        "playground:index",
        "playground:random_games",
        "playground:random_games_dice",
        "playground:random_games_raffle",
        "playground:karaoke",
        "playground:url_to_qr_code",
        "line_bot:line_bot_add_friend",
        "ocean_station:index",
        "coast_guard_mart:product_list",
        "badminton_court_management:booking_page",
    ]
    base_url = f"{request.scheme}://{request.get_host()}"
    urls = []
    for name in url_names:
        try:
            path = reverse(name)
        except NoReverseMatch:
            continue
        urls.append(f"{base_url}{path}")
    return TemplateResponse(
        request,
        "sitemap.xml",
        {"urls": urls},
        content_type="application/xml",
    )
