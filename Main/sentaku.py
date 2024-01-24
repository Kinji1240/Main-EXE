from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.core.window import Window
import japanize_kivy
import csv
import os
import subprocess

class ImageSelectorApp(App):
    def build(self):
        # ウィンドウのサイズを設定
        Window.size = (600, 300)

        # レイアウトの作成
        layout = BoxLayout(orientation='horizontal', spacing=10)

        # 左側のボックスレイアウト
        left_layout = BoxLayout(orientation='vertical', spacing=10)

        # 右側のボックスレイアウト
        right_layout = BoxLayout(orientation='vertical', spacing=10)

        # 画像表示用のウィジェットの作成
        image1 = Image(source='fuukei.jpg')
        image2 = Image(source='haikeihafguruma.jpg')

        # 選択ボタンの作成
        button1 = Button(text='アナログ時計を選択', on_press=self.change_text_clock)
        
        button2 = Button(text='デジタル時計を選択', on_press=self.change_clock_text)
        button2.bind(on_press=self.digital_clock)

        # レイアウトにウィジェットを追加
        left_layout.add_widget(image1)
        left_layout.add_widget(button1)

        right_layout.add_widget(image2)
        right_layout.add_widget(button2)

        # メインのレイアウトに左右のレイアウトを追加
        layout.add_widget(left_layout)
        layout.add_widget(right_layout)

        return layout

    

    def change_text_clock(self, instance):
        
        print("アナログ時計を選択が押されました。")
        # ファイルの読み込みと書き込みはここで行います
        file_path = "onoD_opt.csv"
            
        # 既存のCSVファイルを読み込む
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            data = list(reader)
        # 必要な部分を変更
        data[9][1] = 1
        print(data[9][1])

        # 新しいCSVファイルに書き出す
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
        
        App.get_running_app().stop()
    

    def change_clock_text(self, instance):
        
        print("デジタル時計を選択が押されました。")
        # ファイルの読み込みと書き込みはここで行います
        #file_path = "MAINSYS\CSV\onoD_opt.csv"
            
        # 既存のCSVファイルを読み込む
        #with open(file_path, mode='r') as file:
        #    reader = csv.reader(file)
        #    data = list(reader)
            
        # 必要な部分を変更
        #data[9][1] = 2

        # 新しいCSVファイルに書き出す
        #with open(file_path, mode='w', newline='') as file:
        #    writer = csv.writer(file)
        #    writer.writerows(data)

        App.get_running_app().stop()

    def digital_clock (self, instance):
        # "haikeigazou.py" を実行
        subprocess.Popen(["python", "time_display_app.py"])
        App.get_running_app().stop()


if __name__ == '__main__':
    ImageSelectorApp().run()
