from PIL import Image, ImageFont
from PIL.ImageDraw import ImageDraw



class ImageWrite:

    def __init__(self):
        event_date = "Practice 2023/09/23"
        img = Image.open('img/ntemplate.png')
        im = ImageDraw(img)
        offset = 262
        datePos = (1360, 140)
        ovr_col = lambda x:(195, 590+(x*offset))
        name_col = lambda x:(392, 590+(x*offset))
        def_col = lambda x:(1525, 590+(x*offset))
        off_col = lambda x:(1790, 590+(x*offset))
        table_font = ImageFont.truetype('fonts/Lato-Black.ttf', 80)
        date_font = ImageFont.truetype('fonts/Segoe_UI_Bold_Italic.ttf', 50)
        im.text(datePos,event_date,fill=(255,255,255),font=date_font)
        for i in range(0,5):
            im.text(ovr_col(i), '76', fill=(0, 0, 0),font=table_font)
            im.text(name_col(i), 'Bobby Dipshit', fill=(0,0,0), font=table_font)
            im.text(def_col(i), '73', fill=(0,0,0), font=table_font)
            im.text(off_col(i), '79', fill=(0, 0, 0), font=table_font)
        img.show()


image = ImageWrite()
