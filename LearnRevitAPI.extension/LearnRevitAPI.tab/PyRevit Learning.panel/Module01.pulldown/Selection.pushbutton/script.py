# -*- coding: utf-8 -*-
__title__   = "Selection"
__doc__     = """Version = 1.0
Date    = 15.06.2024
________________________________________________________________
Description:

This is the placeholder for a .pushbutton
You can use it to start your pyRevit Add-In

________________________________________________________________
How-To:

1. [Hold ALT + CLICK] on the button to open its source folder.
You will be able to override this placeholder.

2. Automate Your Boring Work ;)

________________________________________________________________
TODO:
[FEATURE] - Describe Your ToDo Tasks Here
________________________________________________________________
Last Updates:
- [15.06.2024] v1.0 Change Description
- [10.06.2024] v0.5 Change Description
- [05.06.2024] v0.1 Change Description 
________________________________________________________________
Author: Erik Frits"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#==================================================
from Autodesk.Revit.DB import *

#.NET Imports
import clr
clr.AddReference("System")
from System.Collections.Generic import List


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
#==================================================
app    = __revit__.Application
uidoc  = __revit__.ActiveUIDocument
doc    = __revit__.ActiveUIDocument.Document #type:Document


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝
#==================================================
# public Wall CreateWallUsingCurve2(Autodesk.Revit.DB.Document document, Level level, WallType wallType)
# {
#     // Build a location line for the wall creation
#     XYZ start = new XYZ(0, 0, 0);
#     XYZ end = new XYZ(10, 10, 0);
#     Line geomLine = Line.CreateBound(start, end);
#
#     // Determine the other parameters
#     double height = 15;
#     double offset = 3;
#
#     // Create a wall using the location line and wall type
#     return Wall.Create(document, geomLine, wallType.Id, level.Id, height, offset, true, true);
# }

collector = FilteredElementCollector(doc)
levels = collector.OfClass(Level).ToElements()

def CreateWallUsingCurve2(doc, level, wallType):

    # Build a location line for the wall creation
    start = XYZ(0, 0, 0)
    end = XYZ(10, 10, 0)
    geomLine = Line.CreateBound(start, end)

    # Determine the other parameters
    height = 15
    offset = 3

    # Create a wall using the location line and wall type
    return Wall.Create(doc, geomLine, wallType.Id, level.Id, height, offset, True, True)

# // Get
# the
# handle
# of
# current
# document.
# UIDocument
# uidoc = commandData.Application.ActiveUIDocument;
#
# // Get
# the
# element
# selection
# of
# current
# document.
# Selection
# selection = uidoc.Selection;
# ICollection < ElementId > selectedIds = uidoc.Selection.GetElementIds();
#
# if (0 == selectedIds.Count)
#     {
#     // If
#     no
#     elements
#     selected. \
#         TaskDialog.Show("Revit", "You haven't selected any elements.");
#     }
#     else
#     {
#         String
#     info = "Ids of selected elements in the document are: ";
#     foreach(ElementId
#     id in selectedIds)
#     {
#         info += "\n\t" + id.IntegerValue;
#     }
#
#     TaskDialog.Show("Revit", info);
#     }


# Get the element selection of current document.
# selection = uidoc.Selection
selectedIds = uidoc.Selection.GetElementIds()

if not selectedIds:
    # If no elements selected.
    print("Revit","You haven't selected any elements.")

else:
    print("Ids of selected elements in the document are: ")
    for el_id in selectedIds:
        print(el_id)

