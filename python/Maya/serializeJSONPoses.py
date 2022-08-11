import pymel.core as pm
import json
from collections import OrderedDict
from pymel.core import Path

def writeOutJSONPose(joints, poseName):
    joints = sorted(joints)
    
    poseDict = OrderedDict()
    
    for jnt in joints:
        #t = list(jnt.translate.get())
        r = list(jnt.rotate.get())
        #poseDict[jnt.nodeName()] = {'t':t, 'r':r}
        poseDict[jnt.nodeName()] = {'r':r}
        
    #print(json.dumps(poseDict, indent=4))
    
    poseFilePath = r"\\vuwstocoissrin1.vuw.ac.nz\SODI_RapidMedia_01\Software\pipeline\python\Maya\jsonPoses\{0}.json".format(poseName)
    
    with open(poseFilePath, 'w') as p:
        json.dump(poseDict, p, indent=4)

#get all the joints below the selected
#joints = pm.ls(sl=True,type='joint', dag=True, ap=True)
#writeOutJSONPose(joints)


def readInJSONPose(poseFilePath, newPose='OptiNoNS_APose', NS=None):
    jsons = poseFilePath.glob("*.json")
    
    jsonPose = [p for p in jsons if newPose in p][0]
    if jsonPose.exists():
       poseData = json.load(open(jsonPose))
       
       for j,v in poseData.iteritems():
           for c, vals in v.iteritems():
               print("{0}:{1}".format(c,vals)) 
               if NS==None:
                   j = pm.PyNode(j)
               else:
                   j = pm.PyNode("{0}:{1}".format(NS,j))
               try:
                   j.attr(c).set(vals)
               except:
                   print("{0} not found".format(j))
    else:
        print("Did not find {0] in the path: {1}".format(newPose, poseFilePath))

#poseFilePath = Path(r"\\vuwstocoissrin1.vuw.ac.nz\SODI_RapidMedia_01\SetupAssets\Maya\jsonPoses")
#readinJSONPose(poseFilePath, 'OptiNoNS_APose')
