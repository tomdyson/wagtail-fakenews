# Wagtail Fake News

Create fake news for testing.

## Installation

1. `pip install git+git://github.com/tomdyson/wagtail-fakenews.git#egg=wagtail-fakenews`
2. Add `fakenews` to `INSTALLED_APPS`
3. `./manage.py migrate fakenews`

## Usage

Create a fake news index page in the Wagtail admin. Fake news items will be created as children of this page. If you have multiple fake news index pages, only the first one will be used. If there are no fake news index pages, `make_fake_items` will try to create one as a child of the first home page.

```bash
# delete existing fake pages and images, create 50 new pages and images
./manage.py make_fake_items 50
# delete existing fake pages
./manage.py make_fake_items 0
# keep existing fake pages and images, create 10 new pages and images
./manage.py make_fake_items --keep_pages --keep_images 10
```

## TODO

 - [x] REST API
 - [x] Simple page template
 - [x] Streamfield?
 - [ ] Publish to PyPi