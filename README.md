<h1> Quiz Master - V1 by Arnav Labhasetwar (24F2006003) </h1>

<h2>About</h2>
<p>Quiz Master is a web app for creating and taking quizzes. It has two roles: Admin and User. Admin manages subjects, chapters, quizzes, and questions. Users register, log in, take quizzes, and view scores.</p>

<h2>Features</h2>
<ul>
    <li>Admin: Log in, create/edit/delete subjects, chapters, quizzes, and questions. View user details.</li>
    <li>User: Register, log in, choose quizzes, take tests, see scores.</li>
    <li>Uses Flask, Jinja2, HTML, CSS, Bootstrap, and SQLite.</li>
</ul>

<h2>How to Run</h2>
<ol>
    <li>Install Python.</li>
    <li>Install required libraries: <code>pip install flask matplotlib flask_sqlalchemy</code>.</li>
    <li>Run the app: <code>python app.py</code>.</li>
    <li>Open in browser: <a href="http://localhost:5000">http://localhost:5000</a> or <a href="http://127.0.0.1:5000">http://127.0.0.1:5000</a>.</li>
</ol>

<h2>Folder Structure</h2>
<ul>
    <li><code>app.py</code>: Main app file.</li>
    <li><code>templates/</code>: HTML files for front-end.</li>
    <li><code>static/</code>: CSS and other files.</li>
    <li><code>quiz_master_v1.sqlite3</code>: SQLite database.</li>
</ul>

<h2>Notes</h2>
<ul>
    <li>Admin account is pre-made in the database.</li>
    <li>Database is created by code, not manually.</li>
    <li>If required, install datetime (usually built into Python).</li>
</ul>