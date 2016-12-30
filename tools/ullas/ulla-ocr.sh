
# Skript för OCR av Ullas tidningskatalog

# Skriptet använder Tesseract 4 för OCR.

# Sätt TESSDATA_PREFIX till den katalog där språk- och konfigurationsfiler för
# tesseract finns. All text i katalogen är på svenska så endast svensk
# språkdata har använts i OCR. Resultat sparas i samma katalog som bildfilen.

export TESSDATA_PREFIX=/Users/pkz/projekt/tmp/tesseract/tesseract

if [ ! -f "$1.txt" ]; then
  tesseract "$1" "$1" --oem 2 --psm 4 -l swe ullas
else
  echo "Skipping $1.txt"
fi
