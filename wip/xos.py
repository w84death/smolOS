from smolos import smolOS
from scroller import Scroller
import _thread

OS_NAME = "XsmolOS the Seeed XIAO Edition"
OS_VERSION  = "1.0"

class XIAOsmolOS(smolOS):
    def __init__(self):
        super().__init__()
        self.scroller = Scroller()

    def boot(self):
        _thread.start_new_thread(self.disp_welcome,())
        super().boot()

    def disp_welcome(self):
        self.scroller.draw_text(OS_NAME)

    def banner(self):
        print("\033[1;34;40m                                           ______  _____")
        print("                     _________ ___  ____  / / __ \\/ ___/")
        print("                    / ___/ __ `__ \\/ __ \\/ / / / /\\__ \\ ")
        print("                   (__  ) / / / / / /_/ / / /_/ /___/ / ")
        print("                  /____/_/ /_/ /_/\\____/_/\\____//____/  X")
        print("  \033[1;5;7m Specialized Microcontroller-Oriented Lightweight Operating System \033[0m\033[1;33;44m  ")
        print("                        ~ EST. July of 2023 ~\n\033[0m")


xos = XIAOsmolOS()
xos.boot()

