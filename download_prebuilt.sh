wget --no-check-certificate --content-disposition "https://owncloud.cesnet.cz/index.php/s/SfAiUupnoBCA8l8/download" -O ${1:-data}/data.zip
unzip ${1:-data}/data.zip -d ${1:-data}
mv ${1:-data}/data-cs/* ${1:-data}
rm ${1:-data}/data.zip
rmdir ${1:-data}/data-cs