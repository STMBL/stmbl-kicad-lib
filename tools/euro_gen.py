#!/usr/bin/env python
import sys

pins = [2, 3, 4, 5, 6, 7, 8, 9, 10]


rm = 5.08
x_offset = 3.54
y_offset_top = -2
y_offset_bot = 10

rm = 3.81
x_offset = 2.3
y_offset_top = -4
y_offset_bot = 3

pad_size = 2.5
drill_pad_size = 1.8
drill_size = 1.5


prefix = "RM"
mid_fix = "_1x"
post_fix = "_UP"

for pin in pins:
    x = (pin - 1) * rm + x_offset
    filename = prefix + str(rm) + mid_fix + str(pin) + post_fix
    with open(filename + ".kicad_mod", mode = "xt") as f:
        f.write("(module stmbl:" + filename + " (layer F.Cu) (tedit 5B519F7C)\n")
        f.write("  (fp_text reference P1 (at 0 " + str(y_offset_top - 1.5) + ") (layer F.SilkS)\n")
        f.write("    (effects (font (size 1.5 1.5) (thickness 0.3)))\n")
        f.write("  )\n")
        f.write("  (fp_text value " + filename + " (at 0 " + str(y_offset_bot + 1.5) + ") (layer F.Fab)\n")
        f.write("    (effects (font (size 1 1) (thickness 0.15)))\n")
        f.write("  )\n")
        f.write("  (fp_line (start " + str(-x_offset) + " " + str(y_offset_top) + ") (end " + str(x) + " " + str(y_offset_top) + ") (layer F.SilkS) (width 0.15))\n")
        f.write("  (fp_line (start " + str(-x_offset) + " " + str(y_offset_bot) + ") (end " + str(x) + " " + str(y_offset_bot) + ") (layer F.SilkS) (width 0.15))\n")
        f.write("  (fp_line (start " + str(-x_offset) + " " + str(y_offset_top) + ") (end " + str(-x_offset) + " " + str(y_offset_bot) + ") (layer F.SilkS) (width 0.15))\n")
        f.write("  (fp_line (start " + str(x) + " " + str(y_offset_top) + ") (end " + str(x) + " " + str(y_offset_bot) + ") (layer F.SilkS) (width 0.15))\n")
        for i in range(pin):
            f.write("  (pad " + str(i + 1) + " thru_hole circle (at " + str(rm * i) + " 0) (size " + str(drill_pad_size) + " " + str(drill_pad_size) + ") (drill " + str(drill_size) + ") (layers *.Cu *.Mask))\n")
            f.write("  (pad " + str(i + 1) + " smd roundrect (at " + str(rm * i) + " 0) (size " + str(pad_size) + " " + str(pad_size) + ") (layers B.Cu B.Mask) (roundrect_rratio 0.25))\n")
        f.write(")\n")