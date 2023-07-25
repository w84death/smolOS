from machine import Pin, PWM
import time
import _thread

# Define constants
BUZZER_PIN = 3
BUZZER_DUTY = 10000
NOTE_DURATION = 0.1
REPEAT = 4
SONGS = [
    ['C', 'D', 'E', 'D', 'C', 'E', 'C', 'A', 'A', 'G', 'A', 'G', 'E', 'C', 'E', 'D'],
    ['C', 'E', 'G', 'E', 'A', 'F', 'D', 'F', 'C', 'D', 'F', 'D', 'G', 'E', 'C', 'E'],
    ['E', 'G', 'B', 'G', 'C', 'A', 'F', 'A', 'E', 'F', 'A', 'F', 'B', 'G', 'E', 'G'],
    ['G', 'B', 'D', 'B', 'E', 'C', 'A', 'C', 'G', 'A', 'C', 'A', 'D', 'B', 'G', 'B'],
    ['C', 'E', 'G', 'E', 'C', 'A', 'F', 'A', 'C', 'G', 'E', 'G', 'C', 'F', 'D', 'F', 'A', 'F', 'D', 'F', 'A', 'G', 'E', 'G', 'A', 'F', 'D', 'F', 'A', 'C', 'A', 'G'],
    ['E', 'G', 'B', 'G', 'E', 'C', 'A', 'C', 'E', 'D', 'F', 'D', 'E', 'G', 'B', 'G', 'C', 'A', 'F', 'A', 'C', 'B', 'G', 'B', 'C', 'A', 'F', 'A', 'C', 'D', 'C', 'B'],
    ['G', 'B', 'D', 'B', 'G', 'E', 'C', 'E', 'G', 'F', 'A', 'F', 'G', 'B', 'D', 'B', 'E', 'C', 'A', 'C', 'E', 'D', 'B', 'D', 'E', 'C', 'A', 'C', 'E', 'F', 'E', 'D']
]

class Buzz:
    """
    A class to handle the Buzz functionalities.
    """
    def __init__(self):
        """
        Initialize the Buzz object.
        """
        self.thread_running = False
        self.notes = {
            'C': 261,
            'D': 294,
            'E': 329,
            'F': 349,
            'G': 392,
            'A': 440,
            'B': 494
        }
        self.buzzer = PWM(Pin(BUZZER_PIN, Pin.OUT))
        self.play_note('C', 0.2)
        print("smolBuzzer: buzz.play_note('A',0.2), buzz.play_demo(), buzz.stop().")
        
    def play_note(self, note, duration):
        """
        Play a specific note for a certain duration.
        """
        if note != ' ':
            self.buzzer.freq(int(self.notes[note]*0.5))
            self.buzzer.duty_u16(BUZZER_DUTY)
            time.sleep(0.05) 
            self.buzzer.freq(self.notes[note])
            self.buzzer.duty_u16(BUZZER_DUTY)
        else:
            self.buzzer.duty_u16(0)
        time.sleep(duration)
        self.buzzer.freq(int(self.notes[note]*0.5))
        self.buzzer.duty_u16(BUZZER_DUTY)
        time.sleep(0.05)
        self.buzzer.duty_u16(0)
    
    def demo_thread(self):
        """
        Play a demo of songs in a new thread.
        """
        while self.thread_running:
            no=0
            for song in SONGS:
                if not self.thread_running:
                    return
                print("smoBuzzer: Track",no)
                for prog in range(REPEAT):
                    progress = "#"
                    for _ in range(prog):
                        progress += "#"
                    for _ in range(REPEAT-prog-1):
                        progress += "_"
                    print("\t["+progress+"]")
                    for note in song:
                        if not self.thread_running:
                            return
                        self.play_note(note, NOTE_DURATION)
                time.sleep(2)
                no+=1
    
    def start_unthreaded(self):        
        """
        Start the demo in the current thread.
        """
        self.thread_running = True
        self.demo_thread()
        
    def start_threaded(self):
        """
        Start the demo in a new thread.
        """
        if not self.thread_running:
            self.thread_running = True
            _thread.start_new_thread(self.demo_thread,())
            print("smoBuzzer: Playing demo track...")
        else:
            print("smoBuzzer: Thread already in use. Kill other backround programs.")
            
    def stop(self):
        """
        Stop the demo.
        """
        self.thread_running = False
        time.sleep(0.1) 
        self.buzzer.duty_u16(0)

# To use this refactored code, you would do something like the following:
# buzz = Buzz()
# buzz.start_threaded()  # to start the demo in a new thread
# or
# buzz.start_unthreaded()  # to start the demo in the current thread
# buzz.stop() to stop the demo
