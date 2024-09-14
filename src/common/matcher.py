import cv2
import numpy as np

SIFT = cv2.SIFT_create()
BF_MATCHER = cv2.BFMatcher()
SIFT_BF_MATCHER_THRESHOLD = 0.80
MIN_GOOD_SIFT_BF_MATCH = 5


def sift_bf_match(img, target_img):
    if img is None or target_img is None:
        return None

    img_kp, img_des = SIFT.detectAndCompute(img, None)
    target_img_kp, target_img_des = SIFT.detectAndCompute(target_img, None)

    matches = BF_MATCHER.knnMatch(img_des, target_img_des, k=2)

    good_matches = []
    for m, n in matches:
        if m.distance < SIFT_BF_MATCHER_THRESHOLD * n.distance:
            good_matches.append(m)

    if len(good_matches) < MIN_GOOD_SIFT_BF_MATCH:
        return None

    src_pts = np.float32([img_kp[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([target_img_kp[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    h, w = img.shape[:2]
    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
    dst = cv2.perspectiveTransform(pts, M)

    center_x = int((dst[0][0][0] + dst[1][0][0] + dst[2][0][0] + dst[3][0][0]) / 4)
    center_y = int((dst[0][0][1] + dst[1][0][1] + dst[2][0][1] + dst[3][0][1]) / 4)

    return center_x, center_y
