import json
import qrcode

def shirt_handler(item_type, items):
    pass

def necklace_handler(item_type, items):
    pass

if __name__ == "__main__":
    # Data you want to encode in the QR code
    data = "Womens New T Medium"
    file_path = "items.json"
    items = {}
    with open(file_path, 'r') as json_file:
        items = json.load(json_file)

    print(items)

    for item_type in items["types"]:
        if item_type in ["T-Shirt", "Tank"]:
            shirt_handler(item_type, items)
        elif item_type in ["Necklace", "Choker"]:
            necklace_handler(item_type, items)

    exit()
    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,  # QR code version (adjust as needed)
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,  # Size of each QR code box
        border=4,     # Border size around the QR code
    )

    # Add the data to the QR code
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR code instance
    img = qr.make_image(fill_color="red", back_color="black")

    # Save the QR code as an image file (e.g., PNG)
    img.save("example_qr_code.png")

    # Display the QR code (requires the PIL library)
    img.show()
