from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.text import LabelBase
import time
import csv


class ClockApp(App):
    def build(self):
        # 
        fontname, fcolar1,fcolar2,fcolar3,fcolar4 = self.load_csv()
        fcolar1 = float(fcolar1)
        fcolar2 = float(fcolar2)
        fcolar3 = float(fcolar3)
        fcolar4 = float(fcolar4)
        
        self.font_path = fontname
        LabelBase.register(name=fontname, fn_regular=self.font_path)

        self.layout = BoxLayout(orientation='vertical')
        self.time_label = Label(
            text=self.get_japanese_time(),
            font_name=fontname,  # 初期フォントを指定
            font_size='40sp',
            halign='center',
            valign='middle',
            color=[fcolar1,fcolar2,fcolar3,fcolar4]  # 色を赤に指定
        )
        
        self.layout.add_widget(self.time_label)
        Clock.schedule_interval(self.update_time, 1)
        return self.layout

    def update_time(self, dt):
        self.time_label.text = self.get_japanese_time()

    def get_japanese_time(self):
        current_time = time.strftime("%H:%M:%S", time.localtime())
        return current_time
    
    def load_csv(self):
        # CSVファイルからボタンの座標を取得するメソッド

        filename = 'MAINSYS\CSV\settings.csv'
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            
            
            fcolar1 = data[0][0]
            fcolar2 = data[0][1]
            fcolar3 = data[0][2]
            fcolar4 = data[0][3]
            fname = data[1][0]
            


        return fname,fcolar1,fcolar2,fcolar3,fcolar4



# アプリ実行
if __name__ == '__main__':
    app = ClockApp()
    app.run()