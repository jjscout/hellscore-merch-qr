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
        short_id = shortuuid.uuid()
        label_content = self.generate_label_content(variation)
        qr_content = self.generate_qr_content(label_content, short_id)

        qr_img = self.generate_qr_image(qr_content)
        img = self.create_empty_canvas()

        self.add_label_to_image(img, label_content)
        self.add_qr_to_image(img, qr_img)

        self.save_image_with_content(img, variation, short_id)
        self.print_generation_info(variation, short_id)

    def generate_label_content(self, variation):
        return (
            f"{variation['type']:>6}, "
            f"{variation['gender']:>6}, "
            f"{variation['size']:>4}"
        )

    def generate_qr_content(self, label_content, short_id):
        youtube_link = "https://youtube.com/HellscoreACappella"
        repo_link = "https://github.com/jjscout/hellscore-merch-qr"
        return f"{youtube_link}, {label_content}, {short_id}, {repo_link}"

    def generate_qr_image(self, qr_content):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_content)
        qr.make(fit=True)
        return qr.make_image(fill_color="black", back_color="white")

    def create_empty_canvas(self):
        return Image.new("RGB", (520, 570), color=(255, 255, 255))

    def load_font(self, font_size):
        font_path = "arial.ttf"  # Specify the path to your font file
        try:
            return ImageFont.truetype(font_path, font_size)
        except IOError:
            return ImageFont.load_default()

    def add_label_to_image(self, img, label_content):
        draw = ImageDraw.Draw(img)
        font = self.load_font(50)
        text_x, text_y = self.calculate_text_position(img, label_content)
        draw.text((text_x, text_y), label_content, font=font, fill=(0, 0, 0))

    def add_qr_to_image(self, img, qr_img):
        qr_x = self.calculate_qr_position(img, qr_img)
        text_height = self.calculate_text_height(img)
        qr_y = text_height + 10
        img.paste(qr_img, (int(qr_x), int(qr_y)))

    def save_image_with_content(self, img, variation, short_id):
        file_name = os.path.join(
            "qrs",
            f"shirt_{variation['type']}_{variation['gender']}_{variation['size']}_{short_id}.png",
        )
        img.save(file_name)

    def print_generation_info(self, variation, short_id):
        if self.verbose:
            print(
                f"Generated QR code for {variation['type']} - {variation['gender']} - Size {variation['size']} - Short ID: {short_id}"
            )

    # Inside the QRCodeGenerator class
    def calculate_text_position(self, img, label_content):
        draw = ImageDraw.Draw(img)
        font = self.load_font(50)  # Adjust font size as needed

        text_bbox = draw.textbbox((0, 0), label_content, font=font)
        text_width, text_height = (
            text_bbox[2] - text_bbox[0],
            text_bbox[3] - text_bbox[1],
        )
        text_x = (img.width - text_width) / 2
        text_y = 10  # Position the text at the top
        return text_x, text_y

    def calculate_text_height(self, img):
        draw = ImageDraw.Draw(img)
        font = self.load_font(50)  # Adjust font size as needed

        label_content = "Sample Text"  # Use a sample text to calculate height
        text_bbox = draw.textbbox((0, 0), label_content, font=font)
        return text_bbox[3] - text_bbox[1]

    def calculate_qr_position(self, img, qr_img):
        return (img.width - qr_img.width * 11.7) / 2  # Adjust the factor as needed

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
