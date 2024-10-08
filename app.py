from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///serdar_plastik_kılavuz.db'
db = SQLAlchemy(app)

class Title(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subtitles = db.relationship('Subtitle', backref='title', cascade="all, delete", lazy=True)

class Subtitle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=True)
    title_id = db.Column(db.Integer, db.ForeignKey('title.id'), nullable=False)

@app.route('/')
def index():
    titles = Title.query.all()
    return render_template('index.html', titles=titles)

@app.route('/view')
def view():
    titles = Title.query.all()
    return render_template('view.html', titles=titles)

@app.route('/content/<int:id>', methods=['GET'])
def content(id):
    subtitle = Subtitle.query.get(id)
    if subtitle:
        return jsonify({
            'id': subtitle.id,
            'name': subtitle.name,
            'content': subtitle.content
        })
    return jsonify({'error': 'Content not found'}), 404

@app.route('/edit_content/<int:id>', methods=['POST'])
def edit_content(id):
    subtitle = Subtitle.query.get(id)
    if subtitle:
        subtitle.content = request.form['content']
        db.session.commit()
        return redirect(url_for('index'))
    return "Content not found", 404

@app.route('/add_title', methods=['POST'])
def add_title():
    title_name = request.form['title_name']
    title = Title(name=title_name)
    db.session.add(title)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit_title/<int:id>', methods=['POST'])
def edit_title(id):
    title = Title.query.get(id)
    if title:
        title.name = request.form['title_name']
        db.session.commit()
        return redirect(url_for('index'))
    return "Title not found", 404

@app.route('/delete_title/<int:id>')
def delete_title(id):
    title = Title.query.get(id)
    if title:
        db.session.delete(title)
        db.session.commit()
        return redirect(url_for('index'))
    return "Title not found", 404

@app.route('/add_subtitle/<int:title_id>', methods=['POST'])
def add_subtitle(title_id):
    title = Title.query.get(title_id)
    if title:
        subtitle_name = request.form['subtitle_name']
        subtitle = Subtitle(name=subtitle_name, title_id=title_id)
        db.session.add(subtitle)
        db.session.commit()
        return redirect(url_for('index'))
    return "Title not found", 404

@app.route('/edit_subtitle/<int:id>', methods=['POST'])
def edit_subtitle(id):
    subtitle = Subtitle.query.get(id)
    if subtitle:
        subtitle.name = request.form['subtitle_name']
        db.session.commit()
        return redirect(url_for('index'))
    return "Subtitle not found", 404

@app.route('/delete_subtitle/<int:id>')
def delete_subtitle(id):
    subtitle = Subtitle.query.get(id)
    if subtitle:
        db.session.delete(subtitle)
        db.session.commit()
        return redirect(url_for('index'))
    return "Subtitle not found", 404



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
