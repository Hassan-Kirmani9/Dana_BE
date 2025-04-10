# miqaat/urls.py

from django.urls import path
from .views import (
    CounterDetailView,
    CounterView,
    FilterMiqaatByTypeView,
    ListCounterView,
    ListMiqaatView,
    LoginView,
    MiqaatView,
    MiqaatDetailView,
    ListZoneView,
    SignupView,
    ZoneView,
    ZoneDetailView,
    ListMenuView,
    MenuView,
    MenuDetailView,
    ListMemberView,
    MemberView,
    MemberDetailView,
    ListUnitView,
    UnitView,
    UnitDetailView,
    ListContainerView,
    ContainerView,
    ContainerDetailView,
    ListMiqaatAttendanceView,
    MiqaatAttendanceView,
    MiqaatAttendanceDetailView,
    ListMiqaatZoneView,
    MiqaatZoneView,
    MiqaatZoneDetailView,
    ListMiqaatMenuView,
    MiqaatMenuView,
    MiqaatMenuDetailView,
    ListCounterPackingView,
    CounterPackingView,
    CounterPackingDetailView,
    ListDistributionView,
    DistributionView,
    DistributionDetailView,
    ListLeftOverDegsView,
    LeftOverDegsView,
    LeftOverDegsDetailView,
)

urlpatterns = [
    path("miqaat/list/", ListMiqaatView.as_view(), name="list-miqaat"),
    path("miqaat/", MiqaatView.as_view(), name="create-miqaat"),
    path("miqaat/<int:pk>/", MiqaatDetailView.as_view(), name="miqaat-detail"),
    path('miqaat/filter/', FilterMiqaatByTypeView.as_view(), name='filter-miqaat-by-type'),
    
    path("zone/list/", ListZoneView.as_view(), name="list-zone"),
    path("zone/", ZoneView.as_view(), name="create-zone"),
    path("zone/<int:pk>/", ZoneDetailView.as_view(), name="zone-detail"),
    
    path("menu/list/", ListMenuView.as_view(), name="list-menu"),
    path("menu/", MenuView.as_view(), name="create-menu"),
    path("menu/<int:pk>/", MenuDetailView.as_view(), name="menu-detail"),
    
    path("member/list/", ListMemberView.as_view(), name="list-member"),
    path("member/", MemberView.as_view(), name="create-member"),
    path("member/<int:pk>/", MemberDetailView.as_view(), name="member-detail"),
    
    path("unit/list/", ListUnitView.as_view(), name="list-unit"),
    path("unit/", UnitView.as_view(), name="create-unit"),
    path("unit/<int:pk>/", UnitDetailView.as_view(), name="unit-detail"),
    
    path("container/list/", ListContainerView.as_view(), name="list-container"),
    path("container/", ContainerView.as_view(), name="create-container"),
    path("container/<int:pk>/", ContainerDetailView.as_view(), name="container-detail"),
    
    path("miqaat-attendance/list/", ListMiqaatAttendanceView.as_view(), name="list-miqaat-attendance", ),
    path("miqaat-attendance/", MiqaatAttendanceView.as_view(), name="create-miqaat-attendance", ),
    path("miqaat-attendance/<int:pk>/", MiqaatAttendanceDetailView.as_view(), name="miqaat-attendance-detail", ),
    
    path("miqaat-zone/list/", ListMiqaatZoneView.as_view(), name="list-miqaat-zone"),
    path("miqaat-zone/", MiqaatZoneView.as_view(), name="create-miqaat-zone"),
    path( "miqaat-zone/<int:pk>/", MiqaatZoneDetailView.as_view(), name="miqaat-zone-detail", ),
    
    path("miqaat-menu/list/", ListMiqaatMenuView.as_view(), name="list-miqaat-menu"),
    path("miqaat-menu/", MiqaatMenuView.as_view(), name="create-miqaat-menu"),
    path("miqaat-menu/<int:pk>/", MiqaatMenuDetailView.as_view(), name="miqaat-menu-detail"),
    
    path("counter-packing/list/", ListCounterPackingView.as_view(), name="list-counter-packing", ),
    path("counter-packing/", CounterPackingView.as_view(), name="create-counter-packing", ),
    path("counter-packing/<int:pk>/", CounterPackingDetailView.as_view(), name="counter-packing-detail", ),
    
    path("distribution/list/", ListDistributionView.as_view(), name="list-distribution"),
    path("distribution/", DistributionView.as_view(), name="create-distribution" ),
    path("distribution/<int:pk>/", DistributionDetailView.as_view(), name="distribution-detail", ),
    
    path("leftover-degs/list/", ListLeftOverDegsView.as_view(), name="list-leftover-degs"),
    path("leftover-degs/", LeftOverDegsView.as_view(), name="create-leftover-degs" ),
    path("leftover-degs/<int:pk>/", LeftOverDegsDetailView.as_view(), name="leftover-degs-detail", ),
    
    path('counter/list/', ListCounterView.as_view(), name='list-counter'),
    path('counter/', CounterView.as_view(), name='create-counter'),
    path('counter/<int:pk>/', CounterDetailView.as_view(), name='counter-detail'),

    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),


]
