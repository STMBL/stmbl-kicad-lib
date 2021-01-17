from sexpdata import loads, Symbol
import sys,os
from pprint import pprint

pins = {}

if len(sys.argv) > 2:
  net_list_file = sys.argv[2]
  designator = sys.argv[1]

  print("nets: ", net_list_file)
  print("part: ", designator)

  net_list = open(net_list_file, "r")
  net_tree = loads(net_list.read())
  net_list.close()
  #print(net_tree[1][0])
  for n in net_tree:
    if isinstance(n, list):
      if n[0] == Symbol("nets"):
        #print(n[0])
        for net in n:
          name = ''
          function = ''
          pin = ''
          if isinstance(net, list):
            #print ("new")
            #print ()
            for item in net:
              if isinstance(item, list):
                if item[0] == Symbol("name"):
                  #some nets start with /, remove
                  name = item[1].replace('/', '',1)
                for item2 in item:
                  if isinstance(item2, list):
                    if item2[0] == Symbol("ref"):
                      if item2[1] == designator:
                        #print (name)
                        #print (item)
                        for item3 in item:
                          if isinstance(item3, list):
                              if item3[0] == Symbol("pin"):
                                pin = item3[1]
                              if item3[0] == Symbol("pinfunction"):
                                function = item3[1]
          if name != '' and function != '' and pin != '':
            pins[pin] = {"function": function, "name": name}
            #print(name)
            #print(function)
            #print(pin)
    #print (pins)

  pprint(pins)

  #NET	"IOBITS<43>"	LOC = "C13"	| IOSTANDARD = LVTTL | DRIVE = 24 | SLEW = SLOW ;	# Bank0 L63P_SCP7

else:
  print("usage: designator(U1) file.net")
