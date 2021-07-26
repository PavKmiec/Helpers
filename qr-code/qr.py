import qrcode

# website link
input_data = "https://deepmind.com/research/publications/Unsupervised-Object-based-Transition-Models-For-Embodied-Agents-in-3D-Partially-Observable-Environments"

# create instance of QR code
qr = qrcode.QRCode(version=3, box_size=10, border=5)

qr.add_data(input_data)
qr.make(fit=True)
img = qr.make_image(fill='black', back_color='white')
img.save('qrcode.png')