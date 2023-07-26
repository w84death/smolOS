WORK
IN
PROGRESS

# smolOS User Manual
Specialized Microcontroller Oriented Lightweight Operating System

Latest documentation available at official homepage:

* smolOS homepage ([http](http://smol.p1x.in/os/). [https](https://smol.p1x.in/os/))

# Introduction
smolOS is a tiny and simple operating system for MicroPython giving the user POSIX-like environment to play and research. It came with a set of tools and demos. System should run on any MicroPython supproted board but it's tested and developed for XIAO RP2040,

# What is an OS?

Acording to the Wikipedia: "An operating system (OS) is system software that manages computer hardware and software resources, and provides common services for computer programs.". In my own mind it's just an interface that helps user interacts with a computer. In that case smolOS is an operating system. In more precise definition it is a shell and a collection of scripts that works on top of MicroPython systems. Imagine command.com to the MS-DOS, bash to Linux. For the end user it realy doesn't metter as long as it transforms a blank microcontroller into a working computer.

My first computer was 486 and a black and white CRT. I was using MS-DOS most of the time and get used to the commadn line interface. Now, some 25 years later I'm using Linux on all my computers and still prefer shell for basic stuff like editing configs, moving files or installing software. I wanted to keep that spirit in the smolOS.

# Simplicity, Universality

Shell. It's not MS-DOS (command.com) nor bash equvalent, it's something in between. I wanted to keep all the commands user friendly. For exampleinstead of UNIX `ls` and DOS `dir` I opted for `list`. From those three only the last says exactly what it does - lists files.

Files. Flat hierarhy. Microcontrollers have few MB of data at the best. It's not a place to store documents it's a place to store few scripts to run our project. Having directories makes thinkgs more complicated, users get confused where they are and the whole ".." to go back was always strange. That's why there is no `mkdir` or `cd`.

# System Overview

The whole system is in one file `smolos.py`. There are additional tools and demos that are optional.

- main file
- build editor
- additional tools

# Hardware

- any micropython board
- xiao rp2040
- neopixel 5x5 grid (display)
- photoresistor (input)
- neopixel LED (output)
- buzzer (sound)

# Manipulating Files

- flat hierarhy
- listing
- preview content
- removing
- renaming/moving
- copying

# Text Editor

- viewing a file
- editing a file

# Included Tools

- ansi
- life
- buzz
- pixel
- scroller
- plasma
- duck

# Running User Programs

- idea
- template

# What to do Next?

- fork
- customize/rename
- run on your custom board
- add features
- add tools
- share the code
