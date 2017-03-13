#!/usr/bin/env bash
today=`date +%Y-%m-%d`
script=`realpath $0`
script_path=`dirname $script`
root_dir=$1
if [ -z "$1" ]; then
    root_dir='.'
fi
output_dir="$root_dir/alyx-backups/$today/"
mkdir -p $output_dir
host='localhost'
user='cyrille'
database='alyx'
port=5432
for name in $script_path/queries/*.sql; do
    bn=$(basename $name)
    bn_noext=${bn%.*}
    psql -h $host -U $user -p $port -d $database -c "\copy ($(cat $name)) to '$output_dir/$bn_noext.tsv' with CSV DELIMITER E'\t' header encoding 'utf-8'"
done
echo "Backup done in $output_dir"

# Upload to Google Sheets.
$script_path/upload-gsheets.py $output_dir