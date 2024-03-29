<?php

$panelRanges = array("mt1"=>[16516,370],
"mt2"=>[334,786],
"mt3"=>[536,1172],
"mt4"=>[1158,1764],
"mt5"=>[1763,2426],
"mt6"=>[2417,3054],
"mt7"=>[3015,3627],
"mt8"=>[3555,4219],
"mt9"=>[4204,4904],
"mt10"=>[4858,5551],
"mt11"=>[5547,6023],
"mt12"=>[5842,6569],
"mt13"=>[6244,6938],
"mt14"=>[6937,7705],
"mt15"=>[7523,7891],
"mt16"=>[7870,8545],
"mt17"=>[8454,9168],
"mt18"=>[9120,9847],
"mt19"=>[9843,10497],
"mt20"=>[10416,11013],
"mt21"=>[10988,11662],
"mt22"=>[11653,12341],
"mt23"=>[12304,12987],
"mt24"=>[12984,13581],
"mt25"=>[13565,14258],
"mt26"=>[14248,14911],
"mt27"=>[14754,15400],
"mt28"=>[15393,16048],
"mt29"=>[15899,16526]);

function getPanel($snp) {
	global $panelRanges;
	$position = intval(substr($snp, 1, -1));
	$valid = array();
	foreach($panelRanges as $panel=>$range) {
		if($range[0] < $range[1]) {
			if($position > $range[0] and $position < $range[1]) {
				array_push($valid, $panel);
			}
		} else {
			if($position > $range[0] or $position < $range[1]) {
				array_push($valid, $panel);
			}
		
		}
	}
	if (count($valid) == 2) {
		return getBestPanel($position, $valid[0], $valid[1]);
	} else {
		return $valid[0];
	}
}

function getBestPanel($position, $panel1, $panel2) {
	global $panelRanges;
	if (min(array(abs($position-$panelRanges[$panel1][0]),abs($position-$panelRanges[$panel1][1]))) > min(array(abs($position-$panelRanges[$panel2][0]),abs($position-$panelRanges[$panel2][1])))) {
		return $panel1;
	} else {
		return $panel2;
	}
}


function getPanelLink($panel) {
	return "https://www.yseq.net/product_info.php?cPath=28_31&products_id=" . (108720 + intval(substr($panel,2)));
}

function curlCladeFinder($snps)
{

	$fields = array(
	            'input' => urlencode($snps),
		                    'json' => urlencode('phyloeq,downstream,products,score,panels')
				            );

	$url = "https://predict.yseq.net/mt-clade-finder/json.php";
	foreach($fields as $key=>$value) { $fields_string .= $key.'='.$value.'&'; }
	rtrim($fields_string, '&');

	$ch = curl_init();

	curl_setopt($ch,CURLOPT_URL, $url);
	curl_setopt($ch,CURLOPT_POST, count($fields));
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	curl_setopt($ch,CURLOPT_POSTFIELDS, $fields_string);
	$result = curl_exec($ch);

	curl_close($ch);
	return $result;
}
function addChildObj(&$json_obj, $childClade, $childObj)
{
	if ($json_obj->{'downstream'}) {
		$count = 0;
		foreach($json_obj->{'downstream'} as $obj) {
			if ($obj->{'clade'} == $childClade) {
				$json_obj->{'downstream'}[$count] = $childObj;
				return;
			}
			addChildObj($json_obj->{'downstream'}[$count], $childClade, $childObj);
			$count++;
		}
	}
}

if(isset($_POST['snps'])) {
        $snps = $_POST['snps'];
	$json = curlCladeFinder($snps);
	$json_obj = json_decode($json);
}

if(isset($_POST['json'])) {
	$json_obj = json_decode(str_replace("'", "\"", $_POST['json']));
}
if(isset($_POST['json']) == False and isset($_GET['snps'])) {

	$snps = $_GET['snps'];
	$json = curlCladeFinder($snps);
	$json_obj = json_decode($json);
}
if(isset($_POST['add'])) {
	$addedClade = $_POST['add'];
	if (isset($_POST['snps'])) {
		$snps = $_POST['snps'];
	}
	if (isset($_GET['snps'])) {
		$snps = $_GET['snps'];
	}
	$addedObj = json_decode(curlCladeFinder($addedClade . "--" . $snps));
	addChildObj($json_obj, $addedClade, $addedObj);
} else {
	if (isset($_POST['new'])) {
		$newClade = $_POST['new'];
		if (isset($_POST['snps'])) {
			$snps = $_POST['snps'];
		}
		if (isset($_GET['snps'])) {
			$snps = $_GET['snps'];
		}
		$json_obj = json_decode(curlCladeFinder($newClade . "--" . $snps));
	}
}


function getPhyloeqHTMLOutput($phyloeq_obj) {
	$phyloq_str = "";
	foreach($phyloeq_obj as $key=>$value) {
		$color = "blue";
		$bold = False;
		$call = $phyloeq_obj->{$key}->{"call"};
		if ($call == "+") {
			$color = "green";
			$bold = True;
		} else {
			if ($call == "-") {
				$color = "red";
				$bold = True;
			} else {
				if ($phyloeq_obj->{$key}->{"product"}) {
					$color = "blue";
					$bold = "True";
				} else {
					$color = "blue";
				}
			}
		}

		$phyloeq_str = $phyloeq_str . ' <font color="' . $color . '">';
		if ($bold) {
			$phyloeq_str = $phyloeq_str . "<b>";
		}
		if ($call == "?") {
		
			if ($phyloeq_obj->{$key}->{"product"}) {
				$phyloeq_str = $phyloeq_str . $key . '<a href="https://www.yseq.net/product_info.php?products_id=' . $phyloeq_obj->{$key}->{"product"} . '" target="_">($)</a></font>';
			} else {
				$phyloeq_str = $phyloeq_str . $key . '<a href="'.getPanelLink(getPanel($key)).'" target="_">($)</a></font>';
			}
		} else {
			$phyloeq_str = $phyloeq_str . $key . $call . "</font>";
		}
		if ($bold) {
			$phyloeq_str = $phyloeq_str . "</b>";
		}
	}
	return $phyloeq_str;
}

