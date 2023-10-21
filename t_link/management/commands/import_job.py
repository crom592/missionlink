from django.core.management.base import BaseCommand
from t_link.models import JobPosting, User

class Command(BaseCommand):
    help = 'Import job postings from JSON data'

    def handle(self, *args, **options):
        # JSON data for job postings
        json_data = [
                    {
                        "id": 1,
                        "type": "Looking for Missionary",
                        "title": "Need volunteers for educational program",
                        "location": "South Korea",
                        "date": "2023-10-20",
                        "language": "en",
                        "description": "We're looking for dedicated individuals to join our educational program in South Korea. Experience in teaching is a plus.",
                        "image": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29",
                        "mapInfo": { "latitude": 37.5665, "longitude": 126.978, "zoom": 10 }
                    },
                    {
                        "id": 2,
                        "type": "단기선교 지원자 찾기",
                        "title": "교육 프로그램을 위한 자원봉사자 필요",
                        "location": "미국",
                        "date": "2023-11-15",
                        "language": "ko",
                        "description": "미국 교육 프로그램에 참여할 헌신적인 개인을 찾고 있습니다. 교육 경험이 있으면 좋습니다.",
                        "image": "https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89",
                        "mapInfo": { "latitude": 37.0902, "longitude": -95.7129, "zoom": 4 }
                    },
                    {
                        "id": 3,
                        "type": "Looking for Missionary",
                        "title": "Join our outreach program",
                        "location": "Japan",
                        "date": "2023-12-01",
                        "language": "en",
                        "description": "We're inviting volunteers for our outreach program in Japan.",
                        "image": "https://images.unsplash.com/photo-1526392060635-9d6019884377",
                        "mapInfo": { "latitude": 35.6895, "longitude": 139.6917, "zoom": 10 }
                    },
                    {
                        "id": 4,
                        "type": "단기선교 지원자 찾기",
                        "title": "Children education support in Vietnam",
                        "location": "Vietnam",
                        "date": "2023-12-10",
                        "language": "en",
                        "description": "Seeking volunteers for a children education program in Vietnam.",
                        "image": "https://images.unsplash.com/photo-1519186880822-548bb3bfae4f",
                        "mapInfo": { "latitude": 14.0583, "longitude": 108.2772, "zoom": 6 }
                    },
                    {
                        "id": 5,
                        "type": "Looking for Missionary",
                        "title": "Healthcare outreach in Brazil",
                        "location": "Brazil",
                        "date": "2024-01-05",
                        "language": "en",
                        "description": "We need healthcare professionals to support our outreach in Brazil.",
                        "image": "https://images.unsplash.com/photo-1503455637927-730bce8583c0",
                        "mapInfo": { "latitude": -14.235, "longitude": -51.9253, "zoom": 5 }
                    },
                    {
                        "id": 6,
                        "type": "단기선교 지원자 찾기",
                        "title": "Community building in India",
                        "location": "India",
                        "date": "2024-02-15",
                        "language": "ko",
                        "description": "Join us in community building activities in India.",
                        "image": "https://images.unsplash.com/photo-1560413904-5695b4974710",
                        "mapInfo": { "latitude": 20.5937, "longitude": 78.9629, "zoom": 5 }
                    },
                    {
                        "id": 7,
                        "type": "Looking for Missionary",
                        "title": "Clean water project in Kenya",
                        "location": "Kenya",
                        "date": "2024-03-10",
                        "language": "en",
                        "description": "Support our clean water project in Kenya. Engineers and professionals are welcome.",
                        "image": "https://images.unsplash.com/photo-1557672172-298e090bd0f1",
                        "mapInfo": { "latitude": -1.2921, "longitude": 36.8219, "zoom": 8 }
                    },
                    {
                        "id": 8,
                        "type": "단기선교 지원자 찾기",
                        "title": "Literacy program in Nepal",
                        "location": "Nepal",
                        "date": "2024-04-20",
                        "language": "ko",
                        "description": "Help us in our literacy program in Nepal. Educators are highly appreciated.",
                        "image": "https://images.unsplash.com/photo-1542903660-eedba2cda473",
                        "mapInfo": { "latitude": 28.3949, "longitude": 84.124, "zoom": 7 }
                    },
                    {
                        "id": 9,
                        "type": "단기선교 지원자 찾기",
                        "title": "태국에서의 음악 교육 프로그램",
                        "location": "태국",
                        "date": "2024-05-01",
                        "language": "ko",
                        "description": "태국에서 아이들에게 음악 교육을 제공하는 프로그램에 자원봉사자가 필요합니다.",
                        "image": "https://images.unsplash.com/photo-1524603699798-5b7445c116c7",
                        "mapInfo": { "latitude": 13.7563, "longitude": 100.5018, "zoom": 10 }
                    },
                    {
                        "id": 10,
                        "type": "단기선교 지원자 찾기",
                        "title": "인도네시아의 환경 보호 활동",
                        "location": "인도네시아",
                        "date": "2024-05-20",
                        "language": "ko",
                        "description": "인도네시아에서 진행하는 환경 보호 활동에 참여할 자원봉사자를 모집합니다.",
                        "image": "https://images.unsplash.com/photo-1485160497022-3e09382fb310",
                        "mapInfo": { "latitude": -0.7893, "longitude": 113.9213, "zoom": 5 }
                    },
                    {
                        "id": 11,
                        "type": "단기선교 지원자 찾기",
                        "title": "필리핀에서의 건강 교육",
                        "location": "필리핀",
                        "date": "2024-06-10",
                        "language": "ko",
                        "description": "필리핀에서 건강 교육 프로그램에 참여할 자원봉사자를 찾고 있습니다.",
                        "image": "https://images.unsplash.com/photo-1501876725168-00c445821c9e",
                        "mapInfo": { "latitude": 12.8797, "longitude": 121.774, "zoom": 6 }
                    },
                    {
                        "id": 12,
                        "type": "단기선교 지원자 찾기",
                        "title": "몽골의 전통 문화 교육",
                        "location": "몽골",
                        "date": "2024-07-01",
                        "language": "ko",
                        "description": "몽골의 전통 문화를 소개하는 교육 프로그램에 참여할 자원봉사자를 모집합니다.",
                        "image": "https://images.unsplash.com/photo-1516202905881-63a8f2ec9906",
                        "mapInfo": { "latitude": 46.8625, "longitude": 103.8467, "zoom": 5 }
                    },
                    {
                        "id": 13,
                        "type": "단기선교 지원자 찾기",
                        "title": "라오스에서의 아동 교육 지원",
                        "location": "라오스",
                        "date": "2024-07-20",
                        "language": "ko",
                        "description": "라오스에서 아동 교육 프로그램에 참여할 자원봉사자를 찾고 있습니다.",
                        "image": "https://images.unsplash.com/photo-1503152394-b8a97459a1e1",
                        "mapInfo": { "latitude": 19.8563, "longitude": 102.4955, "zoom": 7 }
                    }
                    ]

        # Create JobPosting objects for each JSON object
        for item in json_data:
            user = User.objects.get(pk=1)  # For example, assign all JobPostings to the first user
            
            job_posting = JobPosting(
                user=user,
                type=item['type'],
                title=item['title'],
                description=item['description'],
                country=item['location'],
                language=item['language'],
                start_date=item['date'],
                image=item['image'],
                latitude=item['mapInfo']['latitude'],
                longitude=item['mapInfo']['longitude'],
                zoom=item['mapInfo']['zoom'],
            )
            
            job_posting.save()
        
        self.stdout.write(self.style.SUCCESS('Successfully imported job postings'))
                