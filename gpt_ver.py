import os
import shutil
import qrcode
import shortuuid
from PIL import Image, ImageDraw, ImageFont

# Define item types, genders, and sizes
item_types = ["shirt", "tank", "bottle", "keychain", "earring"]
genders = ["mens", "womens"]
sizes = ["S", "M", "L", "XL", "XXL", "XXXL"]

# Generate item variations programmatically
item_variations = []

for item_type in item_types:
    if item_type in ["bottle", "keychain", "earring"]:
        # Use empty string for gender and size for the new item types
        item_variations.append({"type": item_type, "gender": "", "size": ""})
    else:
        # Generate variations for other item types
        for gender in genders:
            for size in sizes:
                item_variations.append(
                    {"type": item_type, "gender": gender, "size": size}
                )

# Font settings
font_path = "arial.ttf"  # You may need to specify the path to a font file
font_size = 36  # Increase the font size
font_color = (0, 0, 0)


# Function to calculate text size
def get_text_size(text, font):
    temp_img = Image.new("RGB", (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)
    return temp_draw.textbbox((0, 0), text, font=font)


# Function to generate a QR code image with text, short identifier, and UUID
def generate_qr_code(variation):
    # Generate a short unique identifier
    short_id = shortuuid.uuid()

    # Define label content with formatted type, gender, and size
    label_content = (
        f"{variation['type']:>6}, "
        f"{variation['gender']:>6}, "
        f"{variation['size']:>4}"
    )

    # Define YouTube and repository links
    youtube_link = "https://www.youtube.com/@HellscoreACappella"
    repo_link = "https://github.com/jjscout/hellscore-merch-qr"

    # Generate a QR code with the specified content
    qr_content = f"{youtube_link}, {label_content}, {short_id}, {repo_link}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_content)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Create an empty canvas (white background)
    img = Image.new("RGB", (500, 550), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Load the font
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()

    # Calculate the text size and position
    text_bbox = get_text_size(label_content, font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    text_x = (img.width - text_width) / 2
    text_y = 10  # Position the text at the top

    # Set the fixed position for the QR code
    qr_x = 5
    qr_y = text_y + text_height + 10  # Position the QR code below the text

    # Add the label text to the image
    draw.text((text_x, text_y), label_content, font=font, fill=font_color)

    # Paste the QR code onto the image
    img.paste(qr_img, (int(qr_x), int(qr_y)))

    # Save the image with embedded label content and QR content in the 'qrs' folder
    file_name = os.path.join(
        "qrs",
        f"shirt_{variation['type']}_{variation['gender']}_{variation['size']}_{short_id}.png",
    )
    img.save(file_name)

    print(
        f"Generated QR code for {variation['type']} - {variation['gender']} - Size {variation['size']} - Short ID: {short_id}"
    )


# Main function
def main():
    # Create 'qrs' folder and empty it if it exists
    if os.path.exists("qrs"):
        shutil.rmtree("qrs")
    os.makedirs("qrs")

    # Loop through each item variation and generate a QR code with embedded label content and QR content
    for variation in item_variations:
        generate_qr_code(variation)

    print("QR code generation completed.")


if __name__ == "__main__":
    main()
