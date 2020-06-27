import os
import math
import requests
from django.core.management.base import BaseCommand
from places import models as place_models


class ApiException(Exception):
    pass


class Command(BaseCommand):

    help = "This command created places?"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="Do you want to created?",
        )

    def handle(self, *args, **options):
        SUCCESS_CODE = "0000"
        PAGE_OF_ROWS = 1000
        API_KEY = "wsFJNnH4nzhIPZTa1law6nz%2B1VOjiV09bJ5kVLLH%2Fv9K7GWk8OL2HJtQ%2B0%2B%2F3MOuSa8lbXV8yF9ilc6b7oKPCA%3D%3D"
        try:
            api_request = requests.get(
                f"http://api.visitkorea.or.kr/openapi/service/rest/EngService/areaBasedList?ServiceKey={API_KEY}&contentTypeId=&areaCode=&sigunguCode=&cat1=&cat2=&cat3=&listYN=Y&MobileOS=ETC&MobileApp=StampKorea&arrange=A&numOfRows=1&pageNo=1&_type=json"
            )

            response = api_request.json()
            result_code = response.get("response").get("header").get("resultCode")
            print(result_code)
            # result_code가 0000라면
            if result_code == SUCCESS_CODE:
                # 전체 데이터 갯수를 가져 옵니다.
                body = response.get("response").get("body")
                totalCount = body.get("totalCount")
                # 총 1000개 데이터를 가져오도록 페이지를 나눕니다.
                numOfRows = totalCount / PAGE_OF_ROWS
                # 올림 가격으로 최종 Page값을 구합니다.
                pageNo = math.ceil(numOfRows)

                context_type = body.get("items").get("item").get("contenttypeid")
                content_id = body.get("items").get("item").get("contentid")
                print(context_type)
                print(content_id)

                api_request = requests.get(
                    f"http://api.visitkorea.or.kr/openapi/service/rest/EngService/detailCommon?ServiceKey={API_KEY}&MobileOS=ETC&MobileApp=StampKorea&contentId={content_id}&defaultYN=Y&firstImageYN=Y&areacodeYN=Y&catcodeYN=Y&addrinfoYN=Y&mapinfoYN=Y&overviewYN=Y&transGuideYN=Y&numOfRows=10&pageNo=1&_type=json"
                )

                print(api_request)
                response = api_request.json()
                result_code = response.get("response").get("header").get("resultCode")

                print(response)
                if result_code == SUCCESS_CODE:
                    result = body.get("items").get("item")

                    print(result)

                # try:
                #     for page in range(pageNo):
                #         api_request = requests.get(
                #             f"http://api.visitkorea.or.kr/openapi/service/rest/EngService/areaBasedList?ServiceKey={API_KEY}&contentTypeId=&areaCode=&sigunguCode=&cat1=&cat2=&cat3=&listYN=Y&MobileOS=ETC&MobileApp=StampKorea&arrange=A&numOfRows={PAGE_OF_ROWS}&pageNo={page + 1}&_type=json"
                #         )

                # except ApiException:
                #     print("멈췄어요")
                #     raise ApiException()
                self.stdout.write(self.style.SUCCESS("places created!"))
            else:
                print(response.get("response").get("header").get("resultMsg"))
        except ApiException as e:
            print(e)
            raise ApiException()
