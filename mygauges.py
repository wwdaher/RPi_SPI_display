# Some functions to generate gauges, dials and textboxes in Python using the PIL library
# Will Daher
# v1.0  2024.11.11
#

import digitalio
import board
from PIL import Image, ImageDraw, ImageFont, ImageColor

# a text box with a border
def mytextbox(
              image='', 
              topleft=(0,0), 
              bottomright=(10,10),
              text="default mytextbox text",
              backgroundcolor=ImageColor.getrgb("black"),
              bordercolor=ImageColor.getrgb("silver"),
              textcolor=ImageColor.getrgb("white"),
              fontloc="/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
              ):
    fontsize = (bottomright[0] - topleft[0]) // 10
    font = ImageFont.truetype(fontloc, fontsize)

    draw=ImageDraw.Draw(image)
    draw.rounded_rectangle(xy=[topleft, bottomright], 
        fill=backgroundcolor, 
        outline=bordercolor, 
        radius=4) 
    middlehorz = topleft[0] + ((bottomright[0] - topleft[0]) // 2)
    middlevert = topleft[1] + ((bottomright[1] - topleft[1]) // 2)
    draw.text(
        xy=(middlehorz, middlevert),
        align='center',
        anchor='mm',
        font_size=2,
        text=text,
        font=font,
        fill=textcolor,
    )
    

# a gauge is 180 degrees. 
def mygauge(
              image='', 
              topleft=(0,0), 
              bottomright=(10,10),
              text="",
              backgroundcolor=ImageColor.getrgb("black"),
              bordercolor=ImageColor.getrgb("silver"),
              dialcolor=ImageColor.getrgb("white"),
              textcolor=ImageColor.getrgb("black"),
              fontloc="/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
              percent=50,
              outline='',
              title='',
        ):
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(xy=[topleft, bottomright], 
        fill=backgroundcolor, 
        outline=bordercolor, 
        radius=4) 
    if title != '':
        titlesize = (bottomright[1] - topleft[1]) // 5
        arctopleft = (topleft[0], topleft[1] + titlesize)
        fontsize = (bottomright[1] - arctopleft[1]) // 10
        titlefont = ImageFont.truetype(fontloc, titlesize)
        draw.text(
                xy=((bottomright[0] - topleft[0])//2 + topleft[0], topleft[1]),
                align='center',
                anchor='ma',
                text=title,
                font=titlefont,
                fill=textcolor,
                )
    else:
        arctopleft = topleft

    pad = 3
    percentangle = 180 * (percent / 100) + 180
    arcwidth = (bottomright[1] - topleft[1]) // 3
    newtopleft = (arctopleft[0] + pad, arctopleft[1] + pad)
    newbottomright = (bottomright[0] - 1, bottomright[1] + (bottomright[1] - arctopleft[1] - pad)) 
    draw.arc(
        (newtopleft, newbottomright), 
        180, percentangle, dialcolor, arcwidth,
    )
    if outline != '':
        draw.arc(
            (newtopleft, newbottomright), 
            180, 360, outline, 1,
        )
        innerarctopleft = (newtopleft[0] + arcwidth , newtopleft[1] + arcwidth )
        innerarcbottomright = (newbottomright[0] - arcwidth , newbottomright[1] - arcwidth )
        draw.arc(
            (innerarctopleft, innerarcbottomright),
            180, 360, outline, 1,
        )
    if text != "":
        fontsize = (bottomright[0] - arctopleft[0]) // 8
        font = ImageFont.truetype(fontloc, fontsize)

        middlehorz = arctopleft[0] + ((bottomright[0] - arctopleft[0]) // 2)
        middlevert = bottomright[1] - ((bottomright[1] - arctopleft[1]) // 20)
        
        draw.text(
            xy=(middlehorz, middlevert),
            align='center',
            anchor='mb',
            text=text,
            font=font,
            fill=textcolor,
        )


# a dial is 360 degrees
def mydial(
              image='', 
              topleft=(0,0), 
              dialsize=50,
              text="",
              backgroundcolor=ImageColor.getrgb("black"),
              bordercolor=ImageColor.getrgb("silver"),
              textcolor=ImageColor.getrgb("white"),
              fontloc="/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
              percent=50,
              outline='',
              title='',
        ):
    draw = ImageDraw.Draw(image)
    bottomright=(topleft[0] + dialsize, topleft[1] + dialsize)
    draw.rounded_rectangle(xy=[topleft, bottomright], 
        fill=backgroundcolor, 
        outline=bordercolor, 
        radius=4) 
    pad = 3
    textcolor = (int(percent * 255//100), int( 255 - (percent * 255 //100)), 0)
    percentangle = 360 * (percent / 100) + 90
    arcwidth = (bottomright[1] - topleft[1]) // 5
    newtopleft = (topleft[0] + pad, topleft[1] + pad)
    newbottomright = (bottomright[0] - pad,  bottomright[1] - pad)
    draw.arc(
        (newtopleft, newbottomright), 
        90, percentangle, textcolor, arcwidth,
    )
    if outline != '':
        if title == '':
            draw.arc(
                (newtopleft, newbottomright), 90, 450, outline, 1 )
        innerarctopleft = (newtopleft[0] + arcwidth , newtopleft[1] + arcwidth )
        innerarcbottomright = (newbottomright[0] - arcwidth , newbottomright[1] - arcwidth )
        draw.arc(
            (innerarctopleft, innerarcbottomright),
            90, 450, outline, 1,
        )
        innerarctopleft = (innerarctopleft[0] + 1 , innerarctopleft[1] + 1 )
        innerarcbottomright = (innerarcbottomright[0] - 1 , innerarcbottomright[1] - 1 )
        for deg in range(90, 450, 36):
            draw.arc((innerarctopleft, innerarcbottomright), deg - 1, deg + 1, outline, 2,)

    if text != "":
        fontsize = (bottomright[0] - topleft[0]) // 6
        font = ImageFont.truetype(fontloc, fontsize)

        middlehorz = topleft[0] + ((bottomright[0] - topleft[0]) // 2)
        middlevert = topleft[1] + ((bottomright[1] - topleft[1]) // 2)
        
        draw.text(
            xy=(middlehorz, middlevert),
            align='center',
            anchor='mm',
            text=text,
            font=font,
            fill=textcolor,
        )
    if title != '':
        titlesize = (bottomright[1] - topleft[1]) // 5
        arctopleft = (topleft[0], topleft[1] + titlesize)
        fontsize = (bottomright[1] - arctopleft[1]) // 10
        titlefont = ImageFont.truetype(fontloc, titlesize)
        draw.text(
                xy=((bottomright[0] - topleft[0])//2 + topleft[0], topleft[1]),
                align='center',
                anchor='ma',
                text=title,
                font=titlefont,
                fill=textcolor,
                )
    else:
        arctopleft = topleft


