# Using Graphics Objects

There are four objects that can be used to display data:
- TextBox: a simple box to display text
- Gauge: a 180 degree (half circle) gauge
- Dial: a 360 degree (full circle) dial
- BarMulti: a horizontal bar graph 

The values for each graph are zero to 100.

- All coordinates are given in pixels.
- All colors are the standard python defined colors that are
interpreted by the ImageColor.getrgb() method. 

For sample usage please see the monitorscreeno.py application.

## TextBox

### Constructor: 
TextBox(image, topleft, bottomleft) 

### Methods:
set_text(text)
- text: the text to display

## Gauge

### Constructor:
gauge(image, topleft, bottomright)

## Dial
### Constructor:
Dial(image, topleft, dialsize)

## BarMulti
### Constructor
BarMulti(image, topleft, bottomright, barcount)

### Methods
set_title(text)
- text: a tupple with one string for each bar

set_percent(values)
- values: a tupple with one value per bar

## Common Parameters
- **topleft**: (x,y) tupple of top left corner
- **bottomright**: (x,y) tupple of bottom right corner
- **image** is the image returned from the PIL Image library


## Common Methods
*Not all methods are implemented for all objects*

**set_background_color(color)**: background color of the object

**set_border_color(color)**: border color of the object

**set_text(text)**: the text displayed over the object

**set_text_color(color)**: color text displayed over the ojbect

**set_percent(percent)**: the value of the dial, gauge or bar chart

**set_outline(color)**: color of the object outline

**set_title(title)**: title of the object

**set_title_color(color)**: color of the object title

**set_dial_color(color)**: color of the dial when displaying a value

**set_dialempty_color(color)**: background color of the dial (at 0%)

**set_gradient(boolean)**: if the color should vary depending on the value

**set_gradient_colors(startcolor, endcolor)**: color of the two endpoints - 0% and 100%. The color will be scaled between these two.

**set_font_loc(loc)**
- loc: the path to the location of the font

**set_font_size(fontsize)**
- fontsize: the default font size in pixels

**refresh()**: redraw the object



