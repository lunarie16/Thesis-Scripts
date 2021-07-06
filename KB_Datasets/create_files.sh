echo "Downloading TeXooPy"
git clone https://github.com/DATEXIS/TeXooPy.git

echo "creating TeXoo-KB"
python kb_creator.py

echo "extracting data from pickle-file to TeXoo-File"
echo "From now on the code won't work because of missing files - I am not allowed to share internal data of Krohne Messtechnik GmbH"
python pickle_to_texoo.py

echo "creating devset by splitting trainset"
python create_dev_from_test.py

echo "creating silver-annotations on all sets"
python create_silver_annotations.py
