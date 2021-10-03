# KalaShop

## Project Summary

The website displays products. Users can add and remove products to/from their cart while also specifying the quantity of each item. They can then enter their address and choose Stripe to handle the payment processing.

[![alt text](https://justdjango.s3-us-west-2.amazonaws.com/media/thumbnails/djecommerce.png "Logo")](https://youtu.be/z4USlooVXG0)

---

## Running this project

Clone or download this repository and open it in your editor of choice.

```
# clone the repository
$ git clone https://github.com/sajjadzoghi/kalashop.git
$ cd kalashop
```

To get this project up and running you should start by having Python installed on your computer. It's advised you create a virtual environment to store your projects dependencies separately.

Create a virtualenv and activate it with these commands on mac/linux terminal:

```
$ python3 -m venv venv
$ . venv/bin/activate
```

Or these commands on Windows cmd:

```
$ py -3 -m venv venv
$ venv\Scripts\activate
```

That will create a new folder `venv` in your project directory. Next, install the project dependencies with:

```
pip install -r requirements.txt
```

Now you can run the project with this command:

```
python manage.py runserver
```
