/* 
Javascript functions to help make the print page more PDF friendly
*/


/* 
mkdocs-material compatibility
Change theme to default mode, when printing

Only called when theme 'material' is specified in the mkdocs.yml file
*/
function change_material_theme(to="default") {

  body = document.getElementsByTagName('body')[0];
  body.setAttribute("data-md-color-scheme", to)
}


/*
Generates a table of contents for the print site page.
Only called when print-site-plugin option 'add_table_of_contents' is set to true
*/
function generate_toc() {

  var ToC = "<nav role='navigation' class='print-page-toc-nav'>" +
      "<h1 class='print-page-toc-title'>Table of Contents</h1>"

  var newLine, el, title, link;

  const toc_elements = document.querySelectorAll("h1,h2,h3,h4,h5,h6")
  
  var current_heading_depth = 0

  for (var i = 0; i < toc_elements.length; i++) {
    
    el = toc_elements[i]

    // Don't put the toc h1 in the toc
    if ( el.classList.contains('print-page-toc-title') ) {
      continue;
    }

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