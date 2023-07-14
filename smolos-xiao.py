# smolOS by Krzysztof Krystian Jankowski
# Homepage: http://smol.p1x.in/os/

import machine
import uos
import gc
import utime
import _thread

class smolOS:
    def __init__(self):
        self.name="smolOS"
        self.version = "0.6b-xiao"
        self.board = "Seeed XIAO RP2040"
        self.turbo = False
        self.cpu_speed_range = {"slow":80,"turbo":133} # Mhz
        self.thread_running = False
        self.power = machine.Pin(11,machine.Pin.OUT)
        self.power.value(1)
        self.led_pixel = WS2812(12,1)
        self.system_led = machine.Pin(25, machine.Pin.OUT)
        self.protected_files = { "boot.py", "main.py" }
        self.user_commands = {
            "banner": self.banner,
            "help": self.help,
            "ls": self.ls,
            "cat": self.cat,
            "rm": self.rm,
            "cls": self.cls,
            "stats": self.stats,
            "turbo": self.toggle_turbo,
            "ed": self.ed,
            "info": self.info,
            "py": self.py,
            "led": self.led,
            "bg": self.bg,
            "kill": self.kill
        }
        self.user_commands_manual = {
            "ls": "list files",
            "cat <filename>": "print filename content",
            "info <filename>": "information about a file",
            "rm <filename>": "remove a file (be careful!)",
            "ed <filename>": "text editor, filename is optional",
            "cls": "clears the screen",
            "banner": "prints system banner",
            "turbo": "toggles turbo mode (100% vs 50% CPU speed)",
            "stats": "system statistics",
            "py <filename>": "runs user program",
            "led": "manipulating on-board LED",
            "bg": "experimental multitasking",
            "kill": "killing background task"

        }
        self.ed_commands_manual = {
            "help": "this help",
            "n": "next page",
            "b ": "back one page",
            "10 <line of text>": "replacing 10-th line with a line of text",
            "a": "append new line at the end of a file",
            "write or save": "write changes to a file (not implemented yet)",
            "quit": "quit"
        }

        self.boot()

    def boot(self):
        machine.freq(self.cpu_speed_range["slow"] * 1000000)
        self.cls()
        self.welcome()
        self.led("boot")
        while True:
            user_input = input("\nsmol $: ")
            parts = user_input.split()
            if len(parts) > 0:
                command = parts[0]
                if command in self.user_commands:
                    if len(parts) > 1:
                        arguments = parts[1:]
                        self.user_commands[command](*arguments)
                    else:
                        self.user_commands[command]()
                else:
                    self.unknown_function()

    def banner(self):
        print("\033[1;33;44m                                 ______  _____")
        print("           _________ ___  ____  / / __ \/ ___/")
        print("          / ___/ __ `__ \/ __ \/ / / / /\__ \ ")
        print("         (__  ) / / / / / /_/ / / /_/ /___/ / ")
        print("        /____/_/ /_/ /_/\____/_/\____//____/  ")
        print("--------------\033[1;5;7mXIAO-RP2040-EDiTiON\033[0;1;33;44m--------------\n\033[0m")

    def welcome(self):
        self.banner()
        self.stats()
        self.print_msg("Type 'help' for a smol manual.")

    def man(self,manual):
        for cmd,desc in manual.items():
            print("\t\033[7m"+cmd+"\033[0m -",desc)
        utime.sleep(0.5)

    def help(self):
        print(self.name+ " version "+self.version+" user commands:\n")
        self.man(self.user_commands_manual)
        print("\n\033[0;32mSystem created by Krzysztof Krystian Jankowski.")
        print("Source code available at \033[4msmol.p1x.in/os/\033[0m")

    def print_err(self, error):
        print("\n\033[1;37;41m\t<!>",error,"<!>\t\033[0m")
        utime.sleep(1)

    def print_msg(self, message):
        print("\n\033[1;30;43m\t->",message,"\t\033[0m")
        utime.sleep(0.5)

    def unknown_function(self):
        self.print_err("unknown function. Try 'help'.")

    def toggle_turbo(self):
        freq = self.cpu_speed_range["turbo"]
        if self.turbo:
             freq = self.cpu_speed_range["slow"]
        machine.freq(freq * 1000000)
        self.turbo = not self.turbo
        self.print_msg("CPU speed set to "+str(freq)+" Mhz")

    def stats(self):
        print("\033[0mBoard:\033[1m",self.board)
        print("\033[0mMicroPython:\033[1m",uos.uname().release)
        print("\033[0m"+self.name + ":\033[1m",self.version,"(size:",uos.stat("main.py")[6],"bytes)")
        print("\033[0mFirmware:\033[1m",uos.uname().version)
        print("\033[0mCPU Speed:\033[1m",machine.freq()*0.000001,"MHz")
        print("\033[0mFree memory:\033[1m",gc.mem_free(),"bytes")
        print("\033[0mFree space:\033[1m",uos.statvfs("/")[0] * uos.statvfs("/")[2],"bytes")

    def cls(self):
         print("\033[2J")

    def ls(self):
        for file in uos.listdir():
            file_size = uos.stat(file)[6]
            additional = ""
            if file in self.protected_files: info = "protected system file"
            print(file,"\t", file_size, "bytes", "\t"+additional)

    def info(self,filename=""):
        if filename == "":
            self.print_err("No file")
            return
        additional = ""
        file_size = uos.stat(filename)[6]
        if filename in self.protected_files: additional = "protected system file"
        print(filename,"\t",file_size,"bytes","\t"+additional)


    def cat(self,filename=""):
        if filename == "":
            self.print_err("Failed to open the file.")
            return
        with open(filename,'r') as file:
            content = file.read()
            print(content)

    def rm(self,filename=""):
        if filename == "":
            self.print_err("Failed to remove the file.")
            return
        if filename in self.protected_files:
            self.print_err("Can not remove system file!")
        else:
            uos.remove(filename)
            self.print_msg("File '{}' removed successfully.".format(filename))

    def py(self,filename=""):
        if filename == "":
            self.print_err("Specify a file name to run.")
            return
        exec(open(filename).read())

    def led(self,turn="on"):
        if turn in ("on",""):
            self.system_led.value(0)
            return
        if turn=="off":
            self.system_led.value(1)
            return
        if turn=="boot":
            for _ in range(4):
                self.system_led.value(0)
                utime.sleep(0.1)
                self.system_led.value(1)
                utime.sleep(0.05)
            self.system_led.value(1)
            return


    def led_hearthbeat(self):
        while self.thread_running:
            for _ in range(2):
                self.system_led.value(1)
                utime.sleep(0.05*4)
                self.system_led.value(0)
                utime.sleep(0.05*4)
            self.system_led.value(1)
            utime.sleep(0.05*14)


    def bg(self):
        if self.thread_running:
            self.print_err("Already running in the background! Use `kill` command.")
            return

        self.thread_running = True
        self.thread = _thread.start_new_thread(self.led_hearthbeat,())
        self.print_msg("LED Hearthbeat running in the background...")

    def kill(self):
        self.thread_running = False
        self.print_msg("LED Hearthbeat killed.")

    # smolEDitor
    # Minimum viable text editor
    def ed(self, filename=""):
        self.page_size = 10
        self.file_edited = False
        print("Welcome to \033[7msmolEDitor\033[0m\nMinimum viable text editor for smol operating system")
        try:
            with open(filename,'r+') as file:
                print("\nEditing existing \033[7m"+filename+"\033[0m file\n")
                lines = file.readlines()
                line_count = len(lines)
                start_index = 0

                while True:
                    if start_index < line_count:
                        end_index = min(start_index + self.page_size,line_count)
                        print_lines = lines[start_index:end_index]

                        print("\033[7m    File:",filename,"Page:",start_index % self.page_size,"Lines:",line_count," (`h` help, `b` back,`n` next page)\033[0m")

                        for line_num,line in enumerate(print_lines,start=start_index + 1):
                            print("{}: {}".format(f"{line_num:03}",line.strip()))

                    user_ed_input = input("\ned $: ")

                    if user_ed_input =="quit":
                        if self.file_edited:
                            self.print_msg("file was edited, `save` it first or write `quit!`")
                    if user_ed_input == "quit!":
                        break

                    if user_ed_input == "help":
                        self.man(self.ed_commands_manual)

                    if user_ed_input == "a":
                        line_count += 1
                        lines.append("")

                    if user_ed_input == "n":
                        if start_index+self.page_size < line_count:
                            start_index += self.page_size
                        else:
                            self.print_msg("There is no next page. This is the last page.")

                    if user_ed_input == "b":
                        if start_index-self.page_size >= 0:
                            start_index -= self.page_size
                        else:
                            self.print_msg("Can not go back, it is a first page already.")

                    if user_ed_input in ("save","write"):
                        self.print_err("Saving not implemented yet")

                    parts = user_ed_input.split(" ",1)
                    if len(parts) == 2:
                        line_number = int(parts[0])
                        new_content = parts[1]
                        self.file_edited = True

                        if line_number > 0 and line_number < line_count:
                            lines[line_number - 1] = new_content + "\n"
                        else:
                            self.print_err("Invalid line number")


        except OSError:
            if filename == "":
                self.print_err("Provide an existing file name after the `ed` command.")
            else:
                self.print_err("Failed to open the file.")

smol = smolOS()


