from django.shortcuts import render
from rest_framework.views import APIView, Response, Request, status
from .models import Pet
from django.forms.models import model_to_dict

# from .serializers import PetSerializer


# Create your views here.
class PetView(APIView):
    def get(self, request: Request) -> Response:
        pets = Pet.objects.all()

        pets_list = []
        for pet in pets:
            pet_dict = model_to_dict(pet)
            pets_list.append(pet_dict)

        return Response(pets_list, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        try:
            pet = Pet.objects.create(**request.data)
            pet_dict = model_to_dict(pet)
            return Response(pet_dict, status.HTTP_201_CREATED)
        except Pet.DoesNotExist:
            return Response({"message": "pet not found"}, status.HTTP_404_NOT_FOUND)
