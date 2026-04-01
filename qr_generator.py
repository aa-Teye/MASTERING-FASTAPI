import qrcode
import os

# Create a folder specifically for our generated QR codes
QR_DIR = "qrcodes"

def create_qr_for_gear(item_name: str) -> str:
    """
    Generates a QR code containing a link to the gear's digital record.
    Saves it as an image file and returns the file path.
    """
    if not os.path.exists(QR_DIR):
        os.makedirs(QR_DIR)
        
    safe_name = item_name.replace(" ", "_")
    file_path = f"{QR_DIR}/{safe_name}_QR.png"
    
    # The data embedded in the QR code. 
    # For now, it points to your local API. Later, you'll change this to your Next.js website URL!
    qr_data = f"http://127.0.0.1:8000/inventory/item/{item_name}"
    
    # Generate the QR Code image
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_path)
    
    return file_path