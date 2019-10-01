# NGINX Cache Cleaner Tools
A small project to make it easy to find (and purge) cached files on an Nginx server.

## Introduction

Nginx caches files under a folder which is defined in the configuration file (nginx.conf).

In every cached file, the cache key, http request details, and the contents of the file are stored. 

To find a cached file, one can search every file by opening it, retrieving the cache key, and search for the occurrence of the keyword in that key. The problem with this approach that it takes time when there are lots of (thousands) files in the folder.

This project aims at solving this problem. To speed up finding and purging cached files. Basically, the solution is creating an index file for every cache folder. In this index file, the path of the cached file will be stored with its corresponding cache key. You can see an entry example as follows:

<pre>
...
/cache/mywebsite/8e979f71b247f19eba8ee545c75feb4c mywebsite.net/css/site.css
...
</pre>

## Creating Index Files

To create index files, create_indexes.py is used. In the file, change the base folder for the cache folders. The script will create index files for every folder under /cache folder on your system. An example cache folder structure may be as follows:

- /cache/mywebsite_static
- /cache/mywebsite_video
- /cache/anothersite_assets

After you run the following;

`python3 create_indexes.py create`

 the index files for each of the folders under /cache will be created under /cache/_cacheindex folder. For the above example, the index files would be as follows:

- /cache/_cacheindex/_cache_mywebsite_static.ind
- /cache/_cacheindex/_cache_mywebsite_video.ind
- /cache/_cacheindex/_cache_anothersite_assets.ind

`create_indexes.py` takes one argument which is the type of operation. It can be "create" or "append". The default value is "append". In the append mode, the script just adds entries for the newly (which means after the last modification time of the index file) cached files to the index file. In the create mode, the index files are created from scratch. So, it's reasonable to put a cron job, that runs this script with create argument every night and another one that runs the script every 3 minute with append argument. A sample cron definition is as follows:

<pre>
*/1 * * * * python3 /opt/nginx-cache-cleaner/create_indexes.py append
0 3 * * * python3 /opt/nginx-cache-cleaner/create_indexes.py create
</pre>

## Find and Purge
To find and purge files, api.py is used.

To use the api, run `python3 api.py`. You can then open http://localhost:8000/cache-cleaner on your browser to test the interface.

You can then add a location block to your nginx configuration as follows:

<pre>
location ~ ^/cache-cleaner {
    set $req_path $1;
    auth_basic "This is a password protected area!";
    auth_basic_user_file /usr/local/openresty/nginx/conf/.htpasswd;
    proxy_pass http://127.0.0.1:8000;
}
</pre>

You need to make api.py run all the time. This can be accomplished by running it on every system start-up. A good solution is to use a process control system like supervisord (http://supervisord.org/)

On the cache cleaner form, there are two fields: "Cache Key" and "Cache Section". Cache Key is looked up in the keys in the index files. You can use regular expression syntax. For example, to find keys ending with .jpg, you can enter `\.jpg$`.

Cache Section is the name of the index file which you select from the combo box.

If you press Query button, the entries in the index file will be displayed underneath. You can see the line numbers of the entries as well.

If you press Delete button, the cached files that are found are deleted and also the corresponding entries are removed from the index file.

## Installation
- Install python3 on your system.

- Clone the repository.

`git clone https://github.com/zafergurel/nginx-cache-cleaner/`

- Make the scripts under bin/ executable:

`
chmod +x bin/*.sh
`

- Run the following the create indexes:

`python3 create_indexes.py create`

- Add cron jobs to create indexes automatically.

<pre>
*/1 * * * * python3 /opt/nginx-cache-cleaner/create_indexes.py append
0 3 * * * python3 /opt/nginx-cache-cleaner/create_indexes.py create
</pre>

- Run the API:

`python3 api.py &`

- Configure Nginx to allow the cache cleaner form to accessed from outside:

<pre>
location ~ ^/cache-cleaner {
    set $req_path $1;
    auth_basic "This is a password protected area!";
    auth_basic_user_file /usr/local/openresty/nginx/conf/.htpasswd;
    proxy_pass http://127.0.0.1:8000;
}
</pre>