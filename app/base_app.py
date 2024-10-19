import time

from func_timeout import FunctionTimedOut

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

    def start_game(self):
        LOGGER.info("Start game")
        self.device.client.device.app_start("com.tencent.tmgp.dnf")

    def exit_game(self):
        LOGGER.info("Exit game")
        self.device.client.device.app_stop("com.tencent.tmgp.dnf")

    def mute_game(self, mute=True):
        LOGGER.info(f"{'Mute' if mute else 'Un-mute'} game")
        self.device.client.device.shell(f"cmd media_session volume --set {0 if mute else 15}")

    def swipe_up(self, coordinate=None, distance=200):
        src = coordinate if coordinate else (
        self.device.client.resolution[0] // 2, self.device.client.resolution[1] // 2)
        dst = (src[0], max(src[1] - distance, 0))
        self.device.swipe(src, dst)

    def swipe_down(self, coordinate=None, distance=200):
        src = coordinate if coordinate else (
        self.device.client.resolution[0] // 2, self.device.client.resolution[1] // 2)
        dst = (src[0], min(src[1] + distance, self.device.client.resolution[1]))
        self.device.swipe(src, dst)

    def swipe_left(self, coordinate=None, distance=200):
        src = coordinate if coordinate else (
        self.device.client.resolution[0] // 2, self.device.client.resolution[1] // 2)
        dst = (max(src[0] - distance, 0), src[1])
        self.device.swipe(src, dst)

    def swipe_right(self, coordinate=None, distance=200):
        src = coordinate if coordinate else (
        self.device.client.resolution[0] // 2, self.device.client.resolution[1] // 2)
        dst = (min(src[0] + distance, self.device.client.resolution[0]), src[1])
        self.device.swipe(src, dst)

    def back(self):
        self.device.client.device.keyevent("BACK")

    def return_to_base_scenario(self):
        LOGGER.info("Start to return to base scenario")

        while True:
            try:
                self.ui_ctx.wait_ui_element(UIElementCtx.CategoryBase, "setting_select_character", timeout=3)
            except FunctionTimedOut:
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

    def change_character(self, character):
        LOGGER.info(f"Change character to {character}")

        self.return_to_base_scenario()
        self.ui_ctx.click_ui_element(UIElementCtx.CategoryBase, "select_character")

        # Scroll to top and search character.
        for i in range(3):
            self.swipe_down()
            time.sleep(0.2)
        time.sleep(5)

        while True:
            try:
                self.ui_ctx.click_ui_element(UIElementCtx.CategoryCharacter, character, timeout=3)
                break
            except LookupError:
                # Character not found, scroll down and re-search.
                self.swipe_up()
                time.sleep(5)
                continue

        try:
            self.ui_ctx.click_ui_element(UIElementCtx.CategoryBase, "change_character")
            self.ui_ctx.wait_ui_element(UIElementCtx.CategoryBase, "package")
        except LookupError:
            # Current character is target character.
            LOGGER.info(f"Current character is already {character}")

        self.return_to_base_scenario()
