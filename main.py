from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('kivy','window_icon','assets/IMG/Logo.png')
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.behaviors.elevation import FakeRectangularElevationBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import StringProperty
from kivy.core.window import Window
from datetime import date
import datetime, csv

Window.size = (350, 600)

class TodoCard(FakeRectangularElevationBehavior, MDFloatLayout):
    title = StringProperty()
    description = StringProperty()
    time = StringProperty()

class TasksistorApp(MDApp):

    def build(self):
        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("assets/Kivy/Main.kv"))
        screen_manager.add_widget(Builder.load_file("assets/Kivy/AddTodo.kv"))
        return screen_manager

    def on_start(self):
        today = date.today()
        wd = date.weekday(today)
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        year = str(datetime.datetime.now().year)
        month = str(datetime.datetime.now().strftime("%b"))
        day = str(datetime.datetime.now().strftime("%d"))
        screen_manager.get_screen("main").date.text = f"{days[wd]}, {day} {month} {year}"
        try:
            self.load_todo()
        except:
            pass

    def on_complete(self, checkbox, value, description, bar):
        if value:
            description.text = f"[s]{description.text}[/s]"
            bar.md_bg_color = 0, 179/255, 0, 1
        else:
            remove = ["[s]", "[/s]"]
            for i in remove:
                description.text = description.text.replace(i, "")
                bar.md_bg_color = 1, 170/255, 23/255, 1

    def time(self):
        time = datetime.datetime.now().strftime("%b %d, %I:%M %p")
        return time

    def add_todo(self, title, description):
        if title != "" and description != "" and len(title) < 21 and len(description) < 61:
            screen_manager.current = "main"
            screen_manager.transition.direction = "right"
            screen_manager.get_screen("main").todo_list.add_widget(TodoCard(title=title.title(), description=description, time=self.time()))
            
            self.save_todo(title, description)

            screen_manager.get_screen("add_todo").description.text = ""
            screen_manager.get_screen("add_todo").title.text = ""
        elif title == "":
            Snackbar(text="Please provide a title!", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08, size_hint_x=(Window.width-(dp(10)*2))/Window.width, bg_color=(1,170/255,23/255,1), font_size="18sp").open()
        elif len(title) > 17:
            Snackbar(text="Title too long!", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08, size_hint_x=(Window.width-(dp(10)*2))/Window.width, bg_color=(1,170/255,23/255,1), font_size="18sp").open()
        elif description == "":
            Snackbar(text="No description found!", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08, size_hint_x=(Window.width-(dp(10)*2))/Window.width, bg_color=(1,170/255,23/255,1), font_size="18sp").open()
        elif len(description) > 55:
            Snackbar(text="Too Long description!", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08, size_hint_x=(Window.width-(dp(10)*2))/Window.width, bg_color=(1,170/255,23/255,1), font_size="18sp").open()

    def remove_all_todo(self):
        screen_manager.get_screen("main").todo_list.clear_widgets()
        f = open("data/data.csv", 'w+', newline='')
        f.close()

    def remove_todo(self, todo, title, description, time):
        title = title.text.title()
        description = description.text
        time = time.text
        row = f'{title},{description},"{time}"'
        try:
            dataOld = open("data/data.csv", "r")
            dataOld = ''.join([i for i in dataOld])
            with open('data/data.csv') as f:
                reader = csv.reader(f)
                data = list(reader)
                for rowCSV in data:
                    try:
                        line = f'{rowCSV[0].title()},{rowCSV[1]},"{rowCSV[2]}"'
                        if row == line:
                            dataOld = dataOld.replace(line, '')
                            f = open("data/data.csv", 'w+', newline='')
                            f.close()
                            f = open('data/data.csv', 'w')
                            f.write(dataOld)
                            f.close()
                            screen_manager.get_screen("main").todo_list.remove_widget(todo)
                            break
                        else:
                            pass
                    except:
                        pass
        except:
            Snackbar(text="Error! Try Clearing the Whole File.", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08, size_hint_x=(Window.width-(dp(10)*2))/Window.width, bg_color=(1,170/255,23/255,1), font_size="18sp").open()

    def save_todo(self, title, description):
        rows = [str(title.title()), str(description), self.time()]
        with open("data/data.csv", 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(rows)

    def load_todo(self):
        with open('data/data.csv') as f:
            reader = csv.reader(f)
            data = list(reader)
            for row in data:
                try:
                    title = row[0]
                    description = row[1]
                    time = row[2]
                    screen_manager.get_screen("main").todo_list.add_widget(TodoCard(title=title, description=description, time=time))
                except:
                    pass

if __name__ == "__main__":
    TasksistorApp().run()