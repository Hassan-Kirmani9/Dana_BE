from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login

class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(email=serializer.validated_data["email"], password=serializer.validated_data["password"])
        
        if user is not None:
            django_login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email
                }
            })
        else:
            return Response({"message": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

# Miqaat
class ListMiqaatView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MiqaatSerializer

    def get_queryset(self):
        return Miqaat.objects.all()

class MiqaatView(APIView):
    # permission_classes = [IsAuthenticated]
    @transaction.atomic
    def post(self, request):
        serializer = MiqaatSerializer(data=request.data)
        if serializer.is_valid():
            miqaat = serializer.save()
            return Response({"message": f"Miqaat created with ID {miqaat.id}"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MiqaatDetailView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        miqaat = get_object_or_404(Miqaat, pk=pk)
        serializer = MiqaatSerializer(miqaat)
        return Response(serializer.data)

    def patch(self, request, pk):
        miqaat = get_object_or_404(Miqaat, pk=pk)
        serializer = MiqaatSerializer(miqaat, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        miqaat = Miqaat.objects.get(pk=pk)
        miqaat.delete()
        return Response({"message": "Miqaat deleted successfully"}, status=status.HTTP_200_OK)
       
class FilterMiqaatByTypeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        miqaat_type = request.query_params.get('miqaat_type')
        
        if not miqaat_type:
            return Response({"error": "miqaat_type query param is required."}, status=status.HTTP_400_BAD_REQUEST)

        valid_types = dict(Miqaat.EVENT_TYPES).keys()
        if miqaat_type not in valid_types:
            return Response({"error": f"Invalid miqaat_type. Valid options are: {', '.join(valid_types)}"},
                            status=status.HTTP_400_BAD_REQUEST)

        miqaats = Miqaat.objects.filter(miqaat_type=miqaat_type)
        serializer = MiqaatSerializer(miqaats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
# Zone
class ListZoneView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ZoneSerializer

    def get_queryset(self):
        return Zone.objects.all()

class ZoneView(APIView):
    permission_classes = [IsAuthenticated]
    @transaction.atomic
    def post(self, request):
        serializer = ZoneSerializer(data=request.data)
        if serializer.is_valid():
            zone = serializer.save()
            return Response({"message": f"Zone created with ID {zone.id}"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ZoneDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        zone = get_object_or_404(Zone, pk=pk)
        serializer = ZoneSerializer(zone)
        return Response(serializer.data)

    def patch(self, request, pk):
        zone = get_object_or_404(Zone, pk=pk)
        serializer = ZoneSerializer(zone, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        zone = get_object_or_404(Zone, pk=pk)
        zone.delete()
        return Response({"message": "Zone deleted successfully"}, status=status.HTTP_200_OK)

# Menu
class ListMenuView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MenuSerializer

    def get_queryset(self):
        return Menu.objects.all()

class MenuView(APIView):
    permission_classes = [IsAuthenticated]
    @transaction.atomic
    def post(self, request):
        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            menu = serializer.save()
            return Response({"message": f"Menu created with ID {menu.id}"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MenuDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        menu = get_object_or_404(Menu, pk=pk)
        serializer = MenuSerializer(menu)
        return Response(serializer.data)

    def patch(self, request, pk):
        menu = get_object_or_404(Menu, pk=pk)
        serializer = MenuSerializer(menu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        menu = get_object_or_404(Menu, pk=pk)
        menu.delete()
        return Response({"message": "Menu deleted successfully"}, status=status.HTTP_200_OK)

# Member
class ListMemberView(ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = ReadMemberSerializer

    def get_queryset(self):
        return Member.objects.all()

class MemberView(APIView):
    permission_classes = [IsAuthenticated]
    @transaction.atomic
    def post(self, request):
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            member = serializer.save()
            return Response({"message": f"Member created with ID {member.id}"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MemberDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        member = get_object_or_404(Member, pk=pk)
        serializer = MemberSerializer(member)
        return Response(serializer.data)

    def patch(self, request, pk):
        member = get_object_or_404(Member, pk=pk)
        serializer = MemberSerializer(member, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        member = get_object_or_404(Member, pk=pk)
        member.delete()
        return Response({"message": "Member deleted successfully"}, status=status.HTTP_200_OK)

# Unit
class ListUnitView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UnitSerializer

    def get_queryset(self):
        return Unit.objects.all()

class UnitView(APIView):
    permission_classes = [IsAuthenticated]
    @transaction.atomic
    def post(self, request):
        serializer = UnitSerializer(data=request.data)
        if serializer.is_valid():
            unit = serializer.save()
            return Response({"message": f"Unit created with ID {unit.id}"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UnitDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        unit = get_object_or_404(Unit, pk=pk)
        serializer = UnitSerializer(unit)
        return Response(serializer.data)

    def patch(self, request, pk):
        unit = get_object_or_404(Unit, pk=pk)
        serializer = UnitSerializer(unit, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        unit = get_object_or_404(Unit, pk=pk)
        unit.delete()
        return Response({"message": "Unit deleted successfully"}, status=status.HTTP_200_OK)

# Container
class ListContainerView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ContainerSerializer

    def get_queryset(self):
        return Container.objects.all()

class ContainerView(APIView):
    permission_classes = [IsAuthenticated]
    @transaction.atomic
    def post(self, request):
        serializer = ContainerSerializer(data=request.data)
        if serializer.is_valid():
            container = serializer.save()
            return Response({"message": f"Container created with ID {container.id}"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContainerDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        container = get_object_or_404(Container, pk=pk)
        serializer = ContainerSerializer(container)
        return Response(serializer.data)

    def patch(self, request, pk):
        container = get_object_or_404(Container, pk=pk)
        serializer = ContainerSerializer(container, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        container = get_object_or_404(Container, pk=pk)
        container.delete()
        return Response({"message": "Container deleted successfully"}, status=status.HTTP_200_OK)

# MiqaatAttendance
class ListMiqaatAttendanceView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReadMiqaatAttendanceSerializer

    def get_queryset(self):
        return MiqaatAttendance.objects.all()

class MiqaatAttendanceView(APIView):
    permission_classes = [IsAuthenticated]
    @transaction.atomic
    def post(self, request):
        serializer = MiqaatAttendanceSerializer(data=request.data)
        if serializer.is_valid():
            attendance = serializer.save()
            return Response({"message": f"MiqaatAttendance created with ID {attendance.id}"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MiqaatAttendanceDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        attendance = MiqaatAttendance.objects.filter(miqaat_id=pk)
        serializer = ReadMiqaatAttendanceSerializer(attendance, many=True)
        return Response({
            "miqaat_attendance": serializer.data
        })

    def patch(self, request, pk):
        attendance = get_object_or_404(MiqaatAttendance, pk=pk)
        serializer = MiqaatAttendanceSerializer(attendance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        attendance = get_object_or_404(MiqaatAttendance, pk=pk)
        attendance.delete()
        return Response({"message": "MiqaatAttendance deleted successfully"}, status=status.HTTP_200_OK)

# MiqaatZone
class ListMiqaatZoneView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MiqaatZoneSerializer

    def get_queryset(self):
        return MiqaatZone.objects.all()

class MiqaatZoneView(APIView):
    permission_classes = [IsAuthenticated]
    @transaction.atomic
    def post(self, request):
        serializer = MiqaatZoneSerializer(data=request.data)
        if serializer.is_valid():
            zone = serializer.save()
            return Response({"message": f"MiqaatZone created with ID {zone.id}"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MiqaatZoneDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        zone = get_object_or_404(MiqaatZone, pk=pk)
        serializer = MiqaatZoneSerializer(zone)
        return Response(serializer.data)

    def patch(self, request, pk):
        zone = get_object_or_404(MiqaatZone, pk=pk)
        serializer = MiqaatZoneSerializer(zone, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        zone = get_object_or_404(MiqaatZone, pk=pk)
        zone.delete()
        return Response({"message": "MiqaatZone deleted successfully"}, status=status.HTTP_200_OK)

# MiqaatMenu
class ListMiqaatMenuView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReadMiqaatMenuSerializer

    def get_queryset(self):
        return MiqaatMenu.objects.all()

class MiqaatMenuView(APIView):
    permission_classes = [IsAuthenticated]
    @transaction.atomic
    def post(self, request):
        serializer = MiqaatMenuSerializer(data=request.data)
        if serializer.is_valid():
            menu = serializer.save()
            return Response({"message": f"MiqaatMenu created with ID {menu.id}"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MiqaatMenuDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        menu = MiqaatMenu.objects.filter(miqaat_id=pk)
        serializer = ReadMiqaatMenuSerializer(menu, many=True)
        return Response({
            "miqaat_menu": serializer.data
        })

    def patch(self, request, pk):
        menu = get_object_or_404(MiqaatMenu, pk=pk)
        serializer = MiqaatMenuSerializer(menu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        menu = get_object_or_404(MiqaatMenu, pk=pk)
        menu.delete()
        return Response({"message": "MiqaatMenu deleted successfully"}, status=status.HTTP_200_OK)

# CounterPacking
class ListCounterPackingView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReadCounterPackingSerializer

    def get_queryset(self):
        return CounterPacking.objects.all()

class CounterPackingView(APIView):
    permission_classes = [IsAuthenticated]
    @transaction.atomic
    def post(self, request):
        serializer = CounterPackingSerializer(data=request.data)
        if serializer.is_valid():
            cp = serializer.save()
            return Response({"message": f"CounterPacking created with ID {cp.id}"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CounterPackingDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        cp = CounterPacking.objects.filter(miqaat_id=pk)
        serializer = ReadCounterPackingSerializer(cp, many=True)
        return Response({
            "counter_packing": serializer.data
        })

    def patch(self, request, pk):
        cp = get_object_or_404(CounterPacking, pk=pk)
        serializer = CounterPackingSerializer(cp, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        cp = get_object_or_404(CounterPacking, pk=pk)
        cp.delete()
        return Response({"message": "CounterPacking deleted successfully"}, status=status.HTTP_200_OK)

# Distribution
class ListDistributionView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReadDistributionSerializer

    def get_queryset(self):
        return Distribution.objects.all()

class DistributionView(APIView):
    permission_classes = [IsAuthenticated]
    @transaction.atomic
    def post(self, request):
        serializer = DistributionSerializer(data=request.data)
        if serializer.is_valid():
            dist = serializer.save()
            return Response({"message": f"Distribution created with ID {dist.id}"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DistributionDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        dist = Distribution.objects.filter(miqaat_id=pk)
        serializer = ReadDistributionSerializer(dist, many=True)
        return Response({
            "distributions": serializer.data
        })

    def patch(self, request, pk):
        dist = get_object_or_404(Distribution, pk=pk)
        serializer = DistributionSerializer(dist, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        dist = get_object_or_404(Distribution, pk=pk)
        dist.delete()
        return Response({"message": "Distribution deleted successfully"}, status=status.HTTP_200_OK)

# LeftOverDegs
class ListLeftOverDegsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReadLeftOverDegsSerializer

    def get_queryset(self):
        return LeftOverDegs.objects.all()

class LeftOverDegsView(APIView):
    permission_classes = [IsAuthenticated]
    @transaction.atomic
    def post(self, request):
        serializer = LeftOverDegsSerializer(data=request.data)
        if serializer.is_valid():
            deg = serializer.save()
            return Response({"message": f"LeftOverDeg created with ID {deg.id}"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LeftOverDegsDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        deg = LeftOverDegs.objects.filter(miqaat_id=pk)
        serializer = ReadLeftOverDegsSerializer(deg, many=True)
        return Response({
            "leftover_degs": serializer.data
        })

    def patch(self, request, pk):
        deg = get_object_or_404(LeftOverDegs, pk=pk)
        serializer = LeftOverDegsSerializer(deg, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        deg = get_object_or_404(LeftOverDegs, pk=pk)
        deg.delete()
        return Response({"message": "LeftOverDeg deleted successfully"}, status=status.HTTP_200_OK)


# Counter
class ListCounterView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CounterSerializer

    def get_queryset(self):
        return Counter.objects.all()

class CounterView(APIView):
    permission_classes = [IsAuthenticated]
    @transaction.atomic
    def post(self, request):
        serializer = CounterSerializer(data=request.data)
        if serializer.is_valid():
            counter = serializer.save()
            return Response(
                {"message": f"Counter created with ID {counter.id}"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CounterDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        counter = get_object_or_404(Counter, pk=pk)
        serializer = CounterSerializer(counter)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        counter = get_object_or_404(Counter, pk=pk)
        serializer = CounterSerializer(counter, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        counter = get_object_or_404(Counter, pk=pk)
        counter.delete()
        return Response(
            {"message": "Counter deleted successfully"},
            status=status.HTTP_200_OK,
        )

