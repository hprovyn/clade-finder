<!DOCTYPE html>
<html>
<head>
        <link rel="stylesheet" type="text/css" href="https://www.yseq.net/ext/jquery/ui/redmond/jquery-ui-1.8.22.css" />
        <link rel="stylesheet" type="text/css" href="https://www.yseq.net/ext/jquery/fancybox/jquery.fancybox-1.3.4.css" />
        <link rel="stylesheet" type="text/css" href="https://www.yseq.net/ext/960gs/960_24_col.css" />
        <link rel="stylesheet" type="text/css" href="https://www.yseq.net/stylesheet.css" />

</head>
<body>
        <div id="bodyWrapper" class="container_24">


                <div id="header" class="grid_24">
                  <div id="storeLogo"><a href="https://www.yseq.net/index.php"><img src="https://www.yseq.net/images/store_logo.png" alt="YSEQ DNA Shop" title="YSEQ DNA Shop" width="552" height="175" /></a></div>
                

                
                <div class="grid_24 ui-widget infoBoxContainer">
                  <div class="ui-widget-header infoBoxHeading">&nbsp;&nbsp;<a href="http://www.yseq.net" class="headerNavigation">Top</a> &raquo; <a href="https://www.yseq.net/index.php" class="headerNavigation">Catalog</a></div>
                </div>


<div style="display:inline-block;text-align: left;">
        <h1>YSEQ Clade Finder (beta version)</h1><br>
    <div style="display:inline-block;padding-top: 50px;padding-right: 30px;padding-bottom: 50px;padding-left: 30px;"><img src="RandomForest.jpg" alt="Random Forest" title="Random Forest" width="300" />
</div><div style="display:inline-block; width:50%;padding-top: 50px;padding-right: 30px;padding-bottom: 50px;padding-left: 80px;">
Developed by Hunter Provyn with input and support from Thomas Krahn (2019).<br>
A light-weight algorithm that takes positive and negative SNPs and returns likely YFull subclade<br><br>

This YSEQ clade finder is open source software and can be cloned from GitHub: <a href="https://github.com/hprovyn/clade-finder">https://github.com/hprovyn/clade-finder</a><br><br>

Please always give a link to <a href="http://predict.yseq.net/clade-finder">this</a> original website as a reference.<br><br><br>

</div></div>
<br>
<div style="padding-right: 30px;padding-bottom: 50px;padding-left: 30px;text-align: left">
<h1>Enter SNPs to find Y-Haplogroup from YFull</h1><br>
Enter SNPs in FTDNA format and press ENTER.<br>
Example:<br><br>
M343+, L21+, DF13+, DF23+, M222-<br><br>
<form action="<?php echo htmlentities($_SERVER['PHP_SELF']); ?>" method="POST">

<?php if(isset($_POST['input'])) { ?>
        <input name=input type="text" value="<?php echo $_POST['input']; ?>" maxlength="5000" size="135"></input>

        <?php
} else { ?>
        <input name=input type="text" maxlength="5000" size="135"></input><?php
} ?>
</form>

<br><br>




<?php if(isset($_POST['input'])) { 
        $corrected = "";
        $unrecognized = array();
        ?>
        <?php $input = trim($_POST["input"]);
        $parsed=str_replace(" ", "", $input);
        #exec('/var/lib/clade-finder/findClade.sh ' . $parsed . ' 2>&1', $output);
        #print_r($output);
        $message = exec('/var/lib/clade-finder/findClade.sh ' . $parsed);
        $predsplit = str_replace("&", "&amp;", $message);
        $predsplit = str_replace("\"", "&quot;", $predsplit);
        echo '<b>Prediction</b><div style="outline: 1px solid black" width="880" height="250"><div id="pred" style="padding:10px;overflow-y: scroll;max-height:230px" id="pred" width="860" height="230"></div></div><br><br>';       
        $updateSrc = true;
} ?>

</div>
<script>
function removeHTMLCodes(html) {
    var a = html.replace(/&amp;#9608;/g, "█")
    a = a.replace(/&quot;/g, "\"")
    a = a.replace(/&amp;nbsp;/g, " ")
    return a
}

var content = " <?php echo $predsplit ?> "
content = removeHTMLCodes(content)
document.getElementById("pred").innerHTML = content;

</script>

</body>
</html>
