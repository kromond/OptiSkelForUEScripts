import unreal

def addFootSpeedForSelectedAnims():
    # This function is to add speed curves using the MotionExtractor animation modifier
    # This function assumes a skeleton from Optitrack with these bone names:
    # LeftToeBase
    # RightToeBase

    # for a manny skeleton these bone names would be:
    # ball_l
    # ball_r

    # These curves can then be used to stick the feet 
    # See here: https://docs.unrealengine.com/5.2/en-US/fix-foot-sliding-with-ik-retargeter-in-unreal-engine/
    # I suspect this fails if the Animation Modifier Library plugin is not loaded

    assets = unreal.EditorUtilityLibrary.get_selected_assets()
    # filter for AnimSequence
    anims = unreal.EditorFilterLibrary.by_class(assets, unreal.AnimSequence)
    for anim in anims:
        
        anim_asset_path = anim.get_outer().get_name() #https://dev.epicgames.com/community/learning/tutorials/qMy2/unreal-engine-solved-tryconvertfilenametolongpackagename-objectpath-warning
        a = unreal.EditorAssetLibrary.load_asset(anim_asset_path)

        # left foot
        motion_mod_l = unreal.MotionExtractorModifier()
        print(motion_mod_l)
        motion_mod_l.set_editor_property("bone_name", "LeftToeBase")
        # motion_mod_l.set_editor_property("bone_name", "ball_l")
        motion_mod_l.set_editor_property("motion_type", unreal.MotionExtractor_MotionType.TRANSLATION_SPEED)
        motion_mod_l.set_editor_property("axis", unreal.MotionExtractor_Axis.XYZ)
        motion_mod_l.on_apply(a)

        # right foot
        motion_mod_r = unreal.MotionExtractorModifier()
        print(motion_mod_r)
        motion_mod_r.set_editor_property("bone_name", "RightToeBase")
        # motion_mod_r.set_editor_property("bone_name", "ball_r")
        motion_mod_r.set_editor_property("motion_type", unreal.MotionExtractor_MotionType.TRANSLATION_SPEED)
        motion_mod_r.set_editor_property("axis", unreal.MotionExtractor_Axis.XYZ)
        motion_mod_r.on_apply(a)

        # save the anim. 
        unreal.EditorAssetLibrary.save_asset(a.get_path_name())
    # also save the skeleton because we added curves
    unreal.EditorAssetLibrary.save_asset(unreal.AnimSequence.get_skeleton(a).get_path_name())
        
    return None