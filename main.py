import kivy

kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.label import Label


class ServiceApp(App):
    def build(self):
        return Label(text='ServiceApp')


if __name__ == '__main__':
    ServiceApp().run()
