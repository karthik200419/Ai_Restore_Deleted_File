import os
import logging
from diffusers import StableDiffusionInpaintPipeline
import torch
from PIL import Image


logging.basicConfig(level=logging.INFO)


class ImageReconstructor:
    def __init__(self):
        """
        Loads the Stable Diffusion inpainting pipeline for image reconstruction.
        """
        try:
            self.pipe = StableDiffusionInpaintPipeline.from_pretrained(
                "runwayml/stable-diffusion-inpainting",
                torch_dtype=torch.float16
            )
            self.pipe = self.pipe.to("cuda") if torch.cuda.is_available() else self.pipe.to("cpu")
            logging.info("Stable Diffusion Inpaint Pipeline loaded successfully.")
        except Exception as e:
            logging.error(f"Failed to load inpainting model: {e}")
            raise

    def reconstruct(self, damaged_image_path, mask_image_path, output_path):
        """
        Reconstructs a damaged image.
        damaged_image_path: path to damaged image
        mask_image_path: mask image showing damaged areas
        output_path: where to save reconstructed image
        """
        try:
            damaged_image = Image.open(damaged_image_path).convert("RGB")
            mask_image = Image.open(mask_image_path).convert("RGB")

            logging.info(f"Reconstructing image: {damaged_image_path}")

            result = self.pipe(
                prompt="Reconstruct the damaged area",
                image=damaged_image,
                mask_image=mask_image
            ).images[0]

            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            result.save(output_path)

            logging.info(f"Image reconstruction complete: {output_path}")
            return output_path

        except Exception as e:
            logging.error(f"Failed to reconstruct image: {e}")
            return None
