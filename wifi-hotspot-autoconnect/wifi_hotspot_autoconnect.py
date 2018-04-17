
import library.hotspot_wrapper as wrapper


def hotspot_exists():
    return wrapper.hotspot_exists()


def autoconnect_status():
    return wrapper.status_hotspot_autoconnect()


def autoconnect_set(value: bool):
    wrapper.set_autoconnect(value)