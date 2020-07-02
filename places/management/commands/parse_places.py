import os
import math
import requests
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.shortcuts import get_object_or_404
from places import models as place_models

SUCCESS_CODE = "0000"
PAGE_OF_ROWS = 1000
API_KEY = "wsFJNnH4nzhIPZTa1law6nz%2B1VOjiV09bJ5kVLLH%2Fv9K7GWk8OL2HJtQ%2B0%2B%2F3MOuSa8lbXV8yF9ilc6b7oKPCA%3D%3D"


class ApiException(Exception):
    pass


class Command(BaseCommand):

    help = "This command created places?"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="Do you want to created?",
        )

    def handle(self, *args, **options):
        try:
            api_request = requests.get(
                f"http://api.visitkorea.or.kr/openapi/service/rest/EngService/areaBasedList?ServiceKey={API_KEY}&contentTypeId=&areaCode=&sigunguCode=&cat1=&cat2=&cat3=&listYN=Y&MobileOS=ETC&MobileApp=StampKorea&arrange=A&numOfRows={PAGE_OF_ROWS}&pageNo=1&_type=json"
            )

            response = api_request.json()
            result_code = response.get("response").get("header").get("resultCode")
            # result_code가 0000라면
            if result_code == SUCCESS_CODE:
                # 전체 데이터 갯수를 가져 옵니다.
                body = response.get("response").get("body")
                totalCount = body.get("totalCount")
                # 총 1000개 데이터를 가져오도록 페이지를 나눕니다.
                numOfRows = totalCount / PAGE_OF_ROWS
                # 올림 가격으로 최종 Page값을 구합니다.
                page = math.ceil(numOfRows)
                for i in range(page):
                    pageNo = i + 1
                    api_request = requests.get(
                        f"http://api.visitkorea.or.kr/openapi/service/rest/EngService/areaBasedList?ServiceKey={API_KEY}&contentTypeId=&areaCode=&sigunguCode=&cat1=&cat2=&cat3=&listYN=Y&MobileOS=ETC&MobileApp=StampKorea&arrange=A&numOfRows={PAGE_OF_ROWS}&pageNo={pageNo}&_type=json"
                    )
                    response = api_request.json()
                    body = response.get("response").get("body")
                    items = body.get("items").get("item")
                    for j in range(len(items)):
                        content_type = items[j].get("contenttypeid")
                        content_id = items[j].get("contentid")
                        place = place_models.Place.objects.filter(
                            Q(content_id=content_id) & Q(content_type=content_type)
                        ).first()

                        if place is not None:
                            print(f"detailCommon에 넘깁니다 {content_type} : {content_id}")
                        else:
                            place = place_models.Place.objects.create(
                                title="test",
                                content_type=content_type,
                                content_id=content_id,
                            )
                            place.save()
                            detailCommon(str(content_type), str(content_id))

                self.stdout.write(self.style.SUCCESS("places created!"))
            else:
                print(response.get("response").get("header").get("resultMsg"))
        except ApiException as e:
            print(e)
            raise ApiException()


