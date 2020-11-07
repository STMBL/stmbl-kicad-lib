from sexpdata import loads, Symbol
import sys,os

net_list_files = []
pcb_file = ""

place_all = []
place_bom = []
bom_all = []
bom_place = []
bom_reduced = []

part_map = [
  ("10u", "stmbl:CP_D6.3", "C134747"),
  ("12pf", "stmbl:C_0603", "C38523"),
  ("100n", "stmbl:C_0603", "C14663"),
  ("10n", "stmbl:C_0603", "C57112"),
  ("33n", "stmbl:C_0603", "C21117"),
  ("18p", "stmbl:C_0603", "C1647"),
  ("10u", "stmbl:C_0805", "C15850"),
  ("1u", "stmbl:C_1206", "C13832"),
  ("16M", "stmbl:Crystal_SMD_3225_4Pads", "C13738"),
  ("25M", "stmbl:Crystal_SMD_3225_4Pads", "C9006"),
  ("12M", "stmbl:Crystal_SMD_3225_4Pads", "C9002"),
  ("12pf", "stmbl:C_0603", "C38523"),
  ("SMCJ75A", "stmbl:D_SMC", "C184464"),
  ("STM32F303RCTx", "stmbl:LQFP-64_12x12_Pitch0.5mm", "C65361"),
  ("4.7u 1.5A", "stmbl:MWSA0503", "C408410"),
  ("22", "stmbl:R_0603", "C23345"),
  ("1.5k", "stmbl:R_0603", "C22843"),
  ("1k", "stmbl:R_0603", "C21190"),
  ("2.7k", "stmbl:R_0603", "C13167"),
  ("30k", "stmbl:R_0603", "C22984"),
  ("56k", "stmbl:R_0603", "C23206"),
  ("10k", "stmbl:R_0603", "C25804"),
  ("100k", "stmbl:R_0603", "C25803"),
  ("EMI", "stmbl:R_0603", "C1034"),
  ("EMI", "stmbl:R_0805", "C1017"),
  ("120", "stmbl:R_0603", "C22787"),
  ("5.1", "stmbl:R_0603", "C25197"),
  ("15k", "stmbl:R_0603", "C22809"),
  ("5.1k", "stmbl:R_0603", "C23186"),
  ("560", "stmbl:R_0603", "C23204"),
  ("22k", "stmbl:R_0603", "C31850"),
  ("470", "stmbl:R_0603", "C23179"),
  ("200", "stmbl:R_0603", "C8218"),
  ("2.2", "stmbl:R_0603", "C22939"),
  ("0.002", "stmbl:R_2512", "C60923"),
  ("s210", "stmbl:SMA_Standard", "C14996"),
  ("SED10070GG", "stmbl:SO-8FL", "C396083"),
  ("B5819W", "stmbl:SOD-123", "C8598"),
  ("RS485", "stmbl:SOIC-8-N", "C6855"),
  ("LM358", "stmbl:SOIC-8-N", "C7950"),
  ("eg3112", "stmbl:SOIC-8-N", "C383538"),
  ("XL7026", "stmbl:SOIC-8-POWER", "C89529"),
  ("XC6206P332MR", "stmbl:SOT-23", "C5446"),
  ("AO3400A", "stmbl:SOT-23", "C20917"),
  ("USBLC6-4SC6", "stmbl:SOT-23-6", "C85364"),
  ("MP2359", "stmbl:SOT-23-6", "C14259"),
  ("100u 1A", "stmbl:SWRB1204S", "C169400"),
]

