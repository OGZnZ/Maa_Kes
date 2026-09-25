from maa.toolkit import Toolkit

for i in Toolkit.find_desktop_windows():
    print(i)


@staticmethod
def find_desktop_windows() -> List[DesktopWindow]:
    """Query all desktop window information.

    Returns:
        List[DesktopWindow]: List of desktop windows
    """
    Toolkit._set_api_properties()
