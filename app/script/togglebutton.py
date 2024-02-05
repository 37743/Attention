from kivy.uix.image import Image
from kivy.uix.behaviors import ToggleButtonBehavior

class ToggleButton(ToggleButtonBehavior, Image):
    def __init__(self,
                 instance=None,
                 down='doc/images/Home_page_shapes/SquareBtn_shadow.png',
                 up='doc/images/Home_page_shapes/SquareBtn_invis.png',
                 **kwargs):
        self.down_state=down
        self.up_state=up
        super(ToggleButton, self).__init__(**kwargs)
        if instance == "home":
            self.state = 'down'
            self.source = self.down_state
        else:
            self.source = self.up_state

    def on_state(self, instance, value):
        if value == 'down':
            self.disabled = True
            self.source = self.down_state
        else:
            self.disabled = False
            self.source = self.up_state
