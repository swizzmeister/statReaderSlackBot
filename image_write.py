from PIL import Image, ImageFont
from PIL.ImageDraw import ImageDraw
import random



class ImageWrite:

    def __init__(self, key_data, heading):
        event_date = heading
        img = Image.open('img/ntemplate.png')
        im = ImageDraw(img)
        offset = 262
        datePos = (1360, 140)
        ovr_col = lambda x:(195, (590+(x*offset)))
        name_col = lambda x:(392, (590+(x*offset)))
        def_col = lambda x:(1525, (590+(x*offset)))
        off_col = lambda x:(1790, (590+(x*offset)))
        table_font = ImageFont.truetype('fonts/Lato-Black.ttf', 80)
        date_font = ImageFont.truetype('fonts/Segoe_UI_Bold_Italic.ttf', 50)
        im.text(datePos,event_date,fill=(255,255,255),font=date_font)
        j =0
        for i in key_data:
            im.text(ovr_col(j), str(i[0]), fill=(0, 0, 0),font=table_font)
            im.text(name_col(j), str(i[1]), fill=(0,0,0), font=table_font)
            im.text(def_col(j), str(i[2]), fill=(0,0,0), font=table_font)
            im.text(off_col(j), str(i[3]), fill=(0, 0, 0), font=table_font)
            j += 1
        self.tempImgPath = "img/temp_" + str(random.randint(1000000, 9999999)) + ".png"
        img.save(self.tempImgPath)


    def get_img_path(self):
        return self.tempImgPath