from django.conf import settings

def get_booking_flex_message(booking):
    """產生預約成功的 Flex Message JSON 結構"""
    return {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "預約成功憑證",
                    "weight": "bold",
                    "color": "#FFFFFF",
                    "size": "lg"
                }
            ],
            "backgroundColor": "#27AE60"
        },
        "hero": {
            "type": "image",
            "url": "https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?auto=format&fit=crop&w=1000&q=80",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": f"{booking.court.gym.name}",
                    "weight": "bold",
                    "size": "xl"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                                {"type": "text", "text": "場地", "color": "#aaaaaa", "size": "sm", "flex": 1},
                                {"type": "text", "text": f"{booking.court.number} 號場", "wrap": True, "color": "#666666", "size": "sm", "flex": 4}
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                                {"type": "text", "text": "日期", "color": "#aaaaaa", "size": "sm", "flex": 1},
                                {"type": "text", "text": f"{booking.booking_date}", "wrap": True, "color": "#666666", "size": "sm", "flex": 4}
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                                {"type": "text", "text": "時間", "color": "#aaaaaa", "size": "sm", "flex": 1},
                                {"type": "text", "text": f"{booking.start_time.strftime('%H:%M')} - {booking.end_time.strftime('%H:%M')}", "wrap": True, "color": "#666666", "size": "sm", "flex": 4}
                            ]
                        }
                    ]
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "style": "secondary",
                    "action": {
                        "type": "uri",
                        "label": "查看我的預約",
                        "uri": f"{settings.LINE_BASE_URL}/badminton/my-bookings/"
                    }
                }
            ]
        }
    }