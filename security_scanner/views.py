import requests
from django.views.generic import TemplateView
from requests.exceptions import ConnectionError, Timeout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


ZAP_API = "http://localhost:8090"


class ScannerDashboardView(TemplateView):
    template_name = "security_scanner/dashboard.html"


class StartScanAPIView(APIView):
    def post(self, request):
        url = request.data.get("url")

        if not url:
            return Response(
                {"error": "Target URL is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Step 1: Access URL (add to Scan Tree)
            requests.get(
                f"{ZAP_API}/JSON/core/action/accessUrl/",
                params={"url": url},
                timeout=5,
            )

            # Step 2: Start Active Scan
            resp = requests.get(
                f"{ZAP_API}/JSON/ascan/action/scan/",
                params={"url": url},
                timeout=10,
            )

        except ConnectionError:
            return Response(
                {
                    "error": "ZAP service is not running.",
                    "hint": "Please run: docker-compose up -d"
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        except Timeout:
            return Response(
                {
                    "error": "ZAP request timed out.",
                    "hint": "ZAP may still be starting up. Try again in a few seconds."
                },
                status=status.HTTP_504_GATEWAY_TIMEOUT
            )

        # Parse response safely
        try:
            data = resp.json()
        except Exception:
            return Response(
                {
                    "error": "Invalid response from ZAP",
                    "raw": resp.text
                },
                status=status.HTTP_502_BAD_GATEWAY
            )

        if "scan" not in data:
            return Response(
                {
                    "error": "ZAP did not return a scan id",
                    "zap_response": data
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            "message": "Scan started successfully!",
            "target": url,
            "scan_id": data["scan"]
        })



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

