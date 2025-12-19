import operator

import os



import ifcopenshell

from gltflib import FileResource

from ifcopenshell import geom

from pygltflib import *



# 载入IFC文件

ifc_file = ifcopenshell.open('../resource/rac_advanced_sample_project.ifc')

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

    # 写出资源文件

    gltf = GLTF2()

    scene = Scene()

    mesh = Mesh()

    # material = Material()

    primitive = Primitive()

    node = Node()

    buffer = Buffer()

    bufferView1 = BufferView()
    bufferView2 = BufferView()
    bufferView3 = BufferView()
    bufferView4 = BufferView()

    accessor1 = Accessor()
    accessor2 = Accessor()
    accessor3 = Accessor()
    accessor4 = Accessor()

    buffer.uri = 'vertices.bin'




    # # 获得所有类
    #
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
    # print(ifcTypes)
    #
    #
    #
    #
    #
    # loadNum = 0
    #
    # loadSumNum = len(ifcTypes)
    #
    # # 获得所有顶点与面
    #
    # for ifcType in ifcTypes:
    #
    #     try:
    #
    #         loadNum += 1
    #
    #         print("[{}/{}] 正在加载 {} ..".format(loadNum,loadSumNum,ifcType))
    #
    #         for ifc_entity in ifc_file.by_type(ifcType):
    #
    #
    #
    #             shape = geom.create_shape(settings, ifc_entity)
    #
    #
    #
    #             ios_vertices = shape.geometry.verts
    #
    #             ios_faces = shape.geometry.faces
    #
    #
    #
    #             for value in [tuple(ios_vertices[i: i + 3]) for i in range(0, len(ios_vertices), 3)]:
    #
    #                 vertices.append(value)
    #
    #             for value in [tuple(ios_faces[i: i + 3]) for i in range(0, len(ios_faces), 3)]:
    #
    #                 faces.append(value)
    #
    #     except:
    #
    #         print(ifcType+"加载失败！")
    #
    #         continue





    for ifc_entity in ifc_file.by_type("IfcRailing"):
        vertices = []

        faces = []
        shape = geom.create_shape(settings, ifc_entity)



        ios_vertices = shape.geometry.verts

        ios_faces = shape.geometry.faces



        for value in [tuple(ios_vertices[i: i + 3]) for i in range(0, len(ios_vertices), 3)]:

            vertices.append(value)

        for value in [tuple(ios_faces[i: i + 3]) for i in range(0, len(ios_faces), 3)]:

            faces.append(value)

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
    print("1:")

    bufferView1.buffer = 0

    bufferView1.byteOffset = 0

    bufferView1.byteLength = bytelen_faces

    bufferView1.target = ELEMENT_ARRAY_BUFFER

    bufferView2.buffer = 0

    bufferView2.byteOffset = bytelen_faces

    bufferView2.byteLength = bytelen - bytelen_faces

    bufferView2.target = ARRAY_BUFFER

    accessor1.bufferView = 0

    accessor1.byteOffset = 0

    accessor1.componentType = UNSIGNED_SHORT

    accessor1.count = len(faces)*3

    accessor1.type = SCALAR

    accessor1.max = [len(vertices) - 1]

    accessor1.min = [0]

    accessor2.bufferView = 1

    accessor2.byteOffset = 0

    accessor2.componentType = FLOAT

    accessor2.count = len(vertices)

    accessor2.type = VEC3

    accessor2.max = maxs

    accessor2.min = mins












    for ifc_entity in ifc_file.by_type("IfcColumn"):
        vertices = []

        faces = []

        shape = geom.create_shape(settings, ifc_entity)



        ios_vertices = shape.geometry.verts

        ios_faces = shape.geometry.faces



        for value in [tuple(ios_vertices[i: i + 3]) for i in range(0, len(ios_vertices), 3)]:

            vertices.append(value)

        for value in [tuple(ios_faces[i: i + 3]) for i in range(0, len(ios_faces), 3)]:

            faces.append(value)

    # 所有的数据要写入一个二进制文件，先开个字节数组存

    vertex_bytearray2 = bytearray()

    # 把面的信息写入字节数组

    for face in faces:

        for value in face:
            vertex_bytearray.extend(struct.pack('H', value))
            vertex_bytearray2.extend(struct.pack('H', value))

    bytelen_faces = len(vertex_bytearray2)

    # 把点的信息写入字节数组

    for vertex in vertices:

        for value in vertex:
            vertex_bytearray.extend(struct.pack('f', value))
            vertex_bytearray2.extend(struct.pack('f', value))

    bytelen2 = len(vertex_bytearray2)
    bytelenNow = len(vertex_bytearray)

    # 点的最大最小值

    mins = [min([operator.itemgetter(i)(vertex) for vertex in vertices]) for i in range(3)]

    maxs = [max([operator.itemgetter(i)(vertex) for vertex in vertices]) for i in range(3)]

    # 定义模型
    print("1:")

    bufferView3.buffer = 0

    bufferView3.byteOffset = bytelen

    bufferView3.byteLength = bytelen_faces

    bufferView3.target = ELEMENT_ARRAY_BUFFER

    bufferView4.buffer = 0

    bufferView4.byteOffset = bytelen+bytelen_faces

    bufferView4.byteLength = bytelen2 - bytelen_faces

    bufferView4.target = ARRAY_BUFFER

    accessor3.bufferView = 2

    accessor3.byteOffset = 0

    accessor3.componentType = UNSIGNED_SHORT

    accessor3.count = len(faces) * 3

    accessor3.type = SCALAR

    accessor3.max = [len(vertices) - 1]

    accessor3.min = [0]

    accessor4.bufferView = 3

    accessor4.byteOffset = 0

    accessor4.componentType = FLOAT

    accessor4.count = len(vertices)

    accessor4.type = VEC3

    accessor4.max = maxs

    accessor4.min = mins




    # # 存储本次值
    #
    # with open("vertices.json", 'w') as file_obj:
    #
    #   json.dump(vertices, file_obj)
    #
    #
    #
    # with open("faces.json", 'w') as file_obj:
    #
    #   json.dump(faces, file_obj)













# add data


buffer.byteLength = bytelenNow

pbr = PbrMetallicRoughness() # Use PbrMetallicRoughness

# pbr.baseColorFactor = [1.0, 0.0, 0.0, 1.0] # solid red
#
# material.pbrMetallicRoughness = pbr

# material.doubleSided = True # make material double sided

# material.alphaMode = MASK   # to get around 'MATERIAL_ALPHA_CUTOFF_INVALID_MODE' warning



primitive.attributes.POSITION = 1
primitive.indices = 0
primitive.mode = 4

# primitive.material = 0

node.mesh = 0

scene.nodes = [0]





# assemble into a gltf structure

gltf.scenes.append(scene)

gltf.meshes.append(mesh)

# gltf.materials.append(material)
#
gltf.meshes[0].primitives.append(primitive)

gltf.nodes.append(node)

gltf.buffers.append(buffer)

gltf.bufferViews.append(bufferView1)

gltf.bufferViews.append(bufferView2)

gltf.bufferViews.append(bufferView3)

gltf.bufferViews.append(bufferView4)

gltf.accessors.append(accessor1)

gltf.accessors.append(accessor2)

gltf.accessors.append(accessor3)

gltf.accessors.append(accessor4)




# gltf.save("triangle.gltf")

gltf.convert_buffers(BufferFormat.BINARYBLOB) # Convert buffers to allow saving as .glb







# save to a .glb file

gltf.save("pygltflib.glb")