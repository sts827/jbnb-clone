from django.core.management.base import BaseCommand
from rooms.models import Facility

## fake Data를 만드는 클래스 입니다
## Django-seed는 Fake를 위한것입니당.... 나중에 코딩할 때 참고!!!
class Command(BaseCommand):

    """ Command-class to Makes Fake Data """

    help = "This command creates facilities"

    def handle(self, *args, **options):
        # 편의시설: amenities
        facilities = [
            "Private entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]
        # Amenity 라는 모듈이 있고 object에 Manager가 C.R.U.D (create, removev, update, delete)를 한다.
        # 장고에서 object를 생성할수 있다.
        for f in facilities:
            Facility.objects.create(name=f)
        self.stdout.write(
            self.style.SUCCESS(f"{len(facilities)} facilities created !!(목록을 생성하였습니다.)")
        )
