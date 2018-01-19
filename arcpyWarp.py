"""
Dan Carver 1/18/2018
The goal of this is to align a raster image over a shapefile of a state
then export the image masked to the state
function was hacked from
https://gis.stackexchange.com/questions/72895/how-to-obtain-an-extent-of-a-whole-shapefile
"""

def extents(fc):
    """
    This function takes in an arcpy object and returns the spatial extent features
    """
    extent = arcpy.Describe(fc).extent
    west = extent.XMin
    south = extent.YMin
    east = extent.XMax
    north = extent.YMax
    width = extent.width
    height = extent.height
    return west, south, east, north, width, height

def shpExtent(shape):
    """
    inputs a shapefile and returns the target points for the warp function
    shape: needs to be a path to a specific shapefile
    """
    #create bounding box around shapefile
    shapeBox = arcpy.MinimumBoundingGeometry_management(shape,
                                             "bounding_box",
                                             "RECTANGLE_BY_AREA")
    #call extent function on shapefile
    w1, s1, e1, n1, wid1, hgt1 = extents(shapeBox)
    #start the formatting for the warp function
    topLeft1 = str(w1) + " " + str(n1)
    topRight1 = str(e1) + " " + str(n1)
    bottomLeft1 = str(w1) + " " + str(s1)
    bottomRight1 = str(e1) + " " + str(s1)

    #aside
    targetPoints = " '{}';'{}';'{}';'{}'".format(topLeft1,topRight1,bottomLeft1,bottomRight1)
    return targetPoints

def rastExtent(raster):
    """
    inputs a raster and returns the target points for the warp function
    raster: needs to be a path to a specific raster
    """
    # import the new raster
    rast = arcpy.sa.Raster(raster)
    #call extent function on raster
    w2, s2, e2, n2, wid2, hgt2 = extents(rast)

    topLeft2 = str(w2) + " " + str(n2)
    topRight2 = str(e2) + " " + str(n2)
    bottomLeft2 = str(w2) + " " + str(s2)
    bottomRight2 = str(e2) + " " + str(s2)

    # concatenate to match string format needed for warp tool
    sourcePoints = " '{}';'{}';'{}';'{}'".format(topLeft2,topRight2,bottomLeft2,bottomRight2)
    return sourcePoints

    print ('raster done')

"""
At this point there is a lot of ways we can manage the file system
using either os.listDic or arcpy.list file
I think that the it will be best to name the features after the state then just
make two list and order them.
setting the workspace to a location where the shp are stored
"""

# Import arcpy modules
import arcpy
from arcpy import env
arcpy.CheckOutExtension("Spatial")
from arcpy.sa import *
workplace = env.workspace = r"D:\Costa Rica"
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("WGS 1984")
arcpy.env.overwriteOutput = True


print ('all loaded')
shapefiles = sorted(arcpy.ListFeatureClasses(workplace))
rasters = sorted(arcpy.ListRasters(workplace))

states = [Alabama,Alaska,Arizona,Arkansas,California,Colorado,Connecticut,
Delaware,Florida,Georgia,Hawaii,Idaho,Illinois,Indiana,Iowa,Kansas,Kentucky,Louisiana,Maine,
Maryland,Massachusetts,Michigan,Minnesota,Mississippi,Missouri,Montana,Nebraska,
Nevada,New Hampshire,New Jersey,New Mexico,New York,North Carolina,North Dakota,
Ohio,Oklahoma,Oregon,Pennsylvania,Rhode Island,South Carolina,South Dakota,
Tennessee,Texas,Utah,Vermont,Virginia,Washington,West Virginia,Wisconsin,Wyoming]


for shape, raster,state in zip(shapefiles, raster, states):
    targetPoints = shpExtent(shape)
    sourcePoints = rastExtent(raster)
    name = state
    warp = arcpy.Warp_management(raster, sourcePoints, targetPoints, name , "POLYORDER1", "NEAREST")
    outExtractByMask = arcpy.sa.ExtractByMask(warp, shape)
    outExtractByMask.save(name+"clip.jpg")
    print( name + ' have been completed')






"""
#create bounding box around shapefile
shapeBox = arcpy.MinimumBoundingGeometry_management(shape1,
                                         "bounding_box",
                                         "RECTANGLE_BY_AREA")

#call extent function on shapefile
w1, s1, e1, n1, wid1, hgt1 = extents(shapeBox)

topLeft1 = str(w1) + " " + str(n1)
topRight1 = str(e1) + " " + str(n1)
bottomLeft1 = str(w1) + " " + str(s1)
bottomRight1 = str(e1) + " " + str(s1)

# concatenate to match string format needed for warp tool
targetPoints = " '{}';'{}';'{}';'{}'".format(topLeft1,topRight1,bottomLeft1,bottomRight1)

print('shp is done')

#load raster
pathToJpg = r"C:\Users\danie\Pictures\humbolt_nature_de_magana.jpg"
rastName = "product"


# import the new raster
rast = arcpy.sa.Raster(pathToJpg)
#call extent function on raster
w2, s2, e2, n2, wid2, hgt2 = extents(rast)

topLeft2 = str(w2) + " " + str(n2)
topRight2 = str(e2) + " " + str(n2)
bottomLeft2 = str(w2) + " " + str(s2)
bottomRight2 = str(e2) + " " + str(s2)

# concatenate to match string format needed for warp tool
sourcePoints = " '{}';'{}';'{}';'{}'".format(topLeft2,topRight2,bottomLeft2,bottomRight2)

print ('raster done')
"""
#run the warp tool
warp = arcpy.Warp_management(rast, sourcePoints, targetPoints, 'product.tif' , "POLYORDER1", "NEAREST")


outExtractByMask = arcpy.sa.ExtractByMask(warp, shape1)
outExtractByMask.save("clipped1.tif")
