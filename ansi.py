class ANSI():
    def __init__(self):
        return

    def header(self):
        print("\n\033[1mANSI Escape Sequences\n")
        print("\033[0mReset all attributes\t\\033[0m\n")

    def list_text_attributes(self):
        print("\033[1mText Attributes\n")
        print("\033[0m\033[1mBold\t\t\\033[1m")
        print("\033[0m\033[2mFaint\t\t\\033[2m")
        print("\033[0m\033[4mUnderline\t\\033[4m")
        print("\033[0m\033[5mBlink\t\t\\033[5m")
        print("\033[0m\033[7mReverse video\t\\033[7m")
        print("\033[0m\033[8mConceal\t\t\\033[8m")
        print("\033[0m\033[9mCrossed-out\t\\033[9m")
        print("\n")

    def list_colors(self):
        print("\033[0;1mText Colors\n")
        print("\033[30mBlack\t\t\\033[30m")
        print("\033[31mRed\t\t\\033[31m")
        print("\033[32mGreen\t\t\\033[32m")
        print("\033[33mYellow\t\t\\033[33m")
        print("\033[34mBlue\t\t\\033[34m")
        print("\033[35mMagenta\t\t\\033[35m")
        print("\033[36mCyan\t\t\\033[36m")
        print("\033[37mWhite\t\t\\033[37m")
        print("\n")

    def list_back_colors(self):
        print("\033[0;1mBackground Colors\n")
        print("\033[37m\033[40mBlack\t\t\\033[40m")
        print("\033[41mRed\t\t\\033[41m")
        print("\033[42mGreen\t\t\\033[42m")
        print("\033[43mYellow\t\t\\033[43m")
        print("\033[44mBlue\t\t\\033[44m")
        print("\033[45mMagenta\t\t\\033[45m")
        print("\033[46mCyan\t\t\\033[46m")
        print("\033[30m\033[47mWhite\t\t\\033[47m")

    def reset_attributes(self):
        print("\033[0m")

ansi = ANSI()
ansi.header()
ansi.list_text_attributes()
ansi.reset_attributes()
ansi.list_colors()
ansi.list_back_colors()

