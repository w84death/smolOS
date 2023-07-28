"""
Simple synthezator for 1-bit music

(c)2023/07 Krzysztof Krystian Jankowski
Homepage: https://smol.p1x.in/os/
"""

from machine import Pin, PWM
import time

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
    def __init__(self):
        self.name = "Buzz"
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
        self.msg("Initialized.")
        
    def play_note(self, note, duration):
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
    
    def demo(self, note_duration):
        self.msg("Playing demo.\nPress Ctrl+C to stop.\n")
        
        while True:
            try:
                no=0
                for song in SONGS:
                    self.msg(f"Track {no}")
                    for prog in range(REPEAT):
                        progress = "#"
                        for _ in range(prog):
                            progress += "#"
                        for _ in range(REPEAT-prog-1):
                            progress += "_"
                        self.msg(f"\t[{progress}]")
                        for note in song:
                            self.play_note(note, note_duration)
                    time.sleep(2)
                    no+=1
            except KeyboardInterrupt:
                self.stop()
                break
            
    def stop(self):
        time.sleep(0.1) 
        self.buzzer.duty_u16(0)

    def msg(self, message)
        print(f"{self.name} : {message}")

    def run(self, note_duration=NOTE_DURATION):
        self.demo(note_duration)

if __name__ == '__main__':
    buzz = Buzz()
    buzz.run()
