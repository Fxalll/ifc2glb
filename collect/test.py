import re
import time

import ifcopenshell
from ifcopenshell import geom

# file_path = '../resource/集成厨房-橱柜-集成吊柜.ifc'
# file_path = '../resource/小便池.ifc'
# file_path = '../resource/rac_advanced_sample_project.ifc'
# ifc_file = ifcopenshell.open(file_path)



# 测试1
# for sub_entity in ifc_file.by_type("IFCEXTRUDEDAREASOLID"):
#     try:
#         settings = geom.settings()
#         shape = geom.create_shape(settings, sub_entity)
#         print(sub_entity)
#         print(shape.verts)
#         print(shape.faces)
#         # ios_vertices = shape.geometry.verts
#         # ios_faces = shape.geometry.faces
#         # print(ios_faces)
#     except Exception as e:
#         print(e)
#         pass



# 测试2

# try:
#     for wall in ifc_file.by_type("IfcFlowTerminal"):
#         for item in wall.Representation.Representations:
#             if item.RepresentationIdentifier == "Body":
#                for shell in item.Items:
#                    print(shell.is_a("IfcExtrudedAreaSolid"))
#                    print(geom.create_shape(geom.settings(), shell).verts)
#                    for i in shell:
#                        for k in i:
#                            if (k.is_a("IfcShapeRepresentation")):
#                                for j in k.Items:
#                                    print(j)
#                                    settings = geom.settings()
#                                    shape = geom.create_shape(settings, j)
#                                    print(shape.verts)
#                                    print(shape.faces)
#
# except Exception as e:
#     # print(e)
#     pass


# 测试3
# extruded_area_solids = ifc_file.by_type("IfcExtrudedAreaSolid")
#
# # Iterate over all IfcExtrudedAreaSolid entities
# for extruded_area_solid in extruded_area_solids:
#     # Get the faces and vertices of the solid
#     print(extruded_area_solid.SweptArea)
#     print(extruded_area_solid.Position)
#     faces = extruded_area_solid.SweptArea.OuterCurve.Points
#     vertices = extruded_area_solid.Position.Location.Coordinates
#
#     # Do something with the faces and vertices
#     print(faces)
#     print(vertices)

# 测试4
# str = "surface-style-254982-door---panel"[14:]
# s = [int(s) for s in re.findall(r'-?\d+\.?\d*', str)][0]
# print(s)

# 测试5
# # 加载ifc文件
# ifc_file = ifcopenshell.open("../resource/01小别墅.ifc")
# # 找到所有门的实例
# products = ifc_file.by_type('IfcProduct')
#
# classList = []
#
# for product in products:
#
#     classList.append(product.is_a())
#
# ifcTypes = list(set(classList))
#
# for ifcType in ifcTypes:
#     doors = ifc_file.by_type(ifcType)
#     # 遍历每个门
#     for door in doors:
#         try:
#             # 获取门名称
#             name = door.Name
#             print(f"Door Name: {name}")
#             # 获取门的所有属性值
#             properties = {}
#             for prop in door.IsDefinedBy:
#                 if prop.is_a("IfcRelDefinesByProperties"):
#                     for pset in prop.RelatingPropertyDefinition.HasProperties:
#                         if pset.is_a("IfcPropertySet"):
#                             for prop in pset.HasProperties:
#                                 if prop.is_a("IfcPropertySingleValue"):
#                                     properties[prop.Name] = prop.NominalValue.wrappedValue
#             # print("Door Properties:")
#             # for prop_name, prop_value in properties.items():
#             #     print(f"\t{prop_name}: {prop_value}")
#             print(properties)
#             # 获取门所在的空间
#             # spaces = door.IsContainedIn[0].RelatedSpaces
#             # for space in spaces:
#             #     space_name = space.Name
#             #     print(f"Located in Space: {space_name}")
#             # 获取门所在的楼层
#             floor = door.ContainedInStructure[0].RelatingStructure.Name
#             print(f"Located on Floor: {floor}")
#             # 在门与空间之间创建联系
#             # if not door.ContainedInStructure[0].RelatingStructure.ContainsElements:
#             #     door_space_rel = ifc_file.create_entity(
#             #         "IfcRelContainedInSpatialStructure", GlobalId=ifc_file.create_guid(),
#             #         OwnerHistory=ifc_file.owner_history(), Name="Door Space Rel",
#             #         RelatedElements=[door]
#             #     )
#             #     ifc_file.create_entity(
#             #         "IfcRelReferencedInSpatialStructure", GlobalId=ifc_file.create_guid(),
#             #         OwnerHistory=ifc_file.owner_history(), Name="Space Door Rel",
#             #         RelatedElements=[door_space_rel.RelatingStructure], RelatedElementsType="IFCSPACE",
#             #         ReferencedElement=door
#             #     )
#         except:
#             continue

# 测试6
# ifc_file = ifcopenshell.open("../resource/01小别墅.ifc")
# ifc_entity = ifc_file.by_type('IFCPROPERTYSINGLEVALUE')
# print(ifc_entity)

# 测试7
# 导入ifcopenshell库
import ifcopenshell

# 打开ifc文件
model = ifcopenshell.open('../resource/01小别墅.ifc')

# 获取所有的IfcProduct实例
products = model.by_type('IfcProduct')

classList = []

for product in products:

    classList.append(product.is_a())

ifcTypes = list(set(classList))

for ifcType in ifcTypes:
    # 过滤部分ifc无关构件
    if (ifcType == 'IfcOpeningElement' or ifcType == 'IfcSpace'):
        continue
    for ifc_entity in model.by_type(ifcType):
        # 检查是否有IsDefinedBy属性
        if ifc_entity.is_a('IfcObject') and ifc_entity.IsDefinedBy:
            # 遍历每个IsDefinedBy属性
            for rel in ifc_entity.IsDefinedBy:
                # 检查是否是IfcRelDefinesByProperties或IfcRelDefinesByType实例
                if rel.is_a('IfcRelDefinesByProperties'):
                    # 获取RelatingPropertyDefinition属性
                    prop_def = rel.RelatingPropertyDefinition
                    # 检查是否是IfcPropertySet实例
                    if prop_def.is_a('IfcPropertySet'):
                        # 获取HasProperties属性
                        props = prop_def.HasProperties
                        # 遍历每个IfcProperty实例
                        for prop in props:
                            # 检查是否是IfcPropertySingleValue实例
                            if prop.is_a('IfcPropertySingleValue'):
                                # 获取Name和NominalValue属性
                                name = prop.Name
                                value = prop.NominalValue.wrappedValue
                                # 打印结果
                                print(f'{ifc_entity}: {name} = {value}')
                elif rel.is_a('IfcRelDefinesByType'):
                    # 获取RelatingType属性
                    type_obj = rel.RelatingType
                    # 检查是否是IfcTypeObject实例
                    if type_obj.is_a('IfcTypeObject'):
                        # 获取HasPropertySets属性
                        prop_sets = type_obj.HasPropertySets or []
                        # 遍历每个IfcPropertySet实例
                        for prop_set in prop_sets:
                            # 检查是否是IfcPropertySet实例
                            if prop_set.is_a('IfcPropertySet'):
                                # 获取HasProperties属性
                                props = prop_set.HasProperties
                                # 遍历每个IfcProperty实例
                                for prop in props:
                                    # 检查是否是IfcPropertySingleValue实例
                                    if prop.is_a('IfcPropertySingleValue'):
                                        # 获取Name和NominalValue属性
                                        name = prop.Name
                                        value = prop.NominalValue.wrappedValue
                                        # 打印结果
                                        print(f'{ifc_entity}: {name} = {value}')

