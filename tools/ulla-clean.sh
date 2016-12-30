
# Skript för att preprocessa bilder före OCR av Ullas katalog
# Kör med t.ex. parallel --bar -a ulla-files.txt ./ulla-clean.sh

# Katalogen består av digitaliserade filer för fram- och baksida av alla kort.

# Skriptet använder ImageMagick för bildbehandling.

# Steg:

# Katalogens kort har röda och blå linjer. Genom stickprov har ett urval av
# färgvärden för dessa linjer valts ut. Dessa och närliggande färger har ersatts med vitt.

# Hörnen har trimmats och en ram överlades varefter despeckle och
# övrig upprensning genomfördes.

# 12% av # nedre delen av bilden beskärdes.

# Bilden sparas bredvid originalet med tillägget ".clean.jpg"

echo "Working on $1"

#if [ ! -f "$1.clean.jpg" ]; then
  echo "Converting..."
  convert "$1" \
  -gravity north -crop 100x88% +repage \
  -alpha set -compose DstOut \
  \( -size 1500x60 xc:none -draw "polygon 0,0 0,60 1500,0"  \
     -write mpr:triangle  +delete  \) \
  \( mpr:triangle             \) -gravity northwest -composite \
  \( mpr:triangle -flip       \) -gravity southwest -composite \
  \( mpr:triangle -flop       \) -gravity northeast -composite \
  \( mpr:triangle -rotate 180 \) -gravity southeast -composite \
  -background white \
  -alpha remove -alpha off \
  -fuzz 20% -fill white -opaque '#FC8486' \
  -fuzz 20% -fill white -opaque '#FEFD86' \
  -fuzz 20% -fill white -opaque '#FFECBA' \
  -fuzz 20% -fill white -opaque '#E7D5EE' \
  -fuzz 20% -fill white -opaque '#E2FAEA' \
  -fuzz 20% -fill white -opaque '#FFFEE8' \
  -fuzz 20% -fill white -opaque '#7AffFE' \
  -fuzz 20% -fill white -opaque '#726FF8' \
  -fuzz 20% -fill white -opaque '#CA111E' \
  -fuzz 20% -fill white -opaque '#FF6976' \
  -fuzz 20% -fill white -opaque '#FF8883' \
  -fuzz 20% -fill white -opaque '#4B9FE2' \
  -blur 1x65535 -contrast -normalize -despeckle -despeckle -sharpen 1 -posterize 3 \
  "$1.clean.jpg"

# -blur 1x65535 -contrast -normalize -despeckle -despeckle -sharpen 1 -posterize 3 \

#else
#  echo "Skipping $1.clean.jpg"
#fi
# För debugvisning av bildfilen på osx
#echo "tell application \"Preview\" to activate" | osascript -
