# Ecommerce Auctions Site

This is an ecommerce auctions site that allows users to create, bid on, and comment on auction listings. The site is built with Django, Bootstrap and SQLite.

## Features

- Users can register and login to the site with their username and password.
- Users can create new auction listings with a title, description, starting bid, category, and optional image URL.
- Users can view all active listings on the homepage.
- Users can view the details of a listing, including the current highest bid.
- Users can place a bid on a listing if their bid is higher than the current highest bid.
- Users can add a listing to their watchlist or remove it from their watchlist.
- Users can leave comments on a listing and view other comments.
- Users can close a listing if they are the owner of the listing. The highest bidder will win the auction.

## Installation

To run this project locally, follow these steps:

1. Clone this repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt` in the project directory.
3. Run the migrations by running `python manage.py makemigrations` and `python manage.py migrate` in the project directory.
4. Create an admin user to access the Django admin interface by running `python manage.py createsuperuser` in the project directory and following the prompts.
5. Run the server by running `python manage.py runserver` in the project directory.
6. Go to [http://127.0.0.1:8000/](^1^) to view the site.


## This is project 2 from CS50 course from Harvard

## License

This project is licensed under the MIT License. See the [LICENSE](^2^) file for more details.
