#SET PARAMS FROM CONFIG
CFG_FILE=config.txt
CFG_CONTENT=$(cat $CFG_FILE | sed -r '/[^=]+=[^=]+/!d' | sed -r 's/\s+=\s/=/g')
eval "$CFG_CONTENT"

PATH=$PATH:$pythonPath:$htslibPath

createTabixTSV_py="$pythonScriptsDir${pathSeparator}createTreeInTabix.py"
findClade_py="$pythonScriptsDir${pathSeparator}findClade.py"

cladeSNPs="$workingDir${pathSeparator}cladeSNPs"
SNPclades="$workingDir${pathSeparator}SNPclades"
positionMarkers="$workingDir${pathSeparator}positionMarkers"

rm $workingDir${pathSeparator}*

python3 "$createTabixTSV_py" "$treeFile" "$markerPositionsTSV" "$cladeSNPs" "$SNPclades" "$positionMarkers"
sort "$cladeSNPs" "-k1,1" "-k2n" | "bgzip" > "$cladeSNPs.bgz"
tabix "-s" "1" "-b" "2" "-e" "3" "$cladeSNPs.bgz"
sort "$SNPclades" "-k1,1" "-k2n" | "bgzip" > "$SNPclades.bgz"
tabix "-s" "1" "-b" "2" "-e" "3" "$SNPclades.bgz"
sort "$positionMarkers" "-k1,1" "-k2n" | "bgzip" > "$positionMarkers.bgz"
tabix "-s" "1" "-b" "2" "-e" "3" "$positionMarkers.bgz"
python3 "$findClade_py" "$cladeSNPs.bgz" "$SNPclades.bgz" "PH1080+, Z1043+, Z1297+, M12+, M241+, L283+, Z1825+, CTS11760-, Z8429-" "$snpPanelConfigPath"
