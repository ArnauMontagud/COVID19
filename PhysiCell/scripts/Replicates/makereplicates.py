# This script provides parameter samples from latin hypercube. The script creates
# a new folder (subdirectory) for each set of parameters, makes changes to a default
# configuration (.xml) file using specified parameter values (in an accompanying .txt file),
# copies the new config file into the new folder

import xml.etree.ElementTree as ET
from shutil import copyfile
import numpy as np
import os
import sys
import random
import time

os.chdir('../../')
def generate_parSamples(Replicas_number, fileOut):

    file = open(fileOut, "w")

    #Write file with samples
    for replica_id in range(Replicas_number):
        folder = 'output_R'+str("%02d"%replica_id)
        file.write("folder"+" "+folder+"\n")
        # set system time as seed
        # create a seed
        seed_value = random.randrange(sys.maxsize)
        omp_num_threads = 8
        # save this seed somewhere. So if you like the result you can use this seed to reproduce it
        file.write("random_seed"+" "+str(seed_value)+"\n")
        file.write("omp_num_threads"+" "+str(omp_num_threads)+"\n")
        file.write("#"+"\n")
    file.close()

def generate_configXML(params_file):
    xml_file_in = 'config/PhysiCell_settings.xml'
    xml_file_out = 'config/tmp.xml'
    copyfile(xml_file_in,xml_file_out)
    tree = ET.parse(xml_file_out)
    xml_root = tree.getroot()
    first_time = True
    output_dirs = []
    with open(params_file) as f:
        for line in f:
            print(len(line),line)
            if (line[0] == '#'):
                continue
            (key, val) = line.split()
            print(key,val)
            print('test')
            if (key == 'folder'):
                if first_time:  # we've read the 1st 'folder'
                    first_time = False
                else:  # we've read  additional 'folder's
                    # write the config file to the previous folder (output) dir and start a simulation
                    print('---write (previous) config file and start its sim')
                    tree.write(xml_file_out)
                xml_file_out = val + '/config.xml'  # copy config file into the output dir
                output_dirs.append(val)
            if ('.' in key):
                k = key.split('.')
                uep = xml_root
                for idx in range(len(k)):
                    uep = uep.find('.//' + k[idx])  # unique entry point (uep) into xml
                uep.text = val
            else:
                if (key == 'folder' and not os.path.exists(val)):
                    print('creating ' + val)
                    os.makedirs(val)
                xml_root.find('.//' + key).text = val

    tree.write(xml_file_out)
    print(output_dirs)

if __name__ == '__main__':
    file = "Seeds.txt"
    Replicas_number = 12
    # Generate samples from Latin Hypercube
    generate_parSamples(Replicas_number, file)
    # Create .xml and folder to each simulation
    generate_configXML(file)