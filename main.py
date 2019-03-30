import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY').encode()


@app.route('/')
def home():
    return render_template('home.jinja2')


@app.route('/add_donation/', methods=['GET', 'POST'])
def add():

    donor_list = Donor.select()

    if request.method == 'POST':
        try:
            # donor_name = Donor.select().where(Donor.name == request.form['don_name_list']).get()
            donor_id = str(request.form['don_name_list'])
            amount = str(request.form['don_amt'])

            new_donation = Donation(value=amount, donor=donor_id)
            new_donation.save()

            return redirect(url_for('home'))

        except Exception as e:
            return render_template('add_donation.jinja2',
                                   error="Please select a valid donor and donation amount,\
                                          then try again!",
                                   donors=donor_list)

    else:
        return render_template('add_donation.jinja2', donors=donor_list)


@app.route('/add_donor/', methods=['GET', 'POST'])
def new_donor():

    donor_list = Donor.select()

    if request.method == 'POST':
        try:
            donor_name = str(request.form['donor_name'])

            new_donor = Donor(name=donor_name)
            new_donor.save()

            return redirect(url_for('add'))

        except Exception as e:
            return render_template('add_donor.jinja2',
                                   error="Please enter a valid donor name, \
                                          then try again!",
                                   donors=donor_list)

    else:
        return render_template('add_donor.jinja2', donors=donor_list)


@app.route('/donations/', methods=['GET', 'POST'])
def all():

    donor_list = Donor.select()
    donations = Donation.select()

    if request.method == 'POST':
        try:
            donor_name = str(request.form['don_name_list'])

            if(donor_name == '*'):
                return render_template('donations.jinja2', donors=donor_list, donations=donations)
            else:
                filt_donations = Donation.select().where(Donation.donor == donor_name)
                return render_template('donations.jinja2',
                                       donors=donor_list,
                                       donations=filt_donations)

        except Exception as e:
            return render_template('donations.jinja2',
                                   error="Please try again!",
                                   donors=donor_list,
                                   donations=donations)
    else:
        return render_template('donations.jinja2', donors=donor_list, donations=donations)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)
