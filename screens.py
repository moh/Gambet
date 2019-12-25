from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.uix.scrollview import ScrollView
from kivy.effects.scroll import ScrollEffect


class Screens_popup(Popup):
    def __init__(self, screen_attach, **kwargs):
        super(Screens_popup, self).__init__(**kwargs)
        self.parent_screen = screen_attach
        self.attach_to = screen_attach
        self.auto_dismiss = False
        self.size_hint = (None, None)
        self.size = [screen_attach.width, screen_attach.height // 2]
        self.usual_size = [screen_attach.width, screen_attach.height // 2]
        # screen_attach.bind(size=self.upd_size)
        self.title, self.kwargs = "", ""

    def upd_size(self, obj, size):
        self.size = [size[0], size[1] // 2]

    def win_screen(self, **kwargs):
        win_sound = SoundLoader.load("sound//win_sound.ogg")
        self.dismiss()
        self.size_hint = (None, None)
        self.size = self.usual_size
        win_sound.play()
        self.title = "Congratulation"
        self.kwargs = kwargs
        content = BoxLayout(orientation="vertical")
        label = Label(text="YOU WIN")
        label.bind(height=label.setter("font_size"))
        content.add_widget(label)
        content.add_widget(Button(text="Win again",
                                  on_press=self.butt_press, size_hint=(.5, .7),
                                  pos_hint={'center_x': .5, "center_y": .5}))
        self.content = content
        self.open()

    def single_mode_a_screen(self, **kwargs):
        win_sound = SoundLoader.load("sound//win_sound.ogg")
        self.size_hint = (None, None)
        self.size = self.usual_size
        self.dismiss()
        win_sound.play()
        self.title = "Congratulation"
        self.kwargs = kwargs
        content = BoxLayout(orientation="vertical")
        label = Label(text="Try to beat Gambet NOW !")
        label.font_size = 2 * self.width / len(label.text)
        content.add_widget(label)
        button_area = BoxLayout(orientation="horizontal")
        button_area.add_widget(Button(text="Beat Gambet",
                                  on_press=self.butt_press, size_hint=(1, .7)
                                  ))
        button_area.add_widget(Button(text="Try again",
                                  on_press=self.butt_press, size_hint=(1,.7)
                                  ))
        content.add_widget(button_area)
        self.content = content
        self.open()

    def single_mode_b_screen(self, **kwargs):
        win_sound = SoundLoader.load("sound//win_sound.ogg")
        self.size_hint = (None, None)
        self.size = self.usual_size
        self.dismiss()
        win_sound.play()
        self.title = "GOOD"
        self.kwargs = kwargs
        content = BoxLayout(orientation="vertical")
        label = Label(text="That wasn't bad, practice more !")
        label.font_size = 2 * self.width / len(label.text)
        content.add_widget(label)
        content.add_widget(Button(text="Try again",
                                  on_press=self.butt_press, size_hint=(.5, .7),
                                  pos_hint={'center_x': .5, "center_y": .5}
                                  ))
        self.content = content
        self.open()

    def lose_screen(self, **kwargs):
        lose_sound = SoundLoader.load("sound//lose.ogg")
        self.size_hint = (None, None)
        self.size = self.usual_size
        self.dismiss()
        lose_sound.play()
        self.title = "Oops"
        self.kwargs = kwargs
        content = BoxLayout(orientation="vertical")
        label = Label(text="YOU LOST")
        label.bind(height=label.setter("font_size"))
        content.add_widget(label)
        button_widget = BoxLayout(orientation="horizontal", size_hint=[1, .7])
        button_widget.add_widget(Button(text="try to win", on_press=self.butt_press))
        button_widget.add_widget(Button(text="Continue", on_press=self.butt_press))
        content.add_widget(button_widget)
        self.content = content
        self.open()

    def exit_screen(self, **kwargs):
        self.size_hint = (None, None)
        self.size = self.usual_size
        self.dismiss()
        self.kwargs = kwargs
        content = BoxLayout(orientation="vertical")
        text1 = "How can you let Gambet defeat you !!"
        label = Label(text="How can you let [b]Gambet[/b] [color=#ff0000ff]defeat [/color]you !!", markup=True)

        label.font_size = 2 * self.width / len(text1)
        # label.bind(height=label.setter("font_size"))
        content.add_widget(label)
        button_widget = BoxLayout(orientation="horizontal", size_hint=[1, .5])
        button_widget.spacing = self.width // 10
        button_widget.add_widget(Button(text="try to WIN", on_press=self.butt_press))
        button_widget.add_widget(Button(text="give up", color=[1, 0, 0, 1], on_press=self.butt_press))
        content.add_widget(button_widget)
        self.content = content
        self.open()

    def invalid_screen(self, **kwargs):
        self.size_hint = (None, None)
        self.size = self.usual_size
        self.dismiss()
        self.kwargs = kwargs
        content = BoxLayout(orientation="vertical")
        label = Label(text="You have entered an incorrect number in B or S value .")
        label.font_size = 2 * self.width / len(label.text)
        content.add_widget(label)
        # button_widget = BoxLayout(orientation="horizontal")  # , size_hint=[1, .7])
        content.add_widget(Button(text="Try again", on_press=self.butt_press, size_hint=[.5, .7],
                                  pos_hint={'center_x': .5, "center_y": .5}))
        # button_widget.add_widget(Button(text="Correct", on_press=self.butt_press))
        self.content = content
        self.open()

    def help_screen(self, **kwargs):
        self.dismiss()
        self.kwargs = kwargs
        self.title = "Quick Help"
        self.size_hint = (1,.95)
        content = BoxLayout(orientation="vertical")

        file = open("help","r")
        text = file.read()
        file.close()

        scroll_label = ScrollView()
        scroll_label.effect_cls = ScrollEffect
        label = Label(text=text, size_hint=(None, None), text_size=(self.width - 25, None), markup=True)
        label.bind(texture_size=label.setter("size"))
        scroll_label.add_widget(label)
        button = Button(text="Test your brain", size_hint=(.5, .2), pos_hint={"center_x": .5, "center_y": .5},
                        on_press=self.butt_press)
        content.add_widget(scroll_label)
        content.add_widget(button)
        self.content = content
        self.open()

    def butt_press(self, butt, *args):
        self.dismiss()
        key = butt.text.replace(" ", "_")
        self.kwargs[key]()
        # # this line should call the function that have the same key name with butt text with _ instead of " "
