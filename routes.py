import os
from PIL import Image

from flask import render_template, redirect, url_for, request

from app import app, db
from forms import CategoryForm, SheetsForm
from models import Category, Sheet


def upload_image(request, category):
    file = request.files['logo']
    path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(path)
    category.logo = file.filename
    db.session.add(category)
    db.session.commit()
    img = Image.open(path)
    img = img.resize((200, 200))
    img.save(path)


@app.route('/')
def index():
    categories = Category.query.all()
    return render_template('index.html', object_list=categories)


@app.route('/cat/<int:cat_id>')
def cat_sheets(cat_id):
    sheets = Sheet.query.filter(Sheet.category_id == cat_id).all()
    category = Category.query.get(cat_id)
    return render_template('sheets.html', object_list=sheets, category=category)


@app.route('/cat/add', methods=['GET', 'POST'])
def add_cat():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data, is_published=form.is_published.data)
        db.session.add(category)
        db.session.commit()
        if request.files['logo'].filename != '':
            upload_image(request, category)
        return redirect(url_for('index'))
    return render_template('add_cat.html', form=form)


@app.route('/sheet/add', methods=['GET', 'POST'])
def add_sheet():
    form = SheetsForm()
    form.category_id.choices = [(c.id, c.name) for c in db.session.query(Category).all()]
    if form.validate_on_submit():
        sheet = Sheet(
            title=form.title.data,
            text=form.text.data,
            is_published=form.is_published.data,
            category_id=form.category_id.data
        )
        db.session.add(sheet)
        db.session.commit()
        return redirect(url_for('cat_sheets', cat_id=sheet.category_id))
    return render_template('add_sheet.html', form=form)


@app.route('/cat/<int:cat_id>/edit', methods=['GET', 'POST'])
def edit_cat(cat_id):
    res = Category.query.get(cat_id)
    form = CategoryForm(name=res.name, is_published=res.is_published)
    if form.validate_on_submit():
        res.name = form.name.data
        res.is_published = form.is_published.data
        db.session.add(res)
        db.session.commit()
        if request.files['logo'].filename != '':
            upload_image(request, res)
        return redirect(url_for('index'))
    return render_template('add_cat.html', form=form)


@app.route('/cat/<int:cat_id>/delete')
def delete_cat(cat_id):
    res = Category.query.get(cat_id)
    db.session.delete(res)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/sheet/<int:sheet_id>/edit', methods=['GET', 'POST'])
def edit_sheet(sheet_id):
    res = Sheet.query.get(sheet_id)
    form = SheetsForm(
        title=res.title,
        text=res.text,
        category_id=res.category_id,
        is_published=res.is_published
    )
    form.category_id.choices = [(c.id, c.name) for c in db.session.query(Category).all()]
    if form.validate_on_submit():
        res.title = form.title.data
        res.text = form.text.data
        res.is_published = form.is_published.data
        res.category_id = form.category_id.data
        db.session.add(res)
        db.session.commit()
        return redirect(url_for('cat_sheets', cat_id=res.category_id))
    return render_template('add_sheet.html', form=form)


@app.route('/sheet/<int:sheet_id>/delete')
def delete_sheet(sheet_id):
    res = Sheet.query.get(sheet_id)
    db.session.delete(res)
    db.session.commit()
    return redirect(url_for('cat_sheets', cat_id=res.category_id))


if __name__ == '__main__':
    app.run(debug=True)
