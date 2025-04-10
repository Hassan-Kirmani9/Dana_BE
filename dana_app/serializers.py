from rest_framework import serializers
from .models import *

from django.contrib.auth import get_user_model

User = get_user_model()

class MiqaatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Miqaat
        fields = '__all__'

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class ReadMemberSerializer(serializers.ModelSerializer):
    counter_name = serializers.SerializerMethodField()
    zone_name= serializers.CharField(source='zone.name')
    class Meta:
        model = Member
        fields = ['id', 'its', 'full_name', 'zone_name', 'counter_name', 'contact_number', 'whatsapp_number', 'email_address', 'mohalla']
    
    def get_counter_name(self, obj):
        return obj.counter.name if hasattr(obj, 'counter') and obj.counter else None

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'

class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = '__all__'

class CounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Counter
        fields = '__all__'

class ReadMiqaatAttendanceSerializer(serializers.ModelSerializer):

    member_id= serializers.IntegerField(source='member.id')
    member_name= serializers.CharField(source='member.full_name')

    counter_id= serializers.IntegerField(source='counter.id')
    counter_name= serializers.CharField(source='counter.name')
    
    zone_id= serializers.IntegerField(source='zone.id')
    zone_name= serializers.CharField(source='zone.name')

    class Meta:
        model = MiqaatAttendance
        fields = ['id', 'miqaat_id', 'member_id', 'member_name', 'counter_id', 'counter_name', 'zone_id', 'zone_name', 'checkin_time', 'checkout_time']

class MiqaatAttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = MiqaatAttendance
        fields = '__all__'

class MiqaatZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiqaatZone
        fields = '__all__'

class MiqaatMenuSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MiqaatMenu
        fields = '__all__'

class ReadMiqaatMenuSerializer(serializers.ModelSerializer):
    menu_id = serializers.IntegerField(source='menu.id')
    menu_name= serializers.CharField(source='menu.name')
    menu_description= serializers.CharField(source='menu.description')
    
    class Meta:
        model = MiqaatMenu
        fields = ['id', 'miqaat_id','menu_description', 'menu_id', 'menu_name']

class CounterPackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CounterPacking
        fields = '__all__'
    
class ReadCounterPackingSerializer(serializers.ModelSerializer):

    miqaat_menu_id = serializers.IntegerField(source='miqaat_menu.id')
    menu_id= serializers.IntegerField(source='miqaat_menu.menu.id')
    menu_name= serializers.CharField(source='miqaat_menu.menu.name')
    unit_id= serializers.IntegerField(source='unit.id')
    unit_name= serializers.CharField(source='unit.name')
    container_id= serializers.IntegerField(source='container.id')
    container_name= serializers.CharField(source='container.name')
    zone_id= serializers.IntegerField(source='zone.id')
    zone_name= serializers.CharField(source='zone.name')
    
    class Meta:
        model = CounterPacking
        fields = ['id', 'miqaat_menu_id','zone_id','zone_name','menu_id', 'menu_name', 'unit_id', 'unit_name', 'container_id', 'container_name', 'filled_percentage', 'quantity']

class DistributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distribution
        fields = '__all__'

class ReadDistributionSerializer(serializers.ModelSerializer):
   
    counter_packing_id= serializers.IntegerField(source='counter_packing.id')
    menu_id= serializers.IntegerField(source='counter_packing.miqaat_menu.menu.id')
    menu_name= serializers.CharField(source='counter_packing.miqaat_menu.menu.name')
    unit_id= serializers.IntegerField(source='counter_packing.unit.id')
    unit_name= serializers.CharField(source='counter_packing.unit.name')
    container_id= serializers.IntegerField(source='counter_packing.container.id')
    container_name= serializers.CharField(source='counter_packing.container.name')
    filled_percentage= serializers.FloatField(source='counter_packing.filled_percentage')
    quantity= serializers.IntegerField(source='counter_packing.quantity')
    zone_id= serializers.IntegerField(source='zone.id')
    zone_name= serializers.CharField(source='zone.name')

    class Meta:
        model = Distribution
        fields = ['id', 'miqaat_id','zone_id','zone_name', 'counter_packing_id', 'menu_id', 'menu_name', 'unit_id', 'unit_name', 'container_id', 'container_name', 'filled_percentage', 'quantity','ibadullah_count','mumin_count']

class LeftOverDegsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeftOverDegs
        fields = '__all__'

class ReadLeftOverDegsSerializer(serializers.ModelSerializer):

    container_id= serializers.IntegerField(source='container.id')
    container_name= serializers.CharField(source='container.name')
    menu_id= serializers.IntegerField(source='menu.id')
    menu_name= serializers.CharField(source='menu.name')
    unit_id= serializers.IntegerField(source='unit.id')
    unit_name= serializers.CharField(source='unit.name')
    zone_id= serializers.IntegerField(source='zone.id')
    zone_name= serializers.CharField(source='zone.name')

    class Meta:
        model = LeftOverDegs
        fields = ['id', 'miqaat_id', 'menu_id', 'menu_name', 'unit_id', 'unit_name', 'zone_id', 'zone_name', 'container_id', 'container_name', 'total_cooked','total_received']


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

