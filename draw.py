from PIL import Image, ImageDraw, ImageFont, ImageFilter

import random
import io

class Recaptcha():

    def __init__(self, fontColor = (0, 0, 0),
                     width = 60 * 40,
                     height = 60,
                     fontPath = 'app/static/arial.ttf',
                     bgColor = (255, 255, 255),
                     fontSize = 36):
        self.width = width
        self.height = height
        self.fontPath = fontPath
        self.bgColor = bgColor
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = ImageFont.truetype(self.fontPath, self.fontSize)
        self.image = Image.new('RGB', (self.width,self.height), self.bgColor)
        self.draw = ImageDraw.Draw(self.image)

    def rndChar(self):
        return chr(random.randint(65, 90))

    def rndColor(self):
        return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

    def rndColor2(self):
        return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

    def generate(self):
        for x in range(self.width):
            for y in range(self.height):
                self.draw.point((x, y), fill= self.rndColor())
        code = ''
        for t in range(4):
            s = self.rndChar()
            self.draw.text((60 * t + 10, 10), s, font=self.font, fill=self.rndColor2())
            code = code + s
        self.image = self.image.filter(ImageFilter.BLUR)
        return code,self.image


ic = Recaptcha(fontColor=(100,211, 90))
strs,code_img = ic.generate()
buf = io.BytesIO()
code_img.save(buf,'JPEG',quality=70)
buf_str = buf.getvalue()
print(buf_str)