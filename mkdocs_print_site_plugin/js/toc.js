
/* 
TODO: Look at https://www.cssscript.com/easy-table-of-contents/ and just change the list style.
*/

window.onload = function get_toc() {

  // body = document.getElementsByTagName('body')[0];


  var ToC = "<nav role='navigation' class='print-page-toc-nav'>" +
      "<h1>Table of Contents</h1>"

  var newLine, el, title, link;

  const toc_elements = document.querySelectorAll("h1,h2,h3,h4,h5,h6")
  
  var current_heading_depth = 0

  for (var i = 0; i < toc_elements.length; i++) {

    
    el = toc_elements[i]
    title = el.innerHTML;
    link = "#" + el.id;
    tag = el.tagName
    tag_level = tag.substring(1)

    while (tag_level > current_heading_depth) {
      current_heading_depth++;
      ToC += "<ul class='print-site-toc-level-" + current_heading_depth + "'>";
    }
    while (tag_level < current_heading_depth) {
      current_heading_depth--;
      ToC += "</ul>"; 
    }

    newLine =
      "<li>" +
        "<a href='" + link + "'>" +
          title +
        "</a>" +
      "</li>";

    ToC += newLine;

  };

  ToC +=
    "</ul>" +
    "</nav>";

    document.querySelectorAll("#print-page-toc")[0].innerHTML = ToC;

}