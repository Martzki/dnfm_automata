import time

from common.log import Logger
from ui.ui import UIElementCtx

LOGGER = Logger(__name__).logger


class BaseApp(object):
    def __init__(self, device, ui_ctx: UIElementCtx):
        self.device = device
        self.ui_ctx = ui_ctx

    def init(self):
        self.device.register_init_handler(self.init_handler)
        self.device.register_frame_handler(self.frame_handler)
        self.device.start()

    def init_handler(self):
        pass

    def frame_handler(self, frame):
        pass

    def exit_game(self):
        pass

    def back(self):
        self.device.client.device.keyevent("BACK")

    def return_to_base_scenario(self):
        LOGGER.info("Start to return to base scenario")

        while True:
            try:
                self.ui_ctx.wait_ui_element(UIElementCtx.CategoryBase, "setting_select_character", timeout=3)
            except TimeoutError:
                self.back()
                continue

            break

        self.back()

        time.sleep(1)

        LOGGER.info("Succeed to return to base scenario")

    def repair_equipments(self):
        LOGGER.info("Start to epair worn equipments")

        self.return_to_base_scenario()

        self.ui_ctx.click_ui_element(UIElementCtx.CategoryBase, "package", timeout=3)
        self.ui_ctx.click_ui_element(UIElementCtx.CategoryBase, "repair", timeout=3)
        self.ui_ctx.click_ui_element(UIElementCtx.CategoryBase, "repair_window_label", timeout=3)

        try:
            self.ui_ctx.click_ui_element(UIElementCtx.CategoryBase, "repair_window_confirm", timeout=3)
        except LookupError:
            self.ui_ctx.click_ui_element(UIElementCtx.CategoryBase, "repair_worn", timeout=3)

            try:
                self.ui_ctx.click_ui_element(UIElementCtx.CategoryBase, "repair_window_confirm", timeout=3)
            except LookupError:
                # Maybe worn is fully repaired.
                pass

        self.return_to_base_scenario()

        LOGGER.info("Succeed to repair worn equipments")
