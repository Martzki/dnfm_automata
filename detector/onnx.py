import onnxruntime
import torch.nn as nn
from ultralytics.utils.plotting import Annotator, colors

from detector.yolo import *

LOGGER = Logger(__name__).logger


class OnnxModel(nn.Module):
    # YOLOv5 MultiBackend class for python inference on various backends
    def __init__(self, weights="yolov5s.pt", device=torch.device("cpu"), dnn=False, data=None, fp16=False, fuse=True):
        super().__init__()
        w = str(weights[0] if isinstance(weights, list) else weights)
        stride = 32  # default stride
        cuda = torch.cuda.is_available() and device.type != "cpu"  # use CUDA

        providers = ["CUDAExecutionProvider", "CPUExecutionProvider"] if cuda else ["CPUExecutionProvider"]
        session = onnxruntime.InferenceSession(w, providers=providers)
        output_names = [x.name for x in session.get_outputs()]
        meta = session.get_modelmeta().custom_metadata_map  # metadata
        if "stride" in meta:
            stride, names = int(meta["stride"]), eval(meta["names"])

        # class names
        if "names" not in locals():
            names = yaml_load(data)["names"] if data else {i: f"class{i}" for i in range(999)}

        self.__dict__.update(locals())  # assign all variables to self

    def forward(self, im, augment=False, visualize=False):
        """Performs YOLOv5 inference on input images with options for augmentation and visualization."""
        if self.fp16 and im.dtype != torch.float16:
            im = im.half()  # to FP16

        im = im.cpu().numpy()  # torch to numpy
        y = self.session.run(self.output_names, {self.session.get_inputs()[0].name: im})

        if isinstance(y, (list, tuple)):
            return self.from_numpy(y[0]) if len(y) == 1 else [self.from_numpy(x) for x in y]
        else:
            return self.from_numpy(y)

    def from_numpy(self, x):
        """Converts a NumPy array to a torch tensor, maintaining device compatibility."""
        return torch.from_numpy(x).to(self.device) if isinstance(x, np.ndarray) else x

    def warmup(self, imgsz=(1, 3, 640, 640)):
        """Performs a single inference warmup to initialize model weights, accepting an `imgsz` tuple for image size."""
        # warmup_types = self.onnx
        if self.device.type != "cpu":
            im = torch.empty(*imgsz, dtype=torch.half if self.fp16 else torch.float, device=self.device)  # input
            for _ in range(2):  #
                self.forward(im)  # warmup


class Onnx(object):
    def __init__(
            self,
            weights,
            data="",
            half=False,  # use FP16 half-precision inference
            imgsz=(640, 640),  # inference size (height, width)
            device="",  # cuda device, i.e. 0 or 0,1,2,3 or cpu
            dnn=False,  # use OpenCV DNN for ONNX inference
    ):
        # Load model
        self.device = select_device(device)
        self.model = OnnxModel(weights, device=self.device, dnn=dnn, data=data, fp16=half)
        self.stride, self.names, self.pt = self.model.stride, self.model.names, False
        self.imgsz = check_img_size(imgsz, s=self.stride)  # check image size
        self.model.warmup(imgsz=(1, 3, *imgsz))  # warmup

    def inference(
            self,
            im0s,
            save_img=False,
            save_crop=False,  # save cropped prediction boxes
            line_thickness=3,  # bounding box thickness (pixels)
            conf_thres=0.25,  # confidence threshold
            iou_thres=0.45,  # NMS IOU threshold
            max_det=1000,  # maximum detections per image
            classes=None,  # filter by class: --class 0, or --class 0 2 3
            augment=False,  # augmented inference
            hide_labels=False,  # hide labels
            hide_conf=False,  # hide confidences
            agnostic_nms=False,  # class-agnostic NMS
    ):
        seen, windows, dt = 0, [], (
            Profile(device=self.device), Profile(device=self.device), Profile(device=self.device))

        im = letterbox(im0s, self.imgsz, stride=self.stride, auto=False)[0]  # padded resize
        im = im.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        im = np.ascontiguousarray(im)  # contiguous

        with dt[0]:
            im = torch.from_numpy(im).to(self.model.device)
            im = im.half() if self.model.fp16 else im.float()  # uint8 to fp16/32
            im /= 255  # 0 - 255 to 0.0 - 1.0
            if len(im.shape) == 3:
                im = im[None]  # expand for batch dim

        # Inference
        with dt[1]:
            pred = self.model(im, augment=augment, visualize=False)

        # NMS
        with dt[2]:
            pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)

        # Second-stage classifier (optional)
        # pred = utils.general.apply_classifier(pred, classifier_model, im, im0s)

        result = []

        # Process predictions
        for i, det in enumerate(pred):  # per image
            seen += 1
            im0 = im0s.copy()
            save_path = str(Path('.') / "inference.png")  # im.jpg
            imc = im0.copy() if save_crop else im0  # for save_crop
            annotator = Annotator(im0, line_width=line_thickness, example=str(self.names))
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    c = int(cls)  # integer class
                    confidence = float(conf)

                    result.append(YoloResult(c, confidence, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3]))))
                    # LOGGER.debug(f"class: {c}, confidence: {confidence}, xyxy: {xyxy}")

                    if save_img or save_crop:  # Add bbox to image
                        c = int(cls)  # integer class
                        label = None if hide_labels else (self.names[c] if hide_conf else f"{self.names[c]} {conf:.2f}")
                        annotator.box_label(xyxy, label, color=colors(c, True))
                    if save_crop:
                        # save_one_box(xyxy, imc, file=Path('.') / "crops" / self.names[c] / f"{p.stem}.jpg", BGR=True)
                        pass

            # Stream results
            im0 = annotator.result()

            # Save results (image with detections)
            if save_img:
                cv2.imwrite(save_path, im0)

            # Print time (inference-only)
            # LOGGER.debug(f"{'' if len(det) else '(no detections), '}{dt[1].dt * 1E3:.1f}ms")

        # Print results
        t = tuple(x.t / seen * 1e3 for x in dt)  # speeds per image
        LOGGER.debug(
            f"Speed: %.1fms pre-process, %.1fms inference, %.1fms NMS per image at shape {(1, 3, *self.imgsz)}" % t)

        return result
