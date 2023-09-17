# steps

# Select the top node of the imported fbx

import maya.cmds as cmds
from pathlib import Path
import random
import imp

def changeMatToRandomColor(mesh_name):
    # get the shape
    mesh_shape = cmds.listRelatives(mesh_name, shapes=True, fullPath=True)
    shading_group = cmds.listConnections(mesh_shape, type='shadingEngine')
    print(shading_group)
    if shading_group:
        materials = cmds.listConnections(shading_group[0], type='phong')
        if materials:
            red, green, blue = random.random(), random.random(), random.random()
            cmds.setAttr(materials[0] + '.color', red, green, blue, type='double3')            

def get_namespace(node_name, name_separator):
        namespace = node_name.split(name_separator)[0]
        return namespace

def remove_namespace(name_separator, ns_to_remove):
    # this will remove the namespace if it's actually a namespace
    # or will remove the prefix from every transform if separated
    # by some other character
    if name_separator == ':':
        cmds.namespace(mergeNamespaceWithRoot=True, removeNamespace=ns_to_remove)
    else:
        # rename everything
        dag_objects = cmds.ls(dagObjects=True, noIntermediate=True, type=("transform"))
        dag_objects_with_ns = [x for x in dag_objects if ns_to_remove in x]
        # Print the list of DAG objects
        for obj in dag_objects_with_ns:
            cmds.rename(obj, obj.split(ns_to_remove)[1][1:])    
    
def rename_hierarchy(root_item, name_separator=":"):
    # Get the list of children below the root item
    children = cmds.listRelatives(root_item, allDescendents=True, type='transform')

    # Add the root item itself to the list
    hierarchy = [root_item] + children

    # Rename each item in the hierarchy
    for item in hierarchy:
        # Split the name based on the separator
        name_parts = item.split(name_separator)

        if len(name_parts) > 1:
            # Extract the desired part after the separator
            new_item_name = name_parts[-1]
            cmds.rename(item, new_item_name)
        else:
            # No separator found, skip renaming
            continue

def delete_all_keys(node, name_separator=':'):
    joints = cmds.ls(node, dag=True, type='joint')
    anim_curves = []
    for joint in joints:
        curves = cmds.listConnections(joint, type='animCurve')
        if curves:
            anim_curves.extend(curves)
    if anim_curves:
        cmds.delete(anim_curves)
        print("Deleted all these curves: {}".format(anim_curves))
        cmds.currentTime(0, edit=True)
        cmds.playbackOptions(minTime=0, maxTime=100)
    else:
        print("No anim curves were found on the joints under {}".format(node))



# test skel.  Look for mesh Look for name separator.  
def test_skel_for_mesh_and_rename(skelToTest, name_separator):
# check the item with the name 'Root', if it's a mesh, do that mesh fix up
    if 'Root' in skelToTest:
        namespace = get_namespace(skelToTest, name_separator)
        # need to tesh the shape node
        shape = cmds.listRelatives(skelToTest, shapes=True)            
        if len(shape) > 1:
            shape = shape[0] # just take the first one
            node_type = cmds.nodeType(shape)
        else:
            node_type = cmds.nodeType(shape)
        print("Shape is: {}, Type is: {}".format(shape, node_type))
        
        # if it's a mesh, rename it from 'Root' to 'Mesh' and make the mesh a random color
        if node_type == 'mesh':
            old_name = "{0}{1}Root".format(namespace, name_separator)
            new_name = "{0}{1}Mesh".format(namespace, name_separator)        
            print(old_name)
            print(new_name)    
            # rename it
            cmds.rename(old_name, new_name)
            print("Root mesh item was renamed to Mesh")
            # recolor it
            changeMatToRandomColor(new_name)
            return new_name, node_type

        if node_type == 'locator':
            print("No mesh found, Root is a locator")  
            old_name = "{0}{1}Root".format(namespace, name_separator)
            new_name = "{0}{1}Locator".format(namespace, name_separator) 
            cmds.rename(old_name, new_name)
            print(new_name, node_type)
            return new_name, node_type 
    else:
        print("Nothing called 'Root' was not found in the test item")
        return None
        

def create_root_bone(root_name, namespace, name_separator):
    # If there is a selection, the new bone will be under that.  
    # # We don't want that.  We want the new joint is under the world with no parent
    cmds.select(clear=True)  
    #check if root bone already exists
    if 'Root' in root_name and cmds.nodeType(root_name) == "joint":
        print("Root bone already exists")
    else:
        #create a new joint at the origin
        root_joint = cmds.joint(name="{}{}Root".format(namespace, name_separator))
        cmds.move(0,0,0, root_joint, absolute=True)
        print("Created a new root bone '{}' at the origin".format(root_joint))
    return root_joint
        
def parent_hips_to_root(root_joint, namespace, name_separator):
    hips_joint = "{}{}Hips".format(namespace,name_separator)
    # Check if the root and hips exist
    if not cmds.objExists(root_joint):
        print("Root joint '{}' does not exist.".format(root_joint))
        return
        
    if not cmds.objExists(hips_joint):
        print("Hips joint '{}' does not exist.".format(hips_joint))
        return
    # Parent the Hips to the Root joint
    cmds.parent(hips_joint, root_joint)
    print("Parented '{}' to '{}'.".format(hips_joint, root_joint))

