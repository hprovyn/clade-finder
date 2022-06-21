<?php if(isset($_POST['input']) and isset($_POST['json'])) {
$input = trim($_POST["input"]);
$parsed=str_replace(" ", "", $input);
#$message = exec('/var/lib/m-clade-finder/findCladeJSON.sh U5b--Z1043+ "json,phyloeq,downstream"');
$message = exec('/var/lib/m-clade-finder/findCladeJSON.sh ' . $parsed . ' "json,' . $_POST['json'] . '"');
echo $message;
}
?>
