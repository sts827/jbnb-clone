from django.core.management.base import BaseCommand
from rooms.models import Amenity

## fake Data를 만드는 클래스 입니다
class Command(BaseCommand):

    """ Command-class to Makes Fake Data """

    help = "This command creates amenities"

    def handle(self, *args, **options):
        # 편의시설: amenities
        amenties = [
            "Air conditioning",
            "Alarm Clock",
            "Balcony",
            "Bathroom",
            "Bathtub",
            "Bed Linen",
            "Boating",
            "Cable TV",
            "Carbon monoxide detectors",
            "Chairs",
            "Children Area",
            "Coffee Maker in Room",
            "Cooking hob",
            "Cookware & Kitchen Utensils",
            "Dishwasher",
            "Double bed",
            "En suite bathroom",
            "Free Parking",
            "Free Wireless Internet",
            "Freezer",
            "Fridge / Freezer",
            "Golf",
            "Hair Dryer",
            "Heating",
            "Hot tub",
            "Indoor Pool",
            "Ironing Board",
            "Microwave",
            "Outdoor Pool",
            "Outdoor Tennis",
            "Oven",
            "Queen size bed",
            "Restaurant",
            "Shopping Mall",
            "Shower",
            "Smoke detectors",
            "Sofa",
            "Stereo",
            "Swimming pool",
            "Toilet",
            "Towels",
            "TV",
        ]
        # Amenity 라는 모듈이 있고 object에 Manager가 C.R.U.D (create, removev, update, delete)를 한다.
        # 장고에서 object를 생성할수 있다.
        for a in amenties:
            Amenity.objects.create(name=a)
        self.stdout.write(self.style.SUCCESS("Amenties Created!!(목록을 생성 하였습니다.)"))
