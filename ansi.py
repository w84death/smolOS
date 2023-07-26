"""
Template for user programs for smolOS

(c)2023/07 Krzysztof Krystian Jankowski
Homepage: https://smol.p1x.in/os/
"""

class ANSI:
    """
    A class to handle the ANSI escape sequences, text attributes, and colors.
    """
    def __init__(self):
        """
        Initialize the ANSI object.
        """
        self.text_attributes = {
            "Bold": "\\033[1m",
            "Faint": "\\033[2m",
            "Underline": "\\033[4m",
            "Blink": "\\033[5m",
            "Reverse video": "\\033[7m",
            "Conceal": "\\033[8m",
            "Crossed-out": "\\033[9m",
        }

        self.text_colors = {
            "Black": "\\033[30m",
            "Red": "\\033[31m",
            "Green": "\\033[32m",
            "Yellow": "\\033[33m",
            "Blue": "\\033[34m",
            "Magenta": "\\033[35m",
            "Cyan": "\\033[36m",
            "White": "\\033[37m",
        }

        self.background_colors = {
            "Black": "\\033[40m",
            "Red": "\\033[41m",
            "Green": "\\033[42m",
            "Yellow": "\\033[43m",
            "Blue": "\\033[44m",
            "Magenta": "\\033[45m",
            "Cyan": "\\033[46m",
            "White": "\\033[47m",
        }

    def list_sequences(self, title, sequences):
        """
        List a set of sequences with a title.
        """
        print(f"\\033[0;1m{title}\\n")
        for name, code in sequences.items():
            print(f"\\033[37m{code}{name}\\t\\t{code}")
        print("\\n")

    def reset_attributes(self):
        """
        Reset all attributes.
        """
        print("\\033[0m")


# To use this refactored code, you would do something like the following:
ansi = ANSI()

print("\\n\\033[1mANSI Escape Sequences\\n")
print("\\033[0mReset all attributes\\t\\\\033[0m\\n")

ansi.list_sequences("Text Attributes", ansi.text_attributes)
ansi.reset_attributes()

ansi.list_sequences("Text Colors", ansi.text_colors)

ansi.list_sequences("Background Colors", ansi.background_colors)
ansi.reset_attributes()
