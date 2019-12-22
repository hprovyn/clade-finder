#SET PARAMS FROM CONFIG
CFG_FILE=config.txt
CFG_CONTENT=$(cat $CFG_FILE | sed -r '/[^=]+=[^=]+/!d' | sed -r 's/\s+=\s/=/g')
eval "$CFG_CONTENT"

PATH=$PATH:$pythonPath:$htslibPath

createTabixTSV_py="$pythonScriptsDir${pathSeparator}createTreeInTabix.py"
cladeFinder_py="$pythonScriptsDir${pathSeparator}cladeFinder.py"

cladeSNPs="$workingDir${pathSeparator}cladeSNPs"
SNPclades="$workingDir${pathSeparator}SNPclades"

rm $workingDir${pathSeparator}*

python3 "$createTabixTSV_py" "$treeFile" "$cladeSNPs" "$SNPclades"
sort "$cladeSNPs" "-k1,1" "-k2n" | "bgzip" > "$cladeSNPs.bgz"
tabix "-s" "1" "-b" "2" "-e" "3" "$cladeSNPs.bgz"
sort "$SNPclades" "-k1,1" "-k2n" | "bgzip" > "$SNPclades.bgz"
tabix "-s" "1" "-b" "2" "-e" "3" "$SNPclades.bgz"

python3 "$cladeFinder_py" "$cladeSNPs" "$SNPclades"
