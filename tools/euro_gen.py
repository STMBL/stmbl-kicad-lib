#!/usr/bin/env python
import sys
import time

pins = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

def line(x0, y0, x1, y1, layer = "F.SilkS"):
    return("  (fp_line (start " + str(x0) + " " + str(y0) + ") (end "  + str(x1) + " " + str(y1) + ") (layer " + layer + ") (width 0.15))\n")

def rect(x0, y0, x1, y1, layer = "F.SilkS"):
    return(line(x0, y0, x1, y0, layer) + line(x1, y0, x1, y1, layer) + line(x1, y1, x0, y1, layer) + line(x0, y1, x0, y0, layer))

def arc(x0, y0, x1, y1, a, layer = "F.SilkS"):
    return("  (fp_arc (start " + str(x0) + " " + str(y0) + ") (end "  + str(x1) + " " + str(y1) + ") (angle " + str(a) + ") (layer " + layer + ") (width 0.15))\n")

def circle(x0, y0, x1, y1, layer = "F.SilkS"):
    return("  (fp_circle (center " + str(x0) + " " + str(y0) + ") (end "  + str(x1) + " " + str(y1) + ") (layer " + layer + ") (width 0.15))\n")

def header(libname, partname):
    return(
        "(module " + libname + ":" + partname + " (layer F.Cu) (tedit " + format(int(time.time()), 'x') + ")\n" +
        "  (fp_text reference P1 (at 0 2.5) (layer F.SilkS) hide (effects (font (size 1.5 1.5) (thickness 0.3))))\n" +
        "  (fp_text value " + partname + " (at 0 -2) (layer F.SilkS) hide (effects (font (size 1 1) (thickness 0.15))))\n"
    )

def footer():
    return(")\n")

def th_pad(name, x, y, size, drill):
    return("  (pad " + str(name + 1) + " thru_hole circle (at " + str(x) + " " + str(y) + ") (size " + str(size) + " " + str(size) + ") (drill " + str(drill) + ") (layers *.Cu *.Mask))\n")

def bot_pad(name, x, y, size):
    return("  (pad " + str(name + 1) + " smd roundrect (at " + str(x) + " " + str(y) + ") (size " + str(size) + " " + str(size) + ") (layers B.Cu B.Mask) (roundrect_rratio 0.25))\n")


def eurostyle_RM508_up_gen(pins):
    rm = 5.08
    filename = "RM" + str(rm) + "_1x" + str(pins) + "_UP"
    pad_size = 2.5
    drill_size = 1.5
    drill_pad_size = drill_size + 0.3

    with open(filename + ".kicad_mod", mode = "w+") as f:
        f.write(header("stmbl", filename))

        # outline
        f.write(rect(-3.5, 3.75, rm * (pins - 1) + 3.5, -4.75))
        f.write(line(-3.5, -4.5, rm * (pins - 1) + 3.5, -4.5))

        # plug outline
        f.write(rect(-rm / 2, 3.75, rm * (pins - 1) + rm / 2, -11.25, "Margin"))
        
        f.write(line(-rm / 2, -4, rm * (pins - 1) + rm / 2, -4))
        f.write(line(-rm / 2, -4, -rm / 2, 2.5))
        f.write(line(rm * (pins - 1) + rm / 2, -4, rm * (pins - 1) + rm / 2, 2.5))
        
        for i in range(pins):
            f.write(th_pad(i, rm * i, 0, drill_pad_size, drill_size))
            f.write(bot_pad(i, rm * i, 0, pad_size))
            f.write(arc(rm * i, 0, rm * i - rm / 2, 2.5, -45))
            f.write(arc(rm * i, 0, rm * i + rm / 2, 2.5, 45))

            f.write(rect(rm * i - 1.25, 1, rm * i + 1.25, -1.25, "Margin"))

        f.write(footer())


def eurostyle_RM508_gen(pins):
    rm = 5.08
    filename = "RM" + str(rm) + "_1x" + str(pins)
    pad_size = 2.5
    drill_size = 1.5
    drill_pad_size = drill_size + 0.3

    with open(filename + ".kicad_mod", mode = "w+") as f:
        f.write(header("stmbl", filename))

        # outline
        f.write(rect(-3.5, 10, rm * (pins - 1) + 3.5, -2))
        f.write(line(-3.5, 8, rm * (pins - 1) + 3.5, 8))

        # plug outline
        f.write(line(-rm / 2, 20, rm * (pins - 1) + rm / 2, 20, "Margin"))
        f.write(line(-rm / 2, 20, -rm / 2, 10, "Margin"))
        f.write(line(rm * (pins - 1) + rm / 2, 20, rm * (pins - 1) + rm / 2, 10, "Margin"))
        
        for i in range(pins):
            f.write(th_pad(i, rm * i, 0, drill_pad_size, drill_size))
            f.write(bot_pad(i, rm * i, 0, pad_size))
            f.write(circle(rm * i, 14, rm * i, 14 - 1.5, "Margin"))
            f.write(line(rm * i - 1.5, 14, rm * i + 1.5, 14, "Margin"))

        f.write(footer())

