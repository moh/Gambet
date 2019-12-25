from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color, Line


class FirstScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(FirstScreen, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 40

    def add_button(self, play, helps):
        self.add_widget(Button(text="Play", on_press=play))  # , size_hint = [1,None], height = self.height//3))
        self.add_widget(Button(text="Help", on_press=helps))


class SecScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(SecScreen, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 40

    def add_button(self, A_pc, single):
        self.add_widget(Button(text="With Gambet", on_press=A_pc))
        self.add_widget(Button(text="Single", on_press=single))


class Bar(BoxLayout):
    def __init__(self, **kwargs):
        super(Bar, self).__init__(**kwargs)
        self.orientation = "horizontal"
        self.point, self.match = 0, 0
        self.size_hint = [None, None]

    def add_widgs(self, back_btn):
        self.back_btn = back_btn
        with self.canvas:
            Color(rgb=(.25, .25, .25))
            Rectangle(pos=self.pos, size=self.size)

        self.label_point = Label(text="Point : ", size_hint=[1, 1])
        self.label_match = Label(text="Match : ", size_hint=[1, 1])
        self.add_widget(self.label_point)
        self.add_widget(self.label_match)
        self.btn = Button(text="Exit", on_press=self.btn_press, size_hint=[.5, 1])
        self.add_widget(self.btn)

    def btn_press(self, btn, *args):
        if btn.text == "Back":
            self.back_btn()
        else:
            game = self.parent
            point = game.point
            if point < 0:
                game.screen.exit_screen(try_to_WIN = game.play, give_up = exit)
            else:
                exit()

    @property
    def point_match_update(self):
        return

    @point_match_update.setter
    def point_match_update(self, value):
        self.label_point.text = "Point : " + str(value[0])
        self.label_match.text = "Match : " + str(value[1])


# 3rd screen ##

class PlayerArea(ScrollView):
    def __init__(self, **kwargs):
        super(PlayerArea, self).__init__(**kwargs)
        self.do_scroll_x = False

    def build_it(self):
        self.player_numb = PlayerNb(self)
        self.add_widget(self.player_numb)


class PlayerNb(GridLayout):
    def __init__(self, parents, **kwargs):
        super(PlayerNb, self).__init__(**kwargs)
        self.cols = 1
        self.size_hint = (1, None)
        self.height = parents.parent.height
        self.cst_height=self.height
        self.bind(minimum_height=self.setter('height'))
        self._number_list = []  # this variable is to store number given by player and B S by program
        self.selected, self.correct = None, True

    @property
    def number_list(self):
        return (self._number_list)

    @number_list.setter
    def number_list(self, value):
        self._number_list.append(value)
        self.add_numbers()

    def add_numbers(self):
        self.height=self.cst_height  # without it self.height will change
        text_l = self._number_list[-1]  # text_list with format [number,b,s]
        text = "[color=#c8e500ff]" + text_l[0] + '[/color]  ' + "    " + text_l[1] + "   [b]B[/b] " + text_l[2] +\
               " [b]S[/b] "
        o_text = text_l[0] + " " + text_l[1] + " " + text_l[2]
        label = Label(text=text, markup=True, size_hint=[1, None])
        label.height = self.height / 3
        label.font_size = self.width / len(o_text)
        self.add_widget(label)


# # enemy area # #

class EnemyArea(ScrollView):
    def __init__(self, **kwargs):
        super(EnemyArea, self).__init__(**kwargs)
        self.do_scroll_x = False

    def build_it(self):  # this method cz parent of this class doesn't exist before add_widget
        self.enemy_numb = EnemyNb(self)
        self.add_widget(self.enemy_numb)


class EnemyNb(GridLayout):
    def __init__(self, parents, **kwargs):
        super(EnemyNb, self).__init__(**kwargs)
        self.cols = 1
        self.size_hint = (1,None)
        self.height = parents.parent.height
        self.cst_height=self.height
        self.bind(minimum_height=self.setter('height'))
        self._number_list = []  # this variable is to store number given by player and B S by program
        self.selected, self.correct = None, False

    @property
    def number_list(self):
        return self._number_list

    @number_list.setter
    def number_list(self, value):
        self._number_list.append(value)
        self.add_numbers()

    def add_numbers(self):
        self.height = self.cst_height  # without this equation self.height will change ( don't know why )
        text_l = self._number_list[-1]  # text_list with format [number,b,s]
        text = "[color=#c8e500ff]" + text_l[0] + '[/color]  ' + "   " + text_l[1] + " [b]B[/b]   " + text_l[2] +\
               " [b]S[/b]"
        o_text = text_l[0] + " " + text_l[1] + " " + text_l[2]
        label = Label(text=text, markup=True, size_hint=(1, None), height=self.height/3)
        label.font_size = self.width / len(o_text)
        self.add_widget(label)

    def on_touch_down(self, touch):
        if not self.correct or self.selected:
            return super(EnemyNb, self).on_touch_down(touch)  # if it is the first time and correct mode
        for label in self.children:
            if label.collide_point(*touch.pos):
                self.selected = label
                with self.canvas:
                    Color(.5, .5, .5, .5)
                    self.rect_selected = Rectangle(pos=self.selected.pos, size=self.selected.size)
                    self.selected.bind(pos=self.update_rectangle)
        return super(EnemyNb, self).on_touch_down(touch)

    def update_rectangle(self, label, pos):
        self.rect_selected.pos = pos
