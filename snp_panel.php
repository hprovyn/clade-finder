<?php

function curlCladeFinder($snps)
{
	$fields_string = "";
	$fields = array(
	            'input' => urlencode($snps),
		                    'json' => urlencode('phyloeq,downstream,products,score,panels')
				            );

	$url = "https://cladefinder.yseq.net/snp_panel_json.php";
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
	if (array_key_exists("downstream", $json_obj)) {
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


$levels = 0;
if(isset($_POST['reset'])) {
	$levels = $_POST['levels'];
	$json_obj = json_decode(str_replace("'", "\"", $_POST['json']));
	$thebranch = $json_obj->{'clade'};
	$json = curlCladeFinder($thebranch . "--2");
	$json_obj = json_decode($json)[0];
}


if(isset($_POST['json']) and !isset($_POST['reset'])) {
	$json_obj = json_decode(str_replace("'", "\"", $_POST['json']));
}
if(isset($_POST['json']) == False and isset($_GET['branch'])) {

	$branch = $_GET['branch'];
	$levels = $_GET['levels'];
	$json = curlCladeFinder($branch . "--" . $levels);
	$json_obj = json_decode($json)[0];
	#echo $json;
}
if(isset($_POST['add'])) {
	$addedClade = $_POST['add'];
	$addedObj = json_decode(curlCladeFinder($addedClade . "--3"))[0];
	addChildObj($json_obj, $addedClade, $addedObj);
} else {
	if (isset($_POST['new'])) {
		$newClade = $_POST['new'];
		$json_obj = json_decode(curlCladeFinder($newClade . "--3"));
	}
}

if(isset($_POST['expandAll']) or isset($_POST['expandAll2']) or isset($_POST['expandAll3'])) {
        $deflevels = 2;
	if (isset($_POST['expandAll'])) {
		$deflevels = 2;
	}

	if (isset($_POST['expandAll2'])) {
		$deflevels = 3;
	}

	if (isset($_POST['expandAll3'])) {
		$deflevels = 4;
	}

	$unexpandedNodes = getLeafNodesWithChildren($json_obj);
	$expandedJSON = curlCladeFinder(join(",",$unexpandedNodes) . "--" . $deflevels);
	$addedObjects = json_decode($expandedJSON);

	foreach($addedObjects as $addedObject) {
		addChildObj($json_obj, $addedObject->{'clade'}, $addedObject);
	}
}

function getLeafNodesWithChildren($obj) {
	$thechildren = array();
	if (array_key_exists("downstream", $obj)) {
		foreach ($obj->{"downstream"} as $child) {
			$thedownstr = getLeafNodesWithChildren($child);
			$thechildren = array_merge($thechildren, $thedownstr);
		}
	}
	if (array_key_exists("children", $obj)) {
		array_push($thechildren, $obj->{"clade"});
	}
	return $thechildren;
}

function getPhyloeqHTMLOutput($phyloeq_obj) {
	$phyloeq_str = "";
	foreach($phyloeq_obj as $key=>$value) {
		$color = "blue";
		$bold = True;

		$phyloeq_str = $phyloeq_str . ' <b><font color="' . $color . '">';
		
		if ($phyloeq_obj->{$key}->{"product"}) {
			$phyloeq_str = $phyloeq_str . '<a href="https://www.yseq.net/product_info.php?products_id=' . $phyloeq_obj->{$key}->{"product"} . '" target="_">'.$key.'</a></font></b>';
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
	if (array_key_exists("children", $json_obj)) {
		return '<button name="add" class="text" type="submit" style="padding:0px;font-size:10px;height:20px;width:20px" value="' . $clade .'">' . '+' . $json_obj->{"children"} . '</button>';
	}
	return "";
}

function getIconsTableHTML($clade) {
	$icons = array('<a href="https://www.yfull.com/tree/' . $clade . '" target="_"><img border="0" alt="Link to ' . $clade . ' on YFull" title="' . $clade . ' on YFull" src="yfull.png" width="16" height="16"></a>', 
		'<a href="https://hras.yseq.net/hras.php?dna_type=y&map_type=alpha&hg=' . $clade . '" target="_"><img border="0" alt="View maps, migrations and statistics on HRAS" title="' . $clade . ' maps, migrations and statistics on HRAS" src="heat.png" width="16" height="16"></a>',
		'<a href="https://www.phylogeographer.com/snp-lookup?' . $clade . '" target="_"><img border="0" alt="View theoretical migration on PhyloGeographer" title="' . $clade . ' on PhyloGeographer" src="phylogeographer.png" width="16" height="16"></a>',
		'<a href="https://phylogeographer.com/what-do-all-these-codes-mean/" target="_"><img src="questionmark.png" height="16" width="16"/></a>', 
		'<button name="expandAll" type="submit">+1</button>', 
		'<button name="expandAll2" type="submit">+2</submit>', 
		'<button name="expandAll3" type="submit">+3</submit>',
		'<button name="reset" type="submit">&#8634;</submit>');
	return '<table border = "1px solid black"><tr><td>' . implode('</td><td>', $icons) . '</td></tr></table>';
}

function recursivelyBuildTree($json_obj, $level, $branchesBelow) {
	echo '<tr><td nowrap align="top">' . getIndent($branchesBelow) . getSpanOrName($json_obj, $level) . "&nbsp;" . getExpandButton($json_obj) . '</td><td>' . getPhyloeqHTMLOutput($json_obj->{"phyloeq"}) . "</td></tr>";
	if (array_key_exists("downstream", $json_obj)) {
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

?>
<html><head></head><body>
<div style="font-family: monospace;">
<form name="interactive_tree" method="post">
<input type="hidden" name="levels" value="<?php echo $levels; ?>">

<input type="hidden" name="json" value="<?php echo str_replace("\"", "'", json_encode($json_obj)); ?>"> 
<?php

if (array_key_exists("clade", $json_obj)) {
	$clade = $json_obj->{"clade"};

	echo 'Most specific position on the <a href="https://www.yfull.com" target="_">YFull</a> <a href="https://www.yfull.com/tree/" target="_">YTree</a> is ' . $clade . getIconsTableHTML($clade);
	echo '<table style="font-size:10;">';
	recursivelyBuildTree($json_obj, 0, "");
	echo '</table>';
} else {
	if (array_key_exists("error", $json_obj)) {
		echo $json_obj->{"error"};
	} else {
		echo "error: malformed backend response";
	}
}
?>
</div>

</body></html>
