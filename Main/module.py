from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.image import Image
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.config import Config
from kivy.clock import Clock
from googleapiclient.discovery import build
from google.auth import load_credentials_from_file






import os
import csv
import time
import datetime 
import japanize_kivy
import subprocess
import requests
import pandas as pd




pixels_per_inch = 96
width_cm = 15
height_cm = 8
width_pixels = int(width_cm * pixels_per_inch / 2.54)
height_pixels = int(height_cm * pixels_per_inch / 2.54)
Window.size = (width_pixels, height_pixels)



################################↓↓↓syoki↓↓↓##############################################################



class SyokiScreen(Screen):
    def __init__(self, **kwargs):
        super(SyokiScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        title_label = Label(
            text="朝の目覚めにこのシステム",
            font_size=66,
            size_hint_y=None,
            height=500,
            halign="center",
        )

        subtitle_label = Label(
            text="Morning Pi",
            font_size=51,
            size_hint_y=None,
            height=100,
            halign="center",
        )

        layout.add_widget(Label())  # 上部の余白用
        layout.add_widget(title_label)
        layout.add_widget(subtitle_label)

        button = Button(text="実行", size_hint=(None, None), size=(150, 50))
        button.bind(on_press=self.show_confirmation_popup)

        center_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        center_layout.add_widget(Label())  # 左側の余白
        center_layout.add_widget(button)
        center_layout.add_widget(Label())  # 右側の余白
        layout.add_widget(center_layout)

        Window.bind(on_resize=self.on_window_resize)

        self.add_widget(layout)

    def on_window_resize(self, instance, width, height):
        self.set_background_color(self.background_color, width, height)

    def on_start(self):
        self.background_color = (0.5, 0.5, 0.5, 1)
        title_color = (1, 1, 1, 1)
        subtitle_color = (1, 1, 1, 1)
        self.set_background_color(self.background_color, Window.width, Window.height)
        self.set_text_color(title_color, subtitle_color)

    def set_background_color(self, color, width, height):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*color)
            Rectangle(pos=self.pos, size=(width, height))

    def set_text_color(self, title_color, subtitle_color):
        self.children[1].color = title_color
        self.children[2].color = title_color

    def show_confirmation_popup(self, instance):
        self.manager.current = 'background_screen'



################################↓↓↓haikei↓↓↓##############################################################


class BackgroundColorScreen(Screen):
    def __init__(self, **kwargs):
        super(BackgroundColorScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        label_background = Label(text="背景色変更")
        self.label_background = label_background

        self.background_color_picker = ColorPicker()
        self.background_color_picker.bind(color=self.on_background_color)

        label_text = Label(text="文字色変更")
        self.label_text = label_text

        self.text_color_picker = ColorPicker()
        self.text_color_picker.bind(color=self.on_text_color)

        button = Button(text="背景色を変更", on_press=self.change_background_and_text_color)

        layout.add_widget(label_background)
        layout.add_widget(self.background_color_picker)
        layout.add_widget(button)

        Window.bind(on_resize=self.on_window_resize)

        self.add_widget(layout)

    def on_window_resize(self, instance, width, height):
        font_size = int(0.04 * height)
        self.label_background.font_size = font_size
        self.label_text.font_size = font_size

    def on_background_color(self, instance, value):
        pass

    def on_text_color(self, instance, value):
        self.label_background.color = value
        self.label_text.color = value

    def change_background_and_text_color(self, instance):
        self.setflg(2)
        background_color = self.background_color_picker.color
        text_color = self.text_color_picker.color

        background_red, background_green, background_blue, background_alpha = background_color
        text_red, text_green, text_blue, text_alpha = text_color



        #self.save_colors_to_csv(csv_path, background_red, background_green, background_blue, background_alpha, text_red, text_green, text_blue, text_alpha)



        setflg_row = 10
        syokiflg_row = 11
        setflg = self.optflg(setflg_row)
        syokiflg = self.optflg(syokiflg_row)
        if syokiflg == '0' and setflg == '0':
            self.manager.current = 'posmover_screen'
        elif syokiflg == '1' and setflg == '1':
            pass
        else :
            subprocess.Popen(["python", "MAINSYS\PROGRAMS\error.py"])
            self.manager.current = 'syoki_screen'


    def save_colors_to_csv(self, csv_file, background_red, background_green, background_blue, background_alpha,
                           text_red, text_green, text_blue, text_alpha):
        with open(csv_file, 'w', newline='') as csvfile:
            fieldnames = ['BackgroundRed', 'BackgroundGreen', 'BackgroundBlue', 'BackgroundAlpha',
                          'TextRed', 'TextGreen', 'TextBlue', 'TextAlpha']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                'BackgroundRed': background_red,
                'BackgroundGreen': background_green,
                'BackgroundBlue': background_blue,
                'BackgroundAlpha': background_alpha,
                'TextRed': text_red,
                'TextGreen': text_green,
                'TextBlue': text_blue,
                'TextAlpha': text_alpha
            })

    def optflg(self, val):
        filename = os.path.join(os.path.dirname(__file__), "onoD_opt.csv")

        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            optdata = data[val][1]
        return optdata

    def setflg(self, flgval):
        filename = os.path.join(os.path.dirname(__file__), "onoD_opt.csv")
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            print(flgval)
            data[4][1] = flgval

        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(data)
        print("保存されました！")



################################↓↓↓posmover↓↓↓##############################################################


class PosMoverScreen(Screen):
    def __init__(self, **kwargs):
        super(PosMoverScreen, self).__init__(**kwargs)
        self.layout = FloatLayout()

        # ボタンリスト
        self.buttons = []  # ここで初期化
        self.background_color = [1, 1, 1, 1]  # デフォルトは白い背景

        bgopt = self.loadhaikei()

        print(bgopt)
        # 背景の色と画像のパスを取得
        background_color, background_image_path = self.get_background_settings(bgopt)
        
        # 背景の色を設定
        with self.layout.canvas.before:
            Color(*background_color)
            self.background_rect = Rectangle(pos=self.layout.pos, size=self.layout.size)

        # 背景画像を設定
        if background_image_path == None:
            with self.layout.canvas.before:
                self.load_background_image(background_image_path)
        
        # ボタンの名前と初期位置
        button_info = [
            {"name": "時計", "pos": (50, 100)},
            {"name": "天気", "pos": (100, 100)},
            {"name": "予定", "pos": (150, 100)},
            {"name": "追加", "pos": (200, 100)},
        ]

        for info in button_info:
            # ボタンを作成
            button = Button(text=info["name"])
            button.size_hint = (None, None)
            button.size = (100, 50)
            button.pos = info["pos"]

            # ボタンが移動したときのイベントを追加
            button.bind(on_touch_move=self.on_button_move)

            # ボタンの背景色と文字色を設定
            button.background_color = self.background_color
            button.color = [0, 0, 0, 1]  # デフォルトは黒い文字

            # ボタンをレイアウトに追加
            self.layout.add_widget(button)

            # ボタンをリストに追加
            self.buttons.append(button)  # ここで追加

        # 確定ボタンを作成
        confirm_button = Button(text="確定", size_hint=(None, None), size=(100, 50), pos=(self.layout.width - 100, 0))
        confirm_button.bind(on_press=self.on_confirm_button_press)
        self.layout.add_widget(confirm_button)


        self.add_widget(self.layout)


    def on_button_move(self, instance, touch):
        # ボタンがタッチされ、移動したときに呼ばれるメソッド
        if instance.collide_point(*touch.pos):
            instance.pos = (touch.x - instance.width / 2, touch.y - instance.height / 2)

    def on_stop(self):
        # アプリケーションが終了するときに呼ばれるメソッド
        self.save_button_positions()

    def get_background_settings(self,bgopt):
        # selected_backgrounds.csvから背景画像のパスを取得
        if bgopt == 1:
            background_image_path = self.get_background_image_path(os.path.join(os.path.dirname(__file__), "selected_backgrounds.csv"))
            return (1, 1, 1, 1), background_image_path
                
        else:
        # selected_backgrounds.csvがない場合はcolor_settings.csvから背景色を取得
            background_color = self.get_background_color(os.path.join(os.path.dirname(__file__), "onoD_opt.csv"))
            return background_color, None

    def get_background_image_path(self, csv_file):
        try:
            with open(csv_file, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) > 0:
                        background_image_path = row[0]
                        return background_image_path
        except FileNotFoundError:
            pass
        return None

    def get_background_color(self, csv_file):
        # color_settings.csvから背景色を取得
        try:
            with open(csv_file, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                data = list(reader)
                background1 = data[8][1]
                background2 = data[8][2]
                background3 = data[8][3]
                background4 = data[8][4]

                background_color = (float(background1), float(background2), float(background3), float(background4))
        except (FileNotFoundError, ValueError, IndexError):
            # ファイルが存在しない、不正な値、またはインデックスエラーが発生した場合はデフォルト値を返す
            background_color = (1, 1, 1, 1)
        return background_color

    def save_button_positions(self):
        # 各ボタンの座標をCSVファイルに保存するメソッド
        filename = os.path.join(os.path.dirname(__file__), "onoD_opt.csv")
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            i=1
            for button in self.buttons:
                button_pos = button.pos
                data[16 +i][1] = button_pos[0]
                data[16 +i][2] = button_pos[1]
                i+=1

        
        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(data)

    def on_confirm_button_press(self, instance):
        # 確定ボタンが押下されたときの処理
        syokiflg,setflg = self.optflg()
        if syokiflg == '0' and setflg == '0':
            self.save_button_positions()
            self.manager.current = 'maindisplay_screen'
        elif syokiflg == '1' and setflg == '1':
            pass
        else :
            subprocess.Popen(["python", "MAINSYS\PROGRAMS\error.py"])


    def load_background_image(self, background_image_path):
        # 背景画像を設定
        if background_image_path:
            with self.layout.canvas.before:
                self.background_image = Rectangle(pos=self.layout.pos, size=self.layout.size, source=background_image_path)

    def on_size(self, instance, value):
        print("on_sizeメソッドが呼ばれました。")
        # ウィンドウサイズが変更されたときに呼び出される関数
        self.update_background_size()


    def update_background_size(self):
        # 背景のサイズをウィンドウのサイズに合わせる
        self.background_rect.size = self.layout.size
    
    def loadhaikei(self):
        filename = os.path.join(os.path.dirname(__file__), "onoD_opt.csv")
        
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            optdata = data[4][1]

        return optdata
    
    def optflg(self):
        filename = os.path.join(os.path.dirname(__file__), "onoD_opt.csv")
        
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            syokiopt = data[11][1]
            setopt = data[10][1]
            

        return syokiopt, setopt



################################↓↓↓mainfacter↓↓↓##############################################################





# 天気情報：WeatherApp
# 予定情報：CalendarApp
# 時計：ClockApp

## インチあたりのピクセル数
pixels_per_inch = 96

# 縦8cm、横15cmのサイズをピクセルに変換
width_cm = 15
height_cm = 8
width_pixels = int(width_cm * pixels_per_inch / 2.54)
height_pixels = int(height_cm * pixels_per_inch / 2.54)

# ウィンドウサイズの指定
Window.size = (width_pixels, height_pixels)

class MainDisplayScreen(Screen):
    def __init__(self, **kwargs):
        super(MainDisplayScreen, self).__init__(**kwargs)
        
        # レイアウトのインスタンスを作成
        self.layout = FloatLayout()
        
        self.background_color = [0, 0, 0, 0]  # デフォルトは黒い背景

        bgopt = self.loadhaikei()
        #self.setflg(1)
        print("bgopt:", bgopt)
        if bgopt == "2":
            #背景色
            background_color = self.get_background_color(os.path.join(os.path.dirname(__file__), "onoD_opt.csv"))
            background_image_path = None
        else:
            # 背景の色と画像のパスを取得
            background_color, background_image_path = self.get_background_settings()
        
        print("background_color:", background_color)
        print("background_image_path:", background_image_path)
        
        
        # 背景の色を設定
        with self.layout.canvas.before:
            Color(*background_color)
            self.background_rect = Rectangle(pos=self.layout.pos, size=self.layout.size)

        # 背景画像を設定
        if background_image_path:
            with self.layout.canvas.before:
                self.load_background_image(background_image_path)
        
        # ウィンドウのサイズ変更時に呼び出す関数を設定
        self.layout.bind(size=self.update_background_size)

        # calenderApp と WeatherApp のインスタンスを作成
        weather_app = WeatherScreen()
        calender_app = CalendarScreen()
        clock_app = DigitalClockScreen()
        #analog_app = MyClockApp()
        #audio_app = MusicPlayerApp()

        # 各アプリのレイアウトを作成
        weather_layout = weather_app.build()
        calendar_layout = calender_app.build()
        #audio_layout = audio_app.build()
        
        clock_judgement = self.loadclockselect()
        print("clock_judgement", clock_judgement)
        if clock_judgement == "2":
            print("デジタル時計を使用します")
            clock_layout = clock_app.build()
            # 時間アプリの座標を読み込みif分追加
            posrow = 17
            x, y = self.load_button_position(posrow)
            clock_layout.pos = (x, y)
        else:
            print("アナログ時計を使用します")
            #clock_layout = analog_app.build()

            posrow = 17
            x, y = self.load_button_position(posrow)
            #clock_layout.pos = (x + 210, y + 115)



        # 天気アプリの座標を読み込み
        posrow = 18
        x, y = self.load_button_position(posrow)
        weather_layout.pos = (x, y)

        # 予定アプリの座標を読み込み
        posrow = 19
        x, y = self.load_button_position(posrow)
        calendar_layout.pos = (x, y)

        # 追加アプリの座標を読み込み
        posrow = 20
        x, y = self.load_button_position(posrow)
        #audio_layout.pos = (x, y)
        #audio_layout.size_hint=(0.15,0.15)

        # 設定ボタンの生成
        button_image_path = os.path.join(os.path.dirname(__file__), '1.png')
        button = Image(source=button_image_path, size_hint=(0.1, 0.15), pos_hint={'top': 1})
        button.bind(on_touch_down=self.on_settings_button_press)

        self.add_widget(self.layout)
        self.layout.add_widget(button)
        weatherumu, calenderumu, clockumu, audioum = self.loadumu()
        if weatherumu == "on":
            self.layout.add_widget(weather_layout)
        if calenderumu == "on":
            self.layout.add_widget(calendar_layout)
        if clockumu == "on":
            self.layout.add_widget(clock_layout)
        #if audioum == "on":
            #self.layout.add_widget(audio_layout)

        


    def on_settings_button_press(self, instance, touch):
        if instance.collide_point(*touch.pos):
            subprocess.Popen(["python", "MAINSYS\PROGRAMS\settings.py"])
            App.get_running_app().stop()

    def get_background_settings(self):
         # selected_backgrounds.csvがない場合はcolor_settings.csvから背景色を取得
        background_image_path = self.get_background_image_path(os.path.join(os.path.dirname(__file__), "selected_backgrounds.csv"))
        
        return (1, 1, 1, 1), background_image_path

    def get_background_image_path(self, csv_file):
        try:
            with open(csv_file, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) > 0:
                        background_image_path = row[0]
                        return background_image_path
        except FileNotFoundError:
            pass
        return None

    def get_background_color(self, csv_file):
        # color_settings.csvから背景色を取得
        try:
            with open(csv_file, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                data = list(reader)
                background1 = data[8][1]
                background2 = data[8][2]
                background3 = data[8][3]
                background4 = data[8][4]

                background_color = (float(background1), float(background2), float(background3), float(background4))
        except (FileNotFoundError, ValueError, IndexError):
            # ファイルが存在しない、不正な値、またはインデックスエラーが発生した場合はデフォルト値を返す
            background_color = (1, 1, 1, 1)
        return background_color
    
    def load_background_image(self, background_image_path):
        # 背景画像を設定
        if background_image_path:
            with self.layout.canvas.before:
                self.background_image = Rectangle(pos=self.layout.pos, size=self.layout.size, source=background_image_path)

    def update_background_size(self, instance, value):
        print("on_sizeメソッドが呼ばれました。")
        # 背景のサイズをウィンドウのサイズに合わせる
        self.background_rect.size = self.layout.size

        # 背景画像のサイズも更新
        if hasattr(self, 'background_image'):
            self.background_image.size = self.layout.size
    
    # CSVファイルからアプリの座標を取得するメソッド
    def load_button_position(self, row):
        filename = os.path.join(os.path.dirname(__file__), "onoD_opt.csv")
        
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            button_pos_x = data[row][1]
            button_pos_x = button_pos_x
            print("Before conversion:", repr(button_pos_x))

            button_pos_x = float(button_pos_x) - 223.0

            button_pos_y = data[row][2]
            button_pos_y = float(button_pos_y)
            button_pos_y = button_pos_y - 132.0

        return button_pos_x, button_pos_y
    
    def loadhaikei(self):
        filename = os.path.join(os.path.dirname(__file__), 'onoD_opt.csv')
        
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            optdata = data[4][1]

        return optdata
    
    def loadumu(self):
        filename = os.path.join(os.path.dirname(__file__), 'onoD_opt.csv')
        
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            optdata1 = data[12][1]
            optdata2 = data[12][2]
            optdata3 = data[12][3]
            optdata4 = data[12][4]

        return optdata1,optdata2,optdata3,optdata4
    
    def loadclockselect(self):
        filename = os.path.join(os.path.dirname(__file__), 'onoD_opt.csv')
        
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            optdata = data[9][1]

        return optdata
    
    def setflg2(self,flgval):   # CSVファイルに設定用フラグを保存するメソッド
        filename = os.path.join(os.path.dirname(__file__), 'onoD_opt.csv')
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            print(flgval)
            data[11][1] = flgval
        
        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(data)
        print("保存されました！")

        return 



################################↓↓↓onoD_weather↓↓↓##############################################################



class WeatherScreen(Screen):
    def get_weather_meaning(self, weather_code):
        if 0 <= weather_code <= 3:
            return "晴れ"
        elif 4 <= weather_code <= 9:
            return "霞、ほこり、砂または煙"
        elif 20 <= weather_code <= 29:
            return "降水、霧、氷霧、または雷雨"
        elif 30 <= weather_code <= 35:
            return "塵嵐、砂嵐"
        elif 36 <= weather_code <= 39:
            return "吹雪または吹雪"
        elif 40 <= weather_code <= 49:
            return "霧または氷"
        elif 50 <= weather_code <= 59:
            return "霧または氷"
        elif 60 <= weather_code <= 69:
            return "霧雨"
        elif 70 <= weather_code <= 79:
            return "雨"
        elif 80 <= weather_code <= 89:
            return "にわか降水"
        elif 90 <= weather_code <= 99:
            return "降雪またはしんしゃく"
        elif 100 <= weather_code <= 199:
            return "あられ"
        else:
            return "不明な天気"
        
    def get_fpass(self):
        filename = os.path.join(os.path.dirname(__file__), 'onoD_opt.csv')
        
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)

            fcolor1 = data[23][1]
            fcolor2 = data[23][2]
            fcolor3 = data[23][3]
            fcolor4 = data[23][4]

            fpass = data[24][1]
        return fpass, fcolor1, fcolor2, fcolor3, fcolor4


    def format_date(self, date_str):
        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M")
        formatted_date = date_obj.strftime("%Y-%m-%d %H:%M")
        return formatted_date

    def build(self):

        fsize = "20"

        layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(0.7,0.7))
        coordinates_df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'IDOKEIDO-UTF8.csv'))

        if 'latitude' in coordinates_df.columns and 'longitude' in coordinates_df.columns:
            self.selected_data = None


            def update_weather(dt):
                # horizontal_layout のウィジェットをクリア
                
                url = "https://api.open-meteo.com/v1/forecast"

                if self.selected_data is None:
                    user_latitude, user_longitude, selected_days = self.loadopt()

                    params = {
                        "latitude": user_latitude,
                        "longitude": user_longitude,
                        "hourly": "temperature_2m",
                        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min"],
                        "timezone": "Asia/Tokyo"
                    }

                    response = requests.get(url, params=params)

                    data = response.json()
                    hourly_data = data["hourly"]
                    daily_data = data["daily"]

                    # 日数に応じて表示するデータの範囲を調整
                    if selected_days == "1":
                        range_end = 1
                    elif selected_days == "3":
                        range_end = 3
                    else:
                        range_end = 1  # デフォルトは1日

                    for i in range(range_end):
                        date = hourly_data["time"][i*24]
                        #formatted_date = self.format_date(date)
                        temperature = hourly_data["temperature_2m"][i]
                        max_temperature = daily_data["temperature_2m_max"][i]
                        min_temperature = daily_data["temperature_2m_min"][i]
                        weather_code = daily_data["weather_code"][i]
                        weather_meaning = self.get_weather_meaning(weather_code)

                        string_to_remove = "2024-01-"
                        #formatted_date = formatted_date.replace(string_to_remove, "")
                        string_to_remove = "2024-02-"
                        #formatted_date = formatted_date.replace(string_to_remove, "")
                        string_to_remove = "00:00"
                        #formatted_date = formatted_date.replace(string_to_remove, "")
                        string_to_remove = "-"
                        #formatted_date = formatted_date.replace(string_to_remove, "/")

                        # 横に並べて表示するために BoxLayout を使用
                        
                        if i == 0:
                            day = "今日\n"
                        elif i == 1:
                            day = "明日\n"
                        elif i == 2:
                            day = "明後日\n"
                        else: day = "" 

                        fpass, fcolor1, fcolor2, fcolor3, fcolor4 = self.get_fpass()

                        weather_label = Label(text=
                                            day      #+f" {formatted_date}日\n" 
                                           +f"\nNow:{temperature} ℃\n"
                                           +f"{max_temperature}℃/{min_temperature}℃\n"
                                           +f"天気: {weather_meaning}\n"
                                           ,font_size=fsize+'sp'
                                           ,font_name=fpass
                                           ,color=[float(fcolor1), float(fcolor2), float(fcolor3), float(fcolor4)])
                        
                        


                        # box に各情報を追加
                        layout.add_widget(weather_label)

                        

                        

                else:
                    layout.add_widget(Label(text=f"エラー: {response.status_code}"))

            update_weather(dt = 10)
            Clock.schedule_interval(update_weather, 1800)

            return layout
        else:
            return Label(text="エラー: CSVファイルに 'latitude' と 'longitude' の列がありません。")

    def loadopt(self):
        # CSVファイルに緯度・経度・日数を保存するメソッド
        filename = os.path.join(os.path.dirname(__file__), 'onoD_opt.csv')
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)

            idodata = data[5][1]
            keidodata = data[5][2]
            daydata = data[6][1]


        return idodata, keidodata, daydata



