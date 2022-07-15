from kivy.config import Config
Config.set('graphics', 'resizable', False)
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
import datetime, json

Window.size = (350, 600)
index = 0

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
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        year = str(datetime.datetime.now().year)
        month = str(datetime.datetime.now().strftime("%b"))
        day = str(datetime.datetime.now().strftime("%d"))
        screen_manager.get_screen("main").date.text = f"{days[wd]}, {day} {month} {year}"
        try:
            self.load_index()
        except Exception as e:
            print(e)

    def on_complete(self, checkbox, value, description, bar, delete):
        if value:
            description.text = f"[s]{description.text}[/s]"
            bar.md_bg_color = 0, 179/255, 0, 1
            delete.text_color = 1, 170/255, 23/255, 1
        else:
            remove = ["[s]", "[/s]"]
            for i in remove:
                description.text = description.text.replace(i, "")
                bar.md_bg_color = 1, 170/255, 23/255, 1
            delete.text_color = 180/255, 180/255, 180/255, 1

    def time(self):
        time = datetime.datetime.now().strftime("%b %d, %I:%M %p")
        return time

    def add_todo(self, title, description):
        if title != "" and description != "" and len(title) < 21 and len(description) < 61:
            screen_manager.current = "main"
            screen_manager.transition.direction = "right"
            screen_manager.get_screen("main").todo_list.add_widget(TodoCard(title=title.title(), description=description))
            
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

    def remove_todo(self, todo, title):
        screen_manager.get_screen("main").todo_list.remove_widget(todo)

  

    def save_index(self):
        global index
        with open("data/index.txt", 'w') as file:
            line = file.writelines(str(index))
        index += 1

    def load_index(self):
        with open("data/index.txt", 'r') as file:
            line = file.readline()
            global index
            index = int(line) +1

    def save_todo(self, title, description):
        with open("data/title.txt", 'w') as file:
            file.write(title + "\n")
        with open("data/description.txt", 'w') as file:
            file.write(description + "\n")
        with open("data/time.txt", 'w') as file:
            file.write(self.time() + "\n")

if __name__ == "__main__":
    TasksistorApp().run()