from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader

class MusicPlayerApp(App):
    def build(self):
        # 音楽ファイルの読み込み
        self.sound = SoundLoader.load(r'Main/六甲おろし.mp3')

        if not self.sound:
            print("音楽ファイルの読み込みに失敗しました。")
            return

        self.state = "play"

        # ウィジェットをレイアウトに追加
        self.layout = BoxLayout(orientation='horizontal')
        self.button_make()

        return self.layout

    def play_music(self, instance):
        if self.state == "play":
            self.state = "stop"
            self.sound.play()

        elif self.state == "stop":
            self.state = "play"
            self.sound.stop()
            self.sound.unbind(on_stop=self.play_music)
        self.button_make()

    def button_make(self):
        play_button = Button(text=f'{self.state}', on_press=self.play_music, size_hint=(1, 1))  # size_hintを変更
        self.layout.clear_widgets()
        self.layout.add_widget(play_button)

if __name__ == '__main__':
    MusicPlayerApp().run()
