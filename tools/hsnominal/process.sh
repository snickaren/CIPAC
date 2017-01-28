
# Demo script for image process.

# 1 Preprocess hole and corners (preprocess) -> .clean1.tif
parallel --eta -a hssample100.txt "python preprocess.py"


# 2 Normalization (knorm) -> normalized.tif
parallel --eta -a hssample100.txt ./knorm.sh


# 3 OCR -> .txt
parallel --eta -a hssample100.txt ./hsnominal-ocr.sh


# 4 Post process textfile -> clean.txt
parallel --eta -a hssample100.txt "python post_process.py"