def detailCommon(content_type, content_id):
    print(f"detailCommon type = {content_type} // id = {content_id}")
    try:
        api_request = requests.get(
            f"http://api.visitkorea.or.kr/openapi/service/rest/EngService/detailCommon?serviceKey={API_KEY}&numOfRows=100&pageNo=1&MobileOS=ETC&MobileApp=StampKorea&contentId={content_id}&countentTypeId={content_type}&defaultYN=Y&firstImageYN=Y&areacodeYN=Y&catcodeYN=Y&addrinfoYN=Y&mapinfoYN=Y&overviewYN=Y&transGuideYN=Y&_type=json"
        )

        response = api_request.json()
        result_code = response.get("response").get("header").get("resultCode")
        # result_code가 0000라면
        if result_code == SUCCESS_CODE:
            # 전체 데이터 갯수를 가져 옵니다.
            body = response.get("response").get("body")
            items = body.get("items").get("item")
            areacode = items.get("areacode")
            sigungucode = items.get("sigungucode")
            cat1 = items.get("cat1")
            if areacode is None:
                region = place_models.Region.objects.get(code=1)
                sub_region = place_models.Sub_Region.objects.get(
                    Q(region__code=1) & Q(code=777)
                )
                main_images = items.get("firstimage")
                cat_type = place_models.Cat_Type.objects.get(code=cat1)
                try:
                    place = place_models.Place.objects.get(content_id=content_id)
                    place.title = items.get("title")
                    place.address = items.get("addr1")
                    place.overview = items.get("overview")
                    place.directions = items.get("directions")
                    place.tel = items.get("tel")
                    place.mapy = items.get("mapx")
                    place.mapx = items.get("mapy")
                    place.zipcode = items.get("zipcode")
                    place.region = region
                    place.region_sub = sub_region
                    place.cat_type = cat_type
                    place.created_time = items.get("createdtime")
                    place.updated_time = items.get("modifiedtime")
                    place.homepage = items.get("homepage")
                    place.save()

                    try:
                        photos = place_models.Photo.objects.get(url=main_images)
                        if photos.url == main_images:
                            print("메인 이미지가 존재합니다.")
                    except place_models.Photo.DoesNotExist:
                        place_models.Photo.objects.create(
                            caption=items.get("title"), url=main_images, place=place,
                        )
                except place_models.Place.DoesNotExist:
                    print("다시 시도하세요")
            else:
                region = place_models.Region.objects.get(code=areacode)
                sub_region = place_models.Sub_Region.objects.get(
                    Q(region__code=region.code) & Q(code=sigungucode)
                )
                main_images = items.get("firstimage")
                cat_type = place_models.Cat_Type.objects.get(code=cat1)
                try:
                    place = place_models.Place.objects.get(content_id=content_id)
                    place.title = items.get("title")
                    place.address = items.get("addr1")
                    place.overview = items.get("overview")
                    place.directions = items.get("directions")
                    place.tel = items.get("tel")
                    place.mapy = items.get("mapx")
                    place.mapx = items.get("mapy")
                    place.zipcode = items.get("zipcode")
                    place.region = region
                    place.region_sub = sub_region
                    place.cat_type = cat_type
                    place.created_time = items.get("createdtime")
                    place.updated_time = items.get("modifiedtime")
                    place.homepage = items.get("homepage")
                    place.save()

                    try:
                        photos = place_models.Photo.objects.get(url=main_images)
                        if photos.url == main_images:
                            print("메인 이미지가 존재합니다.")
                    except place_models.Photo.DoesNotExist:
                        place_models.Photo.objects.create(
                            caption=items.get("title"), url=main_images, place=place,
                        )
                except place_models.Place.DoesNotExist:
                    print("다시 시도하세요")

        else:
            print(response.get("response").get("header").get("resultMsg"))

        detailIntro(content_type, content_id)
        detailInfo(content_type, content_id)
        detailImage(content_id)
    except ApiException as e:
        print(e)
        raise ApiException()


