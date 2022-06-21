function getColorized(snp) {
	var repl = snp.replaceAll("A","<span style=\"color:green\">A</span>")
	var repl = repl.replaceAll("C","<span style=\"color:blue\">C</span>")
	var repl = repl.replaceAll("G","<span style=\"color:black\">G</span>")
	var repl = repl.replaceAll("T","<span style=\"color:red\">T</span>")
	return repl
}

function differences() {
	var html = "<table border=\"1\"><tr><td>" + headers[0] + "</td><td>" + headers[1] + "</td><td>" + headers[2] + "</td><td>" + headers[3] + "</td></tr>"
	for( var i = 0; i < rows.length; i++) {
		if (rows[i][1] != rows[i][2]) {
			html += '<tr><td>' + rows[i][0] + '</td><td>' + getColorized(rows[i][1]) + '</td><td>' + getColorized(rows[i][2]) + '</td><td style="text-align:center"><a href="' + rows[i][3] + '" target="_"><span style="color:blue">'+rows[i][4]+'</span></a></td></tr>'
		}
	}
	html += "</table>"
	document.getElementById("comparisonTable").innerHTML = html
}

function shared() {
	var html = "<table border=\"1\"><tr><td>" + headers[0] + "</td><td>" + headers[1] + "</td><td>" + headers[2] + "</td><td>" + headers[3] + "</td></tr>"
	for( var i = 0; i < rows.length; i++) {
		if (rows[i][1] == rows[i][2]) {
			html += '<tr><td>' + rows[i][0] + '</td><td>' + getColorized(rows[i][1]) + '</td><td>' + getColorized(rows[i][2]) + '</td><td style="text-align:center"><a href="' + rows[i][3] + '" target="_"><span style="color:blue">'+rows[i][4]+'</span></a></td></tr>'
		}
	}
	html += "</table>"
	document.getElementById("comparisonTable").innerHTML = html
}

function alll() {
	var html = "<table border=\"1\"><tr><td>" + headers[0] + "</td><td>" + headers[1] + "</td><td>" + headers[2] + "</td><td>" + headers[3] + "</td></tr>"
	for( var i = 0; i < rows.length; i++) {
		
			html += '<tr><td>' + rows[i][0] + '</td><td>' + getColorized(rows[i][1]) + '</td><td>' + getColorized(rows[i][2]) + '</td><td style="text-align:center"><a href="' + rows[i][3] + '" target="_"><span style="color:blue">'+rows[i][4]+'</span></a></td></tr>'
		}
	
	html += "</table>"
	document.getElementById("comparisonTable").innerHTML = html
}


rows.sort((a,b) => parseInt(a[0].substring(5)) > parseInt(b[0].substring(5)))
differences()
