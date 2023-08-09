import os
import cv2
import pydload
import logging
import numpy as np
import onnxruntime
from detector_utils import preprocess_image

def dummy(x):
    return x

class Detector:
    global detection_model,classes
#    detection_model = "C:\\Users\\ryana\\Downloads\\detector_v2_base_checkpoint.onnx"
#    classes = "C:\\Users\\ryana\\Downloads\\detector_v2_default_classes"
    detection_model = onnxruntime.InferenceSession("C:\\Users\\ryana\\Downloads\\detector_v2_default_checkpoint.onnx")
    classes = [c.strip() for c in open("C:\\Users\\ryana\\Downloads\\detector_v2_default_classes").readlines() if c.strip()]

    def detect(img_path, mode="default", min_prob=None):
        if mode == "fast":
            image, scale = preprocess_image(img_path, min_side=480, max_side=800)
            if not min_prob:
                min_prob = 0.5
        else:
            image, scale = preprocess_image(img_path)
            if not min_prob:
                min_prob = 0.6

        outputs = detection_model.run(
            [s_i.name for s_i in detection_model.get_outputs()],
            {detection_model.get_inputs()[0].name: np.expand_dims(image, axis=0)},
        )

        labels = [op for op in outputs if op.dtype == "int32"][0]
        scores = [op for op in outputs if isinstance(op[0][0], np.float32)][0]
        boxes = [op for op in outputs if isinstance(op[0][0], np.ndarray)][0]

        boxes /= scale
        processed_boxes = []
        for box, score, label in zip(boxes[0], scores[0], labels[0]):
            if score < min_prob:
                continue
            box = box.astype(int).tolist()
            label = classes[label]
            processed_boxes.append(
                {"box": [int(c) for c in box], "score": float(score), "label": label}
            )
        detection_model.end_profiling()
        return processed_boxes

    def censor(img_path, out_path=None, visualize=False, parts_to_blur=[]):
        if not out_path and not visualize:
            print(
                "No out_path passed and visualize is set to false. There is no point in running this function then."
            )
            return

        image = cv2.imread(img_path)
        boxes = Detector.detect(img_path)

        if parts_to_blur:
            boxes = [i["box"] for i in boxes if i["label"] in parts_to_blur]
        else:
            boxes = [i["box"] for i in boxes]

        for box in boxes:
            part = image[box[1] : box[3], box[0] : box[2]]
            image = cv2.rectangle(
                image, (box[0], box[1]), (box[2], box[3]), (0, 0, 0), cv2.FILLED
            )

        if visualize:
            cv2.imshow("Blurred image", image)
            cv2.waitKey(0)

        if out_path:
            cv2.imwrite(out_path, image)


if __name__ == "__main__":
    m = Detector()
    print(m.detect("/Users/bedapudi/Desktop/n2.jpg"))

"""
    def __init__(model_name="default"):
        checkpoint_url = FILE_URLS[model_name]["checkpoint"]
        classes_url = FILE_URLS[model_name]["classes"]

        home = os.path.expanduser("~")
        model_folder = os.path.join(home, f".NudeNet/")
        if not os.path.exists(model_folder):
            os.makedirs(model_folder)

        checkpoint_name = os.path.basename(checkpoint_url)
        checkpoint_path = os.path.join(model_folder, checkpoint_name)
        classes_path = os.path.join(model_folder, "classes")

        if not os.path.exists(checkpoint_path):
            print("Downloading the checkpoint to", checkpoint_path)
            pydload.dload(checkpoint_url, save_to_path=checkpoint_path, max_time=None)

        if not os.path.exists(classes_path):
            print("Downloading the classes list to", classes_path)
            pydload.dload(classes_url, save_to_path=classes_path, max_time=None)

        self.detection_model = onnxruntime.InferenceSession(checkpoint_path)

        self.classes = [c.strip() for c in open(classes_path).readlines() if c.strip()]
"""