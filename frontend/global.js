url = ""

function load_javascript_file(src_) {
    var s = document.createElement("script");
    s.type = "text/javascript";
    s.src = url + "/" + src_;
    document.getElementsByTagName("head")[0].appendChild(s);
}
function load_css_file(src_) {
    var s = document.createElement("link");
    s.rel = "stylesheet";
    s.href = url + "/" + src_;
    document.getElementsByTagName("head")[0].appendChild(s); 
}