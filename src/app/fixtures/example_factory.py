from factory import Faker
from factory.django import DjangoModelFactory
from django.utils.timezone import get_current_timezone
from app.models import Example, Issue, Project


class ExampleFactory(DjangoModelFactory):
    class Meta:
        model = Example

    def __init__(self, project: Project, issue: Issue):
        self.project = project
        self.issue = issue

    created_at = Faker(
        "date_time_between",
        start_date="-90d",
        end_date="now",
        tzinfo=get_current_timezone(),
    )
    media_url = Faker(
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
