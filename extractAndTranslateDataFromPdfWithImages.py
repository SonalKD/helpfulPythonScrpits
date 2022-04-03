from pikepdf import Pdf, PdfImage
import pytesseract
from PIL import Image
from googletrans import Translator

filename = '/path/to/your.pdf'
translator = Translator()
example = Pdf.open(filename)

for i, page in enumerate(example.pages):
    for j, (name, raw_image) in enumerate(page.images.items()):
        image = PdfImage(raw_image)
        out = image.extract_to(fileprefix=f"{filename}-page{i:03}-img{j:03}")
        textdata = pytesseract.image_to_string(Image.open(out))

        finalResult = translator.translate(textdata.strip())
        print("-"*100)
        print(finalResult.text)
        
        
