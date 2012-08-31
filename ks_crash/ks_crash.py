import os
import json

from flask import Flask, jsonify
from flask import render_template, redirect, url_for, request

from gevent.pywsgi import WSGIServer
from juggernaut import Juggernaut

from models.report import Report

def create_app():
    return Flask(__name__)

app = create_app()
app.debug = True
app.config.from_pyfile("config.py")

jug = Juggernaut()

@app.route('/')
def index():
    return render_template('reports.html')

@app.route('/api/crashes/', methods=['POST'])
def crashes():
    if request.method == 'POST':
        json_file = request.files['reports']
        reports = json.loads(json_file.read())
        for report_dict in reports:
            crash_id = report_dict['crash_id']
            if Report.get(crash_id) is None:
                report = Report(crash_id, report_dict)
                report.save()
                jug.publish('report-channel', report.__dict__)
        return jsonify(success=True)
    return redirect(url_for('index'))

@app.route('/api/reports.json', methods=['GET'])
def reports():
    reports = Report.all()
    reports = [report.__dict__ for report in reports]
    return jsonify(reports=reports)

@app.route('/api/reports/<crash_id>.json', methods=['GET'])
def report(crash_id):
    report = Report.get(crash_id)
    return jsonify(report=report.__dict__)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    http_server = WSGIServer(('', port), app)
    http_server.serve_forever()
