from django.shortcuts import render
import requests
from django.http import JsonResponse

# Create your views here.

ZAP_API = "http://localhost:8090"


def start_scan(request):
    url = request.GET.get("url")

    resp = requests.get(
        f"{ZAP_API}/JSON/ascan/action/scan/",
        params={"url": url},
    )

    return JsonResponse({
        "message": "Scan started",
        "scan_id": resp.json()["scan"]
    })
