
# import numpy as np
# import pandas as pd
import json
import pprint as pp
import re
import os,sys

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


def print_test(*args):
    print("####################")
    print("SELF-TEST: %s" % args)
    print("--------------------")
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

def convert_block_groups_geojson_to_geoid_lut(geoid_data,**options):
    '''
    Purpose: generate LUT (look up table) of GEOIDs => polygons based on the block-groups.geojson file

    # Format:
     {
     "type": "FeatureCollection",
     "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
     "features": [
         { "type": "Feature",
           "properties":
               { "GEOID": "480139604021",
               #...
               }, 
      { 
        "type": "Polygon", 
        "coordinates": 
        [ [ 
          [ -98.484237, 28.957106 ], 
               #...
        ] ] 
       }, 

    i.e.
    geoidval = data['features'][0][properties][GEOID]
    polygon  = data['features'][0]['geometry']['coordinates']
    '''
    lut_dict = {}
    for index, feature in enumerate( geoid_data['features'] ):
        geoidval = feature['properties']['GEOID']
        #if ( feature['geometry']['type'] == "Polygon" ):
        if ( re.match(r"%s" % ".*Polygon.*", feature['geometry']['type']) ):

            lut_dict[ geoidval ] = {}
            lut_dict[ geoidval ]['geometry'] = {}
            lut_dict[ geoidval ]['geometry'] = feature['geometry']
        else:
            print("ERROR: missing entry Polygon on line %s" % (index))
            print(json.dumps( feature ))
            # TODO: this is bad, throw exception instead
            sys.exit()
            # TODO: placeholder for when proper error handling implemented
            return
    return lut_dict

def get_polygon_by_geoid( target_geoid, geoid_lut,**options):
    '''
    Purpose: return polygon definition for a geoid
    '''
    if( target_geoid not in geoid_lut ): 
        print("ERROR: GEOID %s not found in lookup table" % (target_geoid))
        # TODO: this is bad, throw exception instead
        system.exit()
        # TODO: placeholder for when proper error handling implemented
        return
    else: 
        # from convert_block_groups_geojson_to_geoid_lut :
        #+ lut_dict[ geoidval ]['geometry'] = feature['geometry']
        return geoid_lut[ target_geoid ]['geometry']



if(__name__ == '__main__'):
    #print_test()
    input_json_path="res/samples" + "/" + "geojson_blockgroup_lut.json"
    output_json_path="t/tmp/jsontest" + "/" + "out.json"
    in_json = retrieve_json_file(input_json_path, **options)
    print_test("see the loaded json:")
    print(json.dumps(in_json))
    print_test("dumping to file the json:")
    save_json_file(in_json, output_json_path, **options)
    # verify stored by loading and dumping
    print(json.dumps(
            retrieve_json_file(output_json_path, **options)
        ))


    # Test the geojson_blockgroup_lut table
    #+ create from sample
    #+ dump to file
    testdef_geoid_simple=0
    opt_generate_lut_file=0
    print_test("geoid LUT - create")

    geoid_path="res/samples"
    if(testdef_geoid_simple == 1):
        geoid_path=geoid_path + "/" "block-groups_entries_three.geojson"
    else:
        geoid_path=geoid_path + "/" "block-groups.geojson"
    output_geoid_lut_path = "t/tmp/geoidtest" + "/" + "geoid_lut.json"
    if( opt_generate_lut_file == 1 ):
        # TODO: validate the number of entries
        # create and dump
        # debug - file is large!
        tmpgeoiddata = retrieve_json_file(geoid_path, **options)
        # ^^^ debug ^^^ 
        print("status: loaded raw geoid data");
        geoid_lut_created = convert_block_groups_geojson_to_geoid_lut(
                 #retrieve_json_file(geoid_path, **options),
                 tmpgeoiddata,
                 **options)
        # vvvv no need, verifying from file load vvvv
        # print(json.dumps( geoid_lut_created ))
        print("status: dumping to file %s" % (output_geoid_lut_path) );
        save_json_file(geoid_lut_created, output_geoid_lut_path, **options)
    else:
        print("SKIPPING ...")
    # load and verify
    print("Loading LUT from file output_geoid_lut_path")
    if(testdef_geoid_simple == 1):
        print(json.dumps(
            retrieve_json_file(output_geoid_lut_path, **options),
            ))
    # pp.pprint(
    #         convert_block_groups_geojson_to_geoid_lut(
    #         retrieve_json_file(geoid_path, **options), **options)
    #             )
    print_test("geoid LUT - load")
    sample_geod = "480139604021"
    # TODO: load from file
    geoid_lut_loaded = retrieve_json_file(output_geoid_lut_path, **options)
    outpoly = get_polygon_by_geoid( sample_geod, geoid_lut_loaded, **options)
    pp.pprint( outpoly )


