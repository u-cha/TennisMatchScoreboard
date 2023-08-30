document.addEventListener("DOMContentLoaded",
                           function() {var qs_data = parseQueryString();
                                        presetSelects(qs_data);
                                        replaceQueryString(qs_data);}
                                    );

function parseQueryString() {
  const urlParams = new URLSearchParams(window.location.search);
  var num_rows = urlParams.get('num_rows');
  var page = urlParams.get('page');
  var filter_by_player_name = urlParams.get('filter_by_player_name');
  if (!num_rows) {
                num_rows = "10";
  };
  if (!page) {
                page = "1";
  };
  if (!filter_by_player_name){
                filter_by_player_name = "all";
  };
  return {
    num_rows: num_rows,
    page: page,
    filter_by_player_name: filter_by_player_name,
  };
};

function presetSelects(qs_data) {
    document.getElementById("num_rows").value = qs_data.num_rows;
    document.getElementById("filter_by_player_name").value = qs_data.filter_by_player_name;
};

function replaceQueryString(qs_data) {
    var url = new URL(window.location.href);
    url.searchParams.set("filter_by_player_name", qs_data.filter_by_player_name);
    url.searchParams.set("num_rows", qs_data.num_rows);
    url.searchParams.set("page", qs_data.page);

    window.history.replaceState({}, '', url);
};

function processNextButton() {
    var url = new URL(window.location.href);
    var currentPageNum = parseInt(url.searchParams.get("page"));
    var nextPageNum = currentPageNum + 1;
    url.searchParams.set("page", nextPageNum);
    window.location.href = url;
};



function processPrevButton() {
    var url = new URL(window.location.href);
    var currentPageNum = parseInt(url.searchParams.get("page"));
    if (currentPageNum > 1) {
        var nextPageNum = currentPageNum - 1;}
    else {
        var nextPageNum = currentPageNum;
    };
        url.searchParams.set("page", nextPageNum);
    window.location.href = url;

};


NextButton.addEventListener("click", function() {processNextButton();});
PrevButton.addEventListener("click", function() {processPrevButton();});