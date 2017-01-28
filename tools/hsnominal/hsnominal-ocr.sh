
# Skript för OCR av HS Nominalkatalog

# Katalogen består av digitaliserade filer för fram- och baksida av alla kort.

# Skriptet använder Tesseract 4 för OCR (version HEAD-6f83ba0).

# Sätt TESSDATA_PREFIX till den katalog där språkfiler mm för tesseract finns.
# Resultat sparas i samma katalog som bildfilen

# Kör med parallel --eta -a hsnominal-files.txt ./hsnominal/hsnominal-ocr.sh

export TESSDATA_PREFIX=/path/to/tesseract/tessdata/parent/folder

if [ ! -f "$1.txt" ]; then
  tesseract "$1.normalized.tif" "$1" --oem 2 --psm 6 -l swe+lat hsnominal
else
  echo "Skipping $1.txt"
fi
