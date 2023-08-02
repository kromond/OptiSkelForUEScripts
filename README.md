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
        + OptiSkel_to_SKM.py
        + serializeJSONPoses.py
    + sound
    + ...

or put them anywhere in your Maya script path
or do like I do and put them anywhere and update your Maya script path like this:
import sys
```
from pathlib import Path
scriptDir = Path("//path_to_where_you_saved_this/OptiSkelForUEScripts/python/Maya/")
if scriptDir not in sys.path:
    sys.path.append(scriptDir)
```


The script is updated to take an FBX exported with a *single skeleton* with either a ":" or "_" for the name separator.  There is a variable to control this

If you exported with the new 'sticks' option, you will have a mesh at the root of the skeleton hirearchy and joints under this.  UE can read this in and use it, but you can Live Link stream on to this because in UE you will see there is no bone named 'Root'.  This script can fix this

The script now poses the skeleton into a perfect A Pose which will make retargeting much nicer

NOTE: only tested with Maya 2022.4 