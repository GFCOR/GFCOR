import sys
import os
import cv2
import numpy as np
from PIL import Image
from rembg import remove

def prep_photo(input_path, output_path="source-prepped.png"):
    print(f"Loading image from {input_path}...")
    img = Image.open(input_path).convert("RGBA")
    
    print("Removing background with rembg...")
    no_bg = remove(img)
    
    # Composite over white background
    background = Image.new("RGBA", no_bg.size, (255, 255, 255, 255))
    composite = Image.alpha_composite(background, no_bg).convert("L")
    
    # Boost contrast with OpenCV CLAHE
    img_np = np.array(composite)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(img_np)
    
    # Save prepped image
    cv2.imwrite(output_path, enhanced)
    print(f"Saved prepped image to {output_path}")

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "source-photo.jpg"
    prep_photo(src)
