from django.shortcuts import render, HttpResponse
from .models import myProduct, contact, Orders, OrderUpdate
from math import ceil
import json

# Create your views here.

def index(request):
    # products = myProduct.objects.all()
    # print(products)
    # n = len(products)
    # nSlides = n//4 + ceil((n/4)-(n//4)) #for intializing no. of slides
    # params = {'no_of_slides': nSlides, 'range':range(1, nSlides),'product': products} #for fetching products to show in templates
    # allprods = [[products, range(1, nSlides), nSlides], [products, range(1, nSlides), nSlides]] #for fetching products in  multiple slides 
    # param = {'allprods':allprods}
    products= myProduct.objects.all()
    # print(products)
    allProds=[]
    catprods= myProduct.objects.values('category', 'id')
    cats= {item["category"] for item in catprods}
    for cat in cats:
        prod=myProduct.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params={'allprods':allProds }
    return render(request,"shop/index.html", params)
def searchMatch(query, item):
    '''return true if query matches the item '''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category:
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    products= myProduct.objects.all()
    # print(products)
    allProds=[]
    catprods= myProduct.objects.values('category', 'id')
    cats= {item["category"] for item in catprods}
    for cat in cats:
        prodtemp=myProduct.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod)!= 0:
            allProds.append([prod, range(1, nSlides), nSlides])

    params={'allprods':allProds,  "msg":"" }
    if len(allProds)==0 or len(query)<1:
        params = {'msg': "please make sure to enter relevent search"}

    return render(request,"shop/search.html", params)



def about(request):
    return render(request, 'shop/about.html')

def contacts(request):
    thanks= False
    if request.method=="POST":
        print(request)
        name=request.POST.get('name', '')
        email=request.POST.get('email', '')
        phone=request.POST.get('phone', '')
        desc=request.POST.get('desc', '')
        Contacts = contact(name=name, email=email, phone=phone, desc=desc)
        Contacts.save()
        thanks = True
        return render(request, 'shop/contact.html', {'thanks':thanks})
       
    return render(request, 'shop/contact.html')

def tracker(request):
    if request.method== "POST":
        OrderId = request.POST.get('OrderId', '')
        email=request.POST.get('email', '')
        # return HttpResponse(f"{OrderId} and {email}")
        try:
            order = Orders.objects.filter(order_id=OrderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=OrderId)
                updates = []
                for item in update:
                    updates.append({'text':item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success" ,"update":updates, "itemsJson":order[0].items_json}, default=str)
                return HttpResponse(response)
                    

            else:
                return HttpResponse('{"status":"noitems"}')

        except Exception as e:
            return HttpResponse('{"status":"error"}')    


    return render(request, 'shop/tracker.html')



def productView(request, myid):
    #fetching the product using id
    product = myProduct.objects.filter(id = myid)
    return render(request, 'shop/prodView.html', {'product': product[0]})

def checkout(request):
    if request.method == "POST":
        itemsJson = request.POST.get('itemsJson', '')
        email  = request.POST.get('email', '')
        name = request.POST.get('name', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        phone = request.POST.get('phone', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        checkout = Orders( items_json=itemsJson, email=email, name=name, address=address, phone=phone, city=city, state=state, zip_code=zip_code)
        checkout.save()

        update = OrderUpdate(order_id=checkout.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = checkout.order_id
        return render(request, 'shop/checkout.html', {'thank':thank, 'id':id})

    return render(request, 'shop/checkout.html')