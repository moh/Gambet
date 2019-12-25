from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.core.audio import SoundLoader


# main_class should have two property : player_number for number entered by player ///  player_input for B and S
class BottomSide(BoxLayout):
    def __init__(self, main_class, **kwargs):
        # main_class isn't always the parent class
        super(BottomSide, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.main_class = main_class
        ''' this is the object of structure class that contain 2 variable,
        player_number(to store player_number),player_input(to store B and S given by him)'''
        self.butt_sound = SoundLoader.load("sound//button_press.ogg")

    def build_it(self):
        self.width = self.parent.width
        self.number_part = NumberPart()  # #this is the part where we display number given by Gambet
        self.input_part1 = InputPart1()  # #where the enter and del key appear
        self.number_butt = NumberButt()  # #where number button appear
        self.add_widget(self.number_part)
        self.add_widget(self.input_part1)
        self.add_widget(self.number_butt)
        self.input_part1.add_part()
        self.number_butt.add_part()


class NumberPart(Label):
    def __init__(self, **kwargs):
        super(NumberPart, self).__init__(**kwargs)
        self._number = ""

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        self._number = value
        if self._number == "":
            self.text = ""
            return
        self.text = "[b]Number : " + str(self._number)+"[/b]"
        self.markup = True


class InputPart1(BoxLayout):
    def __init__(self, **kwargs):
        super(InputPart1, self).__init__(**kwargs)
        self.orientation = "horizontal"
        # turn = True mean player turn ,match_4=True mean the number much player_number without order
        self._turne, self.match_4 = True, False
        self._v_boule, self._v_strike = 0, 0
        self.single_mode = False
        self.player_number, self._number_guess = "", ""
        self.boule_time = True  # this is true when it is the time to enter boule value
        self.size_hint = [None, 1]
        self.width = Window.width

    def add_part(self):
        self.number_butt = self.parent.number_butt
        self.number_part = self.parent.number_part
        self.update_widgets()

    @property
    def turne(self):
        return self._turne

    @turne.setter
    def turne(self, value):
        self._turne = value
        self.update_widgets()

    # this method help to update widgets when we change B,S,number,number_guess
    def set_value(self, **kwargs):
        output_list = []
        for key in kwargs:
            if key not in ("B", "S", "Number", "Guess_N", "New_Number"): raise Exception("key error, not 'B' or 's'")
            if key == "B":
                self._v_boule = kwargs[key]
            elif key == "S":
                self._v_strike = kwargs[key]
            elif key == "Number":
                self.player_number += kwargs[key]  # # += because it will update each character when we click nb button
            elif key == "Guess_N":
                self._number_guess = kwargs[key]
            elif key == "New_Number":
                self.player_number = kwargs[key]  # # = instead of += cz some function need to reset the value of number
        self.update_widgets()

    def get_B_S(self):
        return [self._v_boule, self._v_strike]

    def update_widgets(self):
        self.clear_widgets()
        self.number_part.clear_widgets()
        self.number_butt.disable_butt('all', False)
        if self._turne or self.single_mode:
            self.number_part.number = ""
            self.add_widget(Label(text="Number : " + self.player_number))
            self.number_butt.disable_butt(
                [nb for nb in self.player_number])  # disable all the buttons that have common number with player_number

        else:
            self.number_part.number = self._number_guess
            self.add_widget(Label(text="B : " + str(self._v_boule)))
            if self._v_boule == 0:
                self.number_butt.disable_butt([str(nb) for nb in range(5, 10)])

            if not self.match_4 and not self.boule_time:
                disable_strike_butt = {str(y) for y in range(10)} - {str(x) for x in range(
                    (4 - int(self._v_boule)) + 1)}  # #allowed number from 0 to 4-boule
                if self._v_boule == "1": disable_strike_butt.add("3")
                if self._v_strike == 0: self.number_butt.disable_butt(list(disable_strike_butt))
                self.add_widget(Label(text="S : " + str(self._v_strike)))

        self.dele = Button(text="Delete", on_press=self.del_butt, size_hint=(None, 1), background_color=[.4, .4, 1, 1],
                           width=2 * self.width / 9)
        self.ent = Button(text="Enter", on_press=self.enter_butt, size_hint=(None, 1), background_color=[.4, .4, 1, 1],
                          width=2 * self.width / 9)
        Window.bind(size=self.upd_size)
        self.add_widget(self.dele)
        self.add_widget(self.ent)

    def upd_size(self, obj, size):
        self.width = obj.width
        self.dele.width = self.ent.width = 2 * self.width / 9

    def enter_butt(self, *args):
        # wrong_sound = SoundLoader.load("sound//wrong_butt.wav")
        if self._turne or self.single_mode:
            if len(self.player_number) == 4:
                self._turne, self.boule_time = False, True
                self.parent.main_class.player_number = self.player_number
                # the first represent the variable of main class
                self.update_widgets()
                # ##
                self.player_number = ""
                self.update_widgets()
                # ##
            else:
                # wrong_sound.play()
                return ()
        else:
            if self.boule_time:
                self.boule_time = False
            else:  # #strike
                self._turne = True
                self.parent.main_class.player_input = self.get_B_S()
                # the first represent player input var of main class
                self.set_value(B=0, S=0, New_Number="")
            self.update_widgets()
        self.parent.butt_sound.play()  # play sound

    def del_butt(self, *args):
        # wrong_sound = SoundLoader.load("sound//wrong_butt.wav")
        if (self._turne or self.single_mode) and len(self.player_number) > 0:
            new_number = self.player_number[:len(self.player_number) - 1]
            self.set_value(New_Number=new_number)  # we use new_number key to reset Number value
        elif not self._turne:
            if self.boule_time:
                self.set_value(B=0)
            else:
                self.set_value(S=0)
        else:
            # wrong_sound.play()
            return
        self.parent.butt_sound.play()  # play sound


class NumberButt(BoxLayout):
    def __init__(self, **kwargs):
        super(NumberButt, self).__init__(**kwargs)
        self.orientation = "horizontal"
        self.build_button()

    def add_part(self):
        self.input_part = self.parent.input_part1

    def build_button(self):
        for num in range(1, 10):
            self.add_widget(Button(text=str(num), on_press=self.check_input, background_color=[.4, .4, 1, 1]))

    def disable_butt(self, butt, state=True):  # butt are butt to disable, state True (disable) or False
        for buttons in self.children:
            if butt == "all":
                buttons.disabled = state
            else:
                if type(butt) == list:
                    if buttons.text in butt: buttons.disabled = state
                else:
                    butt.disabled = True
                    break

    def check_input(self, butt, *args):
        self.parent.butt_sound.play()  # play sound

        boule_value, strike_value = self.input_part.get_B_S()[0], self.input_part.get_B_S()[1]
        turne, boule_time = self.input_part.turne, self.input_part.boule_time
        single_mode = self.input_part.single_mode
        if (turne and len(self.input_part.player_number) < 4) or single_mode:
            self.input_part.set_value(Number=butt.text)
            if len(self.input_part.player_number) == 4:
                self.disable_butt('all')
            self.disable_butt(butt)
        elif not turne:
            if boule_time:
                self.input_part.set_value(B=butt.text)
                self.disable_butt('all')

            elif not boule_time:
                self.input_part.set_value(S=butt.text)
                self.disable_butt('all')
