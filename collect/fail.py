# for ifc_entity in ifc_file.by_type("IfcRailing"):
#
#     vertices = []
#
#     faces = []
#
#     shape = geom.create_shape(settings, ifc_entity)
#
#
#
#     ios_vertices = shape.geometry.verts
#
#     ios_faces = shape.geometry.faces
#
#
#
#     for value in [tuple(ios_vertices[i: i + 3]) for i in range(0, len(ios_vertices), 3)]:
#
#         vertices.append(value)
#
#
#
#     for value in [tuple(ios_faces[i: i + 3]) for i in range(0, len(ios_faces), 3)]:
#
#         faces.append(value)
#
#
# # 所有的数据要写入一个二进制文件，先开个字节数组存
#
# vertex_bytearray = bytearray()
#
# # 把面的信息写入字节数组
#
# for face in faces:
#
#     for value in face:
#         vertex_bytearray.extend(struct.pack('H', value))
#
# bytelen_faces = len(vertex_bytearray)
#
# # 把点的信息写入字节数组
#
# for vertex in vertices:
#
#     for value in vertex:
#         vertex_bytearray.extend(struct.pack('f', value))
#
# bytelen = len(vertex_bytearray)
#
# # 点的最大最小值
#
# mins = [min([operator.itemgetter(i)(vertex) for vertex in vertices]) for i in range(3)]
#
# maxs = [max([operator.itemgetter(i)(vertex) for vertex in vertices]) for i in range(3)]
#
# # 定义模型
# print("1:")
#
# model.buffers=[(Buffer(byteLength=bytelen, uri='vertices.bin'))]
# model.bufferViews = [
#     BufferView(buffer=0, byteOffset=0, byteLength=bytelen_faces, target=BufferTarget.ELEMENT_ARRAY_BUFFER.value)]
# model.bufferViews.append(BufferView(buffer=0, byteOffset=bytelen_faces, byteLength=bytelen - bytelen_faces,
#                                     target=BufferTarget.ARRAY_BUFFER.value))
# model.accessors = [
#     Accessor(bufferView=0, byteOffset=0, componentType=ComponentType.UNSIGNED_SHORT.value, count=len(faces)*3,
#              type="SCALAR", min=[0], max=[len(vertices) - 1])]
# model.accessors.append(
#     Accessor(bufferView=1, byteOffset=0, componentType=ComponentType.FLOAT.value, count=len(vertices), type="VEC3",
#              min=mins, max=maxs))
# model.meshes = [Mesh(primitives=[Primitive(attributes=Attributes(POSITION=1), indices=0, mode=4)])]
#
#
# for ifc_entity in ifc_file.by_type("IfcColumn"):
#
#     vertices = []
#
#     faces = []
#
#     shape = geom.create_shape(settings, ifc_entity)
#
#
#
#     ios_vertices = shape.geometry.verts
#
#     ios_faces = shape.geometry.faces
#
#
#
#     for value in [tuple(ios_vertices[i: i + 3]) for i in range(0, len(ios_vertices), 3)]:
#
#         vertices.append(value)
#
#     for value in [tuple(ios_faces[i: i + 3]) for i in range(0, len(ios_faces), 3)]:
#
#         faces.append(value)
#
#
#
# # 所有的数据要写入一个二进制文件，先开个字节数组存
#
# vertex_bytearray2 = bytearray()
#
# # 把面的信息写入字节数组
#
# for face in faces:
#
#     for value in face:
#         vertex_bytearray.extend(struct.pack('H', value))
#         vertex_bytearray2.extend(struct.pack('H', value))
#
# bytelen_faces = len(vertex_bytearray2)
#
# # 把点的信息写入字节数组
#
# for vertex in vertices:
#
#     for value in vertex:
#         vertex_bytearray.extend(struct.pack('f', value))
#         vertex_bytearray2.extend(struct.pack('f', value))
#
# bytelen2 = len(vertex_bytearray2)
# bytelenNow = len(vertex_bytearray)
#
# # 点的最大最小值
#
# mins = [min([operator.itemgetter(i)(vertex) for vertex in vertices]) for i in range(3)]
#
# maxs = [max([operator.itemgetter(i)(vertex) for vertex in vertices]) for i in range(3)]
#
# # 定义模型
# print("2:")
#
# model.buffers=[(Buffer(byteLength=bytelenNow, uri='vertices.bin'))]
# model.bufferViews.append(
#     BufferView(buffer=0, byteOffset=bytelen, byteLength=bytelen_faces, target=BufferTarget.ELEMENT_ARRAY_BUFFER.value))
# model.bufferViews.append(BufferView(buffer=0, byteOffset=bytelen+bytelen_faces, byteLength=bytelen2 - bytelen_faces,
#                                     target=BufferTarget.ARRAY_BUFFER.value))
# model.accessors.append(
#     Accessor(bufferView=2, byteOffset=0, componentType=ComponentType.UNSIGNED_SHORT.value, count=len(faces)*3,
#              type="SCALAR", min=[0], max=[len(vertices) - 1]))
# model.accessors.append(
#     Accessor(bufferView=3, byteOffset=0, componentType=ComponentType.FLOAT.value, count=len(vertices), type="VEC3",
#              min=mins, max=maxs))
# model.meshes.append(Mesh(primitives=[Primitive(attributes=Attributes(POSITION=3), indices=2, mode=4)]))

