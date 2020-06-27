import os
import math
import requests
from django.core.management.base import BaseCommand
from places import models as place_models

SUCCESS_CODE = "0000"


class ApiException(Exception):
    pass


class Command(BaseCommand):

    help = "This command created Catagory?"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="Do you want to created?",
        )

    def handle(self, *args, **options):

        PAGE_OF_ROWS = "100"
        API_KEY = "wsFJNnH4nzhIPZTa1law6nz%2B1VOjiV09bJ5kVLLH%2Fv9K7GWk8OL2HJtQ%2B0%2B%2F3MOuSa8lbXV8yF9ilc6b7oKPCA%3D%3D"
        try:
            api_request = requests.get(
                f"http://api.visitkorea.or.kr/openapi/service/rest/EngService/categoryCode?ServiceKey={API_KEY}&numOfRows={PAGE_OF_ROWS}&pageNo=1&MobileOS=ETC&MobileApp=Stamp_Korea&_type=json"
            )

            response = api_request.json()
            result_code = response.get("response").get("header").get("resultCode")
            print(result_code)
            # result_code가 0000라면
            if result_code == SUCCESS_CODE:
                # 전체 데이터 갯수를 가져 옵니다.
                body = response.get("response").get("body")
                items = body.get("items").get("item")

                for i in range(len(items)):

                    code = items[i].get("code")
                    name = items[i].get("name")

                    try:
                        place_models.Cat_Type.objects.get(code=code)

                    except place_models.Cat_Type.DoesNotExist:
                        place_models.Cat_Type.objects.create(code=code, name=name)
                        print("성공")
                self.stdout.write(self.style.SUCCESS("places created!"))
            else:
                print(response.get("response").get("header").get("resultMsg"))
        except ApiException as e:
            print(e)
            raise ApiException()
