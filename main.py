# smolOS by Krzysztof Krystian Jankowski
# from smol import smolOS
# (c)2023.07 KKJ^P1X
import machine
import uos
import gc

class smolOS:
    def __init__(self):
        self.name="smolOS"
        self.version = "0.3"
        self.files = uos.listdir()
        self.protected_files = { "boot.py",  "main.py" }
        self.user_commands = {
            "welcome": self.welcome,
            "help": self.help,
            "ls": self.ls,
            "cat": self.cat,
            "rm": self.rm,
            "ed": self.ed,
            "cls": self.cls,
            "mhz": self.set_cpu_mhz,
            "info": self.info
        }

        self.boot()

    def boot(self):
        self.set_cpu_mhz(80)
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

    def welcome(self):
        print("\n\n\n\n")
        print("______________________________________________")
        print("                                 ______  _____")
        print("           _________ ___  ____  / / __ \/ ___/")
        print("          / ___/ __ `__ \/ __ \/ / / / /\__ \ ")
        print("         (__  ) / / / / / /_/ / / /_/ /___/ / ")
        print(" _[..]  /____/_/ /_/ /_/\____/_/\____//____/  ")
        print("==============================================")
        print("\n")
        self.info()
        print("\n\n\n\n")
        print("smolInfo: Type 'help' for a smol manual.\n\n")

    def help(self):
        print(self.name+ " Version "+self.version+" user commands:\n")
        print("ls - list files\ncat filename - print file\nrm filename - remove file\ned filename - text editor\nwelcome - welcome screen\ncls - clear screen\nmhz 160 - set CPU speed (80-160) in MHz\ninfo - hardware and software information")
        print("\nSystem created by Krzysztof Krystian Jankowski")
        print("Code available at github and smol.p1x.in/os/")

    def unknown_function(self):
        print("smolError: unknown function. Try 'help'.")

    def set_cpu_mhz(self, freq="80"):
        freq = int(freq)
        if freq >= 80 and freq <= 160:
            machine.freq(freq * 1000000)
        else:
            print("smolError: wrong CPU frequency. Use between 80 and 160 MHz.")

    def info(self):
        print(self.name + ":" + self.version)
        print("MicroPython:", uos.uname().release)
        print("Firmware:", uos.uname().version)
        print("CPU Speed:", machine.freq()*0.000001, "MHz")
        print("Free memory:", gc.mem_free(), "bytes")
        print("Free space:", uos.statvfs("/")[0] * uos.statvfs("/")[2], "bytes")

    def cls(self):
         print("\033[2J")

    def ls(self):
        self.files = uos.listdir()
        for file in self.files:
            file_size = uos.stat(file)[6]
            info = ""
            if file in self.protected_files: info = "protected system file"
            print(file,"\t", file_size, "bytes", "\t"+info)

    def cat(self, filename):
        try:
            with open(filename, 'r') as file:
                content = file.read()
                print(content)
        except OSError:
            print("smolError: Failed to open the file.")

    def rm(self, filename):
        try:
            if filename in self.protected_files:
                print("smolError: Can not remove system file!")
            else:
                uos.remove(filename)
                print("smolInfo: File '{}' removed successfully.".format(filename))
        except OSError:
            print("smolError: Failed to remove the file.")

    def ed(self, filename=""):
        self.edversion="0.3"
        self.cls()
        print("Welcome to smolEDitor\n\nWrite h for help\nq to quit\n")
        try:
            with open(filename, 'r+') as file:
                print("Editing "+filename+" file")
                lines = file.readlines()
                line_count = len(lines)
                start_index = 0

                while True:
                    if start_index < line_count:
                        end_index = min(start_index + 10, line_count)
                        print_lines = lines[start_index:end_index]

                        # Print the lines with line numbers
                        for line_num, line in enumerate(print_lines, start=start_index + 1):
                            print("{}: {}".format(line_num, line.strip()))
                    user_ed_input = input("\ned $: ")

                    if user_ed_input == "q":
                        break

                    if user_ed_input == "h":
                        print("smolEDitor V"+self.edversion+"\n\nn - next 10 lines\nb - back 10 lines\n1 Hello, World - replacing first line\na - add new line\nw - write to file\nh - this help\nq - quit")

                    if user_ed_input == "a":
                        lines_count += 11

                    if user_ed_input == "n":
                        if start_index+10 < line_count:
                            start_index += 10
                        else:
                            print("smolError: out of lines in this file.")

                    if user_ed_input == "b":
                        if start_index-10 >= 0:
                            start_index -= 10
                        else:
                            print("smolError: out of lines in this file.")

                    if user_ed_input == "w":
                        print("smolWarning: Not implemented yet.")

                    parts = user_ed_input.split(" ", 1)
                    if len(parts) == 2:
                        line_number = int(parts[0])
                        new_content = parts[1]

                        if line_number > 0 and line_number <= line_count:
                            lines[line_number - 1] = new_content + "\n"
                        else:
                            print("smolError: Invalid line number.")
                    else:
                        print("smolError: Invalid input format.")

        except OSError:
            print("smolError: Failed to open the file.")

smol = smolOS()
