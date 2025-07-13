from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required

from .forms import ContactForms
from .models import Contact
from . import db


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    
    if current_user.is_authenticated:
        contacts = Contact.query.filter_by(user_id=current_user.id).all()
        print("contact:",contacts)
        
    return render_template('home.html', user=current_user, contacts=contacts)

#contact page
@views.route('/contacts' , methods=['GET', 'POST'])
@login_required
def contacts():
    contacts = Contact.query.filter_by(user_id=current_user.id).all()
    if not contacts:
        flash("No contacts found", category="info")
        return redirect(url_for('views.home'))
    
    if request.method == 'POST':
        search = request.form.get('search')
        if search:
            contacts = Contact.query.filter_by(user_id=current_user.id).filter(Contact.name.contains(search)).all()
            if not contacts:
                flash("No contacts found", category="info")
                return redirect(url_for('views.home'))
        else:
            contacts = Contact.query.filter_by(user_id=current_user.id).all()
    else:
        contacts = Contact.query.filter_by(user_id=current_user.id).all()

    return render_template('contacts.html', contacts=contacts)



#add contact
@views.route('/add', methods=['GET', 'POST'])
@login_required
def add_contact():
    form = ContactForms()
    if form.validate_on_submit():
        new_contact = Contact(
            name=form.name.data,
            date=form.date.data,
            user_id=current_user.id
        )

        db.session.add(new_contact)
        db.session.commit()

        flash("Contact added successfully!", category="success")
        return redirect(url_for('views.home')) # back to home page
    return render_template('add_contact.html', form=form)


#edit contact
@views.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_contact(id):
    contact = Contact.query.get_or_404(id)

    # if contact.user_id != current_user.id:
    #     flash("You are not authorized to edit this contact", category="error")
    #     return redirect(url_for('views.home'))
    
    form = ContactForms(obj=contact)
    if form.validate_on_submit():
        contact.name = form.name.data
        contact.date = form.date.data

        db.session.commit()

        flash("Contact updated successfully!", category="success")
        return redirect(url_for('views.home')) # back to home page
    elif request.method == 'GET':
        form.name.data = contact.name
        form.date.data = contact.date
    else:
        flash("Error updating contact", category="error")
        return redirect(url_for('views.home'))
    
    return render_template('edit_contact.html', form=form, contact=contact)

#delete contact
@views.route('/delete/<int:id>')
@login_required
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    # if contact.user_id != current_user.id:
    #     flash("You are not authorized to delete this contact", category="error")
    #     return redirect(url_for(''))
    
    db.session.delete(contact)
    db.session.commit()
    flash(f"Contact'{contact.name}' has been deleted", category="success")
    return redirect(url_for('views.home'))