rot_package = [("stmbl:QFN-28_EP_5x5_Pitch0.5mm", -90.0), ("stmbl:SOT-223", 180.0), ("stmbl:SOIC-16", -90.0), ("stmbl:SOT-23-5", -180.0), ("stmbl:SOT-23-6", -180.0), ("stmbl:SOT-23", -180.0), ("stmbl:SOIC-8-N", -90.0), ("stmbl:SOIC-8-POWER", -90.0), ("stmbl:Oscillator_SMD_0603_4Pads", -90.0), ("stmbl:LQFP-48_7x7mm_Pitch0.5mm", -90.0), ("stmbl:LQFP-64_12x12_Pitch0.5mm", -90.0), ("stmbl:CP_D6.3", -180.0), ("stmbl:SWRB1204S", -180.0), ("stmbl:MWSA0503", -180.0), ("stmbl:WS2812B-3535", 180.0), ("stmbl:wsp2812b", 180.0)]
rot_part = [("C383538", 90.0), ("C123083", 90.0)]

package_remap = [("R_0805", "0805"), ("R_0603", "0603"), ("R_0402", "0402"), ("C_0805", "0805"), ("C_0603", "0603"), ("C_0402", "0402")]

# ("C37448", -90.0), ("C9669", -90.0)

def remap_footprint(footprint):
  for f in package_remap:
    if f[0] == footprint:
      footprint = f[1]
  return footprint 

def parse_module(module):
  if isinstance(module[1], Symbol):
    package = module[1]._val
  else:
    package = module[1]
  x = ""
  y = ""
  a = ""
  ref = ""
  layer = ""
  attr = ""
  for n in module[2:]:
    if isinstance(n, list):
      if n[0] == Symbol('layer'):
        if isinstance(n[1], Symbol):
          layer = n[1]._val
        else:
          layer = n[1]
        if layer == "F.Cu":
          layer = "top"
        else:
          layer = "bottom"
      if n[0] == Symbol('at'):
        x = n[1]
        y = n[2]
        if len(n) > 3:
          a = n[3]
        else:
          a = "0"
      if n[0] == Symbol('attr'):
        if isinstance(n[1], Symbol):
          attr = n[1]._val
        else:
          attr = n[1]
      if n[0] == Symbol('fp_text'):
        if n[1] == Symbol('reference'):
          if isinstance(n[2], Symbol):
            ref = n[2]._val
          else:
            ref = n[2]
  for p in rot_package: 
    if p[0] == package:
      a = float(a) + p[1]
  for p in bom_all:
    if p[0] == ref:
      for lp in rot_part:
        if lp[0] == p[3]:
          a = float(a) + lp[1]
          #print("rotate", p[3], p[0])
  place_all.append((ref, package, layer, attr, x, y, a))

def parse_place(node):
  if isinstance(node, list):
    for n in node:
      if isinstance(n, list):
        if n[0] == Symbol('module'):
          parse_module(n)

def parse_comp(comp):
  if isinstance(comp, list):
    ref = ""
    val = ""
    footprint = ""
    lcsc = ""
    mfg = ""
    mfg_no = ""
    src = ""
    tol = ""
    vol = ""
    for n in comp:
      if n[0] == Symbol("ref"):
        if isinstance(n[1], Symbol):
          ref = n[1]._val
        else:
          ref = n[1]
      if n[0] == Symbol("value"):
        if isinstance(n[1], Symbol):
          val = n[1]._val
        else:
          val = n[1]
      if n[0] == Symbol("footprint"):
        if isinstance(n[1], Symbol):
          footprint = n[1]._val
        else:
          footprint = n[1]
      if n[0] == Symbol("fields"):
        for c in n[1:]:
          if c[0] == Symbol("field"):
            if c[1][0] == Symbol("name"):
              if c[1][1] == Symbol("LCSC") or c[1][1] == "LCSC":
                if isinstance(c[2], Symbol):
                  lcsc = c[2]._val
                else:
                  lcsc = c[2]
              if c[1][1] == Symbol("Manufacturer") or c[1][1] == "Manufacturer":
                if isinstance(c[2], Symbol):
                  mfg = c[2]._val
                else:
                  mfg = c[2]
              if c[1][1] == Symbol("Manufacturer No") or c[1][1] == "Manufacturer No":
                if isinstance(c[2], Symbol):
                  mfg_no = c[2]._val
                else:
                  mfg_no = c[2]
              if c[1][1] == Symbol("Source") or c[1][1] == "Source":
                if isinstance(c[2], Symbol):
                  src = c[2]._val
                else:
                  src = c[2]
              if c[1][1] == Symbol("Tolerance") or c[1][1] == "Tolerance":
                if isinstance(c[2], Symbol):
                  tol = c[2]._val
                else:
                  tol = c[2]
              if c[1][1] == Symbol("Voltage") or c[1][1] == "Voltage":
                if isinstance(c[2], Symbol):
                  vol = c[2]._val
                else:
                  vol = c[2]
    if lcsc == "":
      for p in part_map:
        if val == p[0] and footprint == p[1]:
          lcsc = p[2]
          print("map " + ref + " " + val + " " + footprint + " => " + lcsc)
    if footprint != "":
      bom_all.append([ref, val, footprint, lcsc, mfg, mfg_no, src, tol, vol, 1])

