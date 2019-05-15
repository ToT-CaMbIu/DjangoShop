from .models import ShopCharacteristic

def settings(request):
    return {'settings': ShopCharacteristic.load()}