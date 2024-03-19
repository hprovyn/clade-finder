<?php
session_start();
if (!file_exists("status.json")) {
	file_put_contents("status.json","{}");
	echo "created<br>";
}
?>
<!DOCTYPE html>
<html>
<head>
        <link rel="stylesheet" type="text/css" href="https://www.yseq.net/ext/jquery/ui/redmond/jquery-ui-1.12.1.css" />
        <link rel="stylesheet" type="text/css" href="https://www.yseq.net/ext/jquery/fancybox/jquery.fancybox-1.3.4.css" />
        <link rel="stylesheet" type="text/css" href="https://www.yseq.net/ext/960gs/960_24_col.css" />
        <link rel="stylesheet" type="text/css" href="https://www.yseq.net/stylesheet.css" />
        <script src="https://www.yseq.net/ext/jquery/jquery-3.5.1.min.js"></script>
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
        <h1>YSEQ Clade Finder (version 1.0)</h1>
    <div style="display:flex"><div style="display:inline-block;padding-top: 0px;padding-right: 20px;padding-bottom: 0px;padding-left: 20px;"><img src="CladeFinder-Logo.png" alt="Clade Finder" title="Clade Finder" width="300" style="vertical-align:middle"/>
</div><div style="display:inline-block; width:50%;padding-top: 0px;padding-right: 20px;padding-bottom: 0px;padding-left: 20px;">
Developed by Hunter Provyn with input and support from Thomas Krahn (2019).<br>
A light-weight algorithm that takes positive and negative SNPs and returns likely subclade from the <a href="https://www.yfull.com">YFull</a> YTree.<br>
Compare to <a href="https://ytree.morleydna.com/predict">Morley DNA Predictor</a>.<br>
<ul><li>Supports submission of SNPs in the following formats:<ul><li>Text</li><li>File - <b>23andMe | AncestryDNA | MyHeritage | <br>FTDNA Family Finder | VCF</b></li></ul></li>
<li>Click <img src="yfull.png" width="16" height="16"> for link to your position on the <a href="https://yfull.com/tree">YFull YTree</a></li>
<li>Click <img src="phylogeographer.png" width="16" height="16"> for link to theoretical migration and relevant forums/groups in <a href="https://phylogeographer.com">PhyloGeographer</a>, a data-driven project that calculates approximate male line migrations from YFull and other ancient samples</li>
<li><font style="color:green">Positive calls in green</font>, <font style="color:red">negative in red</font></li>
<li>Click button to expand subclade (number of children indicated)</li>
<li>SNPs marked with ($) may be tested at YSEQ, link goes to product</li>
<li>SNPs marked with (?) are not yet available at YSEQ, link goes to Wish a SNP</li></ul>

Terms of Service / Privacy Statement: This site does not use cookies or store your information in any way. Files uploaded are immediately deleted by script subsequent to analysis. For more details, refer to <a href="https://www.yseq.net/privacy.php">YSEQ Privacy Notice</a><br><br>
This YSEQ clade finder is open source software and can be cloned from GitHub: <a href="https://github.com/hprovyn/clade-finder">https://github.com/hprovyn/clade-finder</a><br><br>

Please always give a link to <a href="http://predict.yseq.net/clade-finder">this</a> original website as a reference.<br><br>

Questions | Bug Reports | Suggestions &#8594;&nbsp;<a href="mailto:hunterprovyn@gmail.com?Subject=CladeFinder">Email</a><br><br>
</div></div></div>
<br>
<div style="padding-right: 30px;padding-bottom: 50px;padding-left: 30px;text-align: left">
<h1>Enter SNPs to find Y-Haplogroup from YFull</h1><br>
<b>(1) Enter SNPs in comma separated format and click SUBMIT.</b><br>
<br>Example: M343+, L21+, DF13+, DF23+, M222-<br><br>

<script>
function reset() {
	document.getElementById("input").value = ""
}
</script>
<form id="text" action="<?php echo htmlentities($_SERVER['PHP_SELF']); ?>" method="POST">
<?php if(isset($_POST['input'])) { ?>
        <textarea form="text" id="input" name=input rows="5" size="135"><?php echo $_POST['input']; ?></textarea>

        <?php
} else { ?>
        <textarea form="text" id="input" name=input rows="5" size="135"></textarea><?php
} ?>
<input type="submit"/></form>
<button onclick="reset()">Reset</button>
<?php 
function unzipIfNecessary($zipped_in, $extracted_dir) {
	$filetype = exec("file " . $zipped_in);
	if (stripos($filetype, "gzip compressed data") !== false) {
		updateSessionStatus("Unzipping Archive");
		exec("mkdir " . $extracted_dir);
		$a = exec("gunzip -ck " . $zipped_in . " > " . $extracted_dir . "/out");
	} else {
		if (stripos($filetype, "Zip archive data") !== false) {
			updateSessionStatus("Unzipping Archive");
			$a = exec("unzip -o ". $zipped_in . " -d " . $extracted_dir);
		} else {
			exec("mkdir " . $extracted_dir);
			exec("mv " . $zipped_in . " " . $extracted_dir . "/out");
		}
	}
}

function getSafeFileName($file) {
	return str_replace(" ", '\\ ', $file);
}

function hasFileOfType($extracted_dir, $type) {
	$files = scandir($extracted_dir, 1);
	$diff = array_diff($files, array("..", "."));
	foreach($diff as $file) {
		$filetype = exec("file " . $extracted_dir . "/" . getSafeFileName($file));
		if (stripos($filetype, $type) !== false) {
			return $file;
		}
	}
	return false;
}

function processVCF($extracted_dir, $vcf) {
	$safename =  $extracted_dir . "/" . getSafeFileName($vcf);
	$safedest = $extracted_dir . "/" . "safe.txt";
	exec('mv ' . $safename . " " . $safedest);
	$reftext = exec('grep -i "reference" ' . $safedest);
	if (stripos($reftext, "hg38") !== false or stripos($reftext, "grch38") !== false or stripos($reftext, "hs38") !== false) {
		replaceYtoChrYifNecessary($safedest);
		$mode = "hg38";
		$hg38out = $safedest;
	}
	if (stripos($reftext, "hg19") !== false or stripos($reftext, "grch37") !== false or stripos($reftext, "human_g1k_v37") !== false or stripos($reftext, "hs37d5") !== false) {
		replaceYtoChrYifNecessary($safedest);
		$mode = "hg19";
	}
	if (isset($mode) == false) {
		$mode = "error";
	}	
	if ($mode == "hg19") {
		updateSessionStatus("Mapping hg19 to hg39");
		$strippedY = $extracted_dir . "/stripped";
		$hg38out = $extracted_dir . "/hg38.vcf";
		exec('head -300 ' . $safedest . ' | grep "#" > ' . $strippedY);
		exec('cat ' . $safedest . ' | grep "chrY" | grep -v "#" >> ' . $strippedY);
		exec('/var/lib/clade-finder/CrossMap.sh ' . $strippedY . ' ' . $hg38out); 
		$safedest = $hg38out;
	}
	if ($mode != "error") {
		updateSessionStatus("Reading VCF to Determine Clade");
		$snps = exec('/var/lib/clade-finder/parseVCF.sh ' . $safedest);
		unlink($safedest);
		removeSessionStatus();
		return $snps;
	} else {
		echo "Error: Unable to determine hg reference.<br>";
		removeSessionStatus();
	}
}

function replaceYtoChrYifNecessary($file) {
	$count = countChrY($file);
	if ($count == 0) {
		echo 'no chrY CHROM in vcf file, converted Y to ChrY standard<br>';
		replaceYtoChrY($file);
	}
}

function countChrY($file) {
	return exec("awk '$0~/^chrY/ {count+=1;} END {print count;}' " . $file);
}

function replaceYtoChrY($file) {
	exec("sed -i 's/^Y/chrY/' " . $file);
}

function processASCII($extracted_dir, $ascii, $alignment) {
	$safename =  $extracted_dir . "/" . getSafeFileName($ascii);
	$safedest = $extracted_dir . "/" . "safe.txt";
	exec('mv ' . $safename . " " . $safedest);
	$snps = exec('/var/lib/clade-finder/findClade23andMe.sh ' . $safedest . ' ' . $alignment);
	unlink($safedest);
        return $snps;
}
?>
<br><br>
<b>(2) File Upload</b>&nbsp;&nbsp;&nbsp;50 MB max size
<br><br>
      <form id="file" action="" method="POST" enctype="multipart/form-data">
	 <input type="file" name="23" onchange="startPoll(); form.submit()"/>
         <div style="text-align:center"><span class="status"></span><div hidden=true id="load"><img height="40" width="40" src="spinner-5.gif"/></div></div>
         <input hidden="true" type="submit"/>
      </form>
      <br><br>
<script>function startPoll() {
document.getElementById("load").style.display='block';
var sessionId = "<?php echo session_id();?>";
(function() {
	var status = $('.status'),
		poll = function() {
			$.ajax({
			url: 'https://cladefinder.yseq.net/status.json',
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
					//alert('ajax polling error');
					//console.log('Ajax polling Error!');
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
$clade_finder_uploads_root = "/usr/local/geospiza/clade-finder/uploads";
if(isset($_FILES['23'])) {
	$errors= array();
		       $file_name = $_FILES['23']['name'];
		       $file_size =$_FILES['23']['size'];
		             $file_tmp =$_FILES['23']['tmp_name'];
		             $file_type=$_FILES['23']['type'];
			     
			     $exploded = explode('.',$_FILES['23']['name']);
			     $file_ext=strtolower(end($exploded));
			     #$file_ext=strtolower(end(explode('.',$_FILES['23']['name'])));
			           
			           $extensions= array("zip", "vcf", "gz", "csv", "txt");
				         
				         if(in_array($file_ext,$extensions)=== false){
						          $errors[]="extension not allowed, please choose a ZIP file.";
							        }
				         
				         if($file_size > 52428800){
						          $errors[]='File size must be under 50 MB';
							        }
				         
				   if(empty($errors)==true){
					         $rando = rand(1,999999);
						 $upload_base_dir = $clade_finder_uploads_root . "/raw";
						 $upload_dir = $upload_base_dir . "/" . $rando;
						 mkdir($upload_dir);
						 move_uploaded_file($file_tmp,$upload_dir."/file.zip");
						 $unzipped_base_dir = $clade_finder_uploads_root . "/extracted";
						 $unzipped_dir = $unzipped_base_dir . "/" . $rando;
		 				 $zipped_file = $upload_dir."/file.zip";
						 unzipIfNecessary($zipped_file, $unzipped_dir);
						 if(file_exists($zipped_file)) {
							 unlink($zipped_file);
						 }
						 rmdir($upload_dir);
						 $hasVCF = hasFileOfType($unzipped_dir, "(VCF)");
						 if ($hasVCF !== false) {
							 $snps = processVCF($unzipped_dir, $hasVCF);
						 } else {							 
							 $hasASCII = hasFileOfType($unzipped_dir, "ASCII text");
							 if ($hasASCII !== false) {
								 //Most consumer autosomal testing companies use hg19
								 $snps = processASCII($unzipped_dir, $hasASCII, "hg19positionMarkers");
							 } else {
								 $hasASCII = hasFileOfType($unzipped_dir, "RSID sidtune playSID");

								 if ($hasASCII !== false) {
									 //FTDNA Family Finder uses hg38
									 $snps = processASCII($unzipped_dir, $hasASCII, "hg38positionMarkers");
								 } else {
									 echo 'Error: Neither VCF nor ASCII file found in uploaded file / root directory of uploaded archive';
								 }
							 }
						 }
						 exec("rm -r " . $unzipped_dir);
						 #foreach(scandir($unzipped_dir, 1) as $file) {
						#	 unlink($unzipped_dir . "/" . $file);			 
						 #}
						 
						 #rmdir($unzipped_dir);
				   } else {
					   print_r($errors);
				   }
}
if (isset($snps) and !empty($snps)) {
	$url = "https://cladefinder.yseq.net/interactive_tree.php";
	
	if (strpos($snps, "==") !== false) {
		$exploded = explode("==", $snps);
		$thesnps = $exploded[0];
		$xyReadSplit = explode(",", $exploded[1]);
		$xReads = intval($xyReadSplit[0]);
		$yReads = intval($xyReadSplit[1]);
	} else {
		$thesnps = $snps;
		$xReads = 0;
		$yReads = 200;
	}
	if ($xReads / $yReads > 40 and $yReads < 150) {
		echo 'Warning: Possible female or corrupted sample<br>' . $xReads . " X reads, " . $yReads . " Y reads<br>";
	} 
	echo '<form id="upload" action="' . $url . '" target="my-iframe" method="post">';
	echo '<input type="hidden" name="snps" id="snps" value="' . $thesnps . '">';
	echo '</form>';
	echo '<div id="ytree">';
	echo '<iframe name="my-iframe" src="' . $url . '" width="95%" height="100%"></iframe></div>';   
	echo '<script>document.forms["upload"].submit();</script>';
	
}?>



<?php if(isset($_POST['input'])) {
$url = "https://cladefinder.yseq.net/interactive_tree.php";

        $input = trim($_POST["input"]);
$parsed=urlencode(str_replace(" ", "", $input));
	echo '<div id="ytree"><iframe src="' . $url . '?snps='.$parsed.'" width="95%" height="100%"></iframe></div>';   
} ?>

</div>

</body><footer><a href="https://icons8.com">Loading Icon from Icons8.com<a></footer>
</html>
