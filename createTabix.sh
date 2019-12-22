#SET PARAMS FROM CONFIG
CFG_FILE=config.txt
CFG_CONTENT=$(cat $CFG_FILE | sed -r '/[^=]+=[^=]+/!d' | sed -r 's/\s+=\s/=/g')
eval "$CFG_CONTENT"

PATH=$PATH:$pythonPath:$htslibPath

createTabixTSV_py="$pythonScriptsDir${pathSeparator}createTreeInTabix.py"

yfullsnps="$workingDir${pathSeparator}yfullsnps"

rm $workingDir${pathSeparator}*

python3 "$createTabixTSV_py" "$treeFile" "$yfullsnps"
sort "$yfullsnps" "-k1,1" "-k2n" | "bgzip" > "$yfullsnps.bgz"
tabix "-s" "1" "-b" "2" "-e" "3" "$yfullsnps.bgz"
