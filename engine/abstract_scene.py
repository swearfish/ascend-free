class AbstractScene:
    """
    The interface for scene manager scenes.
    Use Scene super-class instead to get auto-wired basic components.
    """

    def enter(self):
        """
        Called when entering the scene. Use it to allocate any resources.
        Note: the scene object might be kept in memory even though the scene is not active anymore
        """
        pass

    def exit(self) -> None:
        """
        Called when leaving the scene. Use it to free any resources.
        Note: the scene object might be kept in memory even though the scene is not active anymore
        """
        pass

    def update(self, total_time: float, frame_time: float) -> None:
        """
        Update the current scene
        :param total_time: The total time passed since scene start
        :param frame_time: The time passed since last update
        """
        pass

    def draw(self) -> None:
        """
        Draw the current scene
        """
        pass

    def handle_back_key(self) -> bool:
        """
        SceneManager will invoke this when back button (ESC key or mouse in the four corners) hit.
        If the scene returns False here, SceneManager won't pop the last scene from history.
        We use this for scenes like Start where back key won't go back to New Game or Main Menu, but
        continue to Galaxy screen instead.
        :return: False if you want to handle back key instead of the SceneManager
        """
        return True

    def use_history(self) -> bool:
        """
        Return False if you don't want this scene to be recorded in history.
        Without history, the back button from the next scene won't return to this one,
        but will return to the last scene that actually returned use_history True.
        We use this for scenes like New Game, Start and Winning.
        """
        return True
