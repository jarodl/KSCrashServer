import os
import json

from flask import Flask
from flask import render_template, redirect, url_for, request
from models.report import Report

def create_app():
    return Flask(__name__)

app = create_app()
app.debug = True
app.config.from_pyfile("config.py")

@app.route('/')
def index():
    reports = Report.all()
    return render_template('index.html', reports=reports)

@app.route('/api/crashes/', methods=['POST'])
def crashes():
    if request.method == 'POST':
        json_file = request.files['reports']
        reports = json.loads(json_file.read())
        for report_dict in reports:
            crash_id = report_dict['crash_id']
            report = Report(crash_id, report_dict)
            report.save()
        return reports.__str__()
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
