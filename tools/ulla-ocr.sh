
# Skript för OCR av Ullas tidningskatalog

# Skriptet använder Tesseract 4 för OCR.

# Sätt TESSDATA_PREFIX till den katalog där språkfiler för tesseract finns.
# Allt text i katalogen är på svenska så endast svensk språkdata har använts i
# OCR. Resultat sparas i samma katalog som bildfilen.

if [ ! -f "$1.txt" ]; then
  export TESSDATA_PREFIX=/Users/pkz/projekt/tmp/tesseract/tesseract
  tesseract "$1.clean.jpg" "$1" --oem 2 --psm 4 -l swe
else
  echo "Skipping $1.txt"
fi
