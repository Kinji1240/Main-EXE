from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from googleapiclient.discovery import build
from google.auth import load_credentials_from_file
import csv
import datetime
import japanize_kivy

class CalendarApp(App):
    def get_fpass(self):
        filename = 'MAINSYS\CSV\settings.csv'
        
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            fpass = data[1][0]
            fcolor1 = data[0][0]
            fcolor2 = data[0][1]
            fcolor3 = data[0][2]
            fcolor4 = data[0][3]
        return fpass, fcolor1, fcolor2, fcolor3, fcolor4
    
    def build(self):
        fsize = "18"

        layout = BoxLayout(orientation='vertical')

        SCOPES = ['https://www.googleapis.com/auth/calendar']
        calendar_id = 'j5gr4sa@gmail.com'
        gapi_creds = load_credentials_from_file(
            'MAINSYS\JSON\j5g-p-403802-f6d11f806041.json',
            SCOPES
        )
        service = build('calendar', 'v3', credentials=gapi_creds[0])

        today = datetime.date.today()
        start_of_day = datetime.datetime(today.year, today.month, today.day, 0, 0, 0).isoformat() + 'Z'
        end_of_day = datetime.datetime(today.year, today.month, today.day, 23, 59, 59).isoformat() + 'Z'

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
    
if __name__ == '__main__':
    CalendarApp().run()
