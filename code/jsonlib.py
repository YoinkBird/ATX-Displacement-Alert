
# import numpy as np
# import pandas as pd
import json
import pprint as pp
import re

# hard-coded globals
resource_dir = "output"
if __name__ == '__main__':
    # global options
    options = {
            'graphics' : 0, # 0 - disable, 1 - enable
            'verbose' : 0, # -1 - absolutely silent 0 - minimal info, 1+ - increasing levels
            }


    # src: https://docs.python.org/3/howto/argparse.html#id1
    import argparse
    # if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--graphics', type=int, default=0) # action="store_true", default=False)
    parser.add_argument('--verbose', type=int, default=0)
    args = parser.parse_args()
    # "args" defined with 'default=<>', no need for a conditional
    options['graphics'] = args.graphics
    options['verbose'] = args.verbose


def print_test():
    print("hi")
    return("hi")

# open and return loaded json file
def retrieve_json_file(filename, **options):
    import json
    verbose = options['verbose']

    # TODO: convert this, want to force everything in one dir. tmp:
    # filepath=("%s/%s" % (resource_dir, filename))
    filepath = filename
    if( verbose >= 1):
        print("" + filepath)

    # open file as json
    loadedjson = str()
    with open(filepath, 'r') as infile:
       loadedjson = json.load(infile)

    # return native object
    return loadedjson

# DUPLICATE from server.py
# save json to file for consumption by whatever else needs it
def save_json_file(response_json, filename, **options):
    verbose = options['verbose']
    if( verbose >= 1):
        print("# save to file")
    # tmp:
    # filepath=("%s/%s" % (resource_dir, filename))
    filepath = filename
    # if ( quiet != 1):
    #     print("mock-response sending to : " + filepath)
    with open(filepath, 'w') as outfile:
       json.dump(response_json, outfile)

    return filename

if(__name__ == '__main__'):
    #print_test()
    input_json_path="res/samples" + "/" + "geojson_blockgroup_lut.json"
    output_json_path="t/tmp/jsontest" + "/" + "out.json"
    in_json = retrieve_json_file(input_json_path, **options)
    print("SELF-TEST: see the loaded json:")
    print(json.dumps(in_json))
    print("SELF-TEST: dumping to file the json:")
    save_json_file(in_json, output_json_path, **options)
    # verify stored by loading and dumping
    print(json.dumps(
            retrieve_json_file(output_json_path, **options)
        ))
