from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os

class TextReconstructor:
    def __init__(self):
        print("[*] Loading text reconstruction model...")
        self.tokenizer = AutoTokenizer.from_pretrained("gpt2")
        self.model = AutoModelForCausalLM.from_pretrained("gpt2")

    def reconstruct(self, damaged_text_path, output_path):
        if not os.path.exists(damaged_text_path):
            print("[!] Damaged text file not found.")
            return None

        with open(damaged_text_path, "r", encoding="utf-8") as f:
            damaged_text = f.read()

        input_ids = self.tokenizer.encode(damaged_text, return_tensors="pt")
        output_ids = self.model.generate(input_ids, max_length=1024)
        reconstructed_text = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(reconstructed_text)

        print(f"[+] Reconstructed text saved to {output_path}")
        return output_path
