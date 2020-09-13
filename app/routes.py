import uuid
import datetime
from flask import render_template, redirect, url_for
from app.models import Paste
from app.forms import PasteForm
from app import app, db, scheduler


def paste_delete():
    current_time = datetime.datetime.utcnow()
    paste = Paste.query.filter(current_time >= Paste.expire_time).delete()
    db.session.commit()


def paste_scheduler():
    delete_paste_scheduler = scheduler.add_job(paste_delete, 'interval', minutes = 10)
    scheduler.start()


paste_scheduler()


@app.route("/", methods=['GET', 'POST'])
def index():
    form = PasteForm()
    if form.validate_on_submit():
        url_uuid = uuid.uuid4()
        paste_time = datetime.datetime.utcnow()
        expire_time = paste_time + datetime.timedelta(minutes = 10)
        paste = Paste(content = form.content.data, uuid = url_uuid.hex, paste_time = paste_time, expire_time = expire_time)
        db.session.add(paste)
        db.session.commit()
        return redirect(url_for('paste', uuid = paste.uuid))
    return render_template('index.html', form=form)


@app.route("/<string:uuid>", methods=['GET'])
def paste(uuid):
    paste = Paste.query.filter_by(uuid = uuid).first_or_404()
    if datetime.datetime.utcnow() <= paste.expire_time:
        return render_template('paste.html', paste=paste)
    else:
        return redirect(url_for('404'))


@app.route("/about")
def about():
    return render_template('about.html')