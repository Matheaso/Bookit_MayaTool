import sys
import importlib
import traceback


def reload_package(package_name):
    for name, module in list(sys.modules.items()):
        if name == package_name or name.startswith(package_name + "."):
            try:
                importlib.reload(module)
            except Exception:
                traceback.print_exc()

def close_ui():
    try:
        import bookit.ui as ui

        if ui.BookitToolUI.dlg_instance:
            ui.BookitToolUI.dlg_instance.close()
            ui.BookitToolUI.dlg_instance.deleteLater()
            ui.BookitToolUI.dlg_instance = None

    except Exception:
        traceback.print_exc()

def run():
    close_ui()
    reload_package('bookit')

    import bookit.ui as ui
    ui.show()
