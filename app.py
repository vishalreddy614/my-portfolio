"""
=============================================================================
Minimalist Cybersecurity & Systems Research Portfolio Backend (Flask)
=============================================================================
This Flask backend serves the editorial cybersecurity portfolio webpage,
processes direct contact form inquiries via standard HTTP POST, and delivers
the resume/curriculum vitae download.

Architecture:
- Strict zero-JavaScript architecture.
- Single-page application rendered via server-side Jinja2 templating.
- Validated POST request parsing with structured console logging.
- Safe local file delivery via Flask's 'send_file'.
=============================================================================
"""

import os
from flask import Flask, render_template, request, send_file, redirect, url_for

# Initialize the Flask application
app = Flask(__name__)

# Secret key used for session security
app.secret_key = "cybersec_portfolio_minimalist_secret_key"


@app.route("/", methods=["GET"])
def home():
    """
    Primary Portfolio Route:
    Loads and renders the editorial portfolio (templates/index.html).
    """
    return render_template("index.html", message_sent=False)


@app.route("/contact", methods=["POST"])
def contact():
    """
    Contact Form Route:
    Receives contact form submissions via standard HTTP POST without JavaScript.
    Captures sender metadata, logs it to stdout, and renders confirmation.
    """
    sender_name = request.form.get("name", "").strip()
    sender_email = request.form.get("email", "").strip()
    subject = request.form.get("subject", "").strip()
    message = request.form.get("message", "").strip()

    # Formatted terminal telemetry
    print("\n" + "=" * 65)
    print("[+] [CONTACT INQUIRY RECEIVED]")
    print(f"[+] SENDER   : {sender_name} <{sender_email}>")
    print(f"[+] SUBJECT  : {subject}")
    print(f"[+] MESSAGE  : {message}")
    print(f"[+] STATUS   : Acknowledged & logged to server stdout")
    print("=" * 65 + "\n")

    return render_template(
        "index.html",
        message_sent=True,
        sender_name=sender_name
    )


@app.route("/download-resume", methods=["GET"])
def download_resume():
    """
    Resume Download Route:
    Delivers the operator's resume directly as an attachment.
    Prioritizes 'resume.pdf' if uploaded to the project root,
    otherwise falls back to 'sample_resume.txt'.
    """
    pdf_resume_path = os.path.join(os.path.dirname(__file__), "resume.pdf")
    txt_resume_path = os.path.join(os.path.dirname(__file__), "sample_resume.txt")

    if os.path.exists(pdf_resume_path):
        file_to_send = pdf_resume_path
        download_name = "Resume_K_Vishal_Reddy.pdf"
    elif os.path.exists(txt_resume_path):
        file_to_send = txt_resume_path
        download_name = "Resume_K_Vishal_Reddy.txt"
    else:
        return "Error 404: Resume file not found on host system.", 404

    return send_file(
        file_to_send,
        as_attachment=True,
        download_name=download_name
    )


if __name__ == "__main__":
    print("[*] Launching Minimalist Cybersecurity Portfolio...")
    print("[*] Host listening at: http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)
