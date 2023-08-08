# OptiSkelForUEScripts
Some Maya scripts for making a skeleton that I can use to bring Optitrack FBX motions from Motive to Unreal Engine

included here are json poses for getting an A Pose on to an optitrack skel
Also included xml to characterize Metahuman skel and Quinn


# How to Run
Keep all the files together

Set your maya project at your desired directory and create project windows, put the files in `python/Maya` in the script folder:
+ Root Directory
    + ...
    + scnenes
    + scripts
        + jsonPoses
        + OptiSkelBuildStickGeo.py
        + OptiSkelPrep.py
        + serializeJSONPoses.py
    + sound
    + ...

or do like I do and put them anywhere and update your Maya script path like this in the maya script editor right at the start:
import sys
```
from pathlib import Path
scriptDir = Path("//path_to_where_you_saved_this/OptiSkelForUEScripts/python/Maya/")
if scriptDir not in sys.path:
    sys.path.append(scriptDir)
```


The script is updated to take an FBX exported with a *single skeleton* with either a ":" or "_" for the name separator.  There is a variable to control this

If you exported an FBX from Motive with the new 'sticks' option, you will have a mesh at the root of the skeleton hirearchy and joints under this.  UE can read this in and use it, but you can not Live Link stream on to this because in UE you will see there is no bone named 'Root'.  This script can fix this by adding a root bone and renaming the mesh

The script now poses the skeleton into a perfect A Pose which will make retargeting much nicer

<<<<<<< HEAD
NOTE: only tested with Maya 2022.4 and UE 5.2
=======
NOTE: only tested with Maya 2022.4 

![image](https://github.com/kromond/OptiSkelForUEScripts/assets/5624947/88c7bd80-aa1e-41a3-afd8-61c031e4e16e)
>>>>>>> 09481c1542705fa80c156743172cf4f6756d46b4
