from buzzer import Buzz
from pixel import neo_pixel
from plasma import neo_plasma

plasma = neo_plasma()
plasma.demo()

pixel0 = neo_pixel(12)
pixel0.color((255,64,64))

pixel1 = neo_pixel(3)
pixel1.color((255,64,64))

buzz=Buzz(4)
buzz.start(False)