def detailIntro(content_type, content_id):
    print(f"detailIntro type = {content_type} // id = {content_id}")
    CODE_NATURE = "76"
    CODE_CULTURE = "78"
    CODE_FESTIVAL = "85"
    CODE_SPORTS = "75"
    CODE_ACCOMMODATION = "80"
    CODE_SHOPPING = "79"
    CODE_CUISINE = "82"
    CODE_TRANSPORTATIONS = "77"
    try:
        api_request = requests.get(
            f"http://api.visitkorea.or.kr/openapi/service/rest/EngService/detailIntro?serviceKey={API_KEY}&numOfRows=100&pageNo=1&MobileOS=ETC&MobileApp=StampKorea&contentId={content_id}&contentTypeId={content_type}&introYN=Y&_type=json"
        )
        response = api_request.json()
        result_code = response.get("response").get("header").get("resultCode")
        # result_code가 0000라면
        if result_code == SUCCESS_CODE:
            # 전체 데이터 갯수를 가져 옵니다.
            body = response.get("response").get("body")
            items = body.get("items").get("item")
            place = place_models.Place.objects.get(content_id=content_id)
            if place.content_type == CODE_NATURE:
                try:
                    place.expagerange = items.get("expagerange")
                    place.expguide = items.get("expguide")
                    place.heritage1 = items.get("heritage1")
                    place.info_center = items.get("info_center")
                    place.rest_date = items.get("rest_date")
                    place.parking = items.get("parking")
                    place.use_time = items.get("use_time")
                    place.save()
                except place_models.Place.DoesNotExist:
                    ApiException()
            elif place.content_type == CODE_CULTURE:
                try:
                    place.infocenterculture = items.get("infocenterculture")
                    place.restdateculture = items.get("restdateculture")
                    place.usefee = items.get("usefee")
                    place.usetimeculture = items.get("usetimeculture")
                    place.parkingculture = items.get("parkingculture")
                    place.save()
                except place_models.Place.DoesNotExist:
                    ApiException()
            elif place.content_type == CODE_FESTIVAL:
                try:
                    place.agelimit = items.get("agelimit")
                    place.bookingplace = items.get("bookingplace")
                    place.discountinfofestival = items.get("discountinfofestival")
                    place.eventstartdate = items.get("eventstartdate")
                    place.eventenddate = items.get("eventenddate")
                    place.eventhomepage = items.get("eventhomepage")
                    place.eventplace = items.get("eventplace")
                    place.placeinfo = items.get("placeinfo")
                    place.playtime = items.get("playtime")
                    place.program = items.get("program")
                    place.sponsor1 = items.get("sponsor1")
                    place.sponsor1tel = items.get("sponsor1tel")
                    place.sponsor2 = items.get("sponsor2")
                    place.sponsor2tel = items.get("sponsor2tel")
                    place.subevent = items.get("subevent")
                    place.usetimefestival = items.get("usetimefestival")
                    place.save()
                except place_models.Place.DoesNotExist:
                    ApiException()
            elif place.content_type == CODE_SPORTS:
                try:
                    place.expagerangeleports = items.get("expagerangeleports")
                    place.infocenterleports = items.get("infocenterleports")
                    place.reservation = items.get("reservation")
                    place.restdateleports = items.get("restdateleports")
                    place.usefeeleports = items.get("usefeeleports")
                    place.usetimeleports = items.get("usetimeleports")
                    place.parkingleports = items.get("parkingleports")
                    place.save()
                except place_models.Place.DoesNotExist:
                    ApiException()
            elif place.content_type == CODE_ACCOMMODATION:
                try:
                    place.checkintime = items.get("checkintime")
                    place.checkouttime = items.get("checkouttime")
                    place.infocenterlodging = items.get("infocenterlodging")
                    place.parkinglodging = items.get("parkinglodging")
                    place.reservationlodging = items.get("reservationlodging")
                    place.subfacility = items.get("subfacility")
                    place.save()
                except place_models.Place.DoesNotExist:
                    ApiException()
            elif place.content_type == CODE_SHOPPING:
                try:
                    place.fairday = items.get("fairday")
                    place.infocentershopping = items.get("infocentershopping")
                    place.opentime = items.get("opentime")
                    place.restdateshopping = items.get("restdateshopping")
                    place.parkingshopping = items.get("parkingshopping")
                    place.save()
                except place_models.Place.DoesNotExist:
                    ApiException()
            elif place.content_type == CODE_CUISINE:
                try:
                    place.firstmenu = items.get("firstmenu")
                    place.treatmenu = items.get("treatmenu")
                    place.infocenterfood = items.get("infocenterfood")
                    place.opentimefood = items.get("opentimefood")
                    place.restdatefood = items.get("restdatefood")
                    place.reservationfood = items.get("reservationfood")
                    place.parkingfood = items.get("parkingfood")
                    place.save()
                except place_models.Place.DoesNotExist:
                    ApiException()
            elif place.content_type == CODE_TRANSPORTATIONS:
                try:
                    place.conven = items.get("conven")
                    place.disablefacility = items.get("disablefacility")
                    place.foreignerinfocenter = items.get("foreignerinfocenter")
                    place.parkingtraffic = items.get("parkingtraffic")
                    place.save()
                except place_models.Place.DoesNotExist:
                    ApiException()
            else:
                print("네")
        else:
            print(response.get("response").get("header").get("resultMsg"))
    except ApiException as e:
        print(e)
        raise ApiException()


