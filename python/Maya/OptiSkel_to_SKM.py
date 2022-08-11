import maya.cmds as cmds
from math import sqrt,pow
import random
import serializeJSONPoses as sp

def addNamespaceToStrings(inputList, NS):
    outlist = []
    for each in inputList:
        outlist.append("{0}:{1}".format(NS,each))
    return outlist
            
def create_shader(name, node_type="lambert"):
    material = cmds.shadingNode(node_type, name=name, asShader=True)
    sg = cmds.sets(name="%sSG" % name, empty=True, renderable=True, noSurfaceShader=True)
    cmds.connectAttr("%s.outColor" % material, "%s.surfaceShader" % sg)
    return material, sg

# get namespace for selected
NS = cmds.ls(sl=True)[0].split(':')[0]

# get joints for selected root
joints =  cmds.ls(sl=True, type="joint", dag=True, ap=True)

# set all rotations to zeros
for j in joints:
    cmds.setAttr(j + '.rotate', 0,0,0, type="double3")
# set tx and tz to zero on hips
cmds.setAttr(NS + ":" + 'Hips.translateX', 0)
cmds.setAttr(NS + ":" + 'Hips.translateZ', 0)

# make some materials with random colors
spheresMat, sphSG = create_shader("SpheresMat")    
sticksMat, stSG = create_shader("SticksMat")
colors = []
for i in range(6):
    tmp=random.uniform(0.2,1.0) 
    colors.append(tmp)  
cmds.setAttr ( (spheresMat + '.color'), colors[0],colors[1],colors[2], type = 'double3' )   
cmds.setAttr ( (sticksMat + '.color'), colors[3],colors[4],colors[5], type = 'double3' )


#scale to .5 or .5 some parts
scalep5 = addNamespaceToStrings([u"LeftHandMiddle1_geo",u"RightHandMiddle1_geo"], NS)
scalep2 = addNamespaceToStrings([u'LIndex3End_geo', u'LeftHandIndex3_geo', u'LeftHandIndex2_geo', u'LMiddle3End_geo', 
    u'LeftHandMiddle3_geo', u'LeftHandMiddle2_geo', u'LRing3End_geo', u'LeftHandRing3_geo', u'LeftHandRing2_geo', 
    u'LPinky3End_geo', u'LeftHandPinky3_geo', u'LeftHandPinky2_geo', u'LeftHandIndex1_geo', u'LeftHandRing1_geo', 
    u'LeftHandPinky1_geo', u'LeftHandThumb1_geo', u'LeftHandThumb2_geo', u'LeftHandThumb3_sphere', u'LeftHandThumb3_geo', u'LThumb3End_geo',
    u'RightHandPinky2_geo', u'RightHandPinky3_geo', u'RPinky3End_geo', u'RightHandPinky1_geo', u'RightHandRing1_geo', 
    u'RightHandIndex1_geo', u'RightHandRing2_geo', u'RightHandRing3_geo', u'RRing3End_geo', u'RightHandMiddle2_geo', 
    u'RightHandMiddle3_geo', u'RMiddle3End_geo', u'RightHandIndex2_geo', u'RightHandIndex3_geo', u'RIndex3End_geo', 
    u'RightHandThumb1_geo',u'RightHandThumb2_geo', u'RightHandThumb3_geo', u'RThumb3End_geo'], NS)
# make a material
spherelist = []
sticklist = []
for i,j in enumerate(joints):
    p1 = cmds.xform( j,q=1,ws=1,t=1) #get position of joint
    #print(j)
    c = cmds.listRelatives(j, children=1) # get the childrent of this joint
    if c:
        for each in c:
            geo = ''
            # get a distance to parent
            p2 = cmds.xform(each,q=1,ws=1,t=1)
            dist = sqrt(pow(p1[0]-p2[0],2)+pow(p1[1]-p2[1],2)+pow(p1[2]-p2[2],2))
            pplane = cmds.polyPlane(axis=[-1,0,0],w=3,h=3,sx=1,sy=1, constructionHistory=False)[0] # make a plane at the child joint
            geo = cmds.rename(pplane, each+"_geo")
            #if geo in scalep5:
            #    cmds.scale(1,.5,.5, geo)
            if geo in scalep2 or geo in scalep5:
                cmds.scale(1,.2,.2, geo)            
            cmds.polyExtrudeFacet(geo, ltz=-dist, lsx=0,lsy=0,lsz=0) #extrude this to the parent
            cmds.xform(geo, piv=[0,0,0], ws=1, a=1)
            sticklist.append(geo)
            cmds.select(geo, r=1)
            cmds.sets(geo, forceElement=stSG)
            # spheres
            noSpheresList = addNamespaceToStrings(["RightUpLeg", "LeftUpLeg","RightHandIndex1","RightHandThumb1","RightHandRing1","RightHandPinky1", 
                "LeftHandIndex1","LeftHandThumb1","LeftHandRing1","LeftHandPinky1", "LeftShoulder", "RightShoulder"],NS)
            if each in noSpheresList:
                # joints with more than one children should only get one sphere
                pass
            else:
                if geo in scalep5:  
                    sph = cmds.polySphere(r=1.25,sx=8,sy=8,name=each+'_sphere', constructionHistory=False)[0]
                    #cmds.scale(2,.4,2, sph)
                elif geo in scalep2:
                    sph = cmds.polySphere(r=0.5,sx=8,sy=8,name=each+'_sphere', constructionHistory=False)[0]
                    #cmds.scale(1,.2,1, sph)  
                else:              
                    sph = cmds.polySphere(r=2.5,sx=8,sy=8,name=each+'_sphere', constructionHistory=False)[0]
                spherelist.append(sph)
                cmds.select(sph, r=1)
                cmds.sets(sph, forceElement=sphSG)
                cmds.rotate(0,0,90,sph)
                cmds.parent(sph, geo)  
                cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
                cmds.select(clear=True)


            cmds.parent(geo, j, r=1,)  #parent this to the child joint

            cnt = cmds.aimConstraint(each,geo, u=[0,1,1])
            cmds.polyNormal(geo,ch=False,normalMode=0)
            cmds.delete(cnt)
            cmds.delete(geo,constructionHistory=True)
            
# read in the stored A pose from the other retarget effort
poseFilePath = Path(r"\\vuwstocoissrin1.vuw.ac.nz\SODI_RapidMedia_01\Software\pipeline\python\Maya\jsonPoses")
sp.readInJSONPose(poseFilePath, 'OptiNoNS_APose', NS)

# save a bindPose
cmds.select(joints, replace=True)
cmds.dagPose(n='bindPose', s=True)
