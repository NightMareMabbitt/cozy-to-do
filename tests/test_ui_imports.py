import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_ui_modules_import():
    import ui.main_window
    import ui.sections
    from ui.sections import HeaderSection, InputSection, GoalsListSection, ActionsSection

    assert ui.main_window is not None
    assert HeaderSection is not None
    assert InputSection is not None
    assert GoalsListSection is not None
    assert ActionsSection is not None
