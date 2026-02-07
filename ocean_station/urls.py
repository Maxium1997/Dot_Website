from django.urls import include, path, re_path

from . import views

app_name = "ocean_station"

urlpatterns = [
    path("", views.index, name="index"),
    re_path(
        r"^(?P<en_name>[^/]+)/",
        include([
            path("", views.detail, name="detail"),
            path("update/", views.update_station, name="update"),
            path(
                "albums/",
                include([
                    path("create/", views.create_album, name="album_create"),
                    path("<int:album_id>/", views.album_detail, name="album_detail"),
                    path("<int:album_id>/update/", views.update_album, name="album_update"),
                    path("<int:album_id>/upload/", views.upload_photos, name="album_upload"),
                    path(
                        "<int:album_id>/photos/",
                        include([
                            path("<int:photo_id>/cover/", views.set_cover_photo, name="photo_cover"),
                            path("<int:photo_id>/delete/", views.delete_photo, name="photo_delete"),
                            path("<int:photo_id>/display/", views.update_photo_display, name="photo_display"),
                            path("reorder/", views.reorder_photos, name="photo_reorder"),
                        ]),
                    ),
                ]),
            ),
        ]),
    ),
]
