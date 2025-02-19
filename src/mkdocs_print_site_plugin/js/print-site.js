/* 
Javascript functions to help make the print page more PDF friendly
*/

/*
Generates a table of contents for the print site page.
Only called when print-site-plugin option 'add_table_of_contents' is set to true
*/
function generate_toc() {

  var ToC = ""

  var el, title, link;

  var headingNumberStyles = "<style>";
  
  function getEntry(link, title, id, level) {
    let className = !!level ? `print-site-toc-level-${level}` : '';
    return `<li class='${className}'>
      <a id='${id}' href='${link}'>${title}</a></li>`;
  }

  function recursion(elements, level) {
    let tocElements = Array.from(elements).filter(el => el.classList.contains('print-page') &&
      (el.id ?? '') != '');

    // Extract table of contents depth
    // basically plugin setting, passed via a data attribute
    var tocDepth = document.getElementById("print-page-toc").getAttribute("data-toc-depth")

    for (var i = 0; i < tocElements.length; i++) {
      // Get the info from the element
      el = tocElements[i];
      link = "#" + el.id;
      tag = el.firstElementChild.tagName;
      tagLevel = tag.substring(1);
      headingNumber = el.getAttribute('heading-number');

      // Get the text of a heading
      // We use .firstChild.nodeValue instead of .innerText
      // because of elements like:
      // <h1 id="index-mkdocs-print-site-plugin">
      //     mkdocs-print-site-plugin<a class="headerlink" href="#index-mkdocs-print-site-plugin" title="Permanent link">↵</a>
      //  </h1>
      title = el.firstElementChild.firstChild.nodeValue;

      if ( ! title ) {
        continue;
      }

      // Ignore the MkDocs keyboard Model
      if ( el.id.indexOf("keyboardModalLabel") > -1 ) {
        continue;
      }

      tocEntryId = `toc-heading-${headingNumber.replaceAll(".", "-")}`;
      headingNumberStyles += `
        .print-site-enumerate-headings #${tocEntryId}:before { content: '${headingNumber} ' }`;

      if (el.classList.contains('md-section')) {
        ToC += "<ul class='print-site-toc-level-" + (+tagLevel+level) + "'>";
        ToC += getEntry(link, title, tocEntryId, null, null);
        recursion(el.children, level + 1);
        ToC += "</ul>"
      } else {
        ToC += getEntry(link, title, tocEntryId, +tagLevel+level);
      }
    }
  }

  ToC = "<ul>"
  let topElements = document.querySelectorAll('#print-site-page > .print-page');
  recursion(topElements, 0);
  ToC += "</ul>"
  headingNumberStyles += '</style>';

  document.querySelectorAll("#print-page-toc nav")[0].insertAdjacentHTML("beforeend", ToC);
  document.querySelectorAll("style")[0].insertAdjacentHTML("afterend", headingNumberStyles);
}


function remove_material_navigation() {

  // Remove left sidebar on print page
  remove_element_by_classname('md-sidebar--primary')
  // Remove tabs navigation on print page
  remove_element_by_classname('md-tabs')
  // Remove search
  remove_element_by_classname('md-search')

}

function remove_mkdocs_theme_navigation() {

  // Remove top navigation bar
  remove_element_by_classname('navbar')
}


function remove_element_by_classname(class_name) {
  var el = document.getElementsByClassName(class_name);
  if( el.length > 0) {
    el[0].style.display = "none"
  }
}
