


branch yoinkbird:
this is for the architecture


inputs: - download from somewhere
  res/samples/ConstructionDataGeocodeATX_py.csv
  res/samples/block-groups.geojson
  sample_multipolygon.json
outputs: - generated from jsonlib in various convoluted ways
  # simple self-test for loading,dumping json
  t/tmp/jsontest/out.json
  # geoid -> polygon look up table
  t/tmp/geoidtest/geoid_lut.json
  # generate the javascript,json file containing polygons and scores
  #+ the '.js' contains the content of the '.json' file
  t/tmp/webgentest/out.js
  t/tmp/webgentest/out.json