def zero_out_skel(root_joint, namespace, name_separator):
    hips_joint = "{}{}Hips".format(namespace,name_separator)
    joint_list = cmds.ls(root_joint, dag=True, type='joint')
    # now select the hiearachy from the root zero out all rotations
    for j in joint_list:
        cmds.setAttr("{}.rotateX".format(j),0)
        cmds.setAttr("{}.rotateZ".format(j),0)
        cmds.setAttr("{}.rotateY".format(j),0)
       
    # Move the hips to 0x 0y
    print(hips_joint)
    cmds.setAttr("{}.translateX".format(hips_joint), 0)
    cmds.setAttr("{}.translateZ".format(hips_joint), 0)

    return None

def get_file_path_and_name():
    # Specify the file filter to limit selection to .fbx files
    file_filter = "FBX Files (*.fbx);;All Files (*.*);;"
    # Create a file dialog for selecting the folder to save the file
    file_path = cmds.fileDialog2(fileMode=0, dialogStyle=2, fileFilter=file_filter)
    # If the user didn't candel, set the file path and name variable and return
    if file_path:
        selected_file = Path(file_path[0])
        # Ensure the selected file has the .fbx extension
        if not selected_file.suffix.lower() == '.fbx':
            selected_file = selected_file.with_suffix('.fbx')
        file_name = selected_file.name
        file_path_obj = selected_file
        return file_path_obj, file_name
    else:
        print("No File named")
        return None, None

# def set_file_name(text_field, window):
#     global file_name
#     file_name = cmds.textFieldGrp(text_field, query=True, text=True)
#     cmds.deleteUI(window, window=True)

# # Usage example:
# # file_path, file_name = get_file_path_and_name()

import maya.mel as mel
# this function just would not work with the python version

def export_fbx(export_file):
    # Set up export options
    #mel.eval('FBXResetExport();')
    mel.eval('FBXExportSmoothingGroups -v true;')
    mel.eval('FBXExportShapes -v true;')
    mel.eval('FBXExportSkins -v true;')
    cmd = 'FBXExport -f "{}";'.format(export_file)
    mel.eval(cmd)

def set_up_optiFBX(name_separator, pose_file_path):
    # taking the first item named Root
    skelToTest = cmds.ls( "*{}Root".format(name_separator))[0]
    root_name, node_type = test_skel_for_mesh_and_rename(skelToTest, name_separator)  
    delete_all_keys(root_name, name_separator)
    namespace = get_namespace(root_name,name_separator)
    root_joint = create_root_bone(root_name, namespace, name_separator)
    parent_hips_to_root(root_joint, namespace, name_separator)
    zero_out_skel(root_joint, namespace, name_separator)

    # set the skel into UE Apose 
    import serializeJSONPoses as sjp
    imp.reload(sjp)
    # pose it in the 'Quinn' A Pose
    print("about to read json pose")
    sjp.read_in_JSON_pose(pose_file_path, new_pose='OptiNoNS_Apose_v02', NS=namespace, name_separator=name_separator)
    root_joint = cmds.ls( "*{}Root".format(name_separator))[0]
    return root_joint, node_type, namespace

def make_geo_and_export(root_joint, node_type,name_separator, namespace):
    # if there is no mesh geo, make some 
    if node_type == 'locator':
        import OptiSkelBuildStickGeo as geo
        imp.reload(geo)
        returnval = geo.build_skeleton_from_selected(root_joint, name_separator)
    # otherwise it's got a mesh and continue

    # remove namespace or prefixed performer name from the joints
    remove_namespace(name_separator, namespace)

    # export, this makes a file save window pop up to set a name an location
    export_file = get_file_path_and_name()[0]
    # export_file is a pathlib.Path object, make it right for windows
    export_fbx(str(export_file.as_posix()))
    
'''
# Here is how I call this in my script editor:
import sys
import maya.cmds as cmds
import maya.mel as mel
import imp
from pathlib import Path
scriptDir = Path("//path_to_where_you_saved_this/OptiSkelForUEScripts/python/Maya/")
if scriptDir not in sys.path:
    sys.path.append(scriptDir.as_posix())

import OptiSkelPrep as osp
imp.reload(osp)

# This script will convert an exported fbx from Optitrack into a posed Skeletal mesh for Unreal Engine
# It is set up for the name separator option to be set to ':' but can be changed with variable
# the script expects an empty scene with just a single fbx in it, with or witout 'sticks' geo 
# if the fbx is without 'sticks' geo, it will create geo for each bone

# a file save window pop up to set a name and a location for the resutling FBX file

name_separator=':'  # if you get this wrong it fails

pose_file_path = scriptDir / ".\\jsonPoses"

root_joint, node_type, namespace = osp.set_up_optiFBX(name_separator, pose_file_path)
# now it's posed with no anim.  From here, make geo if needed, remove namespace if needed, export FBX
osp.make_geo_and_export(root_joint, node_type,name_separator, namespace)
'''