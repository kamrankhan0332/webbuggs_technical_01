from django.db.models import Count, Q
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Color, SubCategory, Product
from .serializers import ColorSerializer, SubCategorySerializer, ProductSerializer


@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
@api_view(['GET', 'POST'])
def color_list(request):
    if request.method == 'GET':
        colors = Color.objects.all()
        serializer = ColorSerializer(colors, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ColorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
@api_view(['GET', 'PUT', 'DELETE'])
def color_detail(request, pk):
    try:
        color = Color.objects.get(pk=pk)
    except Color.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ColorSerializer(color)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ColorSerializer(color, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        color.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
@api_view(['GET', 'POST'])
def subcategory_list(request):
    if request.method == 'GET':
        subcategories = SubCategory.objects.all()
        serializer = SubCategorySerializer(subcategories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        request.data['created_by'] = request.user.id
        request.data['updated_by'] = request.user.id
        serializer = SubCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
@api_view(['GET', 'PUT', 'DELETE'])
def subcategory_detail(request, pk):
    try:
        subcategory = SubCategory.objects.get(pk=pk)
    except SubCategory.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = SubCategorySerializer(subcategory)
        return Response(serializer.data)

    elif request.method == 'PUT':
        request.data['updated_by'] = request.user.id
        serializer = SubCategorySerializer(subcategory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        subcategory.delete()
        return Response(status=204)


@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        print(request.data)

        request.data['created_by'] = request.user.id
        request.data['updated_by'] = request.user.id
        print(request.data)
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == 'PUT':
        request.data['updated_by'] = request.user.id
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=204)


@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
@api_view(['GET'])
def top_three_categories(request):
    categories = SubCategory.objects.annotate(product_count=Count('product')).order_by('-product_count')[:3]
    data = []
    for category in categories:
        data.append({'name': category.name, 'product_count': category.product_count})
    return Response(data)


@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
@api_view(['GET'])
def product_filter(request):
    query_params = request.query_params
    search_term = query_params.get('detail', '')
    products = Product.objects.filter(
        Q(sku__icontains=search_term) |
        Q(title__icontains=search_term) |
        Q(description__icontains=search_term)
    )
    data = []
    for product in products:
        data.append({'title': product.title, 'category': product.category.name, 'description': product.description,
                     'sku': product.sku, 'created_by': product.created_by.username})
    return Response(data)
