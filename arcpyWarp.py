"""
Dan Carver 1/18/2018
The goal of this is to align a raster image over a shapefile of a state
then export the image masked to the state
function was hacked from
https://gis.stackexchange.com/questions/72895/how-to-obtain-an-extent-of-a-whole-shapefile
"""


# Import arcpy modules
import arcpy
from arcpy import env
arcpy.CheckOutExtension("Spatial")
from arcpy.sa import *
env.workspace = r"D:\Costa Rica"
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("WGS 1984")
arcpy.env.overwriteOutput = True


print ('all loaded')

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


#Load shape file
shape1 = r"D:\Costa Rica\N16_05_2000LC030\N16_05_2000.shp"

#create bounding box around shapefile
shapeBox = arcpy.MinimumBoundingGeometry_management(shape1,
                                         "bounding box",
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

#run the warp tool
warp = arcpy.Warp_management(rast, sourcePoints, targetPoints, 'product.tif' , "POLYORDER1", "NEAREST")


outExtractByMask = arcpy.sa.ExtractByMask(warp, shape1)
outExtractByMask.save("clipped1.tif")


