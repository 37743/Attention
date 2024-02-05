from kivy.uix.textinput import TextInput

class DateTextInput(TextInput):
    ''' Inherits from TextInput,
    limits number of characters to 2'''
    max_characters = 2
    def insert_text(self, substring, from_undo=False):
        if len(self.text) >= self.max_characters and self.max_characters >= 0:
            substring = ""
        TextInput.insert_text(self, substring, from_undo)
        if self.text != ""\
              and self.hint_text == "MM"\
                  and int(self.text) > 12:
            self.text = ""
        if self.text != ""\
              and self.hint_text == "DD"\
                  and int(self.text)> 31:
            self.text = "" 