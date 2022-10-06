# OptiSkelForUEScripts
Some Maya scripts for making a skeleton that I can use to bring Optitrack FBX motions from Motive to Unreal Engine

Also included xml to characterize Metahuman skel


# How to Run
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


Make sure your skeleton's naming convention follows this pattern: `NameSpace_JointName`. Example: Jane_Root

Select your skeleton hierarchy and run `serializeJSONPoses.py` then `OptiSkel_to_SKM.py` to get a A-Pose skeletal mesh that is in the same pose as UE Metahuman.

For Maya 2022 uses python 3 and the '.iteritems' method needs to change to '.items'
