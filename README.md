# WIP: Sync
A simple application to fetch top songs by the artist using flask redis and celery queues.

![sync](https://user-images.githubusercontent.com/42143636/109423241-b7615800-7a04-11eb-8d3a-f1541b4523ad.PNG)

Installation   
------------
```
$ git clone https://github.com/vsvinav/sync.git
$ cd sync
$ pip3 install -r requirements.txt
```

Usage   
-----
Run the web server : `$ python3 app.py`

Run the celery backend: `$ celery -A app.celery worker --loglevel=INFO`
