from machine import Pin, PWM
import time
import _thread

class smolBuzzer():
    def __init__(self):
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

        self.buzzer = PWM(Pin(3, Pin.OUT))
        self.play_note('C',0.2)
        print("smolBuzzer: buzz.play_note('A',0.2), buzz.play_demo(), buzz.stop().")
        
    def play_note(self,note,duration):
        if note != ' ':
            self.buzzer.freq(int(self.notes[note]*0.5))
            self.buzzer.duty_u16(10000)
            time.sleep(0.05) 
            self.buzzer.freq(self.notes[note])  # set the buzzer frequency
            self.buzzer.duty_u16(10000)            
        else:
            self.buzzer.duty_u16(0)

        time.sleep(duration)      # play the note for the desired duration
        self.buzzer.freq(int(self.notes[note]*0.5))
        self.buzzer.duty_u16(10000)
        time.sleep(0.05)
        
        self.buzzer.duty_u16(0) 

    def demo_thread(self):
        song0 = ['C', 'D', 'E', 'D', 'C', 'E', 'C', 'A', 'A', 'G', 'A', 'G', 'E', 'C', 'E', 'D']
        song1 = ['C', 'E', 'G', 'E', 'A', 'F', 'D', 'F', 'C', 'D', 'F', 'D', 'G', 'E', 'C', 'E']
        song2 = ['E', 'G', 'B', 'G', 'C', 'A', 'F', 'A', 'E', 'F', 'A', 'F', 'B', 'G', 'E', 'G']
        song3 = ['G', 'B', 'D', 'B', 'E', 'C', 'A', 'C', 'G', 'A', 'C', 'A', 'D', 'B', 'G', 'B']
        song4 = ['C', 'E', 'G', 'E', 'C', 'A', 'F', 'A', 'C', 'G', 'E', 'G', 'C', 'F', 'D', 'F', 'A', 'F', 'D', 'F', 'A', 'G', 'E', 'G', 'A', 'F', 'D', 'F', 'A', 'C', 'A', 'G']
        song5 = ['E', 'G', 'B', 'G', 'E', 'C', 'A', 'C', 'E', 'D', 'F', 'D', 'E', 'G', 'B', 'G', 'C', 'A', 'F', 'A', 'C', 'B', 'G', 'B', 'C', 'A', 'F', 'A', 'C', 'D', 'C', 'B']
        song6 = ['G', 'B', 'D', 'B', 'G', 'E', 'C', 'E', 'G', 'F', 'A', 'F', 'G', 'B', 'D', 'B', 'E', 'C', 'A', 'C', 'E', 'D', 'B', 'D', 'E', 'C', 'A', 'C', 'E', 'F', 'E', 'D']


        playlist = [song0,song1,song2,song3,song4,song5,song6]
        note_duration = 0.1
        repeat = 4
        
        while self.thread_running:
            no=0
            for song in playlist:
                if not self.thread_running:
                        return
                print("smoBuzzer: Track",no)
                for prog in range(repeat):
                    progress = "#"
                    for _ in range(prog):
                        progress += "#"
                    for _ in range(repeat-prog-1):
                        progress += "_"
                        
                    print("\t["+progress+"]")
                    for note in song:
                        if not self.thread_running:
                            return
                        self.play_note(note, note_duration)
                time.sleep(2)
                no+=1
    
    def play_demo(self):
        if not self.thread_running:
            self.thread_running = True
            _thread.start_new_thread(self.demo_thread,())
            print("smoBuzzer: Playing demo track...")
        else:
            print("smoBuzzer: Thread already in use. Kill other backround programs.")
            
    def stop(self):
        self.thread_running = False
        time.sleep(0.1) 
        self.buzzer.duty_u16(0)
        

buzz = smolBuzzer()
buzz.play_demo()