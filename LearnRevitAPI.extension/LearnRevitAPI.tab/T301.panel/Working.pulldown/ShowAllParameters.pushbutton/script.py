# -*- coding: utf-8 -*-
__title__   = "ShowAllParameters"
__doc__     = """Version = 1.0
Date    = 17.03.2025
________________________________________________________________
TODO:
[FEATURE] - Describe Your ToDo Tasks Here
________________________________________________________________
Last Updates:
- [17.03.2025] v1.0 Change Description
________________________________________________________________
Author: JAY"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#==================================================
from Autodesk.Revit.DB import *

#.NET Imports
import clr
clr.AddReference('System')
import collections
import clr
from Autodesk.Revit.DB import *
from pyrevit import revit, DB, script


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


# 프로젝트의 모든 Parameter 찾기
binding_map = doc.ParameterBindings
iterator = binding_map.ForwardIterator()

output = script.get_output()
output.print_md("## 🔍 현재 프로젝트의 모든 Project Parameter 목록")

while iterator.MoveNext():
    definition = iterator.Key
    if definition:
        output.print_md("- **{}**".format(definition.Name))
