#SET PARAMS FROM CONFIG
#THIS MUST BE ABSOLUTE PATH TO CONFIG FILE
CFG_FILE=/var/lib/clade-finder/config.txt
CFG_CONTENT=$(cat $CFG_FILE | sed -r '/[^=]+=[^=]+/!d' | sed -r 's/\s+=\s/=/g')
eval "$CFG_CONTENT"

PATH=$PATH:$pythonPath

findClade_py="$pythonScriptsDir${pathSeparator}findClade.py"

cladeSNPs="$workingDir${pathSeparator}cladeSNPs"
SNPclades="$workingDir${pathSeparator}SNPclades"

python3 "$findClade_py" "$cladeSNPs.bgz" "$SNPclades.bgz" $1