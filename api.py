'''Nginx Cache Cleaner API
A small project to make it easy to find (and purge)
cached files on an Nginx server.
'''
from flask import stream_with_context, Flask, request, Response, render_template
import os, signal, subprocess, argparse, time, re

app = Flask(__name__)
xstr = lambda s: s or ""
current_dir = os.path.dirname(os.path.realpath(__file__))
get_path = lambda p: os.path.join(current_dir, (p or ""))

@app.route('/cache-cleaner/purge', methods=["POST"])
def purge():
    '''The endpoint to find entries in an index file,
    then delete the corresponding cached files and removing
    those entries from the index.
    '''
    keyword = xstr(request.form.get("keyword"))
    cache_index_file = xstr(request.form.get("cache_index_file"))

    if cache_index_file == '' or keyword == '':
        return Response("error: invalid-parameter", mimetype='text/plain')

    output, error = subprocess.Popen([get_path("bin/purge_cache.sh"), keyword, cache_index_file], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    output_text = output.decode()
    output_text = str.strip(output_text)

    error_text = error.decode() if error else ""
    error_text = str.strip(error_text)

    return Response(output_text + "\n\n" + error_text, mimetype='text/plain')

@app.route('/cache-cleaner/inspect', methods=["POST"])
def inspect():
    '''The endpoint to find entries in an index file
    '''
    keyword = xstr(request.form.get("keyword"))
    cache_index_file = xstr(request.form.get("cache_index_file"))

    if cache_index_file == '' or keyword == '':
        return Response("error: invalid-parameter", mimetype='text/plain')

    output, error = subprocess.Popen([get_path("bin/search_index.sh"), keyword, cache_index_file], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    output_text = output.decode()
    error_text = error.decode if error else ""

    return Response(output_text + "\n\n" + error_text, mimetype='text/plain')

@app.route('/cache-cleaner/form')
@app.route('/cache-cleaner/')
@app.route('/cache-cleaner')
def clean_cache_page():
    '''Renders clean-cache.html template
    '''
    index_folder = "/cache/_cacheindex"
    index_files = []
    for f in os.listdir(index_folder):
        index_files.append(index_folder + "/" + f)
    index_files = sorted(index_files)
    return render_template("clean-cache.html", index_files=index_files)


if __name__ == "__main__":
    pid = os.getpid()
    with open("api.pid", "w") as pid_file:
        pid_file.write(str(pid))
    app.run(host='0.0.0.0', port=8000)