################################↓↓↓onoD_calendar↓↓↓##############################################################



class CalendarScreen(Screen):
    def get_fpass(self):
        filename = os.path.join(os.path.dirname(__file__),'onoD_opt.csv')
        
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            fpass = data[24][1]

            fcolor1 = data[23][1]
            fcolor2 = data[23][2]
            fcolor3 = data[23][3]
            fcolor4 = data[23][4]
        return fpass, fcolor1, fcolor2, fcolor3, fcolor4
    
    def build(self):
        fsize = "18"

        layout = BoxLayout(orientation='vertical')

        SCOPES = ['https://www.googleapis.com/auth/calendar']
        calendar_id = 'j5gr4sa@gmail.com'
        gapi_creds = load_credentials_from_file(
            os.path.join(os.path.dirname(__file__),'j5g-p-403802-f6d11f806041.json'),
            SCOPES
        )
        service = build('calendar', 'v3', credentials=gapi_creds[0])

        day = datetime.date.today()
        start_of_day = datetime.datetime(day.year, day.month, day.day, 0, 0, 0).isoformat() + 'Z'
        end_of_day = datetime.datetime(day.year, day.month, day.day, 23, 59, 59).isoformat() + 'Z'

        event_list = service.events().list(
            calendarId=calendar_id, timeMin=start_of_day, timeMax=end_of_day,
            maxResults=10, singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = event_list.get('items', [])
        schedule = "[今日の予定]\n"

        for event in events:
            start_time = event['start'].get('dateTime', event['start'].get('date'))
            end_time = event['end'].get('dateTime', event['end'].get('date'))
            summary = event['summary']

            if 'date' in start_time:
                schedule += f'{start_time}: {summary} (終日)\n'
            else:
                schedule += f'{start_time} ～ {end_time}: {summary}\n'

        string_to_remove = "2023-"
        schedule = schedule.replace(string_to_remove, "")
        string_to_remove = ":00+09:00"
        schedule = schedule.replace(string_to_remove, " ")
        string_to_remove = "-"
        schedule = schedule.replace(string_to_remove, "/")
        string_to_remove = "T"
        schedule = schedule.replace(string_to_remove, " ")

        fpass, fcolor1, fcolor2, fcolor3, fcolor4 = self.get_fpass()

        # フォントを変更
        schedule_label = Label(text=schedule,
                               font_size=fsize + 'sp', 
                               font_name=fpass,
                               color=[float(fcolor1), float(fcolor2), float(fcolor3), float(fcolor4)])  # color を使用
        layout.add_widget(schedule_label)

        return layout



################################↓↓↓onoD_clock↓↓↓##############################################################



class DigitalClockScreen(Screen):
    def build(self):
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
        # CSVファイルからフォントの色とフォント情報を取得するメソッド

        filename = os.path.join(os.path.dirname(__file__),'onoD_opt.csv')
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            
            fpass = data[24][1]
            fcolor1 = data[23][1]
            fcolor2 = data[23][2]
            fcolor3 = data[23][3]
            fcolor4 = data[23][4]
            

        return fpass,fcolor1,fcolor2,fcolor3,fcolor4
    







################################↓↓↓app↓↓↓##############################################################
    


class MainApp(App):
    def build(self):
        screen_manager = ScreenManager()

        syoki_screen = SyokiScreen(name='syoki_screen')
        background_screen = BackgroundColorScreen(name='background_screen')
        posmover_screen = PosMoverScreen(name='posmover_screen')
        maindisplay_screen = MainDisplayScreen(name='maindisplay_screen')

        screen_manager.add_widget(syoki_screen)
        screen_manager.add_widget(background_screen)
        screen_manager.add_widget(posmover_screen)
        screen_manager.add_widget(maindisplay_screen)

        return screen_manager


if __name__ == "__main__":
    MainApp().run()
