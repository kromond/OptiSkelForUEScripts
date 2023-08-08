import maya.cmds as cmds
from math import sqrt,pow
import random


def add_namespace_to_strings(input_list, NS, namespace_token):
    out_list = []
    for each in input_list:
        out_list.append("{0}{1}{2}".format(NS,namespace_token,each))
    return out_list
            
def create_shader(name, node_type="lambert"):
    material = cmds.shadingNode(node_type, name=name, asShader=True)
    sg = cmds.sets(name="%sSG" % name, empty=True, renderable=True, noSurfaceShader=True)
    cmds.connectAttr("%s.outColor" % material, "%s.surfaceShader" % sg)
    return material, sg

def build_skeleton_from_selected(root_joint, namespace_token):
    #selected = cmds.ls(sl=True)[0]
    if namespace_token in root_joint:
        # get namespace for selected
        NS = cmds.ls(root_joint)[0].split(namespace_token)[0]
        # print("NS var is :{}".format(NS))
    else:
        NS = ""
        namespace_token = ""
    # get joints for selected root
    joints =  cmds.ls(root_joint, type="joint", dag=True, ap=True)

    # make some materials with random colors
    spheres_mat, sph_SG = create_shader("SpheresMat")    
    sticks_mat, st_SG = create_shader("SticksMat")
    colors = []
    for i in range(6):
        tmp=random.uniform(0.2,1.0) 
        colors.append(tmp)  
    cmds.setAttr ( (spheres_mat + '.color'), colors[0],colors[1],colors[2], type = 'double3' )   
    cmds.setAttr ( (sticks_mat + '.color'), colors[3],colors[4],colors[5], type = 'double3' )


    #scale to .5 or .5 some parts
    scalep5 = add_namespace_to_strings([u"LeftHandMiddle1_geo",u"RightHandMiddle1_geo"], NS, namespace_token)
    scalep2 = add_namespace_to_strings([u'LIndex3End_geo', u'LeftHandIndex3_geo', u'LeftHandIndex2_geo', u'LMiddle3End_geo', 
        u'LeftHandMiddle3_geo', u'LeftHandMiddle2_geo', u'LRing3End_geo', u'LeftHandRing3_geo', u'LeftHandRing2_geo', 
        u'LPinky3End_geo', u'LeftHandPinky3_geo', u'LeftHandPinky2_geo', u'LeftHandIndex1_geo', u'LeftHandRing1_geo', 
        u'LeftHandPinky1_geo', u'LeftHandThumb1_geo', u'LeftHandThumb2_geo', u'LeftHandThumb3_sphere', u'LeftHandThumb3_geo', u'LThumb3End_geo',
        u'RightHandPinky2_geo', u'RightHandPinky3_geo', u'RPinky3End_geo', u'RightHandPinky1_geo', u'RightHandRing1_geo', 
        u'RightHandIndex1_geo', u'RightHandRing2_geo', u'RightHandRing3_geo', u'RRing3End_geo', u'RightHandMiddle2_geo', 
        u'RightHandMiddle3_geo', u'RMiddle3End_geo', u'RightHandIndex2_geo', u'RightHandIndex3_geo', u'RIndex3End_geo', 
        u'RightHandThumb1_geo',u'RightHandThumb2_geo', u'RightHandThumb3_geo', u'RThumb3End_geo'], NS, namespace_token)
    # make a material
    sphere_list = []
    stick_list = []
    for i,joint in enumerate(joints):
        p1 = cmds.xform( joint,q=1,ws=1,t=1) #get position of jointoint
        c = cmds.listRelatives(joint, children=1) # get the childrent of this joint
        if c:
            for each in c:
                geo = ''
                # get a distance to parent
                p2 = cmds.xform(each,q=1,ws=1,t=1)
                dist = sqrt(pow(p1[0]-p2[0],2)+pow(p1[1]-p2[1],2)+pow(p1[2]-p2[2],2))
                pplane = cmds.polyPlane(axis=[-1,0,0],w=3,h=3,sx=1,sy=1, constructionHistory=False)[0] # make a plane at the child joint
                geo = cmds.rename(pplane, joint+"_geo")
                #if geo in scalep5:
                #    cmds.scale(1,.5,.5, geo)
                if geo in scalep2 or geo in scalep5:
                    cmds.scale(1,.2,.2, geo)            
                cmds.polyExtrudeFacet(geo, ltz=-dist, lsx=0,lsy=0,lsz=0) #extrude this to the parent
                cmds.xform(geo, piv=[0,0,0], ws=1, a=1)
                cmds.select(geo, r=1)
                cmds.sets(geo, forceElement=st_SG)
                
                # spheres
                noSpheresList = add_namespace_to_strings(["RightUpLeg", "LeftUpLeg","RightHandIndex1","RightHandThumb1","RightHandRing1","RightHandPinky1", 
                    "LeftHandIndex1","LeftHandThumb1","LeftHandRing1","LeftHandPinky1", "LeftShoulder", "RightShoulder"],NS, namespace_token)
                if each in noSpheresList:
                    # joints with more than one children should only get one sphere
                    pass
                else:
                    if geo in scalep5:  
                        sph = cmds.polySphere(r=1.25,sx=8,sy=8,name=joint+'_sphere', constructionHistory=False)[0]
                    elif geo in scalep2:
                        sph = cmds.polySphere(r=0.5,sx=8,sy=8,name=joint+'_sphere', constructionHistory=False)[0]
                    else:              
                        sph = cmds.polySphere(r=2.5,sx=8,sy=8,name=joint+'_sphere', constructionHistory=False)[0]
                    cmds.select(sph, r=1)
                    cmds.sets(sph, forceElement=sph_SG)
                    cmds.rotate(0,0,90,sph)
                    cmds.parent(sph, geo)  
                    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
                    cmds.select(clear=True)

                cmds.parent(geo, joint, r=1,)  #parent this to the child joint
                # aim it down the bone
                cnt = cmds.aimConstraint(each,geo, u=[0,1,1])
                cmds.polyNormal(geo,ch=False,normalMode=0)
                cmds.delete(cnt)
                # parent the geo and sphere, which is a child, to the world and freeze xforms
                geo =cmds.parent(geo, world=True)
                cmds.makeIdentity(geo, apply=True, t=1, r=1, s=1, n=0)
                cmds.delete(geo,constructionHistory=True)  # delete history
                # parent to the world and bind it to the joint
                if each not in noSpheresList:
                    # some geos are sharing spheres
                    sph = cmds.parent(sph, world=True)
                    cmds.skinCluster(sph, joint, bindMethod=0, normalizeWeights=0)
                    sphere_list.append(sph[0])
                cmds.skinCluster(geo, joint, bindMethod=0, normalizeWeights=0)
                geolist = stick_list.append(geo[0])

    # now duplicate all this new geo, merge it, bind the merged geo and copy over the weights
    merged_list = [x for x in sphere_list] + [x for x in stick_list]
    dupes = cmds.duplicate(merged_list)
    combined_mesh = cmds.polyUnite(dupes, name="combinedMesh", ch=False)[0]
    cmds.delete(dupes) # delete the left over transform
    # bind this combined mesh to get a skin cluster
    cmds.skinCluster(combined_mesh, root_joint)
    # Combine the skin weights from all the separate meshes onto the combined mesh
    for geo1 in merged_list:
        skin_cluster = cmds.ls(cmds.listHistory(geo1), type='skinCluster')
        if not skin_cluster:
            print(f"No skinCluster found for {geo1}. Skipping...")
            continue
        cmds.skinPercent(skin_cluster[0], geo1, nrm=True, transform=combined_mesh)
    cmds.delete(merged_list)
    # save a bindPose
    # cmds.select(joints, replace=True)
    # cmds.dagPose(n='bindPose', s=True)
    return combined_mesh


