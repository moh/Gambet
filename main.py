from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.storage.jsonstore import JsonStore
from number import Numbers
from bottom_side import BottomSide
from areas import *
from screens import Screens_popup
from kivy.config import Config


class Game(BoxLayout):
    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        # ## screen nb
        self.scr_nb = 0
        # ##
        self.orientation = "vertical"
        self.size = Window.size
        self.bar = Bar()
        self.bar.size = [self.width, self.height // 10]
        self.bar.pos = [0, self.height - self.bar.height]
        self.add_widget(self.bar)
        self.bar.add_widgs(self.back_btn)
        # ##
        self.scr = Widget()
        self.scr.size = [self.width, self.height - self.bar.height]
        self.scr.canvas.before.add(Rectangle(source="img//first_background.png", size=self.scr.size))
        self.proceed_scr(FirstScreen(), self.play, self.helps)
        self.add_widget(self.scr)

        self.screen = Screens_popup(self)

        self.gambet_mode = True

        # store section
        self.store = JsonStore("b_s.json")
        self.point, self.match = 0, 0
        if not(self.store.exists("value")):
            self.store.put("value", point=0, match=0)
            self.score_match = [0, 0]
        else:
            self.score_match = [self.store.get("value")["point"], self.store.get("value")["match"]]

    # for screen loading
    def proceed_scr(self, scr1, *args):
        if type(scr1) == FirstScreen:
            self.scr_number = 0
            self.bar.btn.text = "Exit"
        elif type(scr1) == SecScreen:
            self.scr.canvas.before.clear()
            self.scr.canvas.before.add(Rectangle(source="img//first_background.png", size=self.scr.size))
            self.scr_number = 1
        self.scr.clear_widgets()
        self.scr.add_widget(scr1)
        scr1.size = [self.scr.width // 3.5, self.scr.height // 3]
        scr1.center = [self.scr.width // 2, self.scr.height // 2]
        scr1.add_button(*args)

# ## buttons functions
    def play(self, *args):
        self.bar.btn.text = "Back"
        self.proceed_scr(SecScreen(), self.with_gambet, self.single)

    def helps(self, btn):
        self.screen.help_screen(Test_your_brain = self.play)

    def back_btn(self, *args):
        screens = [(FirstScreen(), (self.play, self.helps)), (SecScreen(), (self.play, self.play))]
        self.proceed_scr(screens[self.scr_number - 1][0], *screens[self.scr_number - 1][1])

    # ##play mode
    def start_game(self):
        self.score_match = [self.point, self.match + 1]
        self.scr.clear_widgets()
        self.scr_number = 2
        self.numbers = Numbers()

        Names = BoxLayout(orientation="horizontal",size_hint=[None,None] , size = [self.scr.width, self.scr.height // 5] )
        Names.add_widget(Label(text="[b]Player[/b]", markup=True, font_size=Names.size[1]/1.5))
        if self.gambet_mode:
            Names.add_widget(Label(text="[b]Gambet[/b]", markup=True, font_size=Names.size[1]/1.5))
        else:
            Names.add_widget(Widget())
        Names.canvas.before.add(
            Rectangle(source="img//vs.png", size_hint=[None, None], size=Names.size, pos=[0, 4 * self.scr.height // 5]))

        self.scr.canvas.before.clear()

        self.composent = BoxLayout(orientation="vertical", size=self.scr.size)
        self.scr.add_widget(self.composent)

        self.nb_display = BoxLayout(orientation="horizontal", width=self.width, height = 8*self.scr.height // 15)
        self.player_section = PlayerArea()
        self.nb_display.add_widget(self.player_section)
        self.player_section.build_it()
        if self.gambet_mode:
            self.enemy_section = EnemyArea()
            self.nb_display.add_widget(self.enemy_section)
            self.enemy_section.build_it()
        else:
            self.nb_display.add_widget(Widget())

        self.btm_side = BottomSide(self)
        self.btm_side.size_hint = [1, None]
        self.btm_side.height = 4*self.scr.height // 15

        self.composent.add_widget(Names)
        self.composent.add_widget(self.nb_display)
        self.composent.add_widget(self.btm_side)

        pict = (Rectangle(source="img//battle_screen.png", size=[self.scr.width, self.scr.height - Names.height]))
        self.scr.canvas.before.add(pict)
        # add line
        with self.scr.canvas.before:
            Color(rgb=[.5, .5, .5])
            Line(points=[self.scr.width/2, self.scr.height, self.scr.width/2, self.btm_side.height])
            Color()
        self.btm_side.build_it()
        # the previous line is here cz build_it will add input_part1
        if not self.gambet_mode:
            self.btm_side.input_part1.single_mode = True
        # nb configuration
        if self.gambet_mode:
            self.nb_guess = self.numbers.get_number()
            self.btm_side.input_part1.set_value(Guess_N=self.nb_guess)

    def with_gambet(self, *args):
        self.gambet_mode = True
        self.start_game()

    def single(self, *args):
        self.gambet_mode = False
        self.start_game()
    
    # var for number list
    @property
    def player_number(self):
        return

    @player_number.setter
    def player_number(self, value):
        b, s = self.numbers.get_boule_strike(value)
        if s == 4:
            l = len(self.numbers.playerValue)
            if self.gambet_mode:
                if self.btm_side.input_part1.single_mode:
                    self.screen.single_mode_b_screen(Try_again=self.with_gambet)
                    if l>10 :
                        self.score_match = [self.point + 10 - l, self.match]
                else:
                    self.screen.win_screen(Win_again=self.with_gambet)
                    self.score_match = [self.point + 20 - l, self.match]
            else:
                if l>5:
                    self.screen.single_mode_b_screen(Try_again=self.single)
                    self.score_match = [self.point + 5, self.match]
                else:
                    self.screen.single_mode_a_screen(Try_again=self.single, Beat_Gambet=self.with_gambet)
                    self.score_match = [self.point + 5 - l, self.match]
        self.player_section.player_numb.number_list = [str(value), str(b), str(s)]

    @property
    def player_input(self):
        return

    @player_input.setter
    def player_input(self, value):
        if value[1] == '4':
            l = len(self.numbers.PCvalue)
            self.screen.lose_screen(try_to_win=self.with_gambet, Continue=self.cont)
            self.score_match = [self.point -10 + l, self.match]

        self.enemy_section.enemy_numb.number_list = [self.nb_guess, str(value[0]), str(value[1])]
        self.nb_guess = self.numbers.get_number(self.nb_guess, int(value[0]), int(value[1]))
        if not self.nb_guess:
            self.screen.invalid_screen(Try_again=self.with_gambet)
        self.btm_side.input_part1.set_value(Guess_N=self.nb_guess)

    # screen function
    def cont(self, *args):
        self.btm_side.input_part1.single_mode = True

    # store property
    @property
    def score_match(self):
        pass

    @score_match.setter
    def score_match(self, value):
        self.point, self.match = value
        self.bar.point_match_update = [self.point, self.match]
        self.store.put("value", point=self.point, match=self.match)


class Main(App):

    Config.set("kivy", "exit_on_escape", 0)
    Config.write()

    def open_settings(self, *args):
        pass

    def on_pause(self):
        return True

    def on_resume(self):
        return True

    def build(self):
        return Game()

Main().run()