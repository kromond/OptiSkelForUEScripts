import pymel.core as pm
import json
from collections import OrderedDict
from pymel.core import Path
import maya.cmds as cmds
import glob
from pathlib import Path

rootDir = cmds.workspace( q=True, rd=True )
scriptDir = rootDir + 'scripts/'
jsonDir = rootDir + 'scripts/jsonPoses/'
jsonDirs = rootDir + 'scripts/jsonPoses/{0}.json'


def writeOutJSONPose(poseFilePath, joints, poseName):
    joints = sorted(joints)
    
    poseDict = OrderedDict()
    
    for jnt in joints:
        #t = list(jnt.translate.get())
        r = list(jnt.rotate.get())
        #poseDict[jnt.nodeName()] = {'t':t, 'r':r}
        poseDict[jnt.nodeName()] = {'r':r}
        
    #print(json.dumps(poseDict, indent=4))
        
    with open("{0}/{1}.json".format(poseFilePath, poseName), 'w') as p:
        json.dump(poseDict, p, indent=4)

#get all the joints below the selected
#joints = pm.ls(sl=True,type='joint', dag=True, ap=True)
#writeOutJSONPose(joints)


def readInJSONPose(poseFilePath, newPose='OptiNoNS_APose', NS=None):
    jsons = glob.glob("{}/*.json".format(poseFilePath))
    
    jsonPose = Path([p for p in jsons if newPose in p][0])
    print("Json pose: {} found".format(jsonPose))
    if jsonPose.exists():
       poseData = json.load(open(jsonPose))
       
       for j,v in poseData.items():
            # Check if the joint exist
            if not cmds.objExists(j):
                print("Root joint '{}' does not exist.".format(j))
                continue
            for c, vals in v.items():
               print("{0}_{1}".format(c,vals)) 
               if NS==None:
                   j = pm.PyNode(j)
               else:
                   j = pm.PyNode("{0}_{1}".format(NS,j))
               try:
                   j.attr(c).set(vals)
               except:
                   print("{0} not found".format(j))
    else:
        print("Did not find {0] in the path: {1}".format(newPose, poseFilePath))

# poseFilePath = Path(r"\\vuwstocoissrin1.vuw.ac.nz\SODI_RapidMedia_01\Software\OptiSkelForUEScripts\python\Maya\jsonPoses")
# readInJSONPose(poseFilePath, 'BinArmsTPose')
# joints = pm.ls(sl=True,type='joint', dag=True, ap=True)
# writeOutJSONPose(poseFilePath, joints, "BinArmsTPose")