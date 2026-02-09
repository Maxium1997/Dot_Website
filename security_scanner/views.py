import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

ZAP_API = "http://localhost:8090"


class StartScanAPIView(APIView):
    def post(self, request):
        url = request.data.get("url")

        if not url:
            return Response(
                {"error": "Target URL is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Step 1: Access URL (add to Scan Tree)
        requests.get(
            f"{ZAP_API}/JSON/core/action/accessUrl/",
            params={"url": url},
        )

        # Step 2: Start Active Scan
        resp = requests.get(
            f"{ZAP_API}/JSON/ascan/action/scan/",
            params={"url": url},
        )

        data = resp.json()

        if "scan" not in data:
            return Response(
                {"error": data},
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

