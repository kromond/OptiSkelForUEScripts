print("Hey Ho, Let's go")

import unreal

def fixup_selected_level_sequence():
    # Get the Actor and Level Sequence Editor subsystems
    actor_system = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    ls_system = unreal.get_editor_subsystem(unreal.LevelSequenceEditorSubsystem)

    # Get the Content Browser selection
    selection = unreal.EditorUtilityLibrary.get_selected_assets()
    # Filter the selection for Level Sequences
    sequences = unreal.EditorFilterLibrary.by_class(selection, unreal.LevelSequence)
    # Iterate over the Level Sequences
    for seq in sequences:
        # load it
        seq_asset_path = seq.get_path_name()
                            # get the start end time of the sequence
        start = seq.get_playback_start()
        end = seq.get_playback_end()
        seq_asset = unreal.EditorAssetLibrary.load_asset(seq_asset_path)
        unreal.log(f"Fixing up {seq_asset}")
        # unreal.LevelSequenceEditorBlueprintLibrary.ge
            # Get track filter names and print them
        bindings = seq.get_bindings()
        seperation = 78
        for binding in bindings:
            name = binding.get_display_name()
            if 'MannyActor' == name:
                tracks = binding.find_tracks_by_type(unreal.MovieScene3DTransformTrack)
                for track in tracks: 
                    # unreal.log(f"track: {track.get_display_name()}")         # look for the tracks with Manny transforms, change the -40 in Y to -80
                    # unreal.log(f"track: {track.get_class()}")  
                    section = track.add_section()
                    # set the section start and end time
                    section.set_range(start-30, end)
                    # set the transform values and add a key at start time
                    for channel in section.get_channels():
                        # unreal.log(f"Channel: {channel.get_name()}")
                        if "Location.Y" in channel.get_name():
                            channel.set_default(-72)
                            channel.add_key(time=unreal.FrameNumber(start-30), new_value=-seperation)
            if 'QuinnActor' == name:
                tracks = binding.find_tracks_by_type(unreal.MovieScene3DTransformTrack)
                for track in tracks: 
                    # unreal.log(f"track: {track.get_display_name()}")         # look for the tracks with Manny transforms, change the -40 in Y to -80
                    # unreal.log(f"track: {track.get_class()}")  
                    section = track.add_section()
                    # set the section start and end time
                    section.set_range(start-30, end)  
                    # set the transform values and add a key at start time
                    for channel in section.get_channels():
                        # unreal.log(f"Channel: {channel.get_name()}")
                        if "Location.Y" in channel.get_name():
                            channel.set_default(72)
                            channel.add_key(time=unreal.FrameNumber(start-30), new_value=seperation)
            # unreal.LevelSequenceEditorBlueprintLibrary.refresh_current_level_sequence()
            # save the sequence
            unreal.EditorAssetLibrary.save_asset(seq.get_path_name(), only_if_is_dirty=True)   


                        