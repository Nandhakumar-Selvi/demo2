from flask import Flask, request, render_template_string

# Create the Flask web application
app = Flask(__name__)

# --- VULNERABILITY 2: Hardcoded Secret ---
# This fake AWS key will be detected by GitHub's Secret Scanner.
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE" 

# This is the HTML template for our page.
# It contains the Cross-Site Scripting (XSS) vulnerability.
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Vulnerable Guestbook</title>
</head>
<body>
    <h1>Welcome to the Guestbook!</h1>
    
    <!-- 
        VULNERABILITY 3 & 4: Cross-Site Scripting (XSS)
        The 'name' variable is printed directly to the page without being sanitized.
        This allows an attacker to inject HTML or JavaScript code.
        This will be found by CodeQL (SAST) and OWASP ZAP (DAST).
    -->
    <h2>Hello, {{ name }}!</h2>

    <p>Try visiting this page with a query parameter in the URL, like:</p>
    <code>/?name=YourName</code>
    
    <p>To see the vulnerability, try this URL:</p>
    <code>/?name=&lt;script&gt;alert('You were hacked!');&lt;/script&gt;</code>

    <hr>
    <p>Secret key found in code: {{ aws_key }}</p>

</body>
</html>
"""

@app.route('/')
def home():
    # Get the 'name' from the URL query parameter. Default to "Guest".
    name_from_url = request.args.get('name', 'Guest')
    
    # Render the template, passing the name and the secret key to it.
    return render_template_string(HTML_TEMPLATE, name=name_from_url, aws_key=AWS_ACCESS_KEY)

# This allows the app to be run directly using "python app.py"
if __name__ == '__main__':
    app.run(debug=True)
