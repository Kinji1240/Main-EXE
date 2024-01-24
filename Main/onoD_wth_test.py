import pandas as pd
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import requests
from datetime import datetime
from kivy.uix.image import Image
import csv
import japanize_kivy


class WeatherApp(App):
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
        filename = 'Main/settings.csv'
        
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            fpass = data[1][0]
            fcolor1 = data[0][0]
            fcolor2 = data[0][1]
            fcolor3 = data[0][2]
            fcolor4 = data[0][3]
        return fpass, fcolor1, fcolor2, fcolor3, fcolor4
    

    def format_date(self, date_str):
        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M")
        formatted_date = date_obj.strftime("%Y-%m-%d %H:%M")
        return formatted_date

    def build(self):
        
        fsize = "20"

        layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(0.7,0.7))
        coordinates_df = pd.read_csv('Main/IDOKEIDO-UTF8.csv')

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
                        formatted_date = self.format_date(date)
                        temperature = hourly_data["temperature_2m"][i]
                        max_temperature = daily_data["temperature_2m_max"][i]
                        min_temperature = daily_data["temperature_2m_min"][i]
                        weather_code = daily_data["weather_code"][i]
                        weather_meaning = self.get_weather_meaning(weather_code)

                        string_to_remove = "2024-01-"
                        formatted_date = formatted_date.replace(string_to_remove, "")
                        string_to_remove = "2024-02-"
                        formatted_date = formatted_date.replace(string_to_remove, "")
                        string_to_remove = "00:00"
                        formatted_date = formatted_date.replace(string_to_remove, "")
                        string_to_remove = "-"
                        formatted_date = formatted_date.replace(string_to_remove, "/")

                        # 横に並べて表示するために BoxLayout を使用
                        
                        if i == 0:
                            day = "今日"
                        elif i == 1:
                            day = "明日"
                        elif i == 2:
                            day = "明後日"
                        else: day = "" 

                        fpass, fcolor1, fcolor2, fcolor3, fcolor4 = self.get_fpass()

                        weather_label = Label(text=
                                            day+f" {formatted_date}日\n" 
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
        filename = 'Main/onoD_opt.csv'
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)

            idodata = data[5][1]
            keidodata = data[5][2]
            daydata = data[6][1]


        return idodata, keidodata, daydata
    

if __name__ == '__main__':
    WeatherApp().run()
