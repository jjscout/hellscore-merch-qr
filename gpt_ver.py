import os
import shutil
import qrcode
import shortuuid
from PIL import Image, ImageDraw, ImageFont


class QRCodeGenerator:
    def __init__(self, verbose=False):
        # Initialize verbose attribute
        self.verbose = verbose

        # Define item types, genders, and sizes
        self.misc = ["Bottle", "Keychain", "Earring", "RoundCoaster", "SquareCoaster"]
        self.necklaces = ["Necklace", "Choker"]
        self.shirt_types = ["Shirt", "Tank", "Bottle", "Keychain", "Earring"]
        self.item_types = self.shirt_types + self.misc + self.necklaces
        self.genders = ["mens", "womens"]
        self.shirt_sizes = ["S", "M", "L", "XL", "XXL", "3XL"]
        self.necklace_sizes = ["S", "L"]

        # Generate item variations programmatically
        self.item_variations = []

    def generate_variations(self):
        for item_type in self.item_types:
            if item_type in self.misc:
                # Use empty string for gender and size for the new item types
                self.fill_misc_variation(item_type)
            elif item_type in self.necklaces:
                self.fill_necklace_variation(item_type)
            else:
                # Generate variations for other item types
                self.fill_shirt_variation(item_type)

    def fill_shirt_variation(self, item_type):
        for gender in self.genders:
            for size in self.shirt_sizes:
                self.item_variations.append(
                    {"type": item_type, "gender": gender, "size": size}
                )

    def fill_necklace_variation(self, item_type):
        for size in self.necklace_sizes:
            self.item_variations.append({"type": item_type, "gender": "", "size": size})

    def fill_misc_variation(self, item_type):
        self.item_variations.append({"type": item_type, "gender": "", "size": ""})

    def generate_qr_code(self, variation):
        # Generate a short unique identifier
        short_id = shortuuid.uuid()

        # Define label content with formatted type, gender, and size
        label_content = (
            f"{variation['type']:>6}, "
            f"{variation['gender']:>6}, "
            f"{variation['size']:>4}"
        )

        # Define YouTube and repository links
        youtube_link = "https://youtube.com/HellscoreACappella"
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
        img = Image.new("RGB", (520, 570), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)

        # Load the font
        try:
            font = ImageFont.truetype("arial.ttf", 50)
        except IOError:
            font = ImageFont.load_default()

        # Calculate the text size and position
        text_bbox = draw.textbbox((0, 0), label_content, font=font)
        text_width, text_height = (
            text_bbox[2] - text_bbox[0],
            text_bbox[3] - text_bbox[1],
        )
        text_x = (img.width - text_width) / 2
        text_y = 10  # Position the text at the top

        # Set the position for the QR code
        qr_x = (img.width - qr_img.width * 11.7) / 2
        qr_y = text_y + text_height + 10  # Position the QR code below the text

        # Add the label text to the image
        draw.text((text_x, text_y), label_content, font=font, fill=(0, 0, 0))

        # Paste the QR code onto the image
        img.paste(qr_img, (int(qr_x), int(qr_y)))

        # Save the image with embedded label content and QR content in the 'qrs' folder
        file_name = os.path.join(
            "qrs",
            f"shirt_{variation['type']}_{variation['gender']}_{variation['size']}_{short_id}.png",
        )
        img.save(file_name)

        if self.verbose:
            print(
                f"Generated QR code for {variation['type']} - {variation['gender']} - Size {variation['size']} - Short ID: {short_id}"
            )

    def generate_qr_codes(self):
        # Create 'qrs' folder and empty it if it exists
        if os.path.exists("qrs"):
            shutil.rmtree("qrs")
        os.makedirs("qrs")

        # Generate variations
        self.generate_variations()

        # Loop through each item variation and generate a QR code with embedded label content and QR content
        for variation in self.item_variations:
            self.generate_qr_code(variation)

        print("QR code generation completed.")


if __name__ == "__main__":
    generator = QRCodeGenerator(verbose=True)
    generator.generate_qr_codes()
