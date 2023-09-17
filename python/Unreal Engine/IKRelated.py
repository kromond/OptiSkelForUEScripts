import unreal

# All this is to work with the Optitrack Skeleton, with a root bone and force front x 

def makeIKRFromSKM(skm):
    # Get the name of this skm, and the path.  This is where we will put the rig
    fname = unreal.EditorAssetLibrary.get_fname(skm)
    fpath = unreal.EditorAssetLibrary.get_path_name(skm).split(".")[0].replace(str(fname),"")
    print("Name: {0}, Path: {1}".format(fname, fpath))

    # ikr = unreal.load_asset(name = '/Game/Characters/Mannequins/Rigs/IK_Mannequin', outer = None)

    # Get the asset tools.
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    
    # Create an IK Rig in the location defined by the file path. For example: ` …/Game/IK_Mannequin`.
    ikr = asset_tools.create_asset(asset_name='IKR_{0}'.format(fname),
        package_path=fpath, asset_class=unreal.IKRigDefinition,
        factory=unreal.IKRigDefinitionFactory())
    
    # Get the IK Rig controller.
    ikr_controller = unreal.IKRigController.get_controller(ikr)
    ikr_controller.set_skeletal_mesh(skm)
    fbik_index = ikr_controller.add_solver(unreal.IKRigFBIKSolver)

    ikr_controller.add_new_goal("hand_l_goal", "LeftHand")
    ikr_controller.add_new_goal("hand_r_goal", "RightHand")
    ikr_controller.add_new_goal("foot_l_goal", "LeftFoot")
    ikr_controller.add_new_goal("foot_r_goal", "RightFoot")
    ikr_controller.add_new_goal("head_goal", "Head")
    ikr_controller.add_bone_setting("Spine", 0)
    ikr_controller.add_bone_setting("Spine1", 0)
    ikr_controller.add_bone_setting("LeftShoulder", 0)
    ikr_controller.add_bone_setting("RightShoulder", 0)
    ikr_controller.add_bone_setting("LeftForeArm", 0)
    ikr_controller.add_bone_setting("RightForeArm", 0)
    ikr_controller.add_bone_setting("RightLeg", 0)
    ikr_controller.add_bone_setting("LeftLeg", 0)

    # spine settings
    spine_setting = ikr_controller.get_bone_settings("Spine", 0)
    spine_setting.rotation_stiffness = 1
    spine1_setting = ikr_controller.get_bone_settings("Spine1", 0)
    spine1_setting.rotation_stiffness = 1
    # other bone settings
    LeftShoulder_setting = ikr_controller.get_bone_settings("LeftShoulder", 0)
    LeftShoulder_setting.rotation_stiffness = 1
    RightShoulder_setting = ikr_controller.get_bone_settings("RightShoulder", 0)
    RightShoulder_setting.rotation_stiffness = 1
    LeftForeArm_setting = ikr_controller.get_bone_settings("LeftForeArm", 0)
    LeftForeArm_setting.use_preferred_angles  = True
    LeftForeArm_setting.preferred_angles = unreal.Vector(0,0,90)
    RightForeArm_setting = ikr_controller.get_bone_settings("RightForeArm", 0)
    RightForeArm_setting.use_preferred_angles  = True
    RightForeArm_setting.preferred_angles = unreal.Vector(0,90,0)
    LeftLeg_setting = ikr_controller.get_bone_settings("LeftLeg", 0)
    LeftLeg_setting.use_preferred_angles  = True
    LeftLeg_setting.preferred_angles = unreal.Vector(0,-90,0)
    RightLeg_setting = ikr_controller.get_bone_settings("RightLeg", 0)
    RightLeg_setting.use_preferred_angles  = True
    RightLeg_setting.preferred_angles = unreal.Vector(0,-90,0)    

    # set these fbik attributes
    fbik = ikr_controller.get_solver_at_index(fbik_index)
    fbik.root_behavior=unreal.PBIKRootBehavior.PRE_PULL
    # fbik.allow_stretch=True

    # set the root bone of the solver
    ikr_controller.set_root_bone("Hips", 0)
    # set the retarget root
    ikr_controller.set_retarget_root("Hips")

    # Add a Retarget Chains with a start bone, end bone, and goal.
    ikr_controller.add_retarget_chain("Root","Root","Root","")
    ikr_controller.add_retarget_chain("Spine", "Spine", "Spine1", "")
    ikr_controller.add_retarget_chain("LeftArm", "LeftArm", "LeftHand", "hand_l_goal")
    ikr_controller.add_retarget_chain("RightArm", "RightArm", "RightHand", "hand_r_goal")
    ikr_controller.add_retarget_chain("LeftLeg", "LeftUpLeg", "LeftToeBase", "foot_l_goal")
    ikr_controller.add_retarget_chain("RightLeg", "RightUpLeg", "RightToeBase", "foot_r_goal")
    ikr_controller.add_retarget_chain("Head", "Neck", "Head", "")
    ikr_controller.add_retarget_chain("LeftClavicle", "LeftShoulder", "LeftShoulder", "")
    ikr_controller.add_retarget_chain("RightClavicle", "RightShoulder", "RightShoulder", "")

    ikr_controller.add_retarget_chain("LeftThumb", "LeftHandThumb1", "LeftHandThumb3", "")
    ikr_controller.add_retarget_chain("LeftIndex", "LeftHandIndex1", "LeftHandIndex3", "")
    ikr_controller.add_retarget_chain("LeftMiddle","LeftHandMiddle1","LeftHandMiddle3","")
    ikr_controller.add_retarget_chain("LeftRing", "LeftHandRing1", "LeftHandRing3","")
    ikr_controller.add_retarget_chain("LeftPinky", "LeftHandPinky1", "LeftHandPinky3", "")

    ikr_controller.add_retarget_chain("RightThumb", "RightHandThumb1", "RightHandThumb3", "")
    ikr_controller.add_retarget_chain("RightIndex", "RightHandIndex1", "RightHandIndex3", "")
    ikr_controller.add_retarget_chain("RightMiddle","RightHandMiddle1","RightHandMiddle3","")
    ikr_controller.add_retarget_chain("RightRing", "RightHandRing1", "RightHandRing3","")
    ikr_controller.add_retarget_chain("RightPinky", "RightHandPinky1", "RightHandPinky3", "")
 
    # Save asset
    unreal.EditorAssetLibrary.save_asset(ikr.get_path_name())
    return ikr

