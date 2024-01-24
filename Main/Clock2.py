import kivy
import math
import pytz
import requests

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Line, Ellipse, InstructionGroup
from kivy.clock import Clock
from datetime import datetime

class AnalogClock(FloatLayout):
    def __init__(self, **kwargs):
        super(AnalogClock, self).__init__(**kwargs)

        # ウィジェットのサイズを10%縮小
        self.size_hint = (0.2, 0.2)

        Clock.schedule_interval(self.update, 60.0 / 60.0)

        # 文字盤の描画
        self.draw_clock_face()

    def update(self, dt):
        self.canvas.clear()
        now = self.get_current_time()

        # 文字盤の描画
        self.draw_clock_face()

        # 時針
        hour_angle = (now.hour % 12 + now.minute / 60.0) * 30
        hour_length = self.width * 0.3
        hour_x = self.center_x + hour_length * self.sin_deg(hour_angle)
        hour_y = self.center_y + hour_length * self.cos_deg(hour_angle)
        self.draw_hand(self.center_x, self.center_y, hour_x, hour_y, Color(1, 0, 0))  # 赤色

        # 分針
        minute_angle = now.minute * 6
        minute_length = self.width * 0.4
        minute_x = self.center_x + minute_length * self.sin_deg(minute_angle)
        minute_y = self.center_y + minute_length * self.cos_deg(minute_angle)
        self.draw_hand(self.center_x, self.center_y, minute_x, minute_y, Color(0, 1, 0))  # 緑色

        # 秒針
        second_angle = now.second * 6
        second_length = self.width * 0.45
        second_x = self.center_x + second_length * self.sin_deg(second_angle)
        second_y = self.center_y + second_length * self.cos_deg(second_angle)
        self.draw_hand(self.center_x, self.center_y, second_x, second_y, Color(0, 0, 1))  # 青色

    def draw_clock_face(self):
        clock_face = InstructionGroup()

        # 中心の円
        #clock_face.add(Color(0, 0, 1))  # 青色
        #clock_face.add(Ellipse(pos=(self.center_x - 10, self.center_y - 10), size=(20, 20)))

        # 文字盤の描画
        for hour in range(1, 13):
            angle = math.radians(-hour * 30 + 60)  # 12時から時計回りに30度ずつ
            text_x = self.center_x + self.width * 0.45 * math.sin(angle)
            text_y = self.center_y + self.width * 0.45 * math.cos(angle)

            # 青色で円を描く
            clock_face.add(Color(1, 1, 1))  # 青色
            clock_face.add(Ellipse(pos=(text_x - 5, text_y - 5), size=(5, 5)))

        self.canvas.add(clock_face)

    def get_current_time(self):
        api_url = 'http://worldtimeapi.org/api/timezone/Etc/UTC'
        
        try:
            response = requests.get(api_url)
            data = response.json()
            utc_time = datetime.strptime(data['utc_datetime'], '%Y-%m-%dT%H:%M:%S.%f%z')
            local_time = utc_time.astimezone(pytz.timezone('Asia/Tokyo'))
            return local_time
        except Exception as e:
            print(f'エラー: {e}')
            return datetime.now()

    def sin_deg(self, degrees):
        return math.sin(math.radians(degrees))

    def cos_deg(self, degrees):
        return math.cos(math.radians(degrees))

    def draw_hand(self, x1, y1, x2, y2, color):
        with self.canvas:
            color
            Line(points=[x1, y1, x2, y2], width=2)

class AnalogClockApp(App):
    def build(self):
        return AnalogClock(pos=(100, 100))  # 位置を直接指定

if __name__ == '__main__':
    AnalogClockApp().run()