function getIndent($branchesBelow) {
	if ($branchesBelow == "") {
		return "";
	}
	$indent = "";
	$array = str_split($branchesBelow);
	for($i = 0; $i < count($array) - 1; $i++) {
		if ($array[$i] == "y") {
			$indent = $indent . "&#9475;&nbsp;";
		} else {
			if ($array[$i] != "") {
				$indent = $indent . "&nbsp;&nbsp;";
			}
		}
	}
	$arraylen = count($array);
	if ($arraylen > 0) {
		if ($array[$arraylen - 1] == "y") {
			$indent = $indent . "&#9507;";
		} else {
			$indent = $indent . "&#9495;";
		}
	}
	
	return $indent . "&#9473;";
}

function getSpanOrName($json_obj, $level) {
	$clade = $json_obj->{"clade"};
#	if ($level == 0) {
#		return '<a href="https://www.yfull.com/tree/' . $clade . '" target="_"><b>' . $clade . '</b></a>';
#	}
	return "<b>" . $clade . "</b>";
}

function getExpandButton($json_obj) {
	$clade = $json_obj->{"clade"};
	if ($json_obj->{"children"}) {
		return '<button name="add" class="text" type="submit" style="padding:0px;font-size:10px;height:20px;width:20px" value="' . $clade .'">' . '+' . $json_obj->{"children"} . '</button>';
	}
	return "";
}

function recursivelyBuildTree($json_obj, $level, $branchesBelow) {
	echo '<tr><td nowrap align="top">' . getIndent($branchesBelow) . getSpanOrName($json_obj, $level) . "&nbsp;" . getExpandButton($json_obj) . '</td><td>' . getPhyloeqHTMLOutput($json_obj->{"phyloeq"}) . "</td></tr>";
	if ($json_obj->{"downstream"}) {
		$len = count($json_obj->{"downstream"});
		$count = 0;
		foreach($json_obj->{"downstream"} as $child) {
			$hasBelow = "y";
			if ($count == $len - 1) {
				$hasBelow = "n";
			}
			recursivelyBuildTree($child, $level + 1, $branchesBelow . $hasBelow);
			$count++;
		}
	}

}

function negativeForAllDownstream($json_obj) {
	$negativeForAll = True;
	if ($json_obj->{"downstream"}) {
		foreach($json_obj->{"downstream"} as $child) {
			$falseForOne = False;
			foreach($child->{"phyloeq"} as $key=>$value) {
				if ($child->{"phyloeq"}->{$key}->{"call"} == "-") {
					$falseForOne = True;
				}
			}
			$negativeForAll = $negativeForAll && $falseForOne;
		}
	} else {
		return False;
	}
	return $negativeForAll;
}

function getPanelsHTML($json_obj) {
	$html = "<br>Available Panels<br><ul>";
	foreach($json_obj->{"panels"} as $child) {
		$html = $html . "<li>" . $child->{"link"} . "&nbsp;<i>" . $child->{"text"} . "</i></li>";
	}
	$html = $html . "</ul><br>";
	return $html;
}
?>
<html><head></head><body>
<div style="font-family: monospace;">
<form name="interactive_tree" method="post">
<input type="hidden" name="snps" value="<?php 
echo $snps;
?>">

<input type="hidden" name="json" value="<?php echo str_replace("\"", "'", json_encode($json_obj)); ?>"> 
<?php

if ($json_obj->{"clade"}) {
	$clade = $json_obj->{"clade"};

	echo 'Most specific position on the <a href="https://www.yfull.com" target="_">YFull</a> <a href="https://www.yfull.com/mtree/" target="_">MTree</a> is ' . $clade . ' <a href="https://www.yfull.com/mtree/' . $clade . '" target="_"><img border="0" alt="Link to ' . $clade . ' on YFull" title="' . $clade . ' on YFull" src="yfull.png" width="16" height="16"></a>&nbsp;<a href="https://phylogeographer.com/scripts/mt_heatmap.php?hg=' . $clade . '" target="_"><img border="0" alt="View heatmap on M Heatmap" title="' . $clade . ' on M Heatmap" src="heat.png" width="16" height="16"></a>&nbsp;<a href="https://phylogeographer.com/what-do-all-these-codes-mean/" target="_"><img src="questionmark.png" height="16" width="16"/></a><br><br>';
	echo '<table style="font-size:10;">';
	recursivelyBuildTree($json_obj, 0, "");
	echo '</table>';
	if (negativeForAllDownstream($json_obj) == True) {
		echo '<br>Negative for all known downstream SNPs<br>';
	}
	$best_score = $json_obj->{"score"};
	if ($json_obj->{"score"} < 0) {
		echo '<br>Warning: Negative score indicates unreliable result<br>';
	}
	if ($json_obj->{"panels"}) {
		echo getPanelsHTML($json_obj);
	}
	if ($json_obj->{"nextPrediction"}) {
		$clade = $json_obj->{"nextPrediction"}->{"clade"};
		$score = $json_obj->{"nextPrediction"}->{"score"};
		echo '<br>Next best prediction (scored ' . $score . ' compared to ' . $best_score . ')&nbsp;<button name="new" class="text" type="submit" style="padding:0px;font-size:10px;height:20px;width:100px" value="' . $clade .'">' . $clade . '</button><br>';
	}
} else {
	echo $json_obj->{"error"};
}
?>
</div>

</body></html>
