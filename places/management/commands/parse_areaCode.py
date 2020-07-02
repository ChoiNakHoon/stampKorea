import os
import requests
from django.core.management.base import BaseCommand
from django.db.models import Q
from places import models as place_models

SUCCESS_CODE = "0000"


class ApiException(Exception):
    pass


class Command(BaseCommand):

    help = "This command created places?"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="Do you want to created?",
        )

    def handle(self, *args, **options):

        PAGE_OF_ROWS = "100"
        API_KEY = "wsFJNnH4nzhIPZTa1law6nz%2B1VOjiV09bJ5kVLLH%2Fv9K7GWk8OL2HJtQ%2B0%2B%2F3MOuSa8lbXV8yF9ilc6b7oKPCA%3D%3D"
        try:
            api_request = requests.get(
                f"http://api.visitkorea.or.kr/openapi/service/rest/EngService/areaCode?ServiceKey={API_KEY}&numOfRows={PAGE_OF_ROWS}&pageNo=1&MobileOS=ETC&MobileApp=Stamp_Korea&_type=json"
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

                    area_code = items[i].get("code")
                    area_name = items[i].get("name")

                    region = place_models.Region.objects.filter(code=area_code).first()

                    if region is not None:
                        if int(region.code) == area_code:
                            print(region.code)
                            if region.code == "8":
                                sub_region = place_models.Sub_Region.objects.create(
                                    region=region, name=region.name, code=1
                                )
                                sub_region.save()
                            else:
                                AreaCode_Sub(region.code, PAGE_OF_ROWS, API_KEY)
                    else:
                        region = place_models.Region.objects.create(
                            code=area_code, name=area_name
                        )
                        region.save()
                self.stdout.write(self.style.SUCCESS("places created!"))
            else:
                print(response.get("response").get("header").get("resultMsg"))
        except ApiException as e:
            print(e)
            raise ApiException()


def AreaCode_Sub(code, rows, key):

    try:
        api_request = requests.get(
            f"http://api.visitkorea.or.kr/openapi/service/rest/EngService/areaCode?ServiceKey={key}&numOfRows={rows}&pageNo=1&MobileOS=ETC&MobileApp=Stamp_Korea&areaCode={code}&_type=json"
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
                area_code = items[i].get("code")
                area_name = items[i].get("name")
                region = place_models.Region.objects.filter(code=code).first()
                try:
                    sub_region = place_models.Sub_Region.objects.get(
                        Q(region=region) & Q(name=area_name)
                    )
                except place_models.Sub_Region.DoesNotExist:
                    sub_region = place_models.Sub_Region.objects.create(
                        region=region, name=area_name, code=area_code
                    )
                    sub_region.save()
        else:
            print(response.get("response").get("header").get("resultMsg"))
    except ApiException as e:
        raise ApiException()
