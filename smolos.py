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

OS_VERSION = "0.9-pre"
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
            "list": self.ls,
            "show": self.cat,
            "remove": self.rm,
            "clear": self.cls,
            "stats": self.stats,
            "turbo": self.toggle_turbo,
            "edit": self.ed,
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
        self.cls()
        self.welcome()
        self.led("boot")
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
                    self.unknown_function()

    def banner(self):
        """
        Display the smolOS banner.
        """
        print("\033[1;33;44m                                 ______  _____")
        print("           _________ ___  ____  / / __ \\/ ___/")
        print("          / ___/ __ `__ \\/ __ \\/ / / / /\\__ \\ ")
        print("         (__  ) / / / / / /_/ / / /_/ /___/ / ")
        print("        /____/_/ /_/ /_/\\____/_/\\____//____/  ")
        print("-------------\033[1;5;7mTINY-OS-FOR-TINY-COMPUTERS\033[0m------------\n\033[0m")

    def welcome(self):
        """
        Display the welcome message.
        """
        self.banner()
        self.stats()
        self.print_msg("Type \'help\' for a smol manual.")

    def man(self, manual):
        """
        Display the manual.
        """
        for cmd, desc in manual.items():
            print("\t\033[7m" + cmd + "\033[0m -", desc)
        utime.sleep(0.5)

    def help(self):
        """
        Display the help message.
        """
        print(self.name + " version " + self.version + " user commands:\n")
        self.man(self.user_commands_manual)
        print("\n\033[0;32mSystem created by Krzysztof Krystian Jankowski.")
        print("Source code available at \033[4msmol.p1x.in/os/\033[0m")

    def print_err(self, error):
        """
        Print an error message.
        """
        print("\n\033[1;37;41m\t<!>", error, "<!>\t\033[0m")
        utime.sleep(0.5)

    def ls(self):
        """
        List the files in the system.
        """
        print("Listing files:")
        files = os.listdir()
        for i, file in enumerate(files):
            print("\t", file)
            if (i+1) % PAGE_SIZE == 0:
                input("\033[7m Press Enter to see more\033[0m")
        print("\n\tTotal files: ", len(files))

    def cat(self, filename=""):
        """
        Display the content of a file.
        """
        if filename:
            try:
                with open(filename, "r") as file:
                    print(file.read())
            except OSError:
                self.print_err("Cannot open file!")
        else:
            self.print_err("No filename provided.")

    def rm(self, filename=""):
        """
        Remove a file from the system.
        """
        if filename:
            if filename not in self.protected_files:
                try:
                    os.remove(filename)
                    print("File", filename, "removed.")
                except OSError:
                    self.print_err("Cannot remove file!")
            else:
                self.print_err("Cannot remove protected file!")
        else:
            self.print_err("No filename provided.")

    def cls(self):
        """
        Clear the system screen.
        """
        print("\033[2J\033[H", end="")

    def stats(self):
        """
        Display the system statistics.
        """
        print("\n\t\033[7mSystem:\033[0m", self.name, "version", self.version)
        print("\t\033[7mBoard:\033[0m", self.board)
        print("\t\033[7mCPU speed:\033[0m", str(machine.freq() // 1000000) + "MHz", "(turbo)" if self.turbo else "(slow)")
        print("\t\033[7mFree memory:\033[0m", gc.mem_free(), "bytes")
        print("\t\033[7mBackground task:\033[0m", self.background_prog if self.background_prog else "none")

    def toggle_turbo(self):
        """
        Toggle the CPU speed between turbo and slow.
        """
        self.turbo = not self.turbo
        if self.turbo:
            machine.freq(self.cpu_speed_range["turbo"] * 1000000)
        else:
            machine.freq(self.cpu_speed_range["slow"] * 1000000)
        self.stats()

    def ed(self, filename=""):
        """
        Edit a file in the system.
        """
        buffer = ""
        if filename:
            try:
                with open(filename, "r") as file:
                    buffer = file.read()
            except OSError:
                pass
        print("\033[7msmolOS text editor\033[0m. Press Ctrl+C to quit.\n")
        while True:
            try:
                buffer += input("> ") + "\n"
            except KeyboardInterrupt:
                break
        with open(filename, "w") as file:
            file.write(buffer)
        print("\nSaved to", filename)

    def info(self, filename=""):
        """
        Display the information of a file.
        """
        if filename:
            try:
                file_info = os.stat(filename)
                print("\n\tFile:", filename)
                print("\tSize:", file_info[6], "bytes")
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
                with open(filename, "r") as file:
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
        if command == "on":
            self.system_led.value(1)
        elif command == "off":
            self.system_led.value(0)
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

# os = smolOS()
# os.boot()
