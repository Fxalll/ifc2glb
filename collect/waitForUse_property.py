import ifcopenshell
from gltflib import GLTF, Scene, Node, Mesh, GLTFModel

# Load the ifc file
# ifc_file = ifcopenshell.open("../resource/IfcWall.ifc")
ifc_file = ifcopenshell.open("../resource/rac_advanced_sample_project.ifc")

# Create an empty gltf model
gltf = GLTFModel()

# Add a scene to the model
scene = Scene()
# scene_index = gltf.add_scene(scene)


# Get all element entities from the ifc file

# print("IfcPropertyDefinition：{}".format(ifc_file.by_type("IfcPropertyDefinition")))
# print("IfcPropertySetDefinition：{}".format(ifc_file.by_type("IfcPropertySetDefinition")))
# print("IfcPropertySet：{}".format(ifc_file.by_type("IfcPropertySet")))
# print("IfcProperty：{}".format(ifc_file.by_type("IfcProperty")))
# print("IfcComplexProperty：{}".format(ifc_file.by_type("IfcComplexProperty")))
# print("IfcSimpleProperty：{}".format(ifc_file.by_type("IfcSimpleProperty")))
# print("===")
# print("IfcRelationship：{}".format(ifc_file.by_type("IfcRelationship")))
# print("IfcRoot：{}".format(ifc_file.by_type("IfcRoot")))
# print("IfcBuildingStorey：{}".format(ifc_file.by_type("IfcBuildingStorey")))
# print("===")



elements = ifc_file.by_type("IfcWall")
# Loop through each element and create a node for gltf
for element in elements:
    # Get the element attributes, such as name, type and quantity
    attributes = element.get_info()
    print(attributes)

    # Convert the attributes to a gltflib.Node object
    # This is a simplified example, you may need to handle more cases and formats
    gltf_node = Node(
        name=attributes["Name"],
        extras={
            "type": attributes["type"],
        }
    )

    # print(gltf_node)

    # Add the node to the model
    # node_index = gltf.add_node(gltf_node)
    gltf.nodes = [Node(mesh=0)]
    gltf.nodes.append(gltf_node)
    # print(gltf)

    # Add the node index to the scene nodes list
    # scene.nodes.append(node_index)

# Export the gltf model as a binary file (.glb)