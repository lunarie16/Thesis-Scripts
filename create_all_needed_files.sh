echo "downloading and extracting data for kb"
cd Krohne_WP
sh extract_information_from_krohne_site.sh

cd ..
echo "creating datasets and kb in texoo-format and creating silver-annotations"
cd KB_Datasets
sh create_files.sh
