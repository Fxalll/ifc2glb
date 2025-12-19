import json

import os

import struct

import operator

import ifcopenshell

from ifcopenshell import geom

from gltflib import (

    GLTF, GLTFModel, Asset, Scene, Node, Mesh, Primitive, Attributes, Buffer, BufferView, Accessor, BufferTarget, ComponentType,
    FileResource, Material, PBRMetallicRoughness)


from core.initObjectPlacement import local_placement
from core.initMaterial import getColor, getColorName, findMaterial
from core.initProperty import getProperty, getLayer, get_keys

def ifcToGltf(ifc_file, file_name="vertices"):
    # 载入IFC文件

    settings = geom.settings()

    # 初始化参数

    bufferViewByteOffset = [[0,0]]
    bufferViewByteLength = []
    accessorFaces = []
    accessorVertices = []
    maxsAll = []
    minsAll = []
    matrixAll = []
    colorIndex = []
    propertyAll = []
    colorAll = getColor(ifc_file)
    colorName = getColorName(ifc_file)

    vertex_bytearray = bytearray()

    # 是否初始化

    isRebuild = True



    if os.path.exists("vertices.json") and os.path.exists("faces.json") and not isRebuild:

        print("调用已有数据：")

        with open("vertices.json") as file_obj:

          vertices = json.load(file_obj)

        with open("faces.json") as file_obj:

          faces = json.load(file_obj)

    else:

        print("初始化：")


        # 初始化
        model = GLTFModel()
        model.asset = Asset(version='2.0')
        model.scene = 0





        # 获得所有类

        products = ifc_file.by_type('IfcProduct')

        classList = []

        for product in products:

            classList.append(product.is_a())

        ifcTypes = list(set(classList))

        ifcTypes = ['IfcWallStandardCase']

        loadNum = 0

        loadSumNum = len(ifcTypes)

        #  成功构件数
        pushNum = 0

        layerAll = getLayer(ifc_file, ifcTypes)




        # 获得所有顶点与面

        for ifcType in ifcTypes:

            try:

                loadNum += 1

                ifcNum = 0

                nowloadNumTotal = len(ifc_file.by_type(ifcType))

                print("\r ", end=' ')

                print("")

                print("[{}/{}] 正在加载 {} ..".format(loadNum,loadSumNum,ifcType))

                print("-> 加载{}的{}个构件".format(ifcType,nowloadNumTotal))

                for ifc_entity in ifc_file.by_type(ifcType):

                    # 面、点数组

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

                    vertex_bytearray_single = bytearray()

                    # 把面的信息写入字节数组

                    for face in faces:

                        for value in face:
                            vertex_bytearray.extend(struct.pack('H', value))
                            vertex_bytearray_single.extend(struct.pack('H', value))

                    bytelen_faces = len(vertex_bytearray_single)

                    # 把点的信息写入字节数组

                    for vertex in vertices:

                        for value in vertex:
                            vertex_bytearray.extend(struct.pack('f', value))
                            vertex_bytearray_single.extend(struct.pack('f', value))

                    bytelen_vertex = len(vertex_bytearray_single) - bytelen_faces

                    # 点的最大最小值

                    minsAll.append([min([operator.itemgetter(i)(vertex) for vertex in vertices]) for i in range(3)])

                    maxsAll.append([max([operator.itemgetter(i)(vertex) for vertex in vertices]) for i in range(3)])

                    # 定义模型参数

                    bufferViewByteLength.append([bytelen_faces,bytelen_vertex])

                    bufferViewByteOffset.append([bufferViewByteOffset[pushNum][1]+bufferViewByteLength[pushNum][0],bufferViewByteOffset[pushNum][1]+bufferViewByteLength[pushNum][0]+bufferViewByteLength[pushNum][1]])

                    accessorFaces.append(len(faces) * 3)

                    accessorVertices.append(len(vertices))

                    # 加载当前构件4x4位置矩阵并放入数组

                    arrayModel = local_placement(ifc_file.by_type(ifcType)[ifcNum].ObjectPlacement).ravel()

                    matrixAll.append(arrayModel.tolist())

                    # 加载材质颜色

                    if not colorName == []:

                        material = ifcopenshell.util.element.get_material(ifc_entity)

                        if not material == None:
                            colorIndex.append(colorName.index(findMaterial(material)))
                        else:
                            colorIndex.append(0)

                    # 加载属性值

                    propertyAll.append(getProperty(ifc_entity))

                    # 成功构件数增加
                    pushNum += 1
                    ifcNum += 1


                    # 进度条数显

                    if (nowloadNumTotal > 1):

                        progressNum = round(ifcNum / (nowloadNumTotal - 1) * 100)

                        print("\r  -> 正在提取并生成GLTF参数值 -{:3}%".format(progressNum), end='  ')



            except Exception as e:

                print("\r ", end=' ')

                print("-> {}跳过加载。({})".format(ifcType,e))

                continue









        # 加载材质索引表
        if not colorName == []:
            model.materials = []
            for i in range(0, len(colorAll)):
                if (colorAll[i][3] == 0):
                    model.materials.append(Material(name=colorName[i],
                        pbrMetallicRoughness=PBRMetallicRoughness(baseColorFactor=colorAll[i], metallicFactor=0.0,
                                                                  roughnessFactor=1.0)))
                else:
                    model.materials.append(Material(name=colorName[i],pbrMetallicRoughness=PBRMetallicRoughness(baseColorFactor=colorAll[i], metallicFactor=0.0, roughnessFactor=1.0), alphaMode="BLEND",doubleSided=True))
        print("\r ", end=' ')
        print("")
        print("")
        print("===================")
        print("该模型GLTF参数值提取完毕")
        print("===================")

        nodesAll = [0]

        print("")
        print("正在生成{}个构件，请稍后".format(pushNum))
        for i in range(0,pushNum):
            propertyAll[i]["Layer"] = get_keys(layerAll, propertyAll[i]['UniqueId'])
            if (i <= 0):
                model.nodes = [Node(name=propertyAll[0]['Parameters'][0]['Name'],mesh=0,matrix=matrixAll[0],extras=propertyAll[0])]
                model.bufferViews= [(
                    BufferView(buffer=0, byteOffset=bufferViewByteOffset[i][1], byteLength=bufferViewByteLength[i][0],
                               target=BufferTarget.ELEMENT_ARRAY_BUFFER.value))]
                model.accessors = [(
                    Accessor(bufferView=i * 2, byteOffset=0, componentType=ComponentType.UNSIGNED_SHORT.value,
                             count=accessorFaces[i],
                             type="SCALAR", min=[0], max=[accessorVertices[i] - 1]))]
                if not colorName == []:
                    model.meshes = [Mesh(primitives=[Primitive(attributes=Attributes(POSITION=1), indices=0, mode=4,material=colorIndex[0])])]
                else:
                    model.meshes = [Mesh(primitives=[Primitive(attributes=Attributes(POSITION=1), indices=0, mode=4)])]

            else:
                nodesAll.append(i)
                model.nodes.append(Node(name=propertyAll[i]['Parameters'][0]['Name'],mesh=i,matrix=matrixAll[i],extras=propertyAll[i]))
                model.bufferViews.append(BufferView(buffer=0, byteOffset=bufferViewByteOffset[i][1], byteLength=bufferViewByteLength[i][0],
                                                target=BufferTarget.ELEMENT_ARRAY_BUFFER.value))
                model.accessors.append(
                    Accessor(bufferView=i * 2, byteOffset=0, componentType=ComponentType.UNSIGNED_SHORT.value,
                             count=accessorFaces[i],
                             type="SCALAR", min=[0], max=[accessorVertices[i] - 1]))
                if not colorName == []:
                    model.meshes.append(
                    Mesh(primitives=[Primitive(attributes=Attributes(POSITION=1 + i * 2), indices=0 + i * 2, mode=4,material=colorIndex[i])]))
                else:
                    model.meshes.append(
                        Mesh(primitives=[Primitive(attributes=Attributes(POSITION=1 + i * 2), indices=0 + i * 2, mode=4)]))


            model.bufferViews.append(BufferView(buffer=0, byteOffset=bufferViewByteOffset[i+1][0], byteLength=bufferViewByteLength[i][1],
                                                target=BufferTarget.ARRAY_BUFFER.value))
            model.accessors.append(
                Accessor(bufferView=(i*2)+1, byteOffset=0, componentType=ComponentType.FLOAT.value, count=accessorVertices[i],
                         type="VEC3",
                         min=minsAll[i], max=maxsAll[i]))
        model.scenes = [Scene(nodes=nodesAll)]




        bytelen = len(vertex_bytearray)
        model.buffers = [(Buffer(byteLength=bytelen, uri='{}.bin'.format(file_name)))]


    # 写出资源文件


    resource = FileResource('{}.bin'.format(file_name), data=vertex_bytearray)

    gltf = GLTF(model=model, resources=[resource])

    return gltf



