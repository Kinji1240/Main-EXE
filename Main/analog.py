from kivy.app import App
from Clock2 import AnalogClock  # Clock2.pyからAnalogClockクラスをインポート


class MyClockApp(App):
    def build(self):
        return AnalogClock()

if __name__ == '__main__':
    MyClockApp().run()
