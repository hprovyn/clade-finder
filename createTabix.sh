#SET PARAMS FROM CONFIG
CFG_FILE=config.txt
CFG_CONTENT=$(cat $CFG_FILE | sed -r '/[^=]+=[^=]+/!d' | sed -r 's/\s+=\s/=/g')
eval "$CFG_CONTENT"

PATH=$PATH:$pythonPath:$htslibPath

createTabixTSV_py="$pythonScriptsDir${pathSeparator}createTreeInTabix.py"
findCladeJSON_py="$pythonScriptsDir${pathSeparator}findCladeJSON.py"
cladeSNPs="$workingDir${pathSeparator}cladeSNPs"
SNPclades="$workingDir${pathSeparator}SNPclades"
hg19PositionMarkers="$workingDir${pathSeparator}hg19positionMarkers"
hg38PositionMarkers="$workingDir${pathSeparator}hg38positionMarkers"
rm $workingDir${pathSeparator}*

python3 "$createTabixTSV_py" "$treeFile" "$hg19markerPositionsTSV" "$hg38markerPositionsTSV" "$cladeSNPs" "$SNPclades" "$hg19PositionMarkers" "$hg38PositionMarkers" "$productsFile" "$toIgnoreFile"
sort "$cladeSNPs" "-k1,1" "-k2n" | "bgzip" > "$cladeSNPs.bgz"
tabix "-s" "1" "-b" "2" "-e" "3" "$cladeSNPs.bgz"
sort "$SNPclades" "-k1,1" "-k2n" | "bgzip" > "$SNPclades.bgz"
tabix "-s" "1" "-b" "2" "-e" "3" "$SNPclades.bgz"
sort "$hg19PositionMarkers" "-k1,1" "-k2n" | "bgzip" > "$hg19PositionMarkers.bgz"
tabix "-s" "1" "-b" "2" "-e" "3" "$hg19PositionMarkers.bgz"
sort "$hg38PositionMarkers" "-k1,1" "-k2n" | "bgzip" > "$hg38PositionMarkers.bgz"
tabix "-s" "1" "-b" "2" "-e" "3" "$hg38PositionMarkers.bgz"

python3 "$findCladeJSON_py" "$cladeSNPs.bgz" "$SNPclades.bgz" "PH1080+, Z1043+, Z1297+, M12+, M241+, L283+, Z1825+, CTS11760-, Z8429-" "phyloeq,downstream,products,score,panels" "$snpPanelConfigPath"