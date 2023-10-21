from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

class TaskAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('/api-job/posting/')  # 여기에는 URL 패턴의 이름을 넣어주세요.

    def test_post_task(self):
        data = {
            'code': 'T011',
            'name': '테스트 능력',
            'description': '테스트 설명'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # 다른 assertion들도 추가할 수 있습니다. 예: 데이터베이스에 값이 제대로 저장되었는지 등
