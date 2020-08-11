from io import BytesIO
import json
import random
from faker import Faker
from PIL import Image, ImageDraw
from django.core.management.base import BaseCommand
from django.core.files.images import ImageFile
from home.models import HomePage
from fakenews.models import FakeNewsIndexPage, FakeNewsPage
from wagtail.images.models import Image as WagtailImage


class Command(BaseCommand):
    help = "Create fake pages and associated images"

    def add_arguments(self, parser):
        # use 0 for deletion only
        parser.add_argument(
            "number", nargs="+", type=int, help="Number of items to create"
        )
        # optionally keep pages, defaults to false
        parser.add_argument(
            "-kp",
            "--keep_pages",
            action="store_true",
            help="Keep existing fake pages instead of deleting them",
        )
        # optionally keep images, defaults to false
        parser.add_argument(
            "-ki",
            "--keep_images",
            action="store_true",
            help="Keep existing fake images instead of deleting them",
        )

    def streamfield(self, fake):
        # create a streamfield containing paragraphs and headings
        blocks = []
        for _ in range(random.randrange(3, 5)):
            heading = fake.sentence()[0:-1]
            blocks.append({u"type": u"heading", u"value": heading})
            paragraphs = []
            for _ in range(random.randrange(2, 4)):
                sentences = []
                for _ in range(random.randrange(3, 6)):
                    sentence = fake.sentence(nb_words=random.randrange(7, 17))
                    sentences.append(sentence)
                paragraphs.append(" ".join(sentences))
            paragraph_block = "<p>" + "</p><p>".join(paragraphs) + "</p>"
            blocks.append({u"type": u"paragraph", u"value": paragraph_block})
        return json.dumps(blocks)

    def create_image(self, text):
        # create a Wagtail image with a random coloured background
        # and a text overlay
        colours = tuple(random.sample(range(255), 3))
        image = Image.new("RGB", (600, 400), color=colours)
        d = ImageDraw.Draw(image)
        d.text((10, 10), text, fill=(255, 255, 255))
        f = BytesIO()
        image.save(f, format="png")
        filename = text.replace(" ", "-").lower() + "-%s-%s-%s.fake" % colours
        wagtail_image = WagtailImage(title=text, file=ImageFile(f, name=filename))
        wagtail_image.save()
        return wagtail_image

    def handle(self, *args, **options):
        if not options["keep_pages"]:
            print("deleting existing fake pages")
            for page in FakeNewsPage.objects.all():
                print("deleting page " + page.title)
                page.delete()
        if not options["keep_images"]:
            print("deleting existing fake images")
            for image in WagtailImage.objects.all():
                image_filename = image.filename
                if image_filename.endswith(".fake"):
                    print("deleting image " + image_filename)
                    image.delete()
        # find the first fake index page, or try to create one
        # under the first home page
        try:
            fake_index_page = FakeNewsIndexPage.objects.all()[0]
        except IndexError:
            home_page = HomePage.objects.all()[0]
            fake_index_page = FakeNewsIndexPage(title="Fake news index")
            home_page.add_child(instance=fake_index_page)
            fake_index_page.save_revision()
        # create fake pages
        fake = Faker()
        number_to_create = options["number"][0]
        for _ in range(number_to_create):
            title = " ".join(fake.words(3)).title()
            fake_page = FakeNewsPage(
                title=title,
                year=fake.year(),
                author=fake.name(),
                introduction=fake.sentence(),
                body=self.streamfield(fake),
            )
            image = self.create_image(title)
            fake_page.image = image
            fake_index_page.add_child(instance=fake_page)
            fake_page.save_revision().publish()
            print("published fake page " + title)
