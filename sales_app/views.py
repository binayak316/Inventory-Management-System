from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from .serializers import SalesItemSerializer, SalesSerializer
from django.contrib.auth.models import Permission
from .models import SalesItem, Sales
from django.db.models import Q
from product_app.models import Product
from third_party.models import Customer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
# Create your views here.

class SalesAPI(GenericAPIView):
    """Sales API is the Generic API view for the Sales items it
    calculates the total, subtotal, grandtotal, tax_amount and discount_amount 
    while selling the products and products is sell to the customers from this inventory """
    serializer_class = SalesSerializer
    permission_classes = [DjangoModelPermissions,IsAuthenticated]
    queryset = Sales.objects.all()


    def get(self, request, pk=None, format=None):
        p = Permission.objects.filter(codename='view_sales')[0]
        user = request.user
        if p in user.user_permissions.filter(pk=p.pk):
            
            id = pk
            if id is not None:
                sell = Sales.objects.get(id=id)
                serializer = SalesSerializer(sell)
                return Response(serializer.data)
            sell = Sales.objects.all()

            customer_search = request.GET.get('customer')
            status_search = request.GET.get('status')
            created_at_str = request.GET.get('created_at')

            start_date_str = request.GET.get('start_date')
            end_date_str = request.GET.get('end_date')

            sale_order = Sales.objects.all()

            # start_date = None
            # end_date = None
            
            # if customer_search or status_search or created_at_str or start_date or end_date:
            #     # done
            #     if customer_search:
            #         sale_order = Sales.objects.filter(Q(customer__name__icontains=customer_search))
            #     # done
            #     elif created_at_str:
            #         created_at = datetime.strptime(created_at_str, '%Y-%m-%d').date()
            #         sale_order = Sales.objects.filter(created_at__startswith =created_at)

                

            #     # done
            #     elif customer_search and status_search and start_date_str  and end_date_str:
            #         start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            #         end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            #         sale_order = Sales.objects.filter(Q(customer__name__icontains=customer_search), Q(status__icontains=status_search), Q(created_at__range=(start_date, end_date)))

            #     # #    not done
            #     # elif customer_search and status_search:
            #     #     sale_order = Sales.objects.filter(Q(customer__name__icontains=customer_search),Q(status__icontains=status_search))
            #     #     print(sale_order)
              
            #     # done
            #     elif start_date_str and end_date_str:
            #         start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            #         end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            #         sale_order = Sales.objects.filter(created_at__range=(start_date, end_date))

            #     if not sale_order:
            #         return Response({'message': 'Not Found'})
                
            #     serializer = SalesSerializer(sale_order, many=True)
            #     return Response({
            #         'data':serializer.data
            #     },status = status.HTTP_200_OK)
            # serializer = SalesSerializer(sell, many=True)
            # return Response(serializer.data)

            if customer_search:
                sale_order = sale_order.filter(customer__name__icontains=customer_search)
            

            if created_at_str:
                created_at = datetime.strptime(created_at_str, '%Y-%m-%d').date()
                sale_order = sale_order.filter(created_at__startswith=created_at)
            
            if start_date_str and end_date_str:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                sale_order = sale_order.filter(created_at__range=(start_date, end_date))
            
            if customer_search and status_search and start_date_str  and end_date_str:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                sale_order = Sales.objects.filter(Q(customer__name__icontains=customer_search), Q(status__icontains=status_search), Q(created_at__range=(start_date, end_date)))
                  

            if not sale_order.exists():
                return Response({'message': 'Not Found'})
            serializer = SalesSerializer(sale_order, many=True)
            return Response({
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        else:
            return Response({'message':"You don't have permissions"}, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request ,*args, **kwargs):

        customer_name = request.data.get('customer')
       
        if customer_name is not None:
            try:
                customer = Customer.objects.get(name=customer_name)
            except Customer.DoesNotExist:
                return Response({
                    'msg': f"Customer with name {customer_name} does not exist",
                    'status': status.HTTP_404_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({
                'msg':'please provide a valid customer name',
                'status':status.HTTP_400_BAD_REQUEST
            })

        serializer = SalesSerializer(data = request.data)

        out_of_stock_products = []
        for item in request.data['sales_items']: 
            product = Product.objects.get(id=int(item['product'])) #sales items is list but the data inside list are quantity and product which are dictionaries so we can access the value of dictionary by ['name']
            if product.current_stock < int(item['quantity']):
                out_of_stock_products.append(product.name)

                # return Response({
                #      "msg" : f"{product.name} is out of stock"
                # })
        if len(out_of_stock_products) > 0:
            return Response(
                {
                    "msg" : f"[{','.join(out_of_stock_products)} ] is  out of stocks."
                }
            )


        if serializer.is_valid():
            serializer.validated_data['customer'] =customer
            serializer.save()
            sales = Sales.objects.get(id=serializer.data['id'])
            
            sales.sub_total = 0
            
            sales.discount_amount = round((sales.disc_percent /100) * sales.get_subtotal(), 3)
            sales.tax_amount = round(float(float(sales.tax_percent)/100) * float(sales.get_subtotal()- sales.discount_amount),3)

            sales.sub_total = round(sales.get_subtotal(), 3)

            sales.grand_total = round(sales.get_grandtotal(), 3)

            sales.save()

            serializer = SalesSerializer(sales)
            #serializer = SalesSerializer(data = request.data) this includes the api with blank data
            #after serializer = SalesSerializer(sales) then it is the serializer which have the values which i put recently
            #this serializer goes to the response

            return Response({
                    'msg': 'Sales is created',
                    'status': status.HTTP_200_OK, 
                    'data': serializer.data,
                }, status=status.HTTP_200_OK)

            

        return Response({'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
         
    def put(self, request, pk):
        try:
            sales = Sales.objects.get(pk=pk)
        except Sales.DoesNotExist:
            return Response({
                'msg': f"Sales with id {pk} does not exist",
                'status': status.HTTP_404_NOT_FOUND,
            }, status=status.HTTP_404_NOT_FOUND)

        customer_name = request.data.get('customer')
        if customer_name is not None:
            try:
                customer = Customer.objects.get(name=customer_name)
            except Customer.DoesNotExist:
                return Response({
                    'msg': f"Customer with name {customer_name} does not exist",
                    'status': status.HTTP_404_NOT_FOUND,
                },status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'msg':'please provide a valid customer name',
                'status':status.HTTP_400_BAD_REQUEST
            })

        serializer = SalesSerializer(sales, data=request.data)

        out_of_stock_products = []
        for item in request.data['sales_items']: 
            product = Product.objects.get(id=int(item['product']))
            if product.current_stock < int(item['quantity']):
                out_of_stock_products.append(product.name)

      
        if len(out_of_stock_products) > 0:
            return Response(
                {
                    "msg" : f"[{','.join(out_of_stock_products)} ] is  out of stocks."
                }
            )

        if serializer.is_valid():
            serializer.validated_data['customer'] = customer
            serializer.save()

            sales.sub_total = 0
            sales.discount_amount = round((sales.disc_percent /100) * sales.get_subtotal(), 3)
            sales.tax_amount = round(float(float(sales.tax_percent)/100) * float(sales.get_subtotal()- sales.discount_amount),3)

            sales.sub_total = round(sales.get_subtotal(), 3)

            sales.grand_total = round(sales.get_grandtotal(), 3)

            sales.save()

        serializer = SalesSerializer(sales)

        if sales.status == 'Failed':
            sales.set_status_failed()
            for sales_item in sales.sales_items.all():
                product = sales_item.product
                quantity = sales_item.quantity
                product.current_stock += quantity
                product.save()

            return Response({
                'msg': 'Sales is updated',
                'status': status.HTTP_200_OK, 
                'data': serializer.data,
            }, status=status.HTTP_200_OK)
        
        Response({'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class SalesItemAPI(GenericAPIView):
    """SalesItem is Generic Api view and it is the process of once like it only calculates total from the products and quantity """
    serializer_class = SalesItemSerializer
    permission_classes = [DjangoModelPermissions,IsAuthenticated]
    queryset = SalesItem.objects.all()
    
    def get(self,request,pk=None,format=None):
        p = Permission.objects.filter(codename='view_purchaseItem')[0]
        user = request.user
        if p in user.user_permissions.filter(pk=p.pk):
            id = pk
            if id is not None:
                sales_item = SalesItem.objects.get(id=id)
                serializer = SalesItemSerializer(sales_item)
                return Response(serializer.data)
            sales_item = SalesItem.objects.all()
            serializer = SalesItemSerializer(sales_item, many=True)
            return Response(serializer.data)
        else:
            return Response({'message':"You don't have permissions"}, status=status.HTTP_400_BAD_REQUEST)


    def post(self,request,*args,**kwargs):
        serializer = SalesItemSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'SalesItem is created'}, status = status.HTTP_201_CREATED)
        return Response({'error':serializer.errors}, status = status.HTTP_400_BAD_REQUEST)

    

from datetime import datetime
from datetime import timedelta
from django.db.models import Sum
def show_sales_report(request):
    if request.method == "POST":
        start_date = request.POST.get('start')
        end_date = request.POST.get('end')

        if start_date and end_date:
            start_date_d = datetime.strptime(start_date, "%Y-%m-%d")
            end_date_d = datetime.strptime(end_date,"%Y-%m-%d")+ timedelta(days=1)

            today = datetime.today()
            if end_date_d or start_date_d > today():
                print('thulo val')
            
            data = Sales.objects.filter(created_at__range=(start_date_d,end_date_d), status = 'Completed')

            sum = data.aggregate(Sum('grand_total'))['grand_total__sum']
            if sum is not None:
                sum = round(sum,4)
            else:
                sum = 0.0
            context = {
                'data':data,
                'sum':sum,
                'start_date_d':start_date_d,
                'end_date_d':end_date_d,
            }
        else:
            return redirect('/dashboard')

        return render(request, 'sales_app/pdf_format_sales.html', context)
    return redirect('/dashboard/')

            


















