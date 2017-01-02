
# Skript för OCR av HS Nominalkatalog

# Katalogen består av digitaliserade filer för fram- och baksida av alla kort.

# Skriptet använder Tesseract 4 för OCR.

# Sätt TESSDATA_PREFIX till den katalog där språkfiler mm för tesseract finns.
# Resultat sparas i samma katalog som bildfilen

export TESSDATA_PREFIX=/path/to/tesseract/tessdata/parent/folder

if [ ! -f "$1.txt" ]; then
  tesseract "$1.clean.jpg" "$1" --oem 2 --psm 4 -l swe+lat hsnominal
else
  echo "Skipping $1.txt"
fi
