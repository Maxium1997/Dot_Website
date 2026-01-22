import requests
import qrcode
import base64
from PIL import Image

from io import BytesIO
from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic import TemplateView
from isodate import parse_duration

# Create your views here.


class PlaygroundView(TemplateView):
    template_name = 'playground/index.html'


class KaraokeView(TemplateView):
    template_name = 'playground/karaoke/index.html'


def search_index(request):
    videos = []
    search_query = ""

    if request.method == 'POST':
        search_query = request.POST.get('search', '').strip()

        if search_query:
            search_url = 'https://www.googleapis.com/youtube/v3/search'
            video_url = 'https://www.googleapis.com/youtube/v3/videos'

            # 第一步：搜尋影片 ID
            search_params = {
                'part': 'snippet',
                'q': f'karaoke lyrics {search_query}',
                'key': settings.YOUTUBE_DATA_API_KEY,
                'maxResults': 9,
                'type': 'video',
                'videoEmbeddable': 'true',  # 確保影片是可以內嵌播放的
            }

            try:
                r = requests.get(search_url, params=search_params)
                r.raise_for_status()
                search_results = r.json().get('items', [])
                video_ids = [item['id']['videoId'] for item in search_results]

                if video_ids:
                    # 第二步：取得影片詳細資訊（長度、高清圖）
                    video_params = {
                        'key': settings.YOUTUBE_DATA_API_KEY,
                        'part': 'snippet,contentDetails',
                        'id': ','.join(video_ids),
                    }
                    rv = requests.get(video_url, params=video_params)
                    rv.raise_for_status()
                    video_results = rv.json().get('items', [])

                    for result in video_results:
                        # 格式化時間 (例如: 4:05)
                        duration_td = parse_duration(result['contentDetails']['duration'])
                        total_seconds = int(duration_td.total_seconds())
                        minutes, seconds = divmod(total_seconds, 60)

                        videos.append({
                            'title': result['snippet']['title'],
                            'id': result['id'],
                            'url': f"https://www.youtube.com/watch?v={result['id']}",
                            'duration': f"{minutes}:{seconds:02d}",
                            'thumbnail': result['snippet']['thumbnails']['high']['url'],
                            'channel': result['snippet']['channelTitle']
                        })
            except Exception as e:
                # 可以在這裡加入錯誤訊息傳給前端，例如 API Key 額度用完
                print(f"YouTube API Error: {e}")

    context = {
        'videos': videos,
        'search_query': search_query
    }
    return render(request, 'playground/karaoke/search/index.html', context)


class URLtoQRcodeView(TemplateView):
    template_name = 'playground/qr_code/index.html'

    def post(self, request, *args, **kwargs):
        url_text = request.POST.get('url_text', '').strip()
        logo_file = request.FILES.get('logo_image')  # 取得上傳的圖片
        qr_image_base64 = None

        if url_text:
            # 1. 產生 QR Code (使用高等級糾錯 ERROR_CORRECT_H)
            # 因為中央會被 Logo 遮住，必須提高糾錯率以免無法掃描
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(url_text)
            qr.make(fit=True)

            # 將 QR Code 轉為 RGBA 模式以便處理透明度或合成
            qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGBA')

            # 2. 如果使用者有上傳 Logo
            if logo_file:
                icon = Image.open(logo_file).convert('RGBA')

                # 計算 Logo 大小 (建議不要超過 QR Code 的 1/4)
                qr_width, qr_height = qr_img.size
                logo_max_size = qr_width // 4

                # 等比例縮放 Logo
                icon.thumbnail((logo_max_size, logo_max_size), Image.Resampling.LANCZOS)

                # 計算置中座標
                icon_w, icon_h = icon.size
                offset_x = (qr_width - icon_w) // 2
                offset_y = (qr_height - icon_h) // 2

                # 將 Logo 貼到 QR Code 上
                # 使用 icon 自身作為遮罩以保留透明背景
                qr_img.paste(icon, (offset_x, offset_y), icon)

            # 3. 轉為 Base64
            buffer = BytesIO()
            qr_img.save(buffer, format="PNG")
            qr_image_base64 = base64.b64encode(buffer.getvalue()).decode()

        return render(request, self.template_name, {
            'qr_image': qr_image_base64,
            'url_text': url_text
        })
