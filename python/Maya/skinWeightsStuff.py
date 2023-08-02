   
import maya.cmds as cmds

# unused functions.  I was thinking for a bit that the skel needed to be rotated in Y (in Maya) and then freezing xforms, 
# but for now keeing the X (in Maya) as fwd

def stash_skin_weights(mesh, skin_cluster):

    stash_data = {}

    # Get the associated components of the skin cluster
    components = cmds.skinCluster(skin_cluster, query=True, geometry=True)[0]
    print("Compnents var: {}".format(components))
    #cmds.select("{}.vtx[*]".format(mesh))
    #vert_list = cmds.ls("{}.vtx[*]".format(components))
    #print("Vert_list: {}".format(vert_list)
    cmds.select("{}.vtx[*]".format(mesh))
    vertexList = [x for x in cmds.ls(sl=1, fl=1) if ".vtx" in x]
    # Store the skin weights

    for vtx in vertexList:
        influenceVals = cmds.skinPercent(skin_cluster, vtx, query=True, value=True)
        influenceNames = cmds.skinPercent(skin_cluster, vtx, transform=None, query=True)
        stash_data[vtx] = zip(influenceNames, influenceVals)
    print("Weights successfully stashed")
    return stash_data
    # Store the associated mesh
    return stash_data


def apply_stashed_skin_weights(stash_data, new_skin_cluster):
    for vtx, influences in stash_data.items():
        for influence, weight in influences:
            cmds.skinPercent(new_skin_cluster, vtx, transformValue=[(influence, weight)])

# reapply the mesh and skinning stash
def bind_stashed_skin_weights(stash_data, namespace, root_joint):
    mesh = "{}:Mesh".format(namespace)
    # Delete the existing skin cluster, if any
    skin_cluster = cmds.ls(cmds.listHistory(mesh), type='skinCluster')
    if skin_cluster:
        cmds.delete(skin_cluster)

    # Create a new skin cluster
    joint_list = cmds.ls(root_joint, type='joint', dag=True)
    new_skin_cluster = cmds.skinCluster(joint_list, mesh, toSelectedBones=True, normalizeWeights=True)[0]

    # Apply the stashed skin weights
    apply_stashed_skin_weights(stash_data, new_skin_cluster)

    # Bind the root joint to the new skin cluster
    cmds.skinCluster(new_skin_cluster, edit=True, skinMethod=0, maximumInfluences=5)
    cmds.skinCluster(new_skin_cluster, edit=True, weightDistribution=1)
    cmds.skinCluster(new_skin_cluster, edit=True, normalizeWeights=1)
    cmds.skinCluster(new_skin_cluster, edit=True, dropoffRate=10)
    cmds.skinCluster(new_skin_cluster, edit=True, maintainMaxInfluences=True)
    cmds.skinCluster(new_skin_cluster, edit=True, removeUnusedInfluence=True)
    cmds.skinCluster(new_skin_cluster, edit=True, removeUnusedVertices=True)

    # Assign the root joint as the bind pose
    cmds.select(root_joint)
    cmds.dagPose(bind=True, geometry=mesh)

    print("Applied stashed skin weights and created a new skin cluster.")