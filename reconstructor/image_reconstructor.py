from diffusers import StableDiffusionInpaintPipeline
import torch
from PIL import Image
import os

class ImageReconstructor:
    def __init__(self):
        print("[*] Loading image reconstruction model...")
        self.pipe = StableDiffusionInpaintPipeline.from_pretrained(
            "runwayml/stable-diffusion-inpainting",
            torch_dtype=torch.float16
        )
        self.pipe.to("cuda")

    def reconstruct(self, damaged_image_path, mask_image_path, output_path):
        if not os.path.exists(damaged_image_path) or not os.path.exists(mask_image_path):
            print("[!] Damaged image or mask file not found.")
            return None

        damaged_image = Image.open(damaged_image_path).convert("RGB")
        mask_image = Image.open(mask_image_path).convert("RGB")

        result = self.pipe(
            prompt="Reconstruct missing parts realistically",
            image=damaged_image,
            mask_image=mask_image
        ).images[0]

        result.save(output_path)
        print(f"[+] Reconstructed image saved to {output_path}")
        return output_path
