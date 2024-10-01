# from paddleocr import PaddleOCR

from src.lib.detector.onnx import *

LOGGER = Logger(__name__).logger


class ImageMatchResult(object):
    def __init__(self, confidence=0.0, center=None, dst=None, shape=None):
        self.confidence = confidence
        self.center = center
        self.dst = dst
        self.shape = shape


class BfMatchKpDes(object):
    def __init__(self, kp_des):
        self.kp = kp_des[0]
        self.des = kp_des[1]

    def is_valid(self):
        return len(self.kp) > 0 and self.des is not None


class Detector(object):
    def __init__(self, weights):
        # self.ocr = PaddleOCR(use_angle_cls=True, lang="ch", show_log=False)
        self.ocr = None
        self.sift = cv2.SIFT_create()
        self.bf_matcher = cv2.BFMatcher()
        self.model = Onnx(weights)

    def ocr_match(self, img, key_text_list):
        result = self.ocr.ocr(img, cls=True)
        for each in result:
            # TODO: replace result with correct ocr result
            for key_text in key_text_list:
                if key_text in each:
                    return each
        return None

    def bf_match_one(self, frame_kp_des, key_img):
        key_img_kp_des = BfMatchKpDes(self.sift.detectAndCompute(key_img, None))
        if not key_img_kp_des.is_valid():
            LOGGER.debug("Failed to get kp and des from key img.")
            return 0, None

        matches = self.bf_matcher.knnMatch(key_img_kp_des.des, frame_kp_des.des, k=2)
        good_matches = []
        for m, n in matches:
            if m.distance < 0.90 * n.distance:
                good_matches.append(m)

        if len(good_matches) <= 4:
            LOGGER.debug("Failed to match by bf")
            return 0, None

        LOGGER.debug("Succeed to match by bf with number of bf good matches: {}".format(len(good_matches)))

        try:
            frame_pts = np.float32([frame_kp_des.kp[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            key_img_pts = np.float32([key_img_kp_des.kp[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)

            M, mask = cv2.findHomography(key_img_pts, frame_pts, cv2.RANSAC, 5.0)
            h, w = key_img.shape[:2]
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)

            center_x = int((dst[0][0][0] + dst[1][0][0] + dst[2][0][0] + dst[3][0][0]) / 4)
            center_y = int((dst[0][0][1] + dst[1][0][1] + dst[2][0][1] + dst[3][0][1]) / 4)
        except cv2.error as e:
            LOGGER.error("bf match failed: {}".format(e))
            return 0, None

        return len(good_matches), center_x, center_y, dst

    def bf_match(self, frame, key_img_list):
        cv2.imwrite("debug_frame.png", frame)
        frame_kp_des = BfMatchKpDes(self.sift.detectAndCompute(frame, None))
        if not frame_kp_des.is_valid():
            return None

        best_matches = [0]
        for key_img in key_img_list:
            result = self.bf_match_one(frame_kp_des, key_img)
            if result and result[0] > best_matches[0]:
                best_matches = result

        return best_matches

    def template_match_one(self, frame, key_img):
        # cv2.imwrite("key_img.png", key_img)
        gray_key_img = cv2.cvtColor(key_img, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(frame, gray_key_img, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        # print(max_val)
        if max_val < 0.65:
            return ImageMatchResult()

        key_img_height, key_img_width, _ = key_img.shape
        center_x = max_loc[0] + key_img_width // 2
        center_y = max_loc[1] + key_img_height // 2

        return ImageMatchResult(max_val, (center_x, center_y), max_loc, [key_img_height, key_img_width])

    def template_match(self, frame, key_img_list):
        # cv2.imwrite("debug_frame.png", frame)

        start = time.time()

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        best = ImageMatchResult()
        for key_img in key_img_list:
            result = self.template_match_one(gray_frame, key_img)
            if result and result.confidence > best.confidence:
                best = result

        cost = 1000 * (time.time() - start)

        if cost > 50:
            LOGGER.debug(f"template match cost {cost}ms")

        return best

    def img_match(self, frame, key_img_list):
        # return self.bf_match(frame, key_img_list)
        return self.template_match(frame, key_img_list)

    def inference(self, frame, conf_thres=0.8, save_img=False) -> [YoloResult]:
        return self.model.inference(frame, conf_thres=conf_thres, save_img=save_img)
