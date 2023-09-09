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
        self.shirt_types = ["Shirt", "Tank", "Bottle"]
        self.item_types = self.shirt_types + self.misc + self.necklaces
        self.genders = ["mens", "womens"]
        self.shirt_sizes = ["S", "M", "L", "XL", "XXL", "3XL"]
        self.shirt_design = ["O", "N"]
        self.necklace_sizes = ["S", "L"]

        # Generate item variations programmatically
        self.item_variations = []

    def generate_variations(self):
        if len(self.item_variations) > 0:
            return
        for item_type in self.item_types:
            self.create_variation(item_type)

    def create_variation(self, item_type):
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
            for design in self.shirt_design:
                for size in self.shirt_sizes:
                    self.item_variations.append(
                        self.fill_variation(
                            item_type=item_type, design=design, gender=gender, size=size
                        )
                    )

    def fill_necklace_variation(self, item_type):
        for size in self.necklace_sizes:
            self.item_variations.append(
                self.fill_variation(
                    item_type=item_type, design="", gender="", size=size
                )
            )

    def fill_misc_variation(self, item_type):
        self.item_variations.append(self.fill_variation(item_type, "", "", ""))

    def fill_variation(self, item_type, design, gender, size):
        return {"type": item_type, "design": design, "gender": gender, "size": size}

    def generate_qr_code(self, variation, short_id):
        label_content = self.generate_label_content(variation)
        qr_content = self.generate_qr_content(label_content, short_id)

        qr_img = self.generate_qr_image(qr_content)
        img = self.create_empty_canvas()

        self.add_label_to_image(img, label_content)
        self.add_qr_to_image(img, qr_img)

        self.print_generation_info(variation, short_id)
        return img

    def generate_label_content(self, variation):
        return (
            f"{variation['type']:>6}, "
            f"{variation['design']}, "
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
        qr_y = text_height + 20
        img.paste(qr_img, (int(qr_x), int(qr_y)))

    def save_image_with_content(self, img, variation, short_id=None, grid=False):
        grid_str = "_grid" if grid else ""
        id_str = short_id if short_id is not None else ""
        file_name = os.path.join(
            "qrs",
            f"{variation['type']}_"
            f"{variation['design']}_"
            f"{variation['gender']}_"
            f"{variation['size']}_"
            f"{id_str}"
            f"{grid_str}"
            ".png",
        )
        img.save(file_name)

    def print_generation_info(self, variation, short_id):
        if self.verbose:
            print(
                f"Generated QR code for {variation['type']} - "
                f"{variation['design']} - "
                f"{variation['gender']} - "
                f"Size {variation['size']} - "
                f"Short ID: {short_id}"
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
            short_id = shortuuid.uuid()
            img = self.generate_qr_code(variation, short_id)
            self.save_image_with_content(img, variation, short_id)

        print("QR code generation completed.")

    def generate_qr_code_grid(self, requested_variation, rows=2, columns=3):
        # Create an empty canvas for the grid
        grid_width = 520 * columns
        grid_height = 570 * rows
        grid_img = Image.new("RGB", (grid_width, grid_height), color=(255, 255, 255))

        # Calculate the spacing between QR codes
        spacing_x = 520
        spacing_y = 570

        # Generate the QR code for the requested variation
        # Generate QR codes for each grid cell
        for row in range(rows):
            for col in range(columns):
                # Calculate the position for this QR code in the grid
                x = col * spacing_x
                y = row * spacing_y
                short_id = shortuuid.uuid()
                img = self.generate_qr_code(requested_variation, short_id)
                # Paste the QR code into the grid
                grid_img.paste(img, (x, y))
        self.print_generation_info(requested_variation, short_id)
        return grid_img

    def generate_qr_code_grid_from_parameters(
        self, item_type, gender, size, rows=2, columns=3
    ):
        variation = self.create_variation(item_type, gender, size)
        return self.generate_qr_code_grid(variation, rows=rows, columns=columns)

    def generate_qr_grids(self):
        # Create 'qrs' folder and empty it if it exists
        if os.path.exists("qrs"):
            shutil.rmtree("qrs")
        os.makedirs("qrs")

        # Generate variations
        self.generate_variations()

        # Loop through each item variation and generate a QR code with embedded label content and QR content
        for variation in self.item_variations:
            img = self.generate_qr_code_grid(variation)
            self.save_image_with_content(img, variation, grid=True)

        print("QR code generation completed.")


if __name__ == "__main__":
    generator = QRCodeGenerator(verbose=True)
    generator.generate_qr_grids()
