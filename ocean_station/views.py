from django.db.models import Q
from django.shortcuts import render

from .models import Station, StationService


def index(request):
    stations = Station.objects.select_related("operator").prefetch_related(
        "services", "attractions", "albums"
    )

    query = request.GET.get("q", "").strip()
    if query:
        stations = stations.filter(
            Q(name__icontains=query)
            | Q(en_name__icontains=query)
            | Q(alias__icontains=query)
            | Q(address__icontains=query)
        )

    region = request.GET.get("region", "").strip()
    if region:
        stations = stations.filter(region=region)

    service = request.GET.get("service", "").strip()
    if service:
        stations = stations.filter(services__service=service)

    stations = stations.distinct().order_by("name")

    map_stations = (
        Station.objects.exclude(latitude__isnull=True)
        .exclude(longitude__isnull=True)
        .values("name", "latitude", "longitude", "region")
        .order_by("name")
    )

    context = {
        "stations": stations,
        "regions": Station.REGION_CHOICES,
        "services": StationService.SERVICE_CHOICES,
        "map_stations": list(map_stations),
        "filters": {
            "q": query,
            "region": region,
            "service": service,
        },
    }
    return render(request, "ocean_station/index.html", context)
