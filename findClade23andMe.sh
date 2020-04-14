#SET PARAMS FROM CONFIG
#THIS MUST BE ABSOLUTE PATH TO CONFIG FILE
CFG_FILE=/var/lib/clade-finder/config.txt
CFG_CONTENT=$(cat $CFG_FILE | sed -r '/[^=]+=[^=]+/!d' | sed -r 's/\s+=\s/=/g')
eval "$CFG_CONTENT"

PATH=$PATH:$pythonPath

findCladeJSON_py="$pythonScriptsDir${pathSeparator}findCladeJSON.py"
findClade23AndMe_py="$pythonScriptsDir${pathSeparator}findClade23andMe.py"
cladeSNPs="$workingDir${pathSeparator}cladeSNPs"
SNPclades="$workingDir${pathSeparator}SNPclades"
positionMarkers="$workingDir${pathSeparator}positionMarkers"
file=$1
python3 $findClade23AndMe_py $1 "$positionMarkers.bgz"