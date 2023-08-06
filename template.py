"""
Template for user programs for smolOS

(c)2023/07 Krzysztof Krystian Jankowski
Homepage: https://smol.p1x.in/os/
"""

import time

# Define constants
MESSAGE_INTERVAL = 10

class Template:
    """
    A template for user programs for smolOS.
    """
    def __init__(self):
        """
        Initialize the Template object.
        """
        self.name = "Template Program"
        self.msg("Program initialized")

    def loop(self):
        """
        Loop where the main logic of the program goes.
        """
        t = 0
        self.msg("Press Ctrl+C to quit.\n")
        while True:
            try:
                if t % MESSAGE_INTERVAL == 0:
                    self.msg(f"Hello... {t} second in!")
                time.sleep(1)
                t += 1
            except KeyboardInterrupt:
                break

    def msg(self, message):
        """
        Print a message from the program.
        """
        print(f"{self.name} : {message}")

if __name__ == '__main__':
    template = Template()
    template.loop()