def detailInfo(content_type, content_id):
    print(f"detailInfo type = {content_type} // id = {content_id}")
    try:
        api_request = requests.get(
            f"http://api.visitkorea.or.kr/openapi/service/rest/EngService/detailInfo?serviceKey={API_KEY}&numOfRows=100&pageNo=1&MobileOS=ETC&MobileApp=StampKorea&contentId={content_id}&contentTypeId={content_type}&listYN=Y&_type=json"
        )

        response = api_request.json()
        result_code = response.get("response").get("header").get("resultCode")
        if SUCCESS_CODE == result_code:
            body = response.get("response").get("body")
            total = body.get("totalCount")
            place = place_models.Place.objects.get(content_id=content_id)
            if total == 0:
                print("자료가 없어요..")
            else:
                items = body.get("items").get("item")
                if total == 1:
                    infoname = items.get("infoname")
                    infotext = items.get("infotext")
                    try:
                        sub_info = place_models.Sub_Info.objects.get(title=infoname)
                    except place_models.Sub_Info.DoesNotExist:
                        sub_info = place_models.Sub_Info.objects.create(
                            place=place, title=infoname, text=infotext
                        )
                        sub_info.save()
                else:
                    for i in range(len(items)):
                        infoname = items[i].get("infoname")
                        infotext = items[i].get("infotext")

                        try:
                            sub_info = place_models.Sub_Info.objects.get(title=infoname)
                        except place_models.Sub_Info.DoesNotExist:
                            sub_info = place_models.Sub_Info.objects.create(
                                place=place, title=infoname, text=infotext
                            )
                            sub_info.save()
        else:
            print(response.get("response").get("header").get("resultMsg"))
    except ApiException:
        raise ApiException()


def detailImage(content_id):
    print(f"detailImage id = {content_id}")
    try:
        api_request = requests.get(
            f"http://api.visitkorea.or.kr/openapi/service/rest/EngService/detailImage?serviceKey={API_KEY}&numOfRows=100&pageNo=1&MobileOS=ETC&MobileApp=StampKorea&contentId={content_id}&imageYN=Y&subImageYN=Y&_type=json"
        )

        response = api_request.json()
        result_code = response.get("response").get("header").get("resultCode")
        if SUCCESS_CODE == result_code:
            body = response.get("response").get("body")
            total = body.get("totalCount")
            place = place_models.Place.objects.get(content_id=content_id)
            if total == 0:
                print("이미지가 없는 것 같아요")
            else:
                items = body.get("items").get("item")
                if total == 1:
                    url = items.get("orifinimgurl")
                    try:
                        photos = place_models.Photo.objects.get(url=url)
                        # print("이미지가 존재합니다.")
                    except place_models.Photo.DoesNotExist:
                        photos = place_models.Photo.objects.create(
                            caption=f"{place.title} - {i+1} of {len(items)} IMAGES",
                            url=url,
                            place=place,
                        )
                        photos.save()
                else:
                    for i in range(len(items)):
                        # print("이미지")
                        url = items[i].get("originimgurl")
                        try:
                            photos = place_models.Photo.objects.get(url=url)
                            # print("이미지가 존재합니다.")
                        except place_models.Photo.DoesNotExist:
                            photos = place_models.Photo.objects.create(
                                caption=f"{place.title} - {i+1} of {len(items)} IMAGES",
                                url=url,
                                place=place,
                            )
                            photos.save()
        else:
            print(response.get("response").get("header").get("resultMsg"))
    except ApiException:
        raise ApiException()
