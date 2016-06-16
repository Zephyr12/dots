bookmarks = [
	["r/aww", "https://www.reddit.com/r/aww"],
	["phys", "http://www.ocr.org.uk/qualifications/as-a-level-gce-physics-b-advancing-physics-h159-h559/"],
	["github", "https://github.com/Zephyr12"],
	["chem", "http://www.ocr.org.uk/qualifications/as-a-level-gce-chemistry-a-h034-h434/"],
	["math", "http://www.ocr.org.uk/qualifications/as-a-level-gce-mathematics-3890-3892-7890-7892/"],
	["comp", "http://www.aqa.org.uk/subjects/ict-and-computer-science/as-and-a-level/computing-2510/past-papers-and-mark-schemes"],
	["r/dnd", "https://www.reddit.com/r/dnd"],
	["inbox", "https://inbox.google.com"],
	["ocremix", "https://www.ocremix.org"],
	["r/linux", "https://www.reddit.com/r/linux"],
	["r/programming", "https://www.reddit.com/r/programming"],
	["r/unix", "https://www.reddit.com/r/unixporn"],
	["r/talesfromtechsupport", "https://www.reddit.com/r/talesfromtechsupport"],
	["r/RWBY", "https://www.reddit.com/r/RWBY"],
	["gmail", "https://www.gmail.com"],
	["youtube", "https://www.youtube.com/feed/subscriptions"]
];

function longestCommonSubstring(string1, string2){
	// init max value
	var longestCommonSubstring = 0;
	// init 2D array with 0
	var table = [],
            len1 = string1.length,
            len2 = string2.length,
            row, col;
	for(row = 0; row <= len1; row++){
		table[row] = [];
		for(col = 0; col <= len2; col++){
			table[row][col] = 0;
		}
	}
	// fill table
        var i, j;
	for(i = 0; i < len1; i++){
		for(j = 0; j < len2; j++){
			if(string1[i] === string2[j]){
				if(table[i][j] === 0){
					table[i+1][j+1] = 1;
				} else {
					table[i+1][j+1] = table[i][j] + 1;
				}
				if(table[i+1][j+1] > longestCommonSubstring){
					longestCommonSubstring = table[i+1][j+1];
				}
			} else {
				table[i+1][j+1] = 0;
			}
		}
	}
	return longestCommonSubstring;
}

function rankSearch(search, item){
	match_len = longestCommonSubstring(search.toLowerCase(), item.toLowerCase());
	ranking = match_len / item.length;
	if (item.startsWith(search)){
		ranking += 1;
	}
	return ranking;
}

function displayResults(results){
	innerHTML = ""
	for (let i = 0; i < results.length; i++){
		res = results[i]
		innerHTML += "<li><a href='"+res[1]+"'>"+res[0]+"</a></li>";
	}
		document.getElementById("results").innerHTML = innerHTML;
}

function refine(a){
	search = document.getElementById(a).value;
	results = []
	if (search.length > 0){
		if (search[0] == "!"){
			results = [["search the net", "https://www.duckduckgo.com/"]]
		}
		else{
			results = bookmarks.sort(function(a, b){
				return rankSearch(search, b[0]) - rankSearch(search, a[0]);
			});
		}
		document.getElementById("form").action = results[0][1];
	}else{
		document.getElementById("form").action = "https://www.duckduckgo.com";
	}
	displayResults(results.slice(0,7));
}
