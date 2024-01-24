from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from datetime import datetime
from kivy.core.text import LabelBase

class CustomColorButtonApp(App):
    def build(self):
        # フォントを登録
        LabelBase.register(name="CustomFont", fn_regular="MAINSYS/FONT/Mystic Soul.ttf")  # フォントの絶対パスを指定

        # ボタンを含むレイアウト
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # ボタンの作成
        self.time_button = Button(
            text=datetime.now().strftime("%H:%M:%S"),
            font_size=20,
            font_name="CustomFont",  # 登録したフォント名を指定
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(200, 100),
            pos=(100, 100),
            background_color=(0, 1, 0, 1)
        )

        # ボタンに対するイベントの設定
        self.time_button.bind(on_press=self.on_button_press)

        # レイアウトにボタンを追加
        layout.add_widget(self.time_button)

        # ラベルの作成
        self.label = Label(text='Button Pressed: ', font_size=20)

        # レイアウトにラベルを追加
        layout.add_widget(self.label)

        # 1秒ごとに更新する関数を設定
        Clock.schedule_interval(self.update_time, 1.0)

        return layout

    def on_button_press(self, instance):
        # ボタンが押されたときの処理
        self.label.text = 'Button Pressed: ' + datetime.now().strftime("%H:%M:%S")

    def update_time(self, dt):
        # 1秒ごとに呼び出される関数で、ボタンのテキストを更新
        self.time_button.text = datetime.now().strftime("%H:%M:%S")

if __name__ == '__main__':
    CustomColorButtonApp().run()
