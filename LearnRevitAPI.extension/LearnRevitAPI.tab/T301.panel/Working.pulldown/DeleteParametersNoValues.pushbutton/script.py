# -*- coding: utf-8 -*-
__title__   = "DeleteParametersNoValues"
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
from pyrevit import script


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

# Collect all elements in the model (except views)
collector = FilteredElementCollector(doc).WhereElementIsNotElementType().ToElements()

# Dictionary to store parameter values
parameter_values = collections.defaultdict(list)

# Iterate over all elements to collect parameter values
for elem in collector:
    for param in elem.Parameters:
        if param and not param.IsReadOnly:
            if param.Definition is not None:
                param_name = param.Definition.Name
            else:
                continue
            if param.StorageType == StorageType.String:
                param_value = param.AsString()
            elif param.StorageType == StorageType.Integer:
                param_value = param.AsInteger()
            elif param.StorageType == StorageType.Double:
                param_value = param.AsDouble()
            else:
                param_value = None

            # Store the parameter values
            parameter_values[param_name].append(param_value)

# Identify parameters that have only empty or default values
empty_parameters = []
non_empty_parameters = []

for param_name, values in parameter_values.items():
    if all(v in [None, "", 0, 0.0] for v in values):
        empty_parameters.append(param_name)
    else:
        non_empty_parameters.append(param_name)

# Begin transaction to delete parameters
t = Transaction(doc, "Delete Unused Parameters")
t.Start()

deleted_parameters = []
undeleted_parameters = []

# Get the project's ParameterBindings
binding_map = doc.ParameterBindings
iterator = binding_map.ForwardIterator()

while iterator.MoveNext():
    definition = iterator.Key
    binding = iterator.Current

    if definition and definition.Name in empty_parameters:
        try:
            # Remove the parameter binding
            doc.ParameterBindings.Remove(definition)
            deleted_parameters.append(definition.Name)
        except Exception as e:
            undeleted_parameters.append(definition.Name)

# Commit transaction
t.Commit()

# Print results
output = script.get_output()
output.print_md("### Deleted Parameters")
for param in deleted_parameters:
    output.print_md("- **{}**".format(param))

output.print_md("### Parameters Not Deleted")
for param in undeleted_parameters:
    output.print_md("- **{}**".format(param))

output.print_md("### Parameters that had values (Retained)")
for param in non_empty_parameters:
    output.print_md("- **{}**".format(param))

# Print Summary
print("Deleted {} unused parameters.".format(len(deleted_parameters)))
print("Could not delete {} parameters".format(len(undeleted_parameters)))
print("Retained {} parameters with values".format(len(non_empty_parameters)))
