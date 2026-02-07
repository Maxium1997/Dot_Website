import json

from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from organization.models import Unit
from .models import Station, StationAlbum, StationPhoto, StationService


def index(request):
    stations = Station.objects.select_related("operator").prefetch_related(
        "services", "attractions", "albums__photos"
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

    stations = list(stations.distinct().order_by("name"))

    for station in stations:
        cover_photo = None
        for album in station.albums.all():
            cover_photo = album.photos.filter(is_cover_image=True).first()
            if cover_photo:
                break
        if not cover_photo:
            for album in station.albums.all():
                cover_photo = album.photos.order_by("sort_order", "created_at").first()
                if cover_photo:
                    break
        station.cover_url = cover_photo.image.url if cover_photo else ""

    map_stations = []
    for station in (
        Station.objects.exclude(latitude__isnull=True)
        .exclude(longitude__isnull=True)
        .values("name", "latitude", "longitude", "region")
        .order_by("name")
    ):
        map_stations.append(
            {
                "name": station["name"],
                "latitude": float(station["latitude"]),
                "longitude": float(station["longitude"]),
                "region": station["region"],
            }
        )

    context = {
        "stations": stations,
        "regions": Station.REGION_CHOICES,
        "services": StationService.SERVICE_CHOICES,
        "map_stations": map_stations,
        "filters": {
            "q": query,
            "region": region,
            "service": service,
        },
    }
    return render(request, "ocean_station/index.html", context)


def detail(request, en_name):
    station = get_object_or_404(
        Station.objects.select_related("operator").prefetch_related(
            "services", "attractions", "albums__photos"
        ),
        en_name=en_name,
    )

    cover_photo = None
    for album in station.albums.all():
        cover_photo = album.photos.filter(is_cover_image=True).first()
        if cover_photo:
            break
    if not cover_photo:
        for album in station.albums.all():
            cover_photo = album.photos.order_by("sort_order", "created_at").first()
            if cover_photo:
                break

    map_station = None
    if station.latitude is not None and station.longitude is not None:
        map_station = {
            "name": station.name,
            "latitude": float(station.latitude),
            "longitude": float(station.longitude),
            "region": station.region,
        }

    context = {
        "station": station,
        "cover_photo": cover_photo,
        "map_station": map_station,
        "regions": Station.REGION_CHOICES,
        "units": list(Unit.objects.order_by("name").values("id", "name")),
        "service_choices": StationService.SERVICE_CHOICES,
        "service_values": list(station.services.values_list("service", flat=True)),
    }
    return render(request, "ocean_station/detail.html", context)


@require_POST
def update_station(request, en_name):
    if not request.user.is_staff:
        return HttpResponseForbidden("Forbidden")

    station = get_object_or_404(Station, en_name=en_name)
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return HttpResponseBadRequest("Invalid JSON")

    allowed_fields = {
        "name",
        "alias",
        "region",
        "operator_id",
        "address",
        "phone",
        "overview",
        "geo_features",
        "exhibit_plan",
        "services",
    }
    data = {k: v for k, v in payload.items() if k in allowed_fields}

    if "region" in data:
        valid_regions = {value for value, _ in Station.REGION_CHOICES}
        if data["region"] not in valid_regions:
            return HttpResponseBadRequest("Invalid region")
        station.region = data["region"]

    if "operator_id" in data:
        try:
            station.operator_id = int(data["operator_id"])
        except (TypeError, ValueError):
            return HttpResponseBadRequest("Invalid operator")

    for field in ["name", "alias", "address", "phone", "overview", "geo_features", "exhibit_plan"]:
        if field in data:
            value = data[field]
            if isinstance(value, str):
                value = value.strip()
            setattr(station, field, value or "")

    station.save()

    if "services" in data and isinstance(data["services"], list):
        valid_services = {value for value, _ in StationService.SERVICE_CHOICES}
        selected = [s for s in data["services"] if s in valid_services]
        StationService.objects.filter(station=station).exclude(service__in=selected).delete()
        existing = set(station.services.values_list("service", flat=True))
        for service in selected:
            if service not in existing:
                StationService.objects.create(station=station, service=service)

    return JsonResponse(
        {
            "name": station.name,
            "alias": station.alias,
            "region": station.region,
            "region_label": station.get_region_display(),
            "operator_name": station.operator.name,
            "address": station.address,
            "phone": station.phone,
            "overview": station.overview,
            "geo_features": station.geo_features,
            "exhibit_plan": station.exhibit_plan,
        }
    )


@require_POST
def create_album(request, en_name):
    if not request.user.is_staff:
        return HttpResponseForbidden("Forbidden")

    station = get_object_or_404(Station, en_name=en_name)
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return HttpResponseBadRequest("Invalid JSON")

    title = (payload.get("title") or "").strip()
    description = (payload.get("description") or "").strip()
    if not title:
        return HttpResponseBadRequest("Title required")

    album = StationAlbum.objects.create(
        station=station,
        title=title,
        description=description or "",
    )

    return JsonResponse(
        {
            "id": album.id,
            "title": album.title,
            "description": album.description,
        }
    )


def album_detail(request, en_name, album_id):
    station = get_object_or_404(Station, en_name=en_name)
    album = get_object_or_404(
        StationAlbum.objects.prefetch_related("photos"),
        id=album_id,
        station=station,
    )

    if request.method == "POST":
        if not request.user.is_staff:
            return HttpResponseForbidden("Forbidden")

        files = request.FILES.getlist("photos")
        for file in files:
            StationPhoto.objects.create(
                album=album,
                image=file,
                is_display=True,
                is_cover_image=False,
            )

    context = {
        "station": station,
        "album": album,
        "photos": album.photos.order_by("sort_order", "created_at"),
    }
    return render(request, "ocean_station/album_detail.html", context)


@require_POST
@user_passes_test(lambda user: user.is_staff)
def update_album(request, en_name, album_id):
    album = get_object_or_404(
        StationAlbum,
        id=album_id,
        station__en_name=en_name,
    )
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return HttpResponseBadRequest("Invalid JSON")

    title = (payload.get("title") or "").strip()
    description = (payload.get("description") or "").strip()
    if not title:
        return HttpResponseBadRequest("Title required")

    album.title = title
    album.description = description
    album.save(update_fields=["title", "description"])

    return JsonResponse({"title": album.title, "description": album.description})


@require_POST
@user_passes_test(lambda user: user.is_staff)
def upload_photos(request, en_name, album_id):
    album = get_object_or_404(
        StationAlbum,
        id=album_id,
        station__en_name=en_name,
    )
    files = request.FILES.getlist("photos")
    if not files:
        return HttpResponseBadRequest("No files")

    created = []
    for file in files:
        photo = StationPhoto.objects.create(
            album=album,
            image=file,
            is_display=True,
            is_cover_image=False,
        )
        created.append(
            {
                "id": photo.id,
                "url": photo.image.url,
                "caption": photo.caption or "",
                "sort_order": photo.sort_order,
                "is_cover_image": photo.is_cover_image,
            }
        )

    return JsonResponse({"photos": created})


@require_POST
@user_passes_test(lambda user: user.is_staff)
def set_cover_photo(request, en_name, album_id, photo_id):
    album = get_object_or_404(
        StationAlbum,
        id=album_id,
        station__en_name=en_name,
    )
    photo = get_object_or_404(StationPhoto, id=photo_id, album=album)

    StationPhoto.objects.filter(album=album, is_cover_image=True).update(is_cover_image=False)
    photo.is_cover_image = True
    photo.save(update_fields=["is_cover_image"])

    return JsonResponse({"photo_id": photo.id, "is_cover_image": True})


@require_POST
@user_passes_test(lambda user: user.is_staff)
def delete_photo(request, en_name, album_id, photo_id):
    photo = get_object_or_404(
        StationPhoto,
        id=photo_id,
        album__id=album_id,
        album__station__en_name=en_name,
    )
    photo.delete()
    return JsonResponse({"deleted": True, "photo_id": photo_id})


@require_POST
@user_passes_test(lambda user: user.is_staff)
def update_photo_display(request, en_name, album_id, photo_id):
    photo = get_object_or_404(
        StationPhoto,
        id=photo_id,
        album__id=album_id,
        album__station__en_name=en_name,
    )
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return HttpResponseBadRequest("Invalid JSON")

    is_display = payload.get("is_display")
    if not isinstance(is_display, bool):
        return HttpResponseBadRequest("Invalid is_display")

    photo.is_display = is_display
    photo.save(update_fields=["is_display"])
    return JsonResponse({"photo_id": photo.id, "is_display": photo.is_display})


@require_POST
@user_passes_test(lambda user: user.is_staff)
def reorder_photos(request, en_name, album_id):
    album = get_object_or_404(
        StationAlbum,
        id=album_id,
        station__en_name=en_name,
    )
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return HttpResponseBadRequest("Invalid JSON")

    updates = payload.get("orders", [])
    if not isinstance(updates, list):
        return HttpResponseBadRequest("Invalid payload")

    for item in updates:
        try:
            photo_id = int(item.get("id"))
            sort_order = int(item.get("sort_order"))
        except (TypeError, ValueError):
            continue
        StationPhoto.objects.filter(album=album, id=photo_id).update(sort_order=sort_order)

    return JsonResponse({"updated": True})
