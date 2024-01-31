import csv
import os
import subprocess
from kivy.app import App
from syoki import App
import japanize_kivy


class GentenApp(App):
    def build(self):
        # CSVファイルに緯度・経度・日数を保存するメソッド
        filename = os.path.join(os.path.dirname(__file__),'onoD_opt.csv')
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            senidata = data[11][1]
        
        if senidata == '0':
            app_path = os.path.join(os.path.dirname(__file__),'syoki.py')
            print(app_path)
        elif senidata == '1':
            app_path = os.path.join(os.path.dirname(__file__),'main_facter.py')
        else:
            app_path = os.path.join(os.path.dirname(__file__),'error.py')
        
        self.stop()  # App.get_running_app() を self に変更
        subprocess.Popen(["python", app_path])
        print("main_facterへ遷移します")
if __name__ == '__main__':
    
    GentenApp().run()

    