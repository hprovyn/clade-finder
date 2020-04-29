#SET PARAMS FROM CONFIG
#THIS MUST BE ABSOLUTE PATH TO CONFIG FILE
CFG_FILE=/var/lib/clade-finder/config.txt
CFG_CONTENT=$(cat $CFG_FILE | sed -r '/[^=]+=[^=]+/!d' | sed -r 's/\s+=\s/=/g')
eval "$CFG_CONTENT"

PATH=$PATH:$pythonPath

parseVCF_py="$pythonScriptsDir${pathSeparator}parseVCF.py"
cladeSNPs="$workingDir${pathSeparator}cladeSNPs"
SNPclades="$workingDir${pathSeparator}SNPclades"
positionMarkers="$workingDir${pathSeparator}hg38positionMarkers"
file=$1
python3 $parseVCF_py $1 "$positionMarkers.bgz" "$cladeSNPs.bgz" "$SNPclades.bgz"