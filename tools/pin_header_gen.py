#!/usr/bin/env python
import sys
import time

pins = [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]

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

def top_pad_rr(name, x, y, size_x, size_y):
  return("  (pad " + str(name + 1) + " smd roundrect (at " + str(x) + " " + str(y) + ") (size " + str(size_x) + " " + str(size_y) + ") (layers F.Cu F.Mask) (roundrect_rratio 0.25))\n")

def top_pad(name, x, y, size):
  return("  (pad " + str(name + 1) + " smd circle (at " + str(x) + " " + str(y) + ") (size " + str(size) + " " + str(size) + ") (layers F.Cu F.Mask))\n")

def bot_pad_rr(name, x, y, size_x, size_y):
  return("  (pad " + str(name + 1) + " smd roundrect (at " + str(x) + " " + str(y) + ") (size " + str(size_x) + " " + str(size_y) + ") (layers B.Cu B.Mask) (roundrect_rratio 0.25))\n")

def bot_pad(name, x, y, size):
  return("  (pad " + str(name + 1) + " smd circle (at " + str(x) + " " + str(y) + ") (size " + str(size) + " " + str(size) + ") (layers B.Cu B.Mask))\n")


def pin_RM254_up_gen(pins, rows):
  rm = 2.54
  filename = "Pin_Header_RM" + str(rm) + "_" + str(rows) + "x" + str(pins) + "_UP"
  top_pad_size = 1.5
  bot_pad_size = 1.75
  drill_size = 1
  drill_pad_size = drill_size + 0.3

  with open(filename + ".kicad_mod", mode = "w+") as f:
    f.write(header("stmbl", filename))

    # outline
    f.write(rect(-rm / 2, -rm / 2, (rows - 1) * rm + rm / 2, rm * (pins - 1) + rm / 2))
    f.write(rect(-rm / 2, -rm / 2, rm / 2, rm / 2))
    
    for r in range(rows):
      for i in range(pins):
        if r == 0 and i == 0:
          f.write(bot_pad_rr(0, 0, 0, bot_pad_size, bot_pad_size))
          f.write(top_pad_rr(0, 0, 0, top_pad_size, top_pad_size))

        else:
          f.write(bot_pad(i * rows + r, r * rm, i * rm, bot_pad_size))
          f.write(top_pad(i * rows + r, r * rm, i * rm, top_pad_size))

        f.write(th_pad(i * rows + r, r * rm, i * rm, drill_pad_size, drill_size))

    f.write(footer())

def pin_RM254_smd_up_1x_gen(pins):
  rm = 2.54
  rows = 1
  filename = "Pin_Header_RM" + str(rm) + "_" + str(rows) + "x" + str(pins) + "_SMD_UP"
  pad_size_y = 1
  pad_size_x = 3

  with open(filename + ".kicad_mod", mode = "w+") as f:
    f.write(header("stmbl", filename))

    # outline
    f.write(rect(-rm / 2, -rm / 2, rm / 2, pins * rm - rm / 2))
    f.write(rect(-rm / 2, -rm / 2, rm / 2, rm / 2))
    
    for i in range(pins):
      if i % 2 == 0:
        f.write(top_pad_rr(i, 1.5, i * rm, pad_size_x, pad_size_y))
      else:
        f.write(top_pad_rr(i, -1.5, i * rm, pad_size_x, pad_size_y))

    f.write(footer())

def pin_RM254_smd_up_1x_inv_gen(pins):
  rm = 2.54
  rows = 1
  filename = "Pin_Header_RM" + str(rm) + "_" + str(rows) + "x" + str(pins) + "_SMD_INV_UP"
  pad_size_y = 1
  pad_size_x = 3

  with open(filename + ".kicad_mod", mode = "w+") as f:
    f.write(header("stmbl", filename))

    # outline
    f.write(rect(-rm / 2, -rm / 2, rm / 2, pins * rm - rm / 2))
    f.write(rect(-rm / 2, -rm / 2, rm / 2, rm / 2))
    
    for i in range(pins):
      if i % 2 == 0:
        f.write(top_pad_rr(i, -1.5, i * rm, pad_size_x, pad_size_y))
      else:
        f.write(top_pad_rr(i, 1.5, i * rm, pad_size_x, pad_size_y))

    f.write(footer())

def pin_RM254_smd_up_2x_gen(pins):
  rm = 2.54
  rows = 2
  filename = "Pin_Header_RM" + str(rm) + "_" + str(rows) + "x" + str(pins) + "_SMD_UP"
  pad_size_y = 1
  pad_size_x = 3

  with open(filename + ".kicad_mod", mode = "w+") as f:
    f.write(header("stmbl", filename))

    # outline
    f.write(rect(-3 * rm / 2, -rm / 2, rm / 2, pins * rm - rm / 2))
    f.write(rect(-rm / 2, -rm / 2, rm / 2, rm / 2))
    
    for i in range(pins):
      f.write(top_pad_rr(i * rows + 0, 1.5, i * rm, pad_size_x, pad_size_y))
      f.write(top_pad_rr(i * rows + 1, -rm - 1.5, i * rm, pad_size_x, pad_size_y))

    f.write(footer())


for p in pins: 
  pin_RM254_smd_up_1x_gen(p)
  pin_RM254_smd_up_1x_inv_gen(p)
  pin_RM254_smd_up_2x_gen(p)
  pin_RM254_up_gen(p, 1)
  pin_RM254_up_gen(p, 2)
