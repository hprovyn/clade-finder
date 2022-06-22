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

function getPanel($position) {
	global $panelRanges;
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



session_start();
if (!file_exists("status.json")) {
	file_put_contents("status.json","{}");
	echo "created<br>";
}
?>
<!DOCTYPE html>
<html>
<head>
        <link rel="stylesheet" type="text/css" href="https://predict.yseq.net/mt-clade-finder/loader2.css" />
        <link rel="stylesheet" type="text/css" href="https://www.yseq.net/ext/jquery/ui/redmond/jquery-ui-1.8.22.css" />
        <link rel="stylesheet" type="text/css" href="https://www.yseq.net/ext/jquery/fancybox/jquery.fancybox-1.3.4.css" />
        <link rel="stylesheet" type="text/css" href="https://www.yseq.net/ext/960gs/960_24_col.css" />
	<link rel="stylesheet" type="text/css" href="https://www.yseq.net/stylesheet.css" />
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<style>
#ytree {
height: 380px;
width: 98%;
overflow-x: auto;
overflow-y: hidden;
resize: both;
position: relative;
z-index: 1;
}
iframe {
width: 100%;
height: 100%;
border: 1;
}
tr.selected td {
background: none repeat scroll 0 0 #FFCF8B;
color: #000000;
}
</style>
</head>
<body>
        <div id="bodyWrapper" class="container_24">


                <div id="header" class="grid_24">
                  <div id="storeLogo"><a href="https://www.yseq.net/index.php"><img src="https://www.yseq.net/images/store_logo.png" alt="YSEQ DNA Shop" title="YSEQ DNA Shop" width="552" height="175" /></a></div>
                

                
                <div class="grid_24 ui-widget infoBoxContainer">
                  <div class="ui-widget-header infoBoxHeading">&nbsp;&nbsp;<a href="http://www.yseq.net" class="headerNavigation">Top</a> &raquo; <a href="https://www.yseq.net/index.php" class="headerNavigation">Catalog</a></div>
                </div>


<div style="display:inline-block;text-align: left;">
        <h1>YSEQ mt Clade Finder (version 0.1 / Beta)</h1>
    <div style="display:flex"><div style="display:inline-block;padding-top: 0px;padding-right: 10px;padding-bottom: 0px;padding-left: 10px;"><img src="YSEQ-mt-CladeFinder_Logo.png" alt="Clade Finder" title="Clade Finder" width="300" style="vertical-align:middle"/><br><small>Logo designed by Chris Rottensteiner</small>
</div><div style="display:inline-block; width:60%;padding-top: 0px;padding-right: 10px;padding-bottom: 0px;padding-left: 10px;">
Developed by Hunter Provyn with input and support from Thomas Krahn (2022).<br>
A minimap2 driven algorithm that takes a FASTA and returns closest matches from NCBI dataset, mapped to the <a href="https://www.yfull.com">YFull</a> MTree.<br>
Compare to <a href="https://dna.jameslick.com/mthap">James Lick mtHap</a>.<br>

This YSEQ mt Clade Finder is open source software and can be cloned from GitHub: <a href="https://github.com/hprovyn/clade-finder">https://github.com/hprovyn/clade-finder</a><br><br>

Please always give a link to <a href="http://predict.yseq.net/mt-clade-finder">this</a> original website as a reference.<br><br>

Questions | Bug Reports | Suggestions &#8594;&nbsp;<a href="mailto:hunterprovyn@gmail.com?Subject=mt-Clade-Finder">Email</a><br><br>
</div></div></div>
<br>
<div style="padding-right: 0px;padding-bottom: 50px;padding-left: 0px;text-align: left">
<div style="display:flex">
<div><h1>Upload FASTA file</h1></div>
<div><br>&nbsp;&nbsp;
      <form id="file" action="" method="POST" enctype="multipart/form-data">
	 <input type="file" name="23" onchange="startPoll(); form.submit()"/>
	 <div style="text-align:center">&nbsp;&nbsp;&nbsp;<span class="status"></span><br><div hidden=true id="load">
<div class="loader" style="display:flex;justify-content:center;align-items:center;width:50px">
<div class="dot"></div><div class="dot"/></div><div class="dot"></div>
<div class="dot"></div><div class="dot"/></div><div class="dot"></div>
<div class="dot"></div><div class="dot"/></div><div class="dot"></div>
<div class="dot"></div><div class="dot"/></div><div class="dot"></div>
<div class="dot"></div><div class="dot"/></div><div class="dot"></div>
<div class="dot"></div><div class="dot"/></div><div class="dot"></div>
<div class="dot"></div><div class="dot"/></div><div class="dot"></div>
<div class="dot"></div><div class="dot"/></div><div class="dot"></div>
<div class="dot"></div>
</div>
</div></div>
         <input hidden="true" type="submit"/>
      </form>
</div></div>
<script>function startPoll() {
document.getElementById("load").style.display='block';
var sessionId = "<?php echo session_id();?>";
(function() {
	var status = $('.status'),
		poll = function() {
			$.ajax({
			url: 'https://predict.yseq.net/mt-clade-finder/status.json',
				dataType: 'json',
				type: 'get',
				success: function(data) {
					if (!(sessionId in data)) {

						status.text('Uploading');
					}
					else {
						if (data[sessionId].uploaded) {
							status.text(data[sessionId].info);
						}
					}
				},
				error: function() {
				}
			});
		},
		pollInterval = setInterval(function() {
			poll();
		}, 3000);
	poll();
})();
}
</script>

<?php
function removeSessionStatus() {
	$statuses = json_decode(file_get_contents("status.json"),true);
	unset($statuses[session_id()]);
	file_put_contents("status.json", json_encode($statuses));
}
function updateSessionStatus($update) {
	if (file_exists("status.json")) {
		$statuses = json_decode(file_get_contents("status.json"),true);
	} else {
		$statuses = array();
	}
	$statuses[session_id()] = array("uploaded"=>true, "info"=>$update);
	file_put_contents("status.json", json_encode($statuses));
}

function clean($fasta) {
	$lines = explode("\n", $fasta);
	if (substr($lines[0],0,1) == ">") {
		$lines = array_slice($lines,1);
	}
	$line = strtoupper(implode("",$lines));
	return ">\n" . preg_replace('/[^AGCT]/','',$line);
}
if(isset($_FILES['23'])) {
	$file_tmp =$_FILES['23']['tmp_name'];
	$file_ext=strtolower(end(explode('.',$_FILES['23']['name'])));
	updateSessionStatus('processing');
	$fasta = clean(file_get_contents($file_tmp));
	#echo $fasta;
	$response = getBestMatchHG($fasta);
	removeSessionStatus(); 
	$_POST['matches'] = $response;
	$_POST['fasta'] = $fasta;
}

if(isset($_POST['matches'])) {
	echo '<div style="display:flex"><div style="display:inline-block;padding-top: 0px;padding-right: 15px;padding-bottom: 0px;padding-left: 0px;"><h1>Matches</h1><br>';
	echo getTable($_POST['matches']);
	echo '</div>';

}

function getTable($result) {
	$tableHTML = '<script>function rowclicked(matchid) {document.getElementById(matchid).click()}</script>';
	$tableHTML .= '<script>function compareclicked(matchid) {document.getElementById(matchid).click()}</script>';
	$tableHTML .= '<form name="matches" method="post">';
	$tableHTML .= '<input type="hidden" name="fasta" value = \'' . $_POST['fasta'] . '\'>';
	$tableHTML .= '<input type="hidden" name="matches" value=\'' .$result. '\'>';
	$json_obj = json_decode($result, true);

	$tableHTML .= '<table border="1"><tr><td>Id</td><td>Haplogroup</td><td>Identity</td><td>Differences</td><td>Comparison Block Length</td></tr>';
	$matches = 0;
	if (!isset($_POST['add'])) {
		if (isset($_POST['compare'])) {
			$_POST['add'] = explode("_*_",$_POST['compare'])[0];
		} else {
			$_POST['add'] = $json_obj['matches'][0]['hg'];
		}
	}
	foreach($json_obj["matches"] as $match) {
		$trSelected = "";
		if (isset($_POST['add']) and $match['hg'] == $_POST['add']) {
			$trSelected = " class='selected' ";
		}
		$matches += 1;
		$tableHTML .= '<tr'.$trSelected.'>' . '<td><a href="https://www.ncbi.nlm.nih.gov/nuccore/' . $match['id'].'/" target="_blank">' . $match['id'] . "</td><td>". '<a href="#" onclick=\'rowclicked("match'.$matches.'")\'>' . $match['hg'] . "</a><button id='match".$matches."' class='text' name='add' type='submit' value='".$match['hg']."' hidden></button></td><td>" . $match['percent'] . "%</td><td style=\"text-align:center\">" . ' <a title="Compare" href="#" onclick=\'compareclicked("compare'.$matches.'")\'>'.$match['differences'].'</a>' . "<button id='compare".$matches."' class='text' name='compare' type='submit' value='".$match['hg']. "_*_" . $match['id']."' hidden></td><td style=\"text-align:center\">" . $match["block"] . "</td></tr>";

	}
	$tableHTML .= '</table></form>';
return $tableHTML;
}

function getBestMatchHG($fasta)
{

	$fields = array('fasta' => urlencode($fasta));

	$url = "https://minimap2.yseq.net:7878/minimap2/json.php";
	foreach($fields as $key=>$value) { $fields_string .= $key.'='.$value.'&'; }
	rtrim($fields_string, '&');

	$ch = curl_init();

	curl_setopt($ch,CURLOPT_URL, $url);
	curl_setopt($ch,CURLOPT_POST, count($fields));
	curl_setopt($ch,CURLOPT_SSL_VERIFYPEER, false);
	curl_setopt($ch,CURLOPT_SSL_VERIFYHOST, false);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	curl_setopt($ch,CURLOPT_POSTFIELDS, $fields_string);
	$result = curl_exec($ch);

	curl_close($ch);
        return $result;
}

function getComparison($fasta, $ncbiid)
{

	$fields = array('fasta' => urlencode($fasta),
	'compare'=> $ncbiid);

	$url = "http://minimap2.yseq.net:7979/minimap2/json.php";
	foreach($fields as $key=>$value) { $fields_string .= $key.'='.$value.'&'; }
	rtrim($fields_string, '&');

	$ch = curl_init();

	curl_setopt($ch,CURLOPT_URL, $url);
	curl_setopt($ch,CURLOPT_POST, count($fields));
	curl_setopt($ch,CURLOPT_SSL_VERIFYPEER, false);
	curl_setopt($ch,CURLOPT_SSL_VERIFYHOST, false);
	curl_setopt($ch,CURLOPT_RETURNTRANSFER, true);
	curl_setopt($ch,CURLOPT_POSTFIELDS, $fields_string);
	$result = curl_exec($ch);

	curl_close($ch);
        return $result;
}



if(isset($_POST['add'])) {

$url = "https://predict.yseq.net/mt-clade-finder/interactive_tree.php";

$input = trim($_POST["add"]);

if (isset($_POST['compare'])) {
	$input = trim(explode("_*_",$_POST['compare'])[0]);
}
$parsed=urlencode(str_replace(" ", "", $input));
	echo '<div id="ytree"><h1>Haplogroup Info</h1><br><iframe src="' . $url . '?snps='.$parsed.'--" width="95%" height="100%"></iframe></div></div>';   
} else {
	if(isset($_POST['matches'])) {
		echo "</div>";
	}

}

function getPosition($sampleMatch) {
	$snp = "";
	if ($sampleMatch['sample'] != "---") {
		$snp = $sampleMatch['sample'];
	} else {
		$snp = $sampleMatch['match'];
	}
	return intval(str_replace(array("A","C","T","G","d"),"",$snp));
}

function getColorized($snp) {
	$snp = str_replace("A",'<span style="color:green">A</span>',$snp);	
	$snp = str_replace("C",'<span style="color:blue">C</span>',$snp);
	$snp = str_replace("G",'<span style="color:black">G</span>',$snp);
	$snp = str_replace("T",'<span style="color:red">T</span>',$snp);
	return $snp;
}
function getComparisonTable($responseObj, $compare) {
	$tableHTML = "<table border = \"1\"><tr><td>Position</td><td>Sample</td><td>".$compare."</td><td>Test Panel</td></tr>";
	foreach($responseObj as $sampleMatch) {
		$position = getPosition($sampleMatch);
		$panel = getPanel($position);
		$panelLink = getPanelLink($panel);
		$tableHTML .= "<tr><td>chrM:" . $position . '</td><td>' . getColorized($sampleMatch['sample']) . "</td><td>" . getColorized($sampleMatch['match']) . '</td><td style="text-align:center">' . '<a href="' . $panelLink . '"><span style="color:blue">' . $panel . '</span></a></td></tr>';
	}
	$tableHTML .= "</table>";
	return $tableHTML;
}

function getComparisonScript($responseObj, $compare) {
	$headers = array("Position","Sample",$compare,"Test Panel");
	$rows = array();
	foreach($responseObj as $sampleMatch) {
		$position = getPosition($sampleMatch);
		$panel = getPanel($position);
		$panelLink = getPanelLink($panel);
		array_push($rows, array("chrM:" . $position, $sampleMatch['sample'], $sampleMatch['match'], $panelLink, $panel));
	}
	$script = '<script> var headersString = \'' . json_encode($headers) . '\';';
	$script .= 'var headers = JSON.parse(headersString);';
	$script .= 'var rows = JSON.parse(\'' . json_encode($rows) . '\');';
	$script .= '</script><button onclick="differences()">Differences</button><button onclick="shared()">Shared</button><button onclick="alll()">All</button><div id="comparisonTable"></div>';

	$script .= '<script src="https://predict.yseq.net/mt-clade-finder/table.js"></script>';
	return $script;
}

if(isset($_POST['compare'])) {
	$compare = explode("_*_", $_POST['compare'])[1];
	echo '<h1>Differences to rCRS</h1> <br>';
	$response = getComparison($_POST['fasta'], $compare);
        $json_obj = json_decode($response, true);
	#echo getComparisonTable($json_obj, $compare);
	echo getComparisonScript($json_obj, $compare);
}
?>

</div>

</body><footer></footer>
</html>
