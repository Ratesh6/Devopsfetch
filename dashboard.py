import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
import urllib.parse

PORT = 9090

# Full paths to your log files
LOG_FILES = {
    "DevOps Fetch Log": "/var/log/devopsfetch/devopsfetch.log",
    "DevOps Fetch Error": "/var/log/devopsfetch/devopsfetch.err",
    "Nginx Access Log": "/mnt/c/Users/Lenovo/Devops_fetch/nginx.log",
    "Nginx Error Log": "/mnt/c/Users/Lenovo/Devops_fetch/nginx_error.log",
    "Docker Log": "/mnt/c/Users/Lenovo/Devops_fetch/docker.log"
}

class DashboardHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse ?file=<filename> parameter
        parsed_path = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed_path.query)
        selected_log = query.get('file', [list(LOG_FILES.keys())[0]])[0]

        # Build sidebar
        sidebar = "<ul>"
        for name in LOG_FILES:
            sidebar += f'<li><a href="/?file={name}">{name}</a></li>'
        sidebar += "</ul>"

        # Read the selected log file
        file_path = LOG_FILES.get(selected_log, "")
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    log_content = f.read()
            except PermissionError:
                log_content = "Permission denied: cannot read this log file."
        else:
            log_content = "Log file not found or empty."

        # Build HTML
        html = f"""
        <html>
        <head>
            <title>DevOps Logs Dashboard</title>
            <meta http-equiv="refresh" content="5">
            <style>
                body {{ font-family: monospace; display: flex; background: #1e1e1e; color: #d4d4d4; }}
                #sidebar {{ width: 220px; padding: 20px; background: #2e2e2e; }}
                #content {{ flex-grow: 1; padding: 20px; overflow-x: auto; }}
                a {{ color: #61dafb; text-decoration: none; }}
                a:hover {{ text-decoration: underline; }}
                pre {{ white-space: pre-wrap; word-wrap: break-word; }}
                h1 {{ color: #61dafb; }}
                ul {{ list-style-type: none; padding: 0; }}
                li {{ margin-bottom: 10px; }}
            </style>
        </head>
        <body>
            <div id="sidebar">
                <h2>Logs</h2>
                {sidebar}
            </div>
            <div id="content">
                <h1>{selected_log}</h1>
                <pre>{log_content}</pre>
            </div>
        </body>
        </html>
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

# Start HTTP server
with HTTPServer(("", PORT), DashboardHandler) as httpd:
    print(f"Dashboard running at http://127.0.0.1:{PORT}")
    httpd.serve_forever()
