import qrcode
import os
from PIL import Image
import re
import logging

# Paths
text_path = '/home/owner/Sticker Store/text'
stickers_path = '/home/owner/Sticker Store/stickers'
sinewaveart_path = '/home/owner/Sticker Store/fiwbart'
qrcodes_path = '/home/owner/Sticker Store/qrcodes'

# Ensuring the directories exist
os.makedirs(text_path, exist_ok=True)
os.makedirs(stickers_path, exist_ok=True)
os.makedirs(sinewaveart_path, exist_ok=True)
os.makedirs(qrcodes_path, exist_ok=True)

def create_qr_code(text, output_folder, file_name, color_scheme="black_on_white"):
    logging.info(f"Encoding text in QR Code: {text}")
    fill_color, back_color = color_scheme_mapping(color_scheme)
    
    # Increase the QR code version if the text is too long
    qr_version = 1 if len(text) < 100 else 2  # Adjust as necessary
    qr = qrcode.QRCode(version=qr_version, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
    
    qr.add_data(text)
    qr.make(fit=True)

    qr_image = qr.make_image(fill_color=fill_color, back_color=back_color)
    qr_file_path = os.path.join(output_folder, file_name + '_qr.png')
    
    # Check QR code image size
    logging.info(f"QR Code size: {qr_image.size}")
    qr_image.save(qr_file_path)
    return qr_file_path

def merge_with_base_image(qr_code_path, base_image_path, output_path):
    try:
        qr_image = Image.open(qr_code_path).convert("RGBA")
        base_image = Image.open(base_image_path).convert("RGBA")

        position = calculate_position(base_image, qr_image)
        
        # Blend without altering QR code pixels
        base_image.paste(qr_image, position, qr_image)
        output_image = base_image.convert("RGB")
        output_image.save(output_path)
    except Exception as e:
        logging.error(f"Error in merging images: {e}")

def color_scheme_mapping(color_scheme):
    """Maps color scheme names to actual colors."""
    # Design perspective: Customizable color schemes for QR codes
    schemes = {
        "black_on_white": ("black", "white"),
        # Add more color schemes here
    }
    return schemes.get(color_scheme, ("black", "white"))

def calculate_position(base_image, qr_image):
    """Calculates the position to place the QR code on the base image."""
    # Design perspective: Intelligent positioning of QR code on the base image
    # Example: Bottom right corner
    return (base_image.width - qr_image.width, base_image.height - qr_image.height)

def blend_images(base_image, qr_image, position):
    """Blends the base image and QR code."""
    # Engineering perspective: Efficient image blending
    blended_image = Image.new("RGBA", base_image.size)
    blended_image.paste(base_image, (0,0))
    blended_image.paste(qr_image, position, qr_image)
    return blended_image

def split_prompts(file_content):
    """Splits the file content into individual prompts."""
    # Assuming each prompt is separated by a newline character
    prompts = file_content.split('\n')
    # Filter out empty strings if there are any
    return [prompt for prompt in prompts if prompt.strip()]

# Rest of the code (e.g., split_prompts, main) remains mostly unchanged but add error handling and logging where necessary
def main():
    for i in range(1, 13):
        base_image_name = f'{i}fiwbart.png'
        base_image_path = os.path.join(sinewaveart_path, base_image_name)
        if not os.path.exists(base_image_path):
            logging.warning(f"Base image not found: {base_image_path}")
            continue

        prompts_file_name = f'{i}fiwbtext'
        prompts_file_path = os.path.join(text_path, prompts_file_name)
        if not os.path.exists(prompts_file_path):
            logging.warning(f"Text file not found: {prompts_file_path}")
            continue

        with open(prompts_file_path, 'r') as file:
            file_content = file.read()

        prompts = split_prompts(file_content)
        if not prompts:
            logging.warning(f"No prompts found in file: {prompts_file_path}")
            continue

        for j, prompt in enumerate(prompts, start=1):
            logging.info(f"Creating QR code for prompt: {prompt}")
            qr_code_path = create_qr_code(prompt, qrcodes_path, f'qr_{i}_{j}')
            output_image_name = f'sticker_{i}_{j}.png'
            output_path = os.path.join(stickers_path, output_image_name)
            merge_with_base_image(qr_code_path, base_image_path, output_path)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)  # Engineering perspective: Basic logging setup
    main()
