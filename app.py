import os
from dotenv import load_dotenv
from flask_cors import CORS
from cms import get_cms_content, format_cms_image
from spotify import write_recent_albums, load_recent_albums, format_song_name
from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__, static_folder="./static", static_url_path="/")
CORS(app)
load_dotenv()
if os.getenv("ENVIRONMENT") != "DEV":
    write_recent_albums()

app.jinja_env.globals.update(format_cms_image=format_cms_image)
app.jinja_env.globals.update(format_song_name=format_song_name)

sched = BackgroundScheduler(daemon=True)
sched.add_job(write_recent_albums,'interval', minutes=120)
sched.start()


@app.route("/")
def index():
    cms_data = get_cms_content()
    recent_albums = load_recent_albums()
    
    featured_album_list = [album for album in recent_albums if album["id"] == cms_data["featured_song_id"]]
    featured_album = featured_album_list[0] if featured_album_list else None
    recent_albums.remove(featured_album)

    return render_template(
        "index.html", 
        cms_data=cms_data, 
        featured_album=featured_album, 
        recent_albums=recent_albums
    )