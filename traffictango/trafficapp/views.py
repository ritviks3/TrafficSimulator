from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from .manager import TrafficManager
from .serializer import *
from rest_framework.response import Response
from json import dumps

class VehicleView(APIView):
    # custom get request
    def getIndividual(self, request):
        id = request.query_params.get('id')
        try:
            isData = Vehicle.objects.get(id=id)
            return Response({
                "x": isData.x,
                "y": isData.y,
                "speed": isData.speed,
                "acceleration": isData.acceleration,
                "id": id,
                "lane": isData.lane
            })
        except Vehicle.DoesNotExist:
            return Response({
                "x": 0,
                "y": 0,
                "speed": 1,
                "acceleration": 0,
                "id": 0,
                "lane": 2
            })
        
    def get(self,request):
        output = [{"x":output.x,"y":output.y,"speed":output.speed,"acceleration":output.acceleration,"id":output.id,"lane":output.lane} for output in Vehicle.objects.all()]
        return Response(output)
    
    def post(self,request):
        serializer = VehicleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"error in post request"})
        
    def put(self,request):
        try:
            isData = Vehicle.objects.get(id=request.data.get('id'))
            isUpdated = VehicleSerializer(isData,data=request.data,partial=True)
            if isUpdated.is_valid(raise_exception=True):
                isUpdated.save()
                return Response(isUpdated.data)
            else:
                return Response({"error in put request"})
        except Vehicle.DoesNotExist:
            self.post(request)
        
    def delete(self,request):
        Vehicle.objects.all().delete()
        return Response({"message": "Data deleted successfully"})
        
        
def send_dictionary(request): 
    # create data dictionary 
    dataDictionary = { 
        'cars': 3,
        'trucks': 1,
        'intersection': 1,
        'roundabout': 1
    } 
    # dump data 
    dataJSON = dumps(dataDictionary) 
    return render(request, 'main / landing.html', {'data': dataJSON})

traffic_manager = TrafficManager()

def add_vehicle(request):
    if request.method == 'POST':
        vehicle = request.data.get('vehicle')
        traffic_manager.add_vehicle(vehicle)
        return Response({'message': 'Vehicle added successfully'})

def remove_vehicle(request):
    if request.method == 'POST':
        vehicle = request.data.get('vehicle')
        traffic_manager.remove_vehicle(vehicle)
        return Response({'message': 'Vehicle removed successfully'})
    
def detect_collision(request):
    if request.method == 'POST':
        traffic_manager.collision_model()
        return Response({'message': 'Collision detection performed'})