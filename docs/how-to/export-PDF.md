# Export to PDF

After enabling the `print-site` plugin in your `mkdocs.yml`, exporting to PDF is as simple as browsing to `/print_page` or `/print_page.html` (url depends on your mkdocs setting `use_directory_urls`). From your browser you can use *File > Print > Save as PDF*.

If you want to automatically create PDFs of your mkdocs website, you can automate the process using a headless chrome plugin.

If you need more control over the PDF layout, I recommend the [mkdocs-with-pdf](https://github.com/orzih/mkdocs-with-pdf) plugin.

??? warning "Avoid creating PDFs with Firefox"
    Firefox has some issues with print margins cutting of content, and anchors links not working properly.
    For more details see [mkdocs-print-site-plugin#56](https://github.com/timvink/mkdocs-print-site-plugin/issues/56)

## Automated export using nodejs and chrome

We can use [nodejs](https://nodejs.org/en/) together with the [puppeteer](https://github.com/puppeteer/puppeteer) headless chrome node.js package:

- Install [nodejs](https://nodejs.org/en/) 
- Download puppeteer in the root of your project using the node package manager: `npm i --save puppeteer`
- Save the script `export_to_pdf.js` (see below) in the root of your project
- Start a webserver with your site (`mkdocs serve`)
- In a separate terminal window, you can now run the PDF export with `url` (to your print page), `pdfPath` (name of output file) and `title` arguments:

```shell
node export_to_pdf.js http://localhost:8000/print_page.html out.pdf 'title'
```

??? example "export_to_pdf.js"

    ```js
    // Credits for script: https://github.com/majkinetor/mm-docs-template/blob/master/source/pdf/print.js
    // Requires: npm i --save puppeteer

    const puppeteer = require('puppeteer');
    var args = process.argv.slice(2);
    var url = args[0];
    var pdfPath = args[1];
    var title = args[2];

    console.log('Saving', url, 'to', pdfPath);

    // date –  formatted print date
    // title – document title
    // url  – document location
    // pageNumber – current page number
    // totalPages – total pages in the document
    headerHtml = `
    <div style="font-size: 10px; padding-right: 1em; text-align: right; width: 100%;">
        <span>${title}</span>  <span class="pageNumber"></span> / <span class="totalPages"></span>
    </div>`;

    footerHtml = ` `;


    (async() => {
        const browser = await puppeteer.launch({
            headless: true,
            executablePath: process.env.CHROME_BIN || null,
            args: ['--no-sandbox', '--headless', '--disable-gpu', '--disable-dev-shm-usage']
        });

        const page = await browser.newPage();
        await page.goto(url, { waitUntil: 'networkidle2' });
        await page.pdf({
            path: pdfPath, // path to save pdf file
            format: 'A4', // page format
            displayHeaderFooter: true, // display header and footer (in this example, required!)
            printBackground: true, // print background
            landscape: false, // use horizontal page layout
            headerTemplate: headerHtml, // indicate html template for header
            footerTemplate: footerHtml,
            scale: 1, //Scale amount must be between 0.1 and 2
            margin: { // increase margins (in this example, required!)
                top: 80,
                bottom: 80,
                left: 30,
                right: 30
            }
        });

        await browser.close();
    })();
    ```

