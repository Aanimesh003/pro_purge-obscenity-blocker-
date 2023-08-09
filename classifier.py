import numpy as np
import onnxruntime
from image_utils import load_images
from PIL import Image as pil_image


class Classifier:

    nsfw_model = None


    def classify(
        image_paths=[],
        batch_size=4,
        image_size=(300,300),
        categories=["safe"],
    ):
        model_path="C:\\Users\\ryana\\Downloads\\BEST.onnx"
        nsfw_model = onnxruntime.InferenceSession(model_path)

        if not isinstance(image_paths, list):
            image_paths = [image_paths]

        loaded_images, loaded_image_paths = load_images(
            image_paths, image_size, image_names=image_paths
        )

        if not loaded_image_paths:
            return {"Check Image Paths"}

        preds = []
        model_preds = []
        while len(loaded_images):
            _model_preds = nsfw_model.run(
                [nsfw_model.get_outputs()[0].name],
                {nsfw_model.get_inputs()[0].name: loaded_images[:batch_size]},
            )[0]
            model_preds.append(_model_preds)
            preds += np.argsort(_model_preds, axis=1).tolist()
            loaded_images = loaded_images[batch_size:]

        probs = []
        for i, single_preds in enumerate(preds):
            single_probs = []
            for j, pred in enumerate(single_preds):
                single_probs.append(
                    model_preds[int(i / batch_size)][int(i % batch_size)][pred]
                )
                preds[i][j] = categories[pred]

            probs.append(single_probs)

        images_preds = {}

        for i, loaded_image_path in enumerate(loaded_image_paths):
            if not isinstance(loaded_image_path, str):
                loaded_image_path = i

            images_preds[loaded_image_path] = {}
            for _ in range(len(preds[i])):
                images_preds[loaded_image_path][preds[i][_]] = float(probs[i][_])

        return images_preds
