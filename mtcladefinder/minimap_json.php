<?php 

function clean($fasta) {
	$lines = explode("\n", $fasta);
	if (substr($lines[0],0,1) == ">") {
		$lines = array_slice($lines,1);
	}
	$line = strtoupper(implode("",$lines));
	return ">target\n" . preg_replace('/[^AGCT]/','',$line);
}


if(isset($_POST['fasta'])){                      
$fasta = clean($_POST['fasta']);
$tmpFolder = strval(random_int(0,99999));
mkdir("tmp/" . $tmpFolder,0777);

$myfile = fopen("tmp/" . $tmpFolder . "/fasta.txt","w");
fwrite($myfile,$fasta);
fclose($myfile);

if(isset($_POST['compare'])) {
	$compare_id = $_POST['compare'];
	$compare_prefix = "/genomes/0/refseq/mt/compare/";
	$command = $compare_prefix . 'haplogrep_mtdna_fasta_compare.py ' . $compare_prefix . 'tmp/' . $tmpFolder . '_1 ' . $compare_prefix . 'tmp/' .$tmpFolder .'_2 /var/www/html/minimap2/tmp/'.$tmpFolder.'/fasta.txt /genomes/0/refseq/mt/ncbi/allncbi/' . $compare_id . '.fasta ' . $compare_prefix . 'haplogrep-2.1.25.jar';
	$message = exec('python3 ' . $command);
	exec("rm -rf tmp/" . $tmpFolder);
	exec("rm -rf " . $compare_prefix . "tmp/" . $tmpFolder . "_*");
	echo $message;
	#echo '{"cmd":"' . $command . '"}';
} else {
$message = exec('python3 /genomes/0/refseq/mt/ncbi/mtdnaCladefinder.py -minimap 3chunk ' . $tmpFolder . '/ /var/www/html/minimap2/tmp/'.$tmpFolder.'/fasta.txt');
exec("rm -rf tmp/" . $tmpFolder);
echo $message;
}
}
?>
