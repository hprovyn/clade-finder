#SET PARAMS FROM CONFIG
#THIS MUST BE ABSOLUTE PATH TO CONFIG FILE
CFG_FILE=/var/lib/clade-finder/config.txt
CFG_CONTENT=$(cat $CFG_FILE | sed -r '/[^=]+=[^=]+/!d' | sed -r 's/\s+=\s/=/g')
eval "$CFG_CONTENT"

PATH=$PATH:$pythonPath

findCladeJSON_py="$pythonScriptsDir${pathSeparator}findCladeJSON.py"

cladeSNPs="$workingDir${pathSeparator}cladeSNPs"
SNPclades="$workingDir${pathSeparator}SNPclades"
snps=$1
params=$2
python3 "$findCladeJSON_py" "$cladeSNPs.bgz" "$SNPclades.bgz" "$snps" "$params"