"""
smolOS - tiny operating system for tiny computers
-------------------------------------------------
Specialized Microcontroller-Oriented Lightweight Operating System

(c)2023/07 Krzysztof Krystian Jankowski
Homepage: https://smol.p1x.in/os/
"""

import machine
import uos
import gc
import utime

# Define constants
CPU_SPEED_SLOW = 40
CPU_SPEED_TURBO = 133
SYSTEM_LED_PIN = 25
PAGE_SIZE = 10

OS_VERSION = "almost-0.9"
OS_VARIANT = "xiao"
OS_BOARD_NAME = "Seeed XIAO RP2040"

# Define smolOS class
class smolOS:
    """
    A class to handle the smolOS functionalities.
    """
    def __init__(self):
        """
        Initialize the smolOS object.
        """
        self.name = "smolOS"
        self.version = OS_VERSION
        self.version += "-"+OS_VARIANT
        self.board = OS_BOARD_NAME
        self.cpu_speed_range = {"slow": CPU_SPEED_SLOW, "turbo": CPU_SPEED_TURBO}  # Mhz
        self.system_led = machine.Pin(SYSTEM_LED_PIN, machine.Pin.OUT)
        self.prompt = "\nsmol $: "
        self.turbo = True
        self.background_prog = ""
        self.protected_files = {"boot.py", "main.py"}
        self.user_commands = {
            "help": self.help,
            "list": self.list,
            "show": self.show,
            "remove": self.remove,
            "clear": self.clear,
            "stats": self.stats,
            "turbo": self.toggle_turbo,
            "edit": self.edit,
            "info": self.info,
            "run": self.run,
            "stop": self.stop,
            "led": self.led,
            "exe": self.exe
        }
        self.user_commands_manual = {
            "list": "list files",
            "show <filename>": "print filename content",
            "info <filename>": "information about a file",
            "remove <filename>": "remove a file (be careful!)",
            "edit <filename>": "text editor, filename is optional",
            "clear": "clears the screen",
            "turbo": "toggles turbo mode (100% vs 50% CPU speed)",
            "stats": "system statistics",
            "run <filename>": "loads and runs user program (load first)",
            "stop": "stops and unloads latest running program",
            "led <command>": "manipulating on-board LED. Commands: `on`, `off`",
            "exe <code>": "Running exec(code)"
        }
        self.boot()

    def boot(self):
        """
        Boot the smolOS.
        """
        machine.freq(self.cpu_speed_range["turbo"] * 1000000)
        self.clear()
        self.welcome()
        while True:
            user_input = input(self.prompt)
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
                    self.try_exec_script(command)

    def banner(self):
        """
        Display the smolOS banner.
        """
        print("\033[1;33;44m                                           ______  _____")
        print("                     _________ ___  ____  / / __ \\/ ___/")
        print("                    / ___/ __ `__ \\/ __ \\/ / / / /\\__ \\ ")
        print("                   (__  ) / / / / / /_/ / / /_/ /___/ / ")
        print("                  /____/_/ /_/ /_/\\____/_/\\____//____/  ")
        print("  \033[1;5;7m Specialized Microcontroller-Oriented Lightweight Operating System \033[0m\033[1;33;44m  ")
        print("                        ~ EST. July of 2023 ~\n\033[0m")

    def welcome(self):
        """
        Display the welcome message.
        """
        self.banner()
        self.stats()
        self.led("boot")
        self.print_msg("Type \'help\' for a smol manual.")

    def man(self, manual):
        """
        Display the manual.
        """
        for cmd, desc in manual.items():
            print("\t\033[7m" + cmd + "\033[0m -", desc)

    def help(self):
        """
        Display the help message.
        """
        print(self.name + " version " + self.version + " user commands:\n")
        self.man(self.user_commands_manual)
        print("\n\033[0;32mSystem created by Krzysztof Krystian Jankowski.")
        print("Source code available at \033[4msmol.p1x.in/os/\033[0m")

    def print_msg(self, message):
        """
        Print a system message.
        """
        print("\n\033[1;34;47m\t->",message,"\t\033[0m")

    def print_err(self, error):
        """
        Print an error message.
        """
        print("\n\033[1;37;41m\t<!>", error, "<!>\t\033[0m")
        
    def ask_user(self, message):
        """
        Inputs user for an yes/no answer.
        """
        answer = input(message +" [yes]/no: ")
        if answer in ("yes", ""):
            return True
        return False
    
    def list(self):
        """
        List the files in the system.
        """
        print("Listing files:")
        files = uos.listdir()
        for i, file in enumerate(files):
            self.info(file, True)
            if (i+1) % PAGE_SIZE == 0:
                input("\033[7m Press Enter to see more\033[0m")
        print("\n\tTotal files: ", len(files))

    def show(self, filename=""):
        """
        Display the content of a file.
        """
        if filename:
            try:
                i=0
                with open(filename, "r") as file:
                    print(file.read())
                    i+=1
                    if (i+1) % PAGE_SIZE == 0:
                        input("\033[7m Press Enter to see more\033[0m")
            except OSError:
                self.print_err("Cannot open file!")
        else:
            self.print_err("No filename provided.")

    def remove(self, filename=""):
        """
        Remove a file from the system.
        """
        if filename:
            if filename not in self.protected_files:
                try:
                    uos.remove(filename)
                    print("File", filename, "removed.")
                except OSError:
                    self.print_err("Cannot remove file!")
            else:
                self.print_err("Cannot remove protected file!")
        else:
            self.print_err("No filename provided.")

    def clear(self):
        """
        Clear the system screen.
        """
        print("\033[2J\033[H", end="")

    def stats(self):
        """
        Display the system statistics.
        """
        print("\t\033[0mBoard:\033[1m",self.board)
        print("\t\033[0mMicroPython:\033[1m",uos.uname().release)
        print("\t\033[0m"+self.name + ":\033[1m",self.version,"(size:",uos.stat("smolos.py")[6],"bytes)")
        print("\t\033[0mFirmware:\033[1m",uos.uname().version)
        turbo_msg = "\033[0mIn power-saving, \033[1mslow mode\033[0m."
        if self.turbo:
            turbo_msg = "\033[0mIn \033[1mturbo mode\033[0m."
        print("\t\033[0mCPU Speed:\033[1m",machine.freq()*0.000001,"MHz",turbo_msg)
        print("\t\033[0mFree memory:\033[1m",gc.mem_free(),"bytes")
        print("\t\033[0mUsed space:\033[1m",uos.stat("/")[0],"bytes")
        print("\t\033[0mFree space:\033[1m",uos.statvfs("/")[0] * uos.statvfs("/")[3],"bytes")
        print("\033[0m")

    def toggle_turbo(self):
        """
        Toggle the CPU speed between turbo and slow.
        """
        self.turbo = not self.turbo
        if self.turbo:
            machine.freq(self.cpu_speed_range["turbo"] * 1000000)
            self.print_msg("CPU speed changed to turbo "+str(self.cpu_speed_range["turbo"]))
        else:
            machine.freq(self.cpu_speed_range["slow"] * 1000000)
            self.print_msg("CPU speed changed to slow "+str(self.cpu_speed_range["slow"]))

    def info(self, filename="", short=False):
        """
        Display the information of a file.
        """
        if filename:
            try:
                file_info = uos.stat(filename)
                print("\t\033[4m", filename,"\033[0m", file_info[6], "bytes")
                if not short:
                    print("\tCreated:", utime.localtime(file_info[7]))
                    print("\tModified:", utime.localtime(file_info[8]))
            except OSError:
                self.print_err("Cannot get info about file!")
        else:
            self.print_err("No filename provided.")

    def run(self, filename=""):
        """
        Run a program in the system.
        """
        if filename:
            try:
                with open(filename+".py", "r") as file:
                    code = file.read()
                self.background_prog = filename
                exec(code)
            except OSError:
                self.print_err("Cannot run program!")
        else:
            self.print_err("No filename provided.")

    def stop(self):
        """
        Stop a running program in the system.
        """
        self.background_prog = ""
        print("Background program stopped.")

    def led(self, command=""):
        """
        Control the system LED.
        """
        if command in ("on",""):
            self.system_led.value(1)
        elif command == "off":
            self.system_led.value(0)
        elif command=="boot":
            for _ in range(4):
                self.system_led.value(0)
                utime.sleep(0.1)
                self.system_led.value(1)
                utime.sleep(0.05)
            self.system_led.value(1)
        else:
            self.print_err("Invalid LED command!")

    def exe(self, code=""):
        """
        Execute a code in the system.
        """
        if code:
            try:
                exec(code)
            except Exception as e:
                self.print_err("Error in executing code!")
        else:
            self.print_err("No code provided.")

    def unknown_function(self):
        """
        Handle unknown function calls.
        """
        self.print_err("Unknown function. Type 'help' for list of functions.")

    def try_exec_script(self,command):
        """
        Trys to execute a script of a same name as given command
        """
        if command+'.py' in uos.listdir():
            self.run(command)
        else:
            self.unknown_function()

    def edit(self, filename=""):
        """
        Edit a file in a minimum viable text editor
        """
        file_edited = False
        edit_mode = True
        show_help = False
        new_file = False
        ed_commands_manual = {
            "help": "this help",
            ">": "next page",
            "<": "previous page",
            "10 <line of text>": "replacing 10-th line with a line of text",
            "append <lines>": "append new line(s) at the end of a file, default 1",
            "write or save": "write changes to a file",
            "name <filename>": "gives new name to opened file",
            "new": "open new empty file",
            "quit": "quit editor"
        }
        print("Welcome to \033[7medit\033[0m program.\nMinimum viable text editor for smol operating system")

        try:
            if filename == "":
                lines = [""]
                line_count = len(lines)
                new_file = True
            else:
                with open(filename,'r+') as file:
                    if filename in self.protected_files:
                        self.print_err("Protected file. View only.")
                    self.print_msg("Loaded existing "+filename+" file.")
                    lines = file.readlines()
                    line_count = len(lines)
            start_index = 0
        except OSError:
            self.print_err("Failed to open the file.")
            return


        while True:
            if edit_mode:
                if start_index < line_count:
                    end_index = min(start_index + PAGE_SIZE,line_count)
                    print_lines = lines[start_index:end_index]
                    display_name = filename
                    if filename=="":
                        display_name = "NEW UNNAMED FILE"

                    print("\033[7m    File:",display_name,"Lines:",line_count," // `h` help, `b` back,`n` next page\t\033[0m")

                    for line_num,line in enumerate(print_lines,start=start_index + 1):
                        print(line_num,":",line.strip())
            else:
                if show_help:
                    self.man(ed_commands_manual)
                    print("\n\033[7mHit [return] button\033[0m (or command) to go back to  editing.\n")

            user_ed_input = input("\ned $: ")

            if user_ed_input =="quit":
                if file_edited:
                    self.print_msg("file was edited, `save` it first or write `quit!`")
                else:
                    self.print_msg("edit closed")
                    break

            if user_ed_input == "quit!":
                self.print_msg("smolEDitor closed")
                break

            if user_ed_input == "help":
                edit_mode = False
                show_help = True

            if user_ed_input in ("","return"):
                if not edit_mode:
                    edit_mode = True
                    show_help = False

            if user_ed_input == "append":
                line_count += 1
                lines.append("")

            if user_ed_input == ">":
                if start_index+PAGE_SIZE < line_count:
                    start_index += PAGE_SIZE
                else:
                    self.print_msg("There is no next page. This is the last page.")

            if user_ed_input == "<":
                if start_index-PAGE_SIZE >= 0:
                    start_index -= PAGE_SIZE
                else:
                    self.print_msg("Can not go back, it is a first page already.")

            if user_ed_input in ("save","write"):
                if filename == "":
                    self.print_err("Your new file has no name. Use `name` followed by a file name and save again.")
                elif filename in self.protected_files:
                    self.print_err("Protected file")
                else:
                    ready = False
                    if new_file:
                        ready = True
                    if filename in uos.listdir():
                        if self.ask_user("You are overwriting an existing file, are you sure?"):
                            ready = True
                    if ready:
                        with open(filename, "w") as file:
                            for line in lines:
                                file.write(line)
                        self.print_msg("Saved in "+ filename)
                        file_edited = False
                        new_file = False

            if user_ed_input == "new":
                lines = [""]
                line_count = len(lines)
                new_file = True
                filename = ""
                
            parts = user_ed_input.split(" ",1)
            if len(parts) == 2:
                if parts[0] == "append":
                    new_lines = int(parts[1])
                    line_count += new_lines
                    for _ in range(new_lines):
                        lines.append("")
                elif parts[0] == "name":
                    if parts[1] in self.protected_files:
                        self.print_err("Protected file")
                    else:
                        filename=parts[1]
                else:
                    line_number = int(parts[0])
                    new_content = parts[1]
                    if line_number > 0 and line_number <= line_count:
                        lines[line_number - 1] = new_content + "\n"
                    else:
                        self.print_err("Invalid line number")
                file_edited = True

"""
End of system file.
Homepage: https://smol.p1x.in/os/
"""
os = smolOS()
os.boot()
