from rest_framework.views import APIView
from rest_framework.response import Response


class StartScanAPIView(APIView):
    def post(self, request):
        url = request.data.get("url")

        return Response({
            "message": "Scan request received!",
            "target": url,
            "scan_id": 0
        })