def eurostyle_RM350_up_gen(pins):
    rm = 3.5
    filename = "RM" + str(rm) + "_1x" + str(pins) + "_UP"
    pad_size = 2.5
    drill_size = 1.5
    drill_pad_size = drill_size + 0.3

    with open(filename + ".kicad_mod", mode = "w+") as f:
        f.write(header("stmbl", filename))

        # outline
        f.write(rect(-2.5, 3, rm * (pins - 1) + 2.5, -4))

        # plug outline
        f.write(rect(-rm / 2, 6.5, rm * (pins - 1) + rm / 2, -5, "Margin"))
               
        for i in range(pins):
            f.write(th_pad(i, rm * i, 0, drill_pad_size, drill_size))
            f.write(bot_pad(i, rm * i, 0, pad_size))
            f.write(line(rm * i - rm / 2, 3, rm * i - rm / 2, -4))
            f.write(line(rm * i + rm / 2, 3, rm * i + rm / 2, -4))
            f.write(line(rm * i - rm / 2, -3, rm * i - rm / 2 + 1, -3))
            f.write(line(rm * i + rm / 2, -3, rm * i + rm / 2 - 1, -3))

            f.write(rect(rm * i - 1, 4, rm * i + 1, 1.5, "Margin"))

        f.write(footer())

def eurostyle_RM350_gen(pins):
    rm = 3.5
    filename = "RM" + str(rm) + "_1x" + str(pins)
    pad_size = 2.5
    drill_size = 1.5
    drill_pad_size = drill_size + 0.3

    with open(filename + ".kicad_mod", mode = "w+") as f:
        f.write(header("stmbl", filename))

        # outline
        f.write(rect(-2.5, 8, rm * (pins - 1) + 2.5, -1.25))

        # plug outline
        f.write(line(-rm / 2, 17, rm * (pins - 1) + rm / 2, 17, "Margin"))
        f.write(line(-rm / 2, 17, -rm / 2, 8, "Margin"))
        f.write(line(rm * (pins - 1) + rm / 2, 17, rm * (pins - 1) + rm / 2, 8, "Margin"))
        
        for i in range(pins):
            f.write(th_pad(i, rm * i, 0, drill_pad_size, drill_size))
            f.write(bot_pad(i, rm * i, 0, pad_size))
            f.write(circle(rm * i, 12, rm * i, 12 - 1.5, "Margin"))
            f.write(line(rm * i - 1.5, 12, rm * i + 1.5, 12, "Margin"))

        f.write(footer())


def eurostyle_RM381_up_gen(pins):
    rm = 3.81
    filename = "RM" + str(rm) + "_1x" + str(pins) + "_UP"
    pad_size = 2.5
    drill_size = 1.5
    drill_pad_size = drill_size + 0.3

    with open(filename + ".kicad_mod", mode = "w+") as f:
        f.write(header("stmbl", filename))

        # outline
        f.write(rect(-2.5, 3, rm * (pins - 1) + 2.5, -4))

        # plug outline
        f.write(rect(-rm / 2, 6.5, rm * (pins - 1) + rm / 2, -5, "Margin"))
       
        for i in range(pins):
            f.write(th_pad(i, rm * i, 0, drill_pad_size, drill_size))
            f.write(bot_pad(i, rm * i, 0, pad_size))
            f.write(line(rm * i - rm / 2, 3, rm * i - rm / 2, -4))
            f.write(line(rm * i + rm / 2, 3, rm * i + rm / 2, -4))
            f.write(line(rm * i - rm / 2, -3, rm * i - rm / 2 + 1, -3))
            f.write(line(rm * i + rm / 2, -3, rm * i + rm / 2 - 1, -3))

            f.write(rect(rm * i - 1, 4, rm * i + 1, 1.5, "Margin"))

        f.write(footer())

def eurostyle_RM381_gen(pins):
    rm = 3.81
    filename = "RM" + str(rm) + "_1x" + str(pins)
    pad_size = 2.5
    drill_size = 1.5
    drill_pad_size = drill_size + 0.3

    with open(filename + ".kicad_mod", mode = "w+") as f:
        f.write(header("stmbl", filename))

        # outline
        f.write(rect(-2.5, 8, rm * (pins - 1) + 2.5, -1.25))

        # plug outline
        f.write(line(-rm / 2, 17, rm * (pins - 1) + rm / 2, 17, "Margin"))
        f.write(line(-rm / 2, 17, -rm / 2, 8, "Margin"))
        f.write(line(rm * (pins - 1) + rm / 2, 17, rm * (pins - 1) + rm / 2, 8, "Margin"))
        
        for i in range(pins):
            f.write(th_pad(i, rm * i, 0, drill_pad_size, drill_size))
            f.write(bot_pad(i, rm * i, 0, pad_size))
            f.write(circle(rm * i, 12, rm * i, 12 - 1.5, "Margin"))
            f.write(line(rm * i - 1.5, 12, rm * i + 1.5, 12, "Margin"))

        f.write(footer())


for p in pins:
    eurostyle_RM508_up_gen(p)
    eurostyle_RM508_gen(p)
    eurostyle_RM350_up_gen(p)
    eurostyle_RM350_gen(p)
    eurostyle_RM381_up_gen(p)
    eurostyle_RM381_gen(p)
