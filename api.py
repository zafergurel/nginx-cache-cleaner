from flask import stream_with_context, Flask, request, Response, render_template
import os, signal, subprocess, argparse, time, re

app = Flask(__name__)
xstr = lambda s: s or ""

@app.route('/purge', methods=["POST"])
def purge():
    keyword = xstr(request.form.get("keyword"))
    cache_index_file = xstr(request.form.get("cache_index_file"))

    if cache_index_file == '' or keyword == '':
        return Response("error: invalid-parameter", mimetype='text/plain')
    elif cache_index_file == "perculus" and len(keyword) < 3:
        return Response("error: keyword-min-3-char", mimetype='text/plain')

    output, error = subprocess.Popen(["bin/purge_cache.sh", keyword, cache_index_file], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    output_text = output.decode()
    output_text = str.strip(output_text)

    error_text = error.decode() if error else ""
    error_text = str.strip(error_text)

    return Response(output_text + "\n\n" + error_text, mimetype='text/plain')

@app.route('/inspect', methods=["POST"])
def inspect():
    keyword = xstr(request.form.get("keyword"))
    cache_index_file = xstr(request.form.get("cache_index_file"))

    if cache_index_file == '' or keyword == '':
        return Response("error: invalid-parameter", mimetype='text/plain')

    output, error = subprocess.Popen(["bin/search_index.sh", keyword, cache_index_file], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    output_text = output.decode()
    error_text = error.decode if error else ""

    return Response(output_text + "\n\n" + error_text, mimetype='text/plain')

@app.route('/cleaner')
def clean_cache_page():
    index_folder = "/cache/_cacheindex"
    index_files = []
    for f in os.listdir(index_folder):
        index_files.append(index_folder + "/" + f)
    return render_template("clean-cache.html", index_files=index_files)
    

if __name__ == "__main__":
    pid = os.getpid()
    with open("api.pid", "w") as pid_file:
        pid_file.write(str(pid))
    app.run(host='0.0.0.0', port=8000)