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
  var current_color_theme = body.getAttribute('data-md-color-scheme')
  
  var beforePrint = function() {
      console.log('Functionality to run before printing.');
      body.setAttribute("data-md-color-scheme", to);
  };
  var afterPrint = function() {
      console.log('Functionality to run after printing');
      body.setAttribute("data-md-color-scheme", current_color_theme); 
  };

  if (window.matchMedia) {
      var mediaQueryList = window.matchMedia('print');
      mediaQueryList.addListener(function(mql) {
          if (mql.matches) {
              beforePrint();
          } else {
              afterPrint();
          }
      });
  }

  window.onbeforeprint = beforePrint;
  window.onafterprint = afterPrint;

}


/*
Generates a table of contents for the print site page.
Only called when print-site-plugin option 'add_table_of_contents' is set to true
*/
function generate_toc() {

  var ToC = "<nav role='navigation' class='print-page-toc-nav'>" +
      "<h1 class='print-page-toc-title'>Table of Contents</h1>"

  var newLine, el, title, link;

  const toc_elements = document.querySelectorAll("#print-site-page h1.nav-section-title, #print-site-page h1.nav-section-title-end, section.print-page h1,section.print-page h2,section.print-page h3,section.print-page h4,section.print-page h5,section.print-page h6")
  
  var current_heading_depth = 0

    // We want to style navigation sections differently. 
    // This flag keeps track of headings that are part of a section.
  var is_section_child = false;

  for (var i = 0; i < toc_elements.length; i++) {
    
    el = toc_elements[i]

    // If the section pages end, change the flag
    if ( el.classList.contains('nav-section-title-end') ) {
      is_section_child = false;
      ToC += "<li style='list-style-type: none; padding-bottom: 1em;'></li>"
      continue;
    }

    // Don't put the toc h1 in the toc
    if ( el.classList.contains('print-page-toc-title') ) {
      continue;
    }
    // Ignore the MkDocs keyboard Model
    if ( el.id.indexOf("keyboardModalLabel") > -1 ) {
      continue;
    }

    title = el.innerText;
    if ( title.length == 0 ) {
      continue;
    }

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

    if ( el.classList.contains('nav-section-title') ) {
      newLine = "<li class='toc-nav-section-title'>" + title + "</li>"; 
      is_section_child = true;
    } else {

      a_class = is_section_child ? " class='toc-nav-section-child'" : "";
      newLine =
        "<li" + a_class + ">" +
          "<a href='" + link + "'>" +
            title +
          "</a>" +
        "</li>";
    }


    ToC += newLine;

  };

  ToC +=
    "</ul>" +
    "</nav>";

    document.querySelectorAll("#print-page-toc")[0].innerHTML = ToC;

}