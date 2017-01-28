from wand.drawing import Drawing
from wand.image import Image
from wand.color import Color
from wand.api import library
import sys
from wand.display import display
import ctypes
import subprocess

library.MagickSetImageFuzz.argtypes = (ctypes.c_void_p, ctypes.c_double)

def clean(imagepath):
    """Batch clean scanned HS nominal catalog card image before OCR."""

    with Image(filename=imagepath) as img:

        # Hole coordinates
        delta = 30
        hole_x = int(img.width/2) - int(delta/2)
        hole_y = int(img.height*0.88)

        avgcol = None
        imgcol = img.clone()
        with Color("black") as black:

            # Find average color (for hole and corner fill)
            imgcol.transparent_color(black, alpha=0.0, fuzz=50)
            imgcol.resize(1, 1)
            avgcol = imgcol[0,0]

            command = ["convert"]
            command.append("'%s'" % imagepath)

            # Add border
            command.append("-bordercolor black -border 10x10 -trim +repage")

            # Fill border and corners with white
            command.append("-fuzz 20% -fill white -draw 'color 5,5 floodfill'")

            # Fill hole at several points to catch stripe
            for delta in [0, 10, 20, 40]:
                command.append("-fuzz 20% -fill white -draw")
                command.append(""" "color %s,%s floodfill" """ % (hole_x + delta, hole_y))


            # add card average color to previously filled areas
            command.append("""\( -clone 0 -fill "%s" -colorize 100 \)""" % avgcol)
            command.append("""\( -clone 0 -negate -threshold 1% -negate -morphology Dilate octagon:10 -blur 0x8 \)""")
            command.append("-compose over")
            command.append("-composite")

            command.append("'%s.clean1.tif'" % imagepath)
            subprocess.run(" ".join(command), shell=True, stdout=subprocess.PIPE)


if __name__ == "__main__":
    path = sys.argv[1]
    clean(path)
