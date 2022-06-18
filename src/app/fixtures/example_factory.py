from collections import OrderedDict
from factory import Faker, SubFactory, Dict, post_generation
from factory.django import DjangoModelFactory
from django.utils.timezone import get_current_timezone
from app.models import Example, Attachment, Tag
from .project_factory import ProjectFactory


class AttachmentFactory(DjangoModelFactory):
    class Meta:
        model = Attachment

    type = Attachment.Type.image
    url = Faker(
        "random_element",
        elements=[
            "https://img.freepik.com/free-vector/hot-dog-cartoon-mascot-with-thumbs-up-character-design-vector-illustration_509778-109.jpg",
            "https://thumbs.dreamstime.com/z/classic-hotdog-isolated-white-background-fast-food-vector-object-big-hot-dog-cartoon-illustration-takeaway-symbol-banner-180303628.jpg",
            "http://clipart-library.com/images/5TRKkABac.png",
            "http://clipart-library.com/images/8cA67a9Ri.png",
            "http://clipart-library.com/images/ziXeXgM5T.jpg",
            "https://image.shutterstock.com/image-illustration/hotdog-clip-art-illustration-design-600w-1483817354.jpg",
            "https://image.shutterstock.com/image-illustration/juicy-hamburger-illustration-design-clip-600w-1487402342.jpg",
            "https://image.shutterstock.com/image-vector/hamburger-meat-lettuce-cheese-tomato-600w-499339315.jpg",
            "https://i.pinimg.com/564x/58/71/50/5871504d228189e217d3b02185841bda.jpg",
            "https://www.nicepng.com/png/full/398-3983609_british-street-food-cartoon-hot-dog.png",
            "https://as1.ftcdn.net/v2/jpg/01/72/54/32/1000_F_172543229_oNco9N2Y7NSYaB42u5CzGqkiyrWaktNO.jpg",
            "https://cliparting.com/wp-content/uploads/2016/09/Cartoon-hot-dog-clipart-kid.png",
            "https://i.pinimg.com/564x/58/71/50/5871504d228189e217d3b02185841bda.jpg",
        ],
    )


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    key = Faker("random_element", elements=["device.os", "make", "model"])
    value = Faker(
        "random_element",
        elements=OrderedDict(
            [
                ("red", 0.45),
                ("blue", 0.35),
                ("green", 0.15),
                ("yellow", 0.05),
            ]
        ),
    )


class ExampleFactory(DjangoModelFactory):
    class Meta:
        model = Example

    project = SubFactory(ProjectFactory)
    issue = None
    created_at = Faker(
        "date_time_between",
        start_date="-90d",
        end_date="now",
        tzinfo=get_current_timezone(),
    )
    predictions = Dict(
        {
            "label": Faker("random_element", elements=["Hotdog", "Not hotdog"]),
            "score": Faker("pyfloat", min_value=0, max_value=1),
            "choices": ["Hotdog", "Not hotdog"],
        }
    )
    annotations = Dict(
        {
            "label": Faker("random_element", elements=["Hotdog", "Not hotdog"]),
            "choices": ["Hotdog", "Not hotdog"],
        }
    )
    metadata = {"a": "b"}

    @post_generation
    def attachments(obj, create, extracted, **kwargs):
        """
        If called like: ExampleFactory(attachments=4) it generates an Example with 4
        attachments. If called without `attachments` argument, it generates a
        single attachment for this example
        """
        if not create:
            return

        if extracted:
            for n in range(extracted):
                AttachmentFactory.create(example=obj)
        else:
            AttachmentFactory.create(example=obj)

    @post_generation
    def tags(obj, create, extracted, **kwargs):
        """
        If called like: ExampleFactory(tags=4) it generates an Example with 4
        tags. If called without `tags` argument, it generates a single tag for this example
        """
        if not create:
            return

        if extracted:
            for n in range(extracted):
                TagFactory.create(example=obj)
        else:
            TagFactory.create(example=obj)