#
# for ifc_entity in ifc_file.by_type("IfcWall"):
#
#     vertices = []
#
#     faces = []
#
#     shape = geom.create_shape(settings, ifc_entity)
#
#
#
#     ios_vertices = shape.geometry.verts
#
#     ios_faces = shape.geometry.faces
#
#
#
#     for value in [tuple(ios_vertices[i: i + 3]) for i in range(0, len(ios_vertices), 3)]:
#
#         vertices.append(value)
#
#     for value in [tuple(ios_faces[i: i + 3]) for i in range(0, len(ios_faces), 3)]:
#
#         faces.append(value)
#
#
#
# # 所有的数据要写入一个二进制文件，先开个字节数组存
#
# vertex_bytearray3 = bytearray()
#
# # 把面的信息写入字节数组
#
# for face in faces:
#
#     for value in face:
#         vertex_bytearray.extend(struct.pack('H', value))
#         vertex_bytearray3.extend(struct.pack('H', value))
#
# bytelen_faces = len(vertex_bytearray3)
#
# # 把点的信息写入字节数组
#
# for vertex in vertices:
#
#     for value in vertex:
#         vertex_bytearray.extend(struct.pack('f', value))
#         vertex_bytearray3.extend(struct.pack('f', value))
#
# bytelen3 = len(vertex_bytearray3)
# bytelenNow = len(vertex_bytearray)
#
# # 点的最大最小值
#
# mins = [min([operator.itemgetter(i)(vertex) for vertex in vertices]) for i in range(3)]
#
# maxs = [max([operator.itemgetter(i)(vertex) for vertex in vertices]) for i in range(3)]
#
# # 定义模型
# print("3:")
#
# model.buffers=[(Buffer(byteLength=bytelenNow, uri='vertices.bin'))]
# model.bufferViews.append(
#     BufferView(buffer=0, byteOffset=bytelen+bytelen2, byteLength=bytelen_faces, target=BufferTarget.ELEMENT_ARRAY_BUFFER.value))
# model.bufferViews.append(BufferView(buffer=0, byteOffset=bytelen+bytelen2+bytelen_faces, byteLength=bytelen3 - bytelen_faces,
#                                     target=BufferTarget.ARRAY_BUFFER.value))
# model.accessors.append(
#     Accessor(bufferView=4, byteOffset=0, componentType=ComponentType.UNSIGNED_SHORT.value, count=len(faces)*3,
#              type="SCALAR", min=[0], max=[len(vertices) - 1]))
# model.accessors.append(
#     Accessor(bufferView=5, byteOffset=0, componentType=ComponentType.FLOAT.value, count=len(vertices), type="VEC3",
#              min=mins, max=maxs))
# model.meshes.append(Mesh(primitives=[Primitive(attributes=Attributes(POSITION=5), indices=4, mode=4)]))


# 存储本次值

# with open("vertices.json", 'w') as file_obj:
#
#   json.dump(vertices, file_obj)
#
#
#
# with open("faces.json", 'w') as file_obj:
#
#   json.dump(faces, file_obj)
