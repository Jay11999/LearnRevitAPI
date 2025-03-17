# -*- coding: utf-8 -*-
__title__   = "DeleteParametersByList"
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
import clr
import sys
import os
from Autodesk.Revit.DB import *
from pyrevit import revit, DB, forms, script


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

# 사용자로부터 삭제할 파라미터 이름 리스트 입력받기
user_input = forms.ask_for_string("삭제할 파라미터 이름들을 콤마로 구분하여 입력하세요:")
if not user_input:
    forms.alert("파라미터 이름이 입력되지 않았습니다. 종료합니다.")
    sys.exit()

param_names = [name.strip() for name in user_input.split(",") if name.strip()]

deleted_binding_names = []   # 바인딩 제거 성공한 이름
failed_binding_names = []    # 바인딩 제거 실패한 이름
deleted_shared_names = []    # 공유 파라미터 삭제 성공한 이름
failed_shared_names = []     # 공유 파라미터 삭제 실패한 이름
found_params_set = set()     # 찾은 파라미터 이름 집합

t = Transaction(doc, "Delete the parameters and clear values")
t.Start()

# ------------------------------
# 1. 프로젝트 파라미터(바인딩) 처리
# ------------------------------
bindings = doc.ParameterBindings
iterator = bindings.ForwardIterator()
iterator.Reset()
definitions_to_delete = []

while iterator.MoveNext():
    definition = iterator.Key
    if definition.Name in param_names:
        definitions_to_delete.append(definition)
        found_params_set.add(definition.Name)

for definition in definitions_to_delete:
    try:
        removed = bindings.Remove(definition)
        if removed:
            deleted_binding_names.append(definition.Name)
        else:
            failed_binding_names.append(definition.Name)
    except Exception as e:
        failed_binding_names.append(definition.Name)

# ------------------------------
# 2. 공유 파라미터 처리
# ------------------------------
shared_params = FilteredElementCollector(doc).OfClass(SharedParameterElement).ToElements()
for sp in shared_params:
    if sp.Name in param_names:
        try:
            doc.Delete(sp.Id)
            deleted_shared_names.append(sp.Name)
        except Exception as e:
            failed_shared_names.append(sp.Name)
        found_params_set.add(sp.Name)

# ------------------------------
# 3. 모델 요소에서 파라미터 값 초기화
# ------------------------------
# 바인딩 제거 후에도 기존 요소에 남은 파라미터 값들을 초기화합니다.
deleted_all = list(set(deleted_binding_names + deleted_shared_names))
if deleted_all:
    elements = FilteredElementCollector(doc).WhereElementIsNotElementType().ToElements()
    for elem in elements:
        for param_name in deleted_all:
            param = elem.LookupParameter(param_name)
            if param and not param.IsReadOnly:
                try:
                    # StorageType에 따라 기본값 할당
                    if param.StorageType == StorageType.String:
                        param.Set("")
                    elif param.StorageType == StorageType.Double:
                        param.Set(0.0)
                    elif param.StorageType == StorageType.Integer:
                        param.Set(0)
                    elif param.StorageType == StorageType.ElementId:
                        param.Set(ElementId.InvalidElementId)
                except Exception as e:
                    # 파라미터 값 초기화 실패 시 무시하고 계속 진행
                    pass

t.Commit()

# ------------------------------
# 4. 결과 출력
# ------------------------------
failed_all = list(set(failed_binding_names + failed_shared_names))
not_found = list(set(param_names) - found_params_set)

print "-------------------------------"
print "Parameter Deletion Summary:"
print "-------------------------------"
print "삭제된 파라미터 (총 {0}):".format(len(deleted_all))
for name in deleted_all:
    print " - {0}".format(name)

print "\n삭제 실패한 파라미터 (총 {0}):".format(len(failed_all))
for name in failed_all:
    print " - {0}".format(name)

print "\n문서에서 찾지 못한 파라미터 (총 {0}):".format(len(not_found))
for name in not_found:
    print " - {0}".format(name)












