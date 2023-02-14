from rest_framework.views import APIView, Response, Request, status
from django.shortcuts import get_object_or_404
from .models import Pet
from groups.models import Group
from traits.models import Trait
from .serializers import PetSerializer
from rest_framework.pagination import PageNumberPagination


# Create your views here.
class PetView(APIView, PageNumberPagination):
    def get(self, request: Request) -> Response:
        trait_param = request.query_params.get("trait")

        if trait_param:
            pets = Pet.objects.filter(traits__name=trait_param)
        else:
            pets = Pet.objects.all()

        result_page = self.paginate_queryset(pets, request, view=self)
        serializer = PetSerializer(result_page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group_data = serializer.validated_data.pop("group")
        traits_data = serializer.validated_data.pop("traits")

        try:
            group = Group.objects.get(
                scientific_name__iexact=group_data["scientific_name"]
            )
        except Group.DoesNotExist:
            group = Group.objects.create(**group_data)

        pet = Pet.objects.create(**serializer.validated_data, group=group)

        for trait in traits_data:
            try:
                trait_obj = Trait.objects.get(name__iexact=trait["name"])
            except Trait.DoesNotExist:
                trait_obj = Trait.objects.create(**trait)
            pet.traits.add(trait_obj)

        serializer = PetSerializer(pet)

        return Response(serializer.data, status.HTTP_201_CREATED)


class PetDetailView(APIView):
    def get(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(pet)

        return Response(serializer.data)

    def patch(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)

        serializer = PetSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        group_data = serializer.validated_data.pop("group", None)
        traits_data = serializer.validated_data.pop("traits", None)

        if group_data:
            try:
                group = Group.objects.get(
                    scientific_name__iexact=group_data["scientific_name"]
                )
            except Group.DoesNotExist:
                group = Group.objects.create(**group_data)
            pet.group = group

        if traits_data:
            new_trait = []
            for trait in traits_data:
                try:
                    trait_obj = Trait.objects.get(name__iexact=trait["name"])
                except Trait.DoesNotExist:
                    trait_obj = Trait.objects.create(**trait)
                new_trait.append(trait_obj)
            pet.traits.set(new_trait)

        for key, value in serializer.validated_data.items():
            setattr(pet, key, value)

        pet.save()
        serializer = PetSerializer(pet)

        return Response(serializer.data)

    def delete(self, request: Request, pet_id: int) -> Response:
        user = get_object_or_404(Pet, id=pet_id)

        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
