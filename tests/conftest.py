def sample_html():
    return """
        <div style="border:2px; border-style:solid; border-color:#000000; padding: 1em; margin-bottom: 1em">
            <h3>Print Site Page</h3>
            <p>First example with text surrounded by a red border. This example also has multiple lines.</p>
        </div>
        <ul>
        <li><a href="a/">page a</a></li>
        <li><a href="z/">page z</a></li>
        <li><a class="bla" style="color: #132" href="page.html#anchor">anchor on page</a></li>
        </ul>
        <p>text</p>
        <h1 id="z">Z</h1>
        <p>text</p>
        <h1 id="a">A</h1>
        <p>text</p>
        <h2 id="sub-one">sub one</h2>
        <p>text</p>
        <h2 id="sub-two">sub two</h2>
        """
