# Udacity - Item catalog app
This repo contains the *Item catalog app*. It's a RESTful website built using the `Flask framework` in Python, `SQLite` as the database, `Bootstrap` for styling and `OAuth 2.0` (Google sign in) for user authentication. Unauthenticated users can view a catalog consisting of categories and items, while users authenticated using Google sign in can perform CRUD operations on both categories and items. The website also exposes two JSON routes that serve JSON-ified category and item data.

## System requirements:
* Python2.7
* Vagrant
* VirtualBox

## Prerequisites:
1. Execute the following commands in your terminal:
```bash
git clone https://github.com/air-walk/udacity-item-catalog-app.git
cd udacity-item-catalog-app/vagrant
vagrant up
vagrant ssh
```
You should now be logged into the VM managed by Vagrant.

## Steps:
1. Execute the following commands inside the VM managed by Vagrant:
```bash
cd /vagrant/catalog
touch client_secrets.json
```
2. Place the contents of `client_secrets.json` shared to you via Udacity's project submission form into the `client_secrets.json` file here.
3. Execute the following command to start the webserver on port `8000`:
```bash
python application.py
```
4. Open a web browser of your choice on your host machine (not in the VM) and navigate to `http://localhost:8000` to view the *Item catalog app*.

## General details about the *Item catalog app*:
* A catalog consists of categories and their asscociated items.
* When a user navigates to the site for the first time, he/she can see all categories in the database. On first time setup, since the database is empty, the page won't show any results.
* Authenticate to the site using the `Login` button on top-right corner of the navbar. Sign in with Google.
* On successful authentication, you'll be redirected to home page, but will now be able to perform CRUD operations on categories as well as items. Also, since you're logged in, the `Login` button in the top-right corner of the navbar will now have changed to `Logout` instead.
* Play around with the site and create a couple categories (and some associated items for those categories).
* Click on `Logout` to log yourself out of the site. You'll be automatically redirected to the home page once you do that.
* If you'd like to access JSON-ified category and item data, that'd be available on routes `/categories.json` (or `/catalog.json`) and `/catalog/<id for a category>.json` (or `/categories/<id for a category>.json`) respectively (replace `<id for a category>` with the `id` of a category whose items you'd like to view).