def makeRTGForManny(ikr_source, ikr_target):
    
    # Get the name of this skm, and the path.  This is where we will put the rig
    fname = unreal.EditorAssetLibrary.get_fname(ikr_source)
    fpath = unreal.EditorAssetLibrary.get_path_name(ikr_source).split(".")[0].replace(str(fname),"")
    # print("Name: {0}, Path: {1}".format(fname, fpath))

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

    # Create an IK Retargeter asset in the location defined by the file path. For example, `.../Game/RTG_Mannequin`.
    rtg = asset_tools.create_asset(asset_name='RTG_{0}'.format(fname), package_path=fpath, asset_class=unreal.IKRetargeter, factory=unreal.IKRetargetFactory())
    
    # Get the IK Retargeter controller
    rtg_controller = unreal.IKRetargeterController.get_controller(rtg)
    
    # Load the Source and Target IK Rigs. 
    rtg_controller.set_ik_rig(unreal.RetargetSourceOrTarget.SOURCE, ikr_source)
    rtg_controller.set_ik_rig(unreal.RetargetSourceOrTarget.TARGET, ikr_target)

    # Map chains using a fuzzy string match, which will force a remap.
    rtg_controller.auto_map_chains(unreal.AutoMapChainType.FUZZY, True)
    
    # All of these will get NONE because they are not in the source, only the target 
    noneList = ["LeftLowerArmTwist01", "LeftLowerArmTwist02", "LeftIndexMetacarpal", "LeftMiddleMetacarpal","LeftRingMetacarpal",
                "LeftPinkyMetacarpal", "LeftUpperArmTwist01","LeftUpperArmTwist02","RightLowerArmTwist01", "RightLowerArmTwist02", 
                "RightIndexMetacarpal", "RightMiddleMetacarpal","RightRingMetacarpal", "RightPinkyMetacarpal", 
                "RightUpperArmTwist01","RightUpperArmTwist02", "LeftCalfTwist01","LeftCalfTwist02","LeftThighTwist01",
                "LeftThighTwist02", "RightCalfTwist01","RightCalfTwist02","RightThighTwist01",
                "RightThighTwist02", "FootRootIK", "LeftFootIK", "RightFootIK","HandRootIK","HandGunIK","LeftHandIK","RightHandIK"]
    for item in noneList:
        rtg_controller.set_source_chain("None", item)
    
    # Because my source is front X, rotate the target to match
    rotation_offset = unreal.Rotator()
    rotation_offset.yaw = -90
    rtg_controller.set_rotation_offset_for_retarget_pose_bone("root", rotation_offset.quaternion(), unreal.RetargetSourceOrTarget.TARGET)

    unreal.EditorAssetLibrary.save_asset(rtg.get_path_name())
    return rtg

def fixRTGChainMapping(rtg_asset):
    rtg_controller = unreal.IKRetargeterController.get_controller(rtg_asset)
    print("RTG: {}".format(rtg_controller))
        # All of these will get NONE
    noneList = ["LeftLowerArmTwist01", "LeftLowerArmTwist02", "LeftIndexMetacarpal", "LeftMiddleMetacarpal","LeftRingMetacarpal",
                "LeftPinkyMetacarpal", "LeftUpperArmTwist01","LeftUpperArmTwist02","RightLowerArmTwist01", "RightLowerArmTwist02", 
                "RightIndexMetacarpal", "RightMiddleMetacarpal","RightRingMetacarpal", "RightPinkyMetacarpal", 
                "RightUpperArmTwist01","RightUpperArmTwist02", "LeftCalfTwist01","LeftCalfTwist02","LeftThighTwist01",
                "LeftThighTwist02", "RightCalfTwist01","RightCalfTwist02","RightThighTwist01",
                "RightThighTwist02", "FootRootIK", "LeftFootIK", "RightFootIK","HandRootIK","HandGunIK","LeftHandIK","RightHandIK"]
    for item in noneList:
        rtg_controller.set_source_chain("None", item)
    print("Chains fixed up")
