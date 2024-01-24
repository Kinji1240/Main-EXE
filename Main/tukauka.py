from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.label import Label
import japanize_kivy
import csv

class AppSelectorApp(App):
    def build(self):
        # ウィンドウのサイズを設定
        Window.size = (800, 300)

        # レイアウトの作成
        self.layout = BoxLayout(orientation='horizontal', spacing=10)

        # 左側のボックスレイアウト
        self.left_layout = BoxLayout(orientation='vertical', spacing=10)

        # 中央のボックスレイアウト
        self.center_layout = BoxLayout(orientation='vertical', spacing=10)

        # 右側のボックスレイアウト
        self.right_layout = BoxLayout(orientation='vertical', spacing=10)

        self.four_layout = BoxLayout(orientation='vertical', spacing=10)

        # 画像表示用のウィジェットの作成
        self.title_label = Label(text="使用するアプリを選択")
        rebutton = Button(text='完了', size_hint=(None, None), size=(50, 50), on_press=self.rebutton)

        self.loadumu()
        self.button_make()

        # レイアウトにウィジェットを追加
        self.layout.add_widget(rebutton)
        self.layout.add_widget(self.title_label)
        self.layout.add_widget(self.left_layout)
        self.layout.add_widget(self.center_layout)
        self.layout.add_widget(self.right_layout)
        #self.layout.add_widget(self.four_layout)

        return self.layout
    
    def loadumu(self):
        filename = 'Main/onoD_opt.csv'
        
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            self.clock_states = data[12][1]
            self.weather_states = data[12][2]
            self.schedule_states = data[12][3]
            self.add_states = data[12][4]

    def change_text_clock(self, instance):

        if self.clock_states == "off":
            self.clock_states = "on"
        elif self.clock_states == "on":
            self.clock_states = "off"
        else:
            self.clock_states = "on"
        self.button_make()
        
    def change_clock_text(self, instance):

        if self.weather_states == "off":
            self.weather_states = "on"
        elif self.weather_states == "on":
            self.weather_states = "off"
        else:
            self.weather_states = "on"
        self.button_make()

    def another_button_action(self, instance):

        if self.schedule_states == "off":
            self.schedule_states = "on"
        elif self.schedule_states == "on":
            self.schedule_states = "off"
        else:
            self.schedule_states = "on"
        self.button_make()
    
    def four_button_action(self, instance):

        if self.add_states == "off":
            self.add_states = "on"
        elif self.add_states == "on":
            self.add_states = "off"
        else:
            self.add_states = "on"
        self.button_make()

    def rebutton(self, instance):
        print("完了ボタンが押されました。")
        file_path = "Main/onoD_opt.csv"
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            data = list(reader)
            data[12][1] = self.clock_states
            data[12][2] = self.weather_states
            data[12][3] = self.schedule_states
            data[12][4] = self.add_states

        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
        
        App.get_running_app().stop()
    
    def button_make(self):
        new_button1 = Button(text=f'時計:{self.clock_states}', on_press=self.change_text_clock)
        new_button2 = Button(text=f'天気:{self.weather_states}', on_press=self.change_clock_text)
        new_button3 = Button(text=f'予定:{self.schedule_states}', on_press=self.another_button_action)
        new_button4 = Button(text=f'追加:{self.add_states}', on_press=self.four_button_action)

        self.left_layout.clear_widgets()
        self.center_layout.clear_widgets()
        self.right_layout.clear_widgets()
        self.four_layout.clear_widgets()

        self.left_layout.add_widget(new_button1)
        self.center_layout.add_widget(new_button2)
        self.right_layout.add_widget(new_button3)
        #self.four_layout.add_widget(new_button4)

if __name__ == '__main__':
    AppSelectorApp().run()