def parse_net(node):
  if isinstance(node, list):
    for n in node:
      if isinstance(n, list):
        if n[0] == Symbol("components"):
          for c in n[1:]:
            if c[0] == Symbol("comp"):
              parse_comp(c[1:])

if len(sys.argv) > 2:
  pcb_file = sys.argv[len(sys.argv) - 1]
  net_list_files = sys.argv[1:len(sys.argv) - 1]

  print("pcb: ", pcb_file)
  print("nets: ", net_list_files)

  pcb = open(pcb_file, "r")
  pcb_tree = loads(pcb.read())
  pcb.close()

  for net_list_file in net_list_files:
    net_list = open(net_list_file, "r")
    net_tree = loads(net_list.read())
    net_list.close()
    parse_net(net_tree)

  parse_place(pcb_tree)

  for p in place_all:
    found = 0
    for b in bom_all:
      if p[0] == b[0]:
        found = 1
    if found == 1:
      place_bom.append(p)
    else:
      print(p[0] + " not in net")

  for b in bom_all:
    found = 0
    for p in place_bom:
      if b[0] == p[0]:
        found = 1
    if found == 1:
      bom_place.append(b)
    else:
      print(b[0] + " not in pcb")

  for b in bom_place:
    found = 0
    if len(bom_reduced) > 0:
      for b2 in bom_reduced:
        if b2[1] == b[1] and b2[2] == b[2] and b2[3] == b[3] and b2[4] == b[4] and b2[5] == b[5] and b2[6] == b[6] and b2[7] == b[7] and b2[8] == b[8]:
          b2[0] += " " + b[0]
          found = 1
          b2[9] += 1
    if found == 0:
      bom_reduced.append(b)

  place_file = open("place.csv", "w")
  place_file.write("Designator,Mid X,Mid Y,Layer,Rotation\n")

  place_bom = sorted(place_bom, key = lambda p: p[0])
  for p in place_bom:
    place_file.write(p[0] + ", " + str(p[4]) + ", " + str(p[5] * -1.0) + ", " + p[2] + ", " + str(p[6]) + "\n")
  place_file.close()

  bom_file = open("bom.csv", "w")
  bom_file.write("Comment,Designator,Footprint,LCSC,Manufacturer,Manufacturer_No,Source,Tolerance,Voltage,Qty\n")

  bom_reduced = sorted(bom_reduced, key = lambda p: p[2])
  for b in bom_reduced:
    #print("(\"" + str(b[1]) + "\", \"" + b[2] + "\", \"" + b[3] + "\"),")
    bom_file.write("\"" + str(b[1]) + " " + remap_footprint(b[2].split(":")[1]) + "\", \"" + b[0] + "\", \"" + remap_footprint(b[2].split(":")[1]) + "\", " + b[3] + ", " + b[4] + ", " + str(b[5]) + ", " + str(b[6]) + ", " + str(b[7]) + ", " + str(b[8]) + ", " + str(b[9]) + "\n")
  bom_file.close()
  # for net_list_file in net_list_files:
  #   f = open(net_list_file, "r")
  #   f_tree = loads(f.read()))
  #   f.close()
else:
  print("usage: bom_pos.py .net .net ... .kicad_pcb")