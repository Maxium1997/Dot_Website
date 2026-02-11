import requests
from django.views.generic import TemplateView
from requests.exceptions import ConnectionError, Timeout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import ScanTarget, ScanResult
from urllib.parse import urlparse


ZAP_API = "http://localhost:8090"


class ScannerDashboardView(TemplateView):
    template_name = "security_scanner/dashboard.html"


class StartScanAPIView(APIView):
    def post(self, request):
        url = request.data.get("url")

        if not url:
            return Response({"error": "Target URL is required"}, status=400)

        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"

        try:
            # 1) Reset session
            requests.get(f"{ZAP_API}/JSON/core/action/newSession/", timeout=10)

            # 2) Create DB target
            target = ScanTarget.objects.create(
                owner=None,
                name=base_url,
                url=base_url
            )

            # 3) Access URL (seed) → 不要太短 timeout
            requests.get(
                f"{ZAP_API}/JSON/core/action/accessUrl/",
                params={"url": base_url},
                timeout=30
            )

            # 4) Start Active Scan directly (不要 spider)
            active_resp = requests.get(
                f"{ZAP_API}/JSON/ascan/action/scan/",
                params={"url": base_url},
                timeout=30
            )

            active_data = active_resp.json()
            print("ZAP active scan response:", active_data)

            if "scan" not in active_data:
                return Response(
                    {"error": "Active scan failed", "zap_response": active_data},
                    status=400
                )

            scan_id = active_data["scan"]

            # 5) Save placeholder
            ScanResult.objects.create(target=target, scan_id=scan_id)

            return Response(
                {"message": "Scan started!", "scan_id": scan_id, "base_url": base_url},
                status=200
            )

        except Timeout:
            return Response(
                {
                    "error": "ZAP timed out starting scan",
                    "hint": "Try scanning a smaller site or increase timeout"
                },
                status=504
            )

        except ConnectionError:
            return Response({"error": "Cannot connect to ZAP"}, status=503)


class ScanProgressAPIView(APIView):
    def get(self, request, scan_id):
        resp = requests.get(
            f"{ZAP_API}/JSON/ascan/view/status/",
            params={"scanId": scan_id},
        )

        return Response({
            "scan_id": scan_id,
            "progress": int(resp.json()["status"])
        })


class ScanAlertsAPIView(APIView):
    def get(self, request):
        """
        Fetch vulnerability alerts from OWASP ZAP.
        """
        resp = requests.get(
            f"{ZAP_API}/JSON/core/view/alerts/"
        )

        data = resp.json()

        return Response({
            "alerts": data.get("alerts", [])
        })


class FinalizeScanAPIView(APIView):
    def post(self, request, scan_id):

        # 不用 get()
        result = (
            ScanResult.objects
            .filter(scan_id=scan_id)
            .order_by("-id")
            .first()
        )

        if not result:
            return Response(
                {"error": "ScanResult not found"},
                status=404
            )

        resp = requests.get(f"{ZAP_API}/JSON/core/view/alerts/")
        alerts = resp.json().get("alerts", [])

        high = len([a for a in alerts if a["risk"] == "High"])
        medium = len([a for a in alerts if a["risk"] == "Medium"])
        low = len([a for a in alerts if a["risk"] == "Low"])

        result.high = high
        result.medium = medium
        result.low = low
        result.report_json = alerts
        result.save()

        return Response({
            "message": "Scan saved successfully!",
            "high": high,
            "medium": medium,
            "low": low,
            "alerts": alerts
        })



