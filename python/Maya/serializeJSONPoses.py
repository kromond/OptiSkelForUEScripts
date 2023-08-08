import pymel.core as pm
import json
from collections import OrderedDict
from pymel.core import Path
import maya.cmds as cmds
import glob
from pathlib import Path

jsonDir = './jsonPoses/'
jsonDirs = './jsonPoses/{0}.json'


def write_out_JSON_pose(pose_file_path, joints, pose_name):
    joints = sorted(joints)
    
    pose_dict = OrderedDict()
    
    for jnt in joints:
        #t = list(jnt.translate.get())
        r = list(jnt.rotate.get())
        #poseDict[jnt.nodeName()] = {'t':t, 'r':r}
        pose_dict[jnt.nodeName()] = {'r':r}
        
    #print(json.dumps(poseDict, indent=4))
        
    with open("{0}/{1}.json".format(pose_file_path, pose_name), 'w') as p:
        json.dump(pose_dict, p, indent=4)

#get all the joints below the selected
#joints = pm.ls(sl=True,type='joint', dag=True, ap=True)
#write_out_JSON_pose(joints)

def read_in_JSON_pose(pose_file_path, new_pose='OptiNoNS_APose', NS=None, name_separator=":"):
    print("NS: {0} name_separator: {1}".format(NS, name_separator))
    jsons = glob.glob("{}\\*.json".format(pose_file_path))
    json_pose = [p for p in jsons if new_pose in p]
    if json_pose:
        print("FOUND the JSON pose file: {}".format(json_pose))
        json_pose = Path(json_pose[0])
        if json_pose.exists():
            pose_data = json.load(open(json_pose))
            for j,v in pose_data.items():
                for c, vals in v.items():
                    print("{0}_{1}".format(c,vals)) 
                    if NS==None:
                        j = pm.PyNode(j)
                    else:
                        j = pm.PyNode("{0}{1}{2}".format(NS,name_separator,j))
                    print("j is now {}".format(j))
                    try:
                        print("j: {0}, c: {1}, vals: {2}".format(j,c,vals))                        
                        j.attr(c).set(vals)
                    except:
                        print("{0}  !! this item failed to pose for some reason".format(j))
    else:
        print("Did not find {0] in the path: {1}".format(new_pose, pose_file_path))

# pose_file_path = Path(r".\jsonPoses")
# read_in_JSON_pose(pose_file_path, 'OptiNoNS_Apose_v02')
# joints = pm.ls(sl=True,type='joint', dag=True, ap=True)
# write_out_JSON_pose(pose_file_path, joints, "BinArmsTPose")