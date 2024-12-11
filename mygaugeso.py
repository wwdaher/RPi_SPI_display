# Some functions to generate gauges, dials and textboxes in Python using the PIL library
# Will Daher
# v1.0  2024.11.11
#

import digitalio
import board
from PIL import Image, ImageDraw, ImageFont, ImageColor

# a text box with a border
class TextBox:

    def __init__(this, image, topleft, bottomright):
        this._topleft = topleft
        this._bottomright = bottomright
        this._text="TextBox"
        this._backgroundcolor=ImageColor.getrgb("black")
#        this._backgroundcolor=(125,125,125,50)
        this._bordercolor=ImageColor.getrgb("silver")
        this._textcolor=ImageColor.getrgb("white")
        this._fontloc="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        this._fontsize = (bottomright[0] - topleft[0]) // 10
        this._font = ImageFont.truetype(this._fontloc, this._fontsize)

        this._draw=ImageDraw.Draw(image, "RGBA")
#        this._txtimg = Image.new('RGBA', image.size, (255,255,255,0))
#        this._draw=ImageDraw.Draw(this._txtimg, "RGBA")
#        this._image = image

        this._middlehorz = topleft[0] + ((bottomright[0] - topleft[0]) // 2)
        this._middlevert = topleft[1] + ((bottomright[1] - topleft[1]) // 2)
        this.__redraw()
        this._draw.text(
            xy=(this._middlehorz, this._middlevert),
            align='center',
            anchor='mm',
            font_size=this._fontsize,
            text=this._text,
            font=this._font,
            fill=this._textcolor,
        )

    def __redraw(this):
        this._draw.rounded_rectangle(xy=[this._topleft, this._bottomright], 
            fill=this._backgroundcolor, 
            outline=this._bordercolor, 
            radius=4
        ) 
    
    def set_text(this, text):
        this._text = text

    def set_background_color(this, backgroundcolor):
        this._backgroundcolor = backgroundcolor

    def set_border_color(this, bordercolor):
        this._bordercolor = bordercolor

    def set_text_color(this, textcolor):
        this._textcolor = textcolor

    def set_font_loc(this, fontloc):
        this._fontloc = fontloc
        this._font = ImageFont.truetype(this._fontloc, this._fontsize)

    def set_font_size(this, fontsize):
        this._fontsize = fontsize
        this._font = ImageFont.truetype(this._fontloc, this._fontsize)

    def refresh(this):
        this.__redraw()
        this._draw.text(
            xy=(this._middlehorz, this._middlevert),
            align='center',
            anchor='mm',
            font_size=this._fontsize,
            text=this._text,
            font=this._font,
            fill=this._textcolor,
        )
#        out = Image.alpha_composite(this._image, this._txtimg)
#        out.show()

# a gauge is 180 degrees. 
class Gauge:
    __arcpad = 3  # how much to shrink the diameter of the value arc

    def __init__(this, image, topleft, bottomright):
        this._topleft = topleft
        this._bottomright = bottomright
        this._text=""
        this._backgroundcolor=ImageColor.getrgb("black")
        this._bordercolor=ImageColor.getrgb("silver")
        this._textcolor=ImageColor.getrgb("black")
        this._dialcolor=ImageColor.getrgb("white")
        this._dialemptycolor=this._backgroundcolor
        this._percent = 50
        this._outline = ''
        this._title = ''

        this._fontloc="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        this._fontsize = (bottomright[0] - topleft[0]) // 10
        this._font = ImageFont.truetype(this._fontloc, this._fontsize)

        this._draw=ImageDraw.Draw(image)
        this._middlehorz = topleft[0] + ((bottomright[0] - topleft[0]) // 2)
        this._middlevert = topleft[1] + ((bottomright[1] - topleft[1]) // 2)
        this.refresh()


    def refresh(this):
        this._draw.rounded_rectangle(xy=[this._topleft, this._bottomright], 
        fill=this._backgroundcolor, 
        outline=this._bordercolor, 
        radius=4) 

        if this._title != '':
            this._titlesize = (this._bottomright[1] - this._topleft[1]) // 5
            this._arctopleft = (this._topleft[0], this._topleft[1] + this._titlesize)
            this._fontsize = (this._bottomright[1] - this._arctopleft[1]) // 10
            this._titlefont = ImageFont.truetype(this._fontloc, this._titlesize)
            this._draw.text(
                xy=((this._bottomright[0] - this._topleft[0])//2 + this._topleft[0], this._topleft[1]),
                align='center',
                anchor='ma',
                text=this._title,
                font=this._titlefont,
                fill=this._textcolor,
            )
        else:
            this._arctopleft = this._topleft

        this._arcwidth = (this._bottomright[1] - this._arctopleft[1]) // 3
        this._arctopleft = (this._arctopleft[0] + this.__arcpad, this._arctopleft[1] + this.__arcpad)
        this._arcbottomright = (this._bottomright[0] - 1, 
                        this._bottomright[1] + (this._bottomright[1] - this._arctopleft[1] - this.__arcpad)) 

        if this._outline != '':
            this._outerarctopleft = this._arctopleft
            this._outerarcbottomright = this._arcbottomright
            this._arctopleft = (this._arctopleft[0] + 1, this._arctopleft[1] + 1)
            this._arcbottomright = (this._arcbottomright[0] - 1, this._arcbottomright[1] - 1)
            this._draw.arc(
                (this._outerarctopleft, this._outerarcbottomright), 
                180, 360, this._outline, 1,
            )
            innerarctopleft = (this._arctopleft[0] + this._arcwidth , this._arctopleft[1] + this._arcwidth )
            innerarcbottomright = (this._arcbottomright[0] - this._arcwidth , this._arcbottomright[1] - this._arcwidth )
            this._draw.arc(
                (innerarctopleft, innerarcbottomright),
                180, 360, this._outline, 1,
            )

        # calculate text size and position 
        this._textfontsize = int((this._bottomright[0] - this._arctopleft[0]) // 8)
        this._textfont = ImageFont.truetype(this._fontloc, this._textfontsize)

        this._textmiddlehorz = this._arctopleft[0] + ((this._bottomright[0] - this._arctopleft[0]) // 2)
        this._textmiddlevert = this._bottomright[1] - ((this._bottomright[1] - this._arctopleft[1]) // 20)
    
        if this._text != "":
            this._draw.text(
                xy=(this._textmiddlehorz, this._textmiddlevert),
                align='center',
                anchor='mb',
                text=this._text,
                font=this._textfont,
                fill=this._textcolor,
            )
        # size of the box we need to erase when putting new text in
        this._oldtextbox = this._draw.textbbox(
                xy=(this._textmiddlehorz, this._textmiddlevert),
                text=this._title,
                font=this._textfont,
                anchor='mb',
                align='center',
            )
        # the text box is far too long, to cut a bit from each end
        this._oldtextbox = (this._oldtextbox[0] + (this._oldtextbox[2] - this._oldtextbox[0]) // 5,
                            this._oldtextbox[1],
                            this._oldtextbox[2] - (this._oldtextbox[2] - this._oldtextbox[0]) // 5,
                            this._oldtextbox[3])

        this.refresh_value()

    def refresh_value(this):
        percentangle = 180 * (this._percent / 100) + 180
        # first set arc to zero
        this._draw.arc(
            (this._arctopleft, this._arcbottomright), 
            180, 360, this._dialemptycolor, this._arcwidth,
        )
        # now set arc value
        this._draw.arc(
            (this._arctopleft, this._arcbottomright), 
            180, percentangle, this._dialcolor, this._arcwidth,
        )

    def refresh_text(this):
        this._draw.rectangle(xy=this._oldtextbox, fill=this._backgroundcolor) 
        this._draw.text(
            xy=(this._textmiddlehorz, this._textmiddlevert),
            anchor='mb',
            text=this._text,
            font=this._textfont,
            fill=this._textcolor,
            )
        this._oldtextbox = this._draw.textbbox(
                xy=(this._textmiddlehorz, this._textmiddlevert),
                text=this._title,
                font=this._textfont,
                anchor='mb',
                align='center',
            )
        # the text box is far too long, to cut a bit from each end
        this._oldtextbox = (this._oldtextbox[0] + (this._oldtextbox[2] - this._oldtextbox[0]) // 5,
                            this._oldtextbox[1],
                            this._oldtextbox[2] - (this._oldtextbox[2] - this._oldtextbox[0]) // 5,
                            this._oldtextbox[3])

    # what's under the gauge, usually a % value 
    def set_text(this, text):
        this._text = text
        this.refresh_text()

    def set_background_color(this, backgroundcolor):
        this._backgroundcolor = backgroundcolor
        this.refresh()

    def set_border_color(this, bordercolor):
        this._bordercolor = bordercolor
        this.refresh()

    def set_dial_color(this, dialcolor):
        this._dialcolor = dialcolor
        this.refresh()

    def set_dialempty_color(this, dialemptycolor):
        this._dialemptycolor = dialemptycolor
        this.refresh()


    def set_text_color(this, textcolor):
        this._textcolor = textcolor
        this.refresh()

    def set_font_loc(this, fontloc):
        this._fontloc = fontloc
        this._font = ImageFont.truetype(this._fontloc, this._fontsize)
        this.refresh()

    def set_outline(this, outline):
        this._outline = outline
        this.refresh()

    def set_title(this, title):
        this._title = title
        this.refresh()

    def set_percent(this, percent):
        this._percent = percent
        this.refresh_value()





# a dial is 360 degrees. 
class Dial:
    __arcpad = 3  # how much to shrink the diameter of the value arc

    def __init__(this, image, topleft, dialsize):
        this._topleft = topleft
        this._dialsize = dialsize
        this._bottomright=(topleft[0] + this._dialsize, topleft[1] + this._dialsize)
        this._text=""
        this._backgroundcolor=ImageColor.getrgb("black")
        this._dialemptycolor=this._backgroundcolor
        this._bordercolor=ImageColor.getrgb("silver")
        this._textcolor=ImageColor.getrgb("black")
        this._titlecolor=ImageColor.getrgb("black")
        this._dialcolor=ImageColor.getrgb("white")
        this._colorgradient = False
        this._colorgradientstart = ImageColor.getrgb('green')
        this._colorgradientend = ImageColor.getrgb('red')
        this._percent = 50
        this._outline = ''
        this._title = ''

        this._fontloc="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        this._fontsize = (this._bottomright[0] - topleft[0]) // 10
        this._font = ImageFont.truetype(this._fontloc, this._fontsize)

        this._draw=ImageDraw.Draw(image)
        this._middlehorz = topleft[0] + ((this._bottomright[0] - topleft[0]) // 2)
        this._middlevert = topleft[1] + ((this._bottomright[1] - topleft[1]) // 2)
        this.refresh()


    def refresh(this):
        this._draw.rounded_rectangle(xy=[this._topleft, this._bottomright], 
        fill=this._backgroundcolor, 
        outline=this._bordercolor, 
        radius=4) 

        if this._title != '':
            this._titlesize = (this._bottomright[1] - this._topleft[1]) // 5
            this._titlefont = ImageFont.truetype(this._fontloc, this._titlesize)
            this._draw.text(
                xy=((this._bottomright[0] - this._topleft[0])//2 + this._topleft[0], this._topleft[1]),
                align='center',
                anchor='ma',
                text=this._title,
                font=this._titlefont,
                fill=this._textcolor,
            )
        this._arctopleft = this._topleft

        this._arcwidth = (this._bottomright[1] - this._arctopleft[1]) // 5
        this._arctopleft = (this._arctopleft[0] + this.__arcpad, this._arctopleft[1] + this.__arcpad)
        this._arcbottomright = (this._bottomright[0] - this.__arcpad, 
                        this._bottomright[1] - this.__arcpad) 

        if this._outline != '':
            this._outerarctopleft = this._arctopleft
            this._outerarcbottomright = this._arcbottomright
            this._arctopleft = (this._arctopleft[0] + 1, this._arctopleft[1] + 1)
            this._arcbottomright = (this._arcbottomright[0] - 1, this._arcbottomright[1] - 1)
            this._draw.arc(
                (this._outerarctopleft, this._outerarcbottomright), 
                90, 450, this._outline, 1,
            )
            innerarctopleft = (this._arctopleft[0] + this._arcwidth , this._arctopleft[1] + this._arcwidth )
            innerarcbottomright = (this._arcbottomright[0] - this._arcwidth , this._arcbottomright[1] - this._arcwidth )
            this._draw.arc(
                (innerarctopleft, innerarcbottomright),
                90, 450, this._outline, 1,
            )
            for deg in range(180, 540, 36):
                this._draw.arc((innerarctopleft, innerarcbottomright), deg - 1, deg + 1, this._outline, 3,)

        # calculate text size and position 
        this._textfontsize = int((this._bottomright[0] - this._arctopleft[0]) // 6)
        this._textfont = ImageFont.truetype(this._fontloc, this._textfontsize)

        this._textmiddlehorz = this._arctopleft[0] + ((this._arcbottomright[0] - this._arctopleft[0]) // 2)
        this._textmiddlevert = this._arctopleft[1] + ((this._arcbottomright[1] - this._arctopleft[1]) // 2)
    
        if this._text != "":
            this._draw.text(
                xy=(this._textmiddlehorz, this._textmiddlevert),
                align='center',
                anchor='mm',
                text=this._text,
                font=this._textfont,
                fill=this._textcolor,
            )
        # size of the box we need to erase when putting new text in
        this._oldtextbox = this._draw.textbbox(
                xy=(this._textmiddlehorz, this._textmiddlevert),
                text=this._text,
                font=this._textfont,
                anchor='mm',
                align='center',
            )
        # the text box is far too long, to cut a bit from each end
#        this._oldtextbox = (this._oldtextbox[0] + (this._oldtextbox[2] - this._oldtextbox[0]) // 5,
#                            this._oldtextbox[1],
#                            this._oldtextbox[2] - (this._oldtextbox[2] - this._oldtextbox[0]) // 5,
#                            this._oldtextbox[3])

        this.refresh_value()

    def refresh_value(this):
        percentangle = 360 * (this._percent / 100) + 180
        # first set arc to zero
        this._draw.arc(
            (this._arctopleft, this._arcbottomright), 
            180, 540, this._dialemptycolor, this._arcwidth,
        )
        if this._colorgradient:
            dialgradientcolor = this._calcgradient()
        else:
            dialgradientcolor = this._dialcolor

        # now set arc value
        this._draw.arc(
            (this._arctopleft, this._arcbottomright), 
            180, percentangle, dialgradientcolor, this._arcwidth,
        )
        if this._title != '':
            this._draw.text(
                xy=((this._bottomright[0] - this._topleft[0])//2 + this._topleft[0], this._topleft[1]),
                align='center',
                anchor='ma',
                font=this._titlefont,
                text=this._title,
                fill=this._titlecolor,
            )

    def refresh_text(this):
        this._draw.rectangle(xy=this._oldtextbox, fill=this._backgroundcolor) 
        this._draw.text(
            xy=(this._textmiddlehorz, this._textmiddlevert),
            anchor='mm',
            text=this._text,
            font=this._textfont,
            fill=this._textcolor,
            )
        this._oldtextbox = this._draw.textbbox(
                xy=(this._textmiddlehorz, this._textmiddlevert),
                text=this._text,
                font=this._textfont,
                anchor='mm',
                align='center',
            )
        # the text box is far too long, to cut a bit from each end
#        this._oldtextbox = (this._oldtextbox[0] + (this._oldtextbox[2] - this._oldtextbox[0]) // 5,
#                            this._oldtextbox[1],
#                            this._oldtextbox[2] - (this._oldtextbox[2] - this._oldtextbox[0]) // 5,
#                            this._oldtextbox[3])
    # what's under the gauge, usually a % value 
    def _calcgradient(this):
        red = int((this._percent / 100) * (this._colorgradientend[0] - this._colorgradientstart[0]) + 
            this._colorgradientstart[0])
        green = int((this._percent / 100) * (this._colorgradientend[1] - this._colorgradientstart[1]) + 
            this._colorgradientstart[1])
        blue = int((this._percent / 100) * (this._colorgradientend[2] - this._colorgradientstart[2]) + 
            this._colorgradientstart[2])
        return (red, green, blue)

    def set_text(this, text):
        this._text = text
        this.refresh_text()

    def set_background_color(this, backgroundcolor):
        this._backgroundcolor = backgroundcolor
        this.refresh()

    def set_border_color(this, bordercolor):
        this._bordercolor = bordercolor
        this.refresh()

    def set_dial_color(this, dialcolor):
        this._dialcolor = dialcolor
        this.refresh()

    def set_dialempty_color(this, dialemptycolor):
        this._dialemptycolor = dialemptycolor
        this.refresh()


    def set_text_color(this, textcolor):
        this._textcolor = textcolor
        this.refresh()

    def set_title_color(this, titlecolor):
        this._titlecolor = titlecolor
        this.refresh()

    def set_font_loc(this, fontloc):
        this._fontloc = fontloc
        this._font = ImageFont.truetype(this._fontloc, this._fontsize)
        this.refresh()

    def set_outline(this, outline):
        this._outline = outline
        this.refresh()

    def set_title(this, title):
        this._title = title
        this.refresh()

    def set_percent(this, percent):
        this._percent = percent
        this.refresh_value()

    def set_gradient(this, colorgradient):
        this._colorgradient = colorgradient
        this.refresh_value()

    def set_gradient_colors(this, startcolor, endcolor):
        this._colorgradientstart = startcolor
        this._colorgradientend = endcolor
        this.refresh_value()


class Bar:
    __barpad = 3  # pad around the bar graph
    __minimumtitlesize = 5

    def _drawaxis(this):
            for o in range(2, 10, 2):
                offset = int((o / 10) * (this._graphbottomright[0] - this._graphtopleft[0]))
                toppoint = ((this._graphtopleft[0] + offset), this._graphtopleft[1])
                bottompoint = ((this._graphtopleft[0] + offset), this._graphbottomright[1])
                this._draw.line(xy=(toppoint, bottompoint), fill=this._graphoutlinecolor, width=1)


    def __init__(this, image, topleft, bottomright):
        this._topleft = topleft
        this._bottomright = bottomright
        this._text=""
        this._backgroundcolor=ImageColor.getrgb("black")
        this._foregroundcolor=ImageColor.getrgb("white")
        this._bordercolor=ImageColor.getrgb("silver")
        this._textcolor=ImageColor.getrgb("black")
        this._titlecolor=ImageColor.getrgb("black")
        this._colorgradient = False
        this._colorgradientstart = ImageColor.getrgb('green')
        this._colorgradientend = ImageColor.getrgb('red')
        this._percent = 50
        this._outline = ''
        this._title = ''
        this._graphoutlinecolor = ImageColor.getrgb('lightblue')

        this._fontloc="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        this._fontsize = (this._bottomright[0] - topleft[0]) // 10
        this._font = ImageFont.truetype(this._fontloc, this._fontsize)

        this._draw=ImageDraw.Draw(image)
        this._middlehorz = topleft[0] + ((this._bottomright[0] - topleft[0]) // 2)
        this._middlevert = topleft[1] + ((this._bottomright[1] - topleft[1]) // 2)
        this.refresh()


    def refresh(this):
        this._draw.rounded_rectangle(xy=[this._topleft, this._bottomright], 
        fill=this._backgroundcolor, 
        outline=this._bordercolor, 
        radius=4) 

        this._graphtopleft = (this._topleft[0] + this.__barpad, 
                              this._topleft[1] + this.__barpad)
        this._graphbottomright = (this._bottomright[0] - this.__barpad, 
                              this._bottomright[1] - this.__barpad) 

        if this._title != '':
            this._titlesize = (this._bottomright[0] - this._topleft[0]) // 15
            this._titlesize = max(this._titlesize, this.__minimumtitlesize)
            this._titlefont = ImageFont.truetype(this._fontloc, this._titlesize)
            this._graphtopleft = (this._graphtopleft[0], this._graphtopleft[1] + this._titlesize)
            this._draw.text(
                xy=((this._bottomright[0] - this._topleft[0])//2 + this._topleft[0], this._topleft[1]),
                align='center',
                anchor='ma',
                text=this._title,
                font=this._titlefont,
                fill=this._textcolor,
            )


        # calculate text size and position 
        this._textfontsize = int((this._graphbottomright[1] - this._graphtopleft[1]) / 2)
        this._textfont = ImageFont.truetype(this._fontloc, this._textfontsize)

        this._textmiddlehorz = this._graphtopleft[0] + ((this._graphbottomright[0] - this._graphtopleft[0]) // 2)
        this._textmiddlevert = this._graphtopleft[1] + ((this._graphbottomright[1] - this._graphtopleft[1]) // 2)
    
        if this._text != "":
            this._draw.text(
                xy=(this._textmiddlehorz, this._textmiddlevert),
                align='center',
                anchor='mm',
                text=this._text,
                font=this._textfont,
                fill=this._textcolor,
            )

        this.refresh_value()

    def refresh_value(this):
        percentwidth =  int((this._percent / 100) * (this._graphbottomright[0] - this._graphtopleft[0]))
        # first set bar to zero
        this._draw.rectangle(
            xy=(this._graphtopleft, this._graphbottomright), 
            fill=this._backgroundcolor, outline=this._graphoutlinecolor, width=1
        )
        if this._colorgradient:
            dialgradientcolor = this._calcgradient()
        else:
            dialgradientcolor = this._foregroundcolor

        # now set arc value
        graphbarbottomright = (this._graphtopleft[0] + percentwidth, this._graphbottomright[1])
        this._draw.rectangle(
            xy=(this._graphtopleft, graphbarbottomright), 
            fill=dialgradientcolor, 
        )

        if this._outline != '':
            this._drawaxis()


    def refresh_text(this):
        this.refresh_value()
        this._draw.text(
            xy=(this._textmiddlehorz, this._textmiddlevert),
            anchor='mm',
            text=this._text,
            font=this._textfont,
            fill=this._textcolor,
            )

    # what's under the gauge, usually a % value 
    def _calcgradient(this):
        red = int((this._percent / 100) * (this._colorgradientend[0] - this._colorgradientstart[0]) + 
            this._colorgradientstart[0])
        green = int((this._percent / 100) * (this._colorgradientend[1] - this._colorgradientstart[1]) + 
            this._colorgradientstart[1])
        blue = int((this._percent / 100) * (this._colorgradientend[2] - this._colorgradientstart[2]) + 
            this._colorgradientstart[2])
        return (red, green, blue)

    def set_text(this, text):
        this._text = text
        this.refresh_text()

    def set_background_color(this, backgroundcolor):
        this._backgroundcolor = backgroundcolor
        this.refresh()

    def set_border_color(this, bordercolor):
        this._bordercolor = bordercolor
        this.refresh()

    def set_foreground_color(this, foregroundcolor):
        this._foregroundcolor = foregroundcolor
        this.refresh()

    def set_text_color(this, textcolor):
        this._textcolor = textcolor
        this.refresh()

    def set_title_color(this, titlecolor):
        this._titlecolor = titlecolor
        this.refresh()

    def set_font_loc(this, fontloc):
        this._fontloc = fontloc
        this._font = ImageFont.truetype(this._fontloc, this._fontsize)
        this.refresh()

    def set_outline(this, outline):
        this._outline = outline
        this.refresh()

    def set_title(this, title):
        this._title = title
        this.refresh()

    def set_percent(this, percent):
        this._percent = percent
        this.refresh_value()

    def set_gradient(this, colorgradient):
        this._colorgradient = colorgradient
        this.refresh_value()

    def set_gradient_colors(this, startcolor, endcolor):
        this._colorgradientstart = startcolor
        this._colorgradientend = endcolor
        this.refresh_value()


class BarMulti:
    __barpad = 3  # pad around the bar graph
    __minimumtitlesize = 5
    __graphborderwidth = 1 # border of multibar graph area

    def _drawaxis(this):
            for o in range(2, 10, 2):
                offset = int((o / 10) * (this._graphbottomright[0] - this._graphtopleft[0]))
                toppoint = ((this._graphtopleft[0] + offset), this._graphtopleft[1])
                bottompoint = ((this._graphtopleft[0] + offset), this._graphbottomright[1])
                this._draw.line(xy=(toppoint, bottompoint), fill=this._outline, 
                                width=this.__graphborderwidth)


    def __init__(this, image=0, topleft=(100,100), bottomright=(200,200), barcount=2):
        this._topleft = topleft
        this._bottomright = bottomright
        this._barcount = barcount
        this._backgroundcolor=ImageColor.getrgb("black")
        this._barcolor=ImageColor.getrgb("white")
        this._baremptycolor=ImageColor.getrgb("darkslategrey")
        this._bordercolor=ImageColor.getrgb("silver")
        this._textcolor=ImageColor.getrgb("black")
        this._titlecolor=ImageColor.getrgb("black")
        this._colorgradient = False
        this._colorgradientstart = ImageColor.getrgb('green')
        this._colorgradientend = ImageColor.getrgb('red')
        this._percent = ()
        this._text = ()
        for i in range(0, barcount): 
            this._percent = this._percent + (i*10, ) # build tuple
            this._text = this._text + ('', ) # build tuple
        this._outline = ''
        this._title = ''
        this._graphoutlinecolor = ImageColor.getrgb('lightblue')

        this._fontloc="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        this._fontsize = (this._bottomright[0] - topleft[0]) // 10
        this._font = ImageFont.truetype(this._fontloc, this._fontsize)

        this._draw=ImageDraw.Draw(image)
        this._middlehorz = topleft[0] + ((this._bottomright[0] - topleft[0]) // 2)
        this._middlevert = topleft[1] + ((this._bottomright[1] - topleft[1]) // 2)
        this.refresh()


    def refresh(this):
        this._draw.rounded_rectangle(xy=[this._topleft, this._bottomright], 
        fill=this._backgroundcolor, 
        outline=this._bordercolor, 
        radius=4) 

        this._graphtopleft = (this._topleft[0] + this.__barpad, 
                              this._topleft[1] + this.__barpad)
        this._graphbottomright = (this._bottomright[0] - this.__barpad, 
                              this._bottomright[1] - this.__barpad) 

        if this._title != '':
            this._titlesize = (this._bottomright[1] - this._topleft[1]) // 4
            if this._titlesize > 12: this._titlesize = 12
            this._titlesize = max(this._titlesize, this.__minimumtitlesize)
            this._titlefont = ImageFont.truetype(this._fontloc, this._titlesize)
            this._graphtopleft = (this._graphtopleft[0], this._graphtopleft[1] + this._titlesize)
            this._draw.text(
                xy=((this._bottomright[0] - this._topleft[0])//2 + this._topleft[0], this._topleft[1]),
                align='center',
                anchor='ma',
                text=this._title,
                font=this._titlefont,
                fill=this._titlecolor,
            )


        #calculate location of each bar
        this._bartopleft = [[0] * 2 ] * this._barcount
        this._barbottomright = [[0] * 2 ] * this._barcount
        this._textmiddlehorz = [[0] * 2 ] * this._barcount
        this._textmiddlevert = [[0] * 2 ] * this._barcount
        singlebarvert = int((this._graphbottomright[1] - this._graphtopleft[1] - (2 * this.__graphborderwidth)) / this._barcount)
        basevert = 0;
        for i in range(0, this._barcount):
            this._bartopleft[i] = (this._graphtopleft[0] + this.__graphborderwidth, 
                                   this._graphtopleft[1] + basevert + this.__graphborderwidth)
            basevert += singlebarvert
            this._barbottomright[i] = (this._graphbottomright[0] + this.__graphborderwidth, 
                                       this._graphtopleft[1]  + this.__graphborderwidth + basevert)
            this._textmiddlehorz[i] = this._bartopleft[i][0] + ((this._barbottomright[i][0] - this._bartopleft[i][0]) // 2)
            this._textmiddlevert[i] = this._bartopleft[i][1] + ((this._barbottomright[i][1] - this._bartopleft[i][1]) // 2)


        # calculate text size and position 
        this._textfontsize = int((this._barbottomright[0][1] - this._bartopleft[0][1]) / 2)
        this._textfont = ImageFont.truetype(this._fontloc, this._textfontsize)

    
        this.refresh_value()

    def refresh_value(this):
        # first set all bars to zero
        this._draw.rectangle(
            xy=(this._graphtopleft, this._graphbottomright), 
            fill=this._baremptycolor, outline=this._graphoutlinecolor, width=this.__graphborderwidth, 
        )

        for i in range(0, this._barcount):
            percentwidth =  int((this._percent[i] / 100) * (this._graphbottomright[0] - this._graphtopleft[0]))
            if this._colorgradient:
                bargradientcolor = this._calcgradient(this._percent[i])
            else:
                bargradientcolor = this._barcolor

            # now change bar value
            graphbarbottomright = (this._bartopleft[i][0] + percentwidth, this._barbottomright[i][1])
            this._draw.rectangle(
                xy=(this._bartopleft[i], graphbarbottomright), 
                fill=bargradientcolor, 
            )

            if this._outline != '':
                this._drawaxis()

            if this._text != '':
                this._draw.text(
                    xy=(this._textmiddlehorz[i], this._textmiddlevert[i]),
                    anchor='mm',
                    text=this._text[i],
                    font=this._textfont,
                    fill=this._textcolor,
                    )



    def refresh_text(this):
        this.refresh_value()

    # what's under the gauge, usually a % value 
    def _calcgradient(this, percent):
        red = int((percent / 100) * (this._colorgradientend[0] - this._colorgradientstart[0]) + 
            this._colorgradientstart[0])
        green = int((percent / 100) * (this._colorgradientend[1] - this._colorgradientstart[1]) + 
            this._colorgradientstart[1])
        blue = int((percent / 100) * (this._colorgradientend[2] - this._colorgradientstart[2]) + 
            this._colorgradientstart[2])
        return (red, green, blue)

    def set_text(this, text):
        if len(text) == this._barcount:
            this._text = text
            this.refresh_text()

    def set_background_color(this, backgroundcolor):
        this._backgroundcolor = backgroundcolor
        this.refresh()

    def set_border_color(this, bordercolor):
        this._bordercolor = bordercolor
        this.refresh()

    def set_bar_color(this, barcolor):
        this._barcolor = barcolor
        this.refresh()

    def set_barempty_color(this, baremptycolor):
        this._baremptycolor = baremptycolor
        this.refresh()

    def set_text_color(this, textcolor):
        this._textcolor = textcolor
        this.refresh()

    def set_title_color(this, titlecolor):
        this._titlecolor = titlecolor
        this.refresh()

    def set_font_loc(this, fontloc):
        this._fontloc = fontloc
        this._font = ImageFont.truetype(this._fontloc, this._fontsize)
        this.refresh()

    def set_graph_outline_color(this, outline):
        this._graphoutlinecolor = outline
        this.refresh()

    def set_outline(this, outline):
        this._outline = outline
        this.refresh()

    def set_title(this, title):
        this._title = title
        this.refresh()

    def set_percent(this, percent):
        if len(percent) == this._barcount:
            this._percent = percent
            this.refresh_value()

    def set_gradient(this, colorgradient):
        this._colorgradient = colorgradient
        this.refresh_value()

    def set_gradient_colors(this, startcolor, endcolor):
        this._colorgradientstart = startcolor
        this._colorgradientend = endcolor
        this.refresh_value()

    
