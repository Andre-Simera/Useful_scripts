
######### INITIALISE QGIS STANDALONE ################

import sys
from qgis.core import (
     QgsApplication, 
     QgsProcessingFeedback, 
     QgsVectorLayer,
     QgsField,
     QgsFields,
     QgsProperty,
     QgsProcessing,
     QgsProcessingFeatureSourceDefinition,
     QgsProcessingOutputLayerDefinition
)

#start QGIS instance without GUI
#Make sure the prefix is correct. Even though QGIS is in '/usr/share/qgis',
#the prefix needs to be '/usr' (assumes Debian OS)

QgsApplication.setPrefixPath('/usr', True)
myqgs = QgsApplication([], False)
myqgs.initQgis()

######### INITIALISE THE PROCESSING FRAMEWORK ################

# Append the path where processing plugin can be found (assumes Debian OS)
sys.path.append('/usr/share/qgis/python/plugins')

#import modules needed
import processing
from processing.core.Processing import Processing
import geopandas as gpd
import os

#start the processing module
processing.core.Processing.Processing.initialize()

######### Soil Analysis Interpolation Maps ############################

df = gpd.read_file('Sample_points.shp')
no_columns = len(df.columns)
print(no_columns)
for seq in range(4,no_columns-1): #Ensure the Sample_points.shp file is formated with values needing to interpolated starting at the same column number as the starting range value.

	IDW_input = 'Sample_points.shp::~::0::~::{}::~::0'.format(seq)
	IDW_output = 'interpolated_raster_{}'.format(seq)

	RasVal2Pt_input = IDW_output
	RasVal2Pt_output = 'interpolated_polygon_{}'.format(seq)

	Clip_input = RasVal2Pt_output + ".shp"
	Clip_output = 'Final_map_{}.shp'.format(seq)
	Farm_boundary = 'Farm_boundary.shp'

	IDW = processing.run("qgis:idwinterpolation",\
	{'INTERPOLATION_DATA': IDW_input,\
	'DISTANCE_COEFFICIENT':2.5,\
	'EXTENT':'323266.347700000, 323861.727600000,8335174.220800000,8335527.756100000 [EPSG:32733]',\
	'PIXEL_SIZE':22.43776,\
	'OUTPUT': IDW_output}) #QgsProcessing.TEMPORARY_OUTPUT

	RasVal2Pt = processing.run("saga:rastervaluestopoints", \
                                   {'GRIDS':RasVal2Pt_input,\
                                    'POLYGONS':None,\
                                    'NODATA':True,\
                                    'TYPE':1,\
                                    'SHAPES':RasVal2Pt_output})

	processing.run("native:clip", \
                       {'INPUT': Clip_input,\
                        'OVERLAY':Farm_boundary,\
                        'OUTPUT':Clip_output})

	Delete_files = "rm {} {}.aux.xml {}.prj {}.cpg {}.dbf {}.mshp {}.prj {}.shp {}.shx".format(IDW_output,IDW_output,IDW_output,RasVal2Pt_output,RasVal2Pt_output,RasVal2Pt_output,RasVal2Pt_output)
        os.system(Delete_files)
