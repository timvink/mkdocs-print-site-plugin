/* 
JS to control how print page is rendered in mkdocs-material theme.

Only included by print-site-plugin when theme: material is specified in the mkdocs.yml file
*/

/* Change theme to default mode, when printing */

window.onload = function change_material_theme() {

    body = document.getElementsByTagName('body')[0];
    body.setAttribute("data-md-color-scheme", "default")
}
