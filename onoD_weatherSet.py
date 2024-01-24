import pandas as pd
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window
from error import ErrorApp
import csv
import japanize_kivy
import os
import subprocess
from datetime import datetime

class WeatherApp(App):

    def build(self):
        layout = BoxLayout(orientation='vertical')
        coordinates_df = pd.read_csv('MAINSYS\CSV\IDOKEIDO-UTF8.csv')

        # coordinates_df（pd.read_csvで読み込んだデータフレーム）の列に 'latitude' と 'longitude' が存在するかを確認
        if 'latitude' in coordinates_df.columns and 'longitude' in coordinates_df.columns:
            self.selected_data = None 
            self.user_latitude = None # 緯度
            self.user_longitude = None # 経度
            self.selected_days = None # 選択した日数

            # プルダウンメニューで都道府県を選択する
            spinner_values = coordinates_df['都道府県'].tolist() 
            spinner = Spinner(text='都道府県を選択', values=spinner_values)

            # 選択した都道府県の緯度経度を変数に代入
            def on_spinner_change(spinner, text):
                self.selected_data = coordinates_df[coordinates_df['都道府県'] == text].iloc[0]
                self.user_latitude = self.selected_data['latitude']
                self.user_longitude = self.selected_data['longitude']

            spinner.bind(text=on_spinner_change)
            layout.add_widget(spinner)

            # 日数を選択する Spinner を追加
            days_spinner = Spinner(text='日数を選択', values=['1', '3'])
            days_spinner.bind(text=self.on_days_spinner_change) # on_days_spinner_changeは76行あたり
            layout.add_widget(days_spinner)

            self.errcon = 0
            def saveopt(idodata, keidodata, daydata):
                if idodata == None or keidodata == None or daydata == None :
                    if self.errcon == 0:
                        self.errcon += 1
                        print(self.errcon)
                        layout.add_widget(Label(text="エラー: 保存する地域を選択してください",color=(1,0,0,1)))
                        pass
                # CSVファイルに緯度・経度・日数を保存するメソッド
                else:
                    filename = 'MAINSYS\CSV\onoD_opt.csv'
                    with open(filename, 'r') as csvfile:
                        reader = csv.reader(csvfile)
                        data = list(reader)

                        data[5][1] = idodata
                        data[5][2] = keidodata
                        data[6][1] = daydata

                    # ここで CSV ファイルに書き込む
                    with open(filename, 'w', newline='') as csvfile:
                        csv_writer = csv.writer(csvfile)
                        csv_writer.writerows(data)

            def re_setting(instance):
                #subprocess.Popen(["python", "MAINSYS\PROGRAMS\settings.py"])
                App.get_running_app().stop()
                return

            update_button = Button(text="地域を保存", size_hint=(None, None))
            update_button.bind(on_press=lambda instance: saveopt(idodata=self.user_latitude, keidodata=self.user_longitude, daydata=self.selected_days))
            layout.add_widget(update_button)

            re_button = Button(text="戻る", size_hint=(None, None))
            re_button.bind(on_press=re_setting)
            layout.add_widget(re_button)

            return layout
        else:
            return Label(text="エラー: CSVファイルに 'latitude' と 'longitude' の列がありません。")
    
    def on_days_spinner_change(self, spinner, text):
        self.selected_days = int(text) # 選択した日数を数値としてselected_days変数に代入

if __name__ == '__main__':
    WeatherApp().run()
