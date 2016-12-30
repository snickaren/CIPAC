
# Beräkna relativ position för det utstämplade hålet
ulx=`convert $1 -format "%[fx:50*w/100]" info:`
uly=`convert $1 -format "%[fx:88*h/100]" info:`

# hitta kortets grundfärg
color=`convert $1 -fuzz 50% -transparent black -scale 1x1 -alpha off -format "%[pixel:u.p{0,0}]" info:`

# justera svarta ytor i hörnen, fyll korthål mm.
convert $1 \
  -bordercolor black -border 10x10 \
  -fuzz 40% -fill white -draw "color $ulx,$uly floodfill" \
  -fuzz 40% -fill white -draw "color 5,5 floodfill" \
  \( -clone 0 -fill "$color" -colorize 100 \) \
  \( -clone 0 -negate -threshold 1% -negate -morphology Dilate octagon:10 -blur 0x8 \) \
  -compose over -composite \
  "$1.clean1.jpg"

# tvätta med Textcleaner (se: http://www.fmwconcepts.com/imagemagick/textcleaner/index.php)
./textcleaner -e normalize -f 20 -o 5 "$1.clean1.jpg" "$1.clean.jpg"
