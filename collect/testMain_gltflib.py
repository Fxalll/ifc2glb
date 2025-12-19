import json

import os

import struct

import operator

import numpy as np

import matplotlib.pyplot as plt

import ifcopenshell

from ifcopenshell import geom

from gltflib import (

    GLTF, GLTFModel, Asset, Scene, Node, Mesh, Primitive, Attributes, Buffer, BufferView, Accessor, AccessorType,

    BufferTarget, ComponentType, GLBResource, FileResource,Material)



# 载入IFC文件

ifc_file = ifcopenshell.open('../resource/IfcWall.ifc')

settings = geom.settings()

vertices = []

faces = []

# 是否初始化

isRebuild = True



if os.path.exists("vertices.json") and os.path.exists("faces.json") and not isRebuild:

    print("调用已有数据。")

    with open("vertices.json") as file_obj:

      vertices = json.load(file_obj)

    with open("faces.json") as file_obj:

      faces = json.load(file_obj)

else:

    print("初始化。")





    # 获得所有类

    products = ifc_file.by_type('IfcProduct')

    classList = []

    for product in products:

        classList.append(product.is_a())

    ifcTypes = list(set(classList))

    print(ifcTypes)





    loadNum = 0

    loadSumNum = len(ifcTypes)

    # 获得所有顶点与面

    for ifcType in ifcTypes:

        try:

            loadNum += 1

            print("[{}/{}] 正在加载 {} ..".format(loadNum,loadSumNum,ifcType))

            for ifc_entity in ifc_file.by_type(ifcType):



                shape = geom.create_shape(settings, ifc_entity)



                ios_vertices = shape.geometry.verts

                ios_faces = shape.geometry.faces



                for value in [tuple(ios_vertices[i: i + 3]) for i in range(0, len(ios_vertices), 3)]:

                    vertices.append(value)

                for value in [tuple(ios_faces[i: i + 3]) for i in range(0, len(ios_faces), 3)]:

                    faces.append(value)

        except:

            print(ifcType+"加载失败！")

            continue





    # for ifc_entity in ifc_file.by_type("IfcRailing"):

    #     shape = geom.create_shape(settings, ifc_entity)

    #

    #     ios_vertices = shape.geometry.verts

    #     ios_faces = shape.geometry.faces

    #

    #     for value in [tuple(ios_vertices[i: i + 3]) for i in range(0, len(ios_vertices), 3)]:

    #         vertices.append(value)

    #

    #     for value in [tuple(ios_faces[i: i + 3]) for i in range(0, len(ios_faces), 3)]:

    #         faces.append(value)

    # for ifc_entity in ifc_file.by_type("IfcColumn"):

    #     shape = geom.create_shape(settings, ifc_entity)

    #

    #     ios_vertices = shape.geometry.verts

    #     ios_faces = shape.geometry.faces

    #

    #     for value in [tuple(ios_vertices[i: i + 3]) for i in range(0, len(ios_vertices), 3)]:

    #         vertices.append(value)

    #     for value in [tuple(ios_faces[i: i + 3]) for i in range(0, len(ios_faces), 3)]:

    #         faces.append(value)

    # for ifc_entity in ifc_file.by_type("IfcWall"):

    #     shape = geom.create_shape(settings, ifc_entity)

    #

    #     ios_vertices = shape.geometry.verts

    #     ios_faces = shape.geometry.faces

    #

    #     for value in [tuple(ios_vertices[i: i + 3]) for i in range(0, len(ios_vertices), 3)]:

    #         vertices.append(value)

    #     for value in [tuple(ios_faces[i: i + 3]) for i in range(0, len(ios_faces), 3)]:

    #         faces.append(value)







    # 存储本次值

    with open("vertices.json", 'w') as file_obj:

      json.dump(vertices, file_obj)



    with open("faces.json", 'w') as file_obj:

      json.dump(faces, file_obj)



# 所有的数据要写入一个二进制文件，先开个字节数组存

vertex_bytearray = bytearray()



# 把面的信息写入字节数组

for face in faces:

    for value in face:

        vertex_bytearray.extend(struct.pack('H', value))



bytelen_faces = len(vertex_bytearray)



# 把点的信息写入字节数组

for vertex in vertices:

    for value in vertex:

        vertex_bytearray.extend(struct.pack('f', value))



bytelen = len(vertex_bytearray)







# 点的最大最小值

mins = [min([operator.itemgetter(i)(vertex) for vertex in vertices]) for i in range(3)]

maxs = [max([operator.itemgetter(i)(vertex) for vertex in vertices]) for i in range(3)]





# 定义模型

# model = GLTFModel(

#     asset=Asset(version='2.0'),

#     scene=0,

#     scenes=[Scene(nodes=[0])],

#     nodes=[Node(mesh=0)],

#     meshes=[Mesh(primitives=[Primitive(attributes=Attributes(POSITION=1), indices=0)])],

#     buffers=[Buffer(byteLength=bytelen, uri='vertices.bin')],

#     bufferViews=[BufferView(buffer=0, byteOffset=0, byteLength=bytelen_faces, target=BufferTarget.ELEMENT_ARRAY_BUFFER.value),

#                 BufferView(buffer=0, byteOffset=bytelen_faces, byteLength=bytelen-bytelen_faces, target=BufferTarget.ARRAY_BUFFER.value)],

#     accessors=[Accessor(bufferView=0, byteOffset=0, componentType=ComponentType.UNSIGNED_SHORT.value, count=12*2, type="SCALAR", min=[0], max=[len(vertices)-1]),

#                 Accessor(bufferView=1, byteOffset=0, componentType=ComponentType.FLOAT.value, count=len(vertices), type="VEC3", min=mins, max=maxs),

#                ],

# )

# 修改定义模型代码，方便后续增加

model = GLTFModel()
model.asset=Asset(version='2.0')
model.scene=0
model.scenes=[Scene(nodes=[0])]
model.nodes=[Node(mesh=0)]
model.meshes=[Mesh(primitives=[Primitive(attributes=Attributes(POSITION=1), indices=0)])]
model.buffers=[Buffer(byteLength=bytelen, uri='vertices.bin')]
model.bufferViews=[BufferView(buffer=0, byteOffset=0, byteLength=bytelen_faces, target=BufferTarget.ELEMENT_ARRAY_BUFFER.value)]
model.bufferViews.append(BufferView(buffer=0, byteOffset=bytelen_faces, byteLength=bytelen-bytelen_faces, target=BufferTarget.ARRAY_BUFFER.value))
model.accessors=[Accessor(bufferView=0, byteOffset=0, componentType=ComponentType.UNSIGNED_SHORT.value, count=12*2, type="SCALAR", min=[0], max=[len(vertices)-1])]
model.accessors.append(Accessor(bufferView=1, byteOffset=0, componentType=ComponentType.FLOAT.value, count=len(vertices), type="VEC3", min=mins, max=maxs))


# 写出资源文件



resource = FileResource('vertices.bin', data=vertex_bytearray)

gltf = GLTF(model=model, resources=[resource])



# 导出gltf或glb

gltf.export('triangle.gltf')

gltf.export('triangle.glb')