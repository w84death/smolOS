# smolOS by Krzysztof Krystian Jankowski
# Homepage: http://smol.p1x.in/os/
# Source version: 0.4c-xiao modified at 2023.07.13


import machine
import uos
import gc
from ws2812 import WS2812

class smolOS:
    def __init__(self):
        self.name="smolOS"
        self.version = "0.5-xiao"
        self.turbo = False
        self.files = uos.listdir()
        self.protected_files = { "boot.py", "main.py" }
        self.user_commands = {
            "banner": self.banner,
            "help": self.help,
            "ls": self.ls,
            "cat": self.cat,
            "rm": self.rm,
            "cls": self.cls,
            "stats": self.stats,
            "mhz": self.set_cpu_mhz,
            "turbo": self.toggle_turbo,
            "ed": self.ed,
            "info": self.info,
            "py": self.py,
            "led": self.led
        }

        self.boot()

    def boot(self):
        self.set_cpu_mhz(133)
        self.led_pixel = WS2812(12,1)
        self.cls()
        self.welcome()
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
        print("______________________________________________")
        print("                                 ______  _____")
        print("           _________ ___  ____  / / __ \/ ___/")
        print("          / ___/ __ `__ \/ __ \/ / / / /\__ \ ")
        print("         (__  ) / / / / / /_/ / / /_/ /___/ / ")
        print(" _[..]  /____/_/ /_/ /_/\____/_/\____//____/  ")
        print("==============XIAO-RP2040-EDiTiON=============")

    def welcome(self):
        print("\n\n\n\n")
        self.banner()
        print("\n")
        self.stats()
        print("\n\n\n\n")
        self.print_msg("Type 'help' for a smol manual.")
        print("\n")

    def help(self):
        print(self.name+ " Version "+self.version+" user commands:\n")
        print("\t`ls` - list files\n\t`cat filename` - print file\n\t`info filename` - info about selected file\n\t`rm filename` - remove file\n\t`ed filename` - text editor\n\t`banner` - system banner\n\t`cls` - clear screen\n\t`mhz` 160 - set CPU speed (80-160) in MHz\n\t`stats` - hardware and software information")
        print("\nSystem created by Krzysztof Krystian Jankowski")
        print("Code available at github and smol.p1x.in/os/")

    def print_err(self, error):
        print("\n\t<!>",error,"<!>")

    def print_msg(self, message):
        print("\n\t->",message)

    def unknown_function(self):
        self.print_err("unknown function. Try 'help'.")

    def set_cpu_mhz(self,freq="80"):
        freq = int(freq)
        if freq >= 80 and freq <= 160:
            machine.freq(freq * 1000000)
            self.print_msg("CPU frequency set to "+str(freq))
        else:
            self.print_err("wrong CPU frequency. Use between 80 and 160 MHz.")

    def toggle_turbo(self):
        if self.turbo:
            self.set_cpu_mhz("80")
        else:
            self.set_cpu_mhz("160")
        self.turbo = not self.turbo

    def stats(self):
        print("Board:",machine.unique_id())
        print("MicroPython:",uos.uname().release)
        print(self.name + ":",self.version,"(size:",uos.stat("main.py")[6],"bytes)")
        print("Firmware:",uos.uname().version)
        print("CPU Speed:",machine.freq()*0.000001,"MHz")
        print("Free memory:",gc.mem_free(),"bytes")
        print("Free space:",uos.statvfs("/")[0] * uos.statvfs("/")[2],"bytes")

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

    def led(self,rgb_color=""):
        if rgb_color=="":
            print("Rainbow!")
            self.led_pixel.rainbow_cycle(0.001)
        else:
            print("LED set to"+rgb_color)
            color = tuple(map(int, rgb_color.split(',')))
            self.led_pixel.pixels_fill(color)
            self.led_pixel.pixels_show()

    # smolEDitor
    # Minimum viable text editor
    def ed(self, filename=""):
        self.page_size = 10
        self.cls()
        print("Welcome to smolEDitor\nA smol text editor for smol operating system\n\nWrite h for help\nq to quit\n\n")
        try:
            with open(filename,'r+') as file:
                print("\nEditing "+filename+" file\n")
                lines = file.readlines()
                line_count = len(lines)
                start_index = 0
                message,error = "",""

                while True:
                    if start_index < line_count:
                        end_index = min(start_index + self.page_size,line_count)
                        print_lines = lines[start_index:end_index]

                        print("-> Page:",start_index % self.page_size,"Lines:",line_count)

                        for line_num,line in enumerate(print_lines,start=start_index + 1):
                            print("{}: {}".format(line_num,line.strip()))

                        if line_count > self.page_size:
                            message = "`b` back,`n` next page\n" + message

                    if not message == "":
                        print("-> ",message)
                    if not error == "":
                        self.print_err(error)
                    message,error = "",""
                    user_ed_input = input("\ned $: ")

                    if user_ed_input in ("q","quit"):
                        break

                    if user_ed_input in ("h","help"):
                        message = "smolEDitor minimum viable text editor\n\n`n` - next",self.page_size,"lines\n`b` - back",self.page_size,"lines\n`n text` - replacing n line with a text\n`a`,`add` - add new line\n`w`,`write`,'save' - write to file\n`h` - this help\n`q` - quit\n"

                    if user_ed_input in ("a","add"):
                        line_count += 1
                        lines.append("")

                    if user_ed_input == "n":
                        if start_index+self.page_size < line_count:
                            start_index += self.page_size
                        else:
                            error = "out of lines in this file."

                    if user_ed_input == "b":
                        if start_index-self.page_size >= 0:
                            start_index -= self.page_size
                        else:
                            error = "out of lines in this file."

                    if user_ed_input in ("w","write","save"):
                        error = "Saving implemented yet"

                    parts = user_ed_input.split(" ",1)
                    if len(parts) == 2:
                        line_number = int(parts[0])
                        new_content = parts[1]

                        if line_number > 0 and line_number < line_count:
                            lines[line_number - 1] = new_content + "\n"
                        else:
                            error = "Invalid line number."

        except OSError:
            if filename == "":
                self.print_err("Provide an existing file name after the `ed` command.")
            else:
                self.print_err("Failed to open the file.")

smol = smolOS()



