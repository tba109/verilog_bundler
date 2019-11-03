import argparse
import json
import os.path
import numpy as np
import ClassVerilogBundle

def generate_fan_out(cvi,fname_inc):
    s = ''
    s = s + 'module ' + cvi.bundle_name + '_fan_out\n'
    s = s + '  (\n'
    s = s + '   ' + 'iface' + ',\n'
    for el in cvi.elements: 
        s = s + '   ' + el + ',\n'
    s = s[:-2] + '\n  );\n\n'
    s = s + '`include \"' + fname_inc + '\"\n'
    s = s + '\n'
    s = s + '   input [' + str(cvi.bundle_width-1) + ':0] ' + 'bundle' + ';\n'
    for el,wi in zip(cvi.elements,cvi.width):
        s = s + '   output [' + str(wi-1) + ':0] ' + el + ';\n'
    s = s + '\n'
    for el,istart,istop in zip(cvi.elements,cvi.start_pos,cvi.stop_pos):
        s = s + 'assign ' + el + ' = iface[' + str(istop) + ':' + str(istart) + '];\n'
    s = s + '\nendmodule\n'
    return s


def generate_fan_in(cvi,fname_inc):
    s = ''
    s = s + 'module ' + cvi.bundle_name + '_fan_in\n'
    s = s + '  (\n'
    s = s + '   ' + 'iface' + ',\n'
    for el in cvi.elements: 
        s = s + '   ' + el + ',\n'
    s = s[:-2] + '\n  );\n\n'
    s = s + '`include \"' + fname_inc + '\"\n'
    s = s + '\n'
    s = s + '   output [' + str(cvi.bundle_width-1) + ':0] ' + 'iface' + ';\n'
    for el,wi in zip(cvi.elements,cvi.width):
        s = s + '   input [' + str(wi-1) + ':0] ' + el + ';\n'
    s = s + '\n'
    s = s + 'assign ' + cvi.bundle_name + ' = \n'
    s = s + '  {\n' 
    s = s + '   {' + str(cvi.zero_pad_width) + '{1\'b0}},\n'
    for el in cvi.elements:
        s = s + '   ' + el + ',\n'
    s = s[:-2] + '\n'
    s = s + '  };\n\n'
    s = s + 'endmodule\n'
    return s
        
def generate_inc(cvi): 
    s = '// Widths\n'
    s = s + 'localparam\n'
    for el,wi in zip(cvi.elements,cvi.width):
        s = s + '  L_WIDTH_' + cvi.bundle_name.upper() + '_' + "{:<16s}".format(el.upper(),' ') + '= ' + str(wi) + ',\n'
    s = s[:-2] + ';\n\n'
    # Start position
    s = s + '// Start position = Previous start + Width\n'
    s = s + 'localparam \n'
    for el,sp in zip(cvi.elements,cvi.start_pos):
        s = s + '  L_START_POS_' + cvi.bundle_name.upper() + '_' + "{:<16s}".format(el.upper(),' ') + '= ' + str(sp) + ',\n'
    s = s[:-2] + ';\n\n'
    # Stop position
    s = s + '// Start position = Previous start + Width\n'
    s = s + 'localparam \n'
    for el,sp in zip(cvi.elements,cvi.stop_pos):
        s = s + '  L_STOP_POS_' + cvi.bundle_name.upper() + '_' + "{:<16s}".format(el.upper(),' ') + '= ' + str(sp) + ',\n'
    s = s[:-2] + ';\n\n'
    # Zero pad and bundle width
    s = s + '// Zero pad width and bundle width\n'
    s = s + 'localparam L_WIDTH_' + cvi.bundle_name.upper() + '_ZERO_PAD = ' + str(cvi.zero_pad_width) + ';\n'
    s = s + 'localparam L_WIDTH_' + cvi.bundle_name.upper() +  ' = ' + str(cvi.bundle_width) + ';\n' 
    return s
    
def main():
    parser = argparse.ArgumentParser(description='Auto generate Verilog 2001 code to define bundle. Output files are written to the same location as the json file')
    parser.add_argument('--json',type=str,help='full path to json bundle defintion file')
    args = parser.parse_args()
    
    try:
        fin = open(args.json,'r')
    except: 
        print('Error: could not open ',args.json)
        return -1
    print()
    
    path = os.path.dirname(args.json) + '/'
    print("path = " + path)
    print("")
    
    bundle = json.load(fin)

    cvi = ClassVerilogBundle.ClassVerilogBundle(bundle[0])
    cvi.printClass()
    print('\n\n')
    
    # Generate the include file
    s_inc = generate_inc(cvi)
    print(s_inc)
    fname_inc = cvi.bundle_name + '_inc.v'
    try:
        fout_inc = open(path + fname_inc,'w')
    except:
        print("Error: could not open ",fname_inc," for writing")
        return -1
    
    # Generate the fan in file
    s_fan_in = generate_fan_in(cvi,fname_inc)
    print(s_fan_in)
    fname_fan_in = cvi.bundle_name + '_fan_in.v'
    try:
        fout_fan_in = open(path + fname_fan_in,'w')
    except:
        print("Error: could not open ",fname_fan_in," for writing")
        return -1
    
    # Generate the fan out file
    s_fan_out = generate_fan_out(cvi,fname_inc)
    print(s_fan_out)
    fname_fan_out = cvi.bundle_name + '_fan_out.v'
    try:
        fout_fan_out = open(path + fname_fan_out,'w')
    except:
        print("Error: could not open ",fname_fan_out," for writing")
        return -1
        
    # Write the files
    fout_inc.write(s_inc)
    fout_fan_in.write(s_fan_in)
    fout_fan_out.write(s_fan_out)
    
    # Wrap up 
    fin.close()
    fout_inc.close()
    fout_fan_in.close()
    fout_fan_out.close()
    
if __name__ == "__main__":
    main()

