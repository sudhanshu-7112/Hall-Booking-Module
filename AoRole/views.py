from datetime import datetime, timedelta
from rest_framework import generics
from AoRole.models import Booked_Hall, Conference_Hall, Conference_Images, DynamicPanel, Hall_booking_Form, Pending_Bookings, UserDepartment
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User
# from rest_framework.throttling import UserRateThrottle
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from AoRole.serializers import AoApprovalSerializer, Conference_Hall_Places, Conference_HallSerializer, Conference_ImagesSerializer, DynamicPanelSerializer, Hall_book_Serializer, Hall_booking_Form_Serializer, HodApprovalSerializer, HodRoleSerializer, UserDepartmentSerializer, UserSerializer
from .user import IsSuperUser

# Create your views here.


class Halls(APIView):
    permission_classes = [IsSuperUser]

    def post(self, request):
        serializer = Conference_HallSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
            return Response(serializer.errors)

        Hall = serializer.data['id']
        files = request.FILES.getlist('image')
        for f in files:
            serializerimage = Conference_ImagesSerializer(
                data={'Hall': Hall, 'image': f})
            if serializerimage.is_valid():
                serializerimage.save()
            else:
                return Response(serializerimage.errors)
        return Response({'messgae': 'Uploaded Succesfully'}, status=status.HTTP_201_CREATED)

    def get(self, request):
        halls = Conference_Hall.objects.filter(occupied=False)
        serializer = Conference_HallSerializer(halls, many=True)
        return Response(serializer.data)


class hallimage(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        hall = self.kwargs.get('hall')
        return Conference_Images.objects.filter(Hall=hall)

    def get_serializer_class(self):
        return Conference_ImagesSerializer


class Userdetails(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    # throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        user = self.request.user.id
        return User.objects.filter(id=user)

    def get_serializer_class(self):
        return UserSerializer


class Register(APIView):
    permission_classes = [IsSuperUser]

    def post(self, request):
        user = User.objects.create_user(
            request.data['username'], request.data['email'], request.data['password'])
        user.first_name = request.data['first_name']
        user.last_name = request.data['last_name']
        user.save()
        return Response({'message': 'Succesfull'}, status=status.HTTP_201_CREATED)


class Panel(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    # throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        user = self.request.user
        if(user.is_superuser):
            return DynamicPanel.objects.filter(role='AO').order_by('-id')
        elif(user.is_staff):
            return DynamicPanel.objects.filter(role='HOD').order_by('-id')
        else:
            return DynamicPanel.objects.filter(role='EMP').order_by('-id')

    def get_serializer_class(self):
        return DynamicPanelSerializer


class Department_Names(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserDepartment.objects.all()
    serializer_class = UserDepartmentSerializer


class AllHall(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        range = request.data['range']
        fd = range[0]
        to = range[1]
        count = request.data['Participant_count']
        user = User.objects.get(id=request.user.id)
        pending = Pending_Bookings.objects.filter(user=user)
        if pending:
            pending[0].from_date = fd
            pending[0].to_date = to
            pending[0].Participant_count = count
            pending[0].save()
        else:
            Pending_Bookings.objects.create(
                user=user, from_date=fd, to_date=to, Participant_count=count)
        available_places = Pending_Bookings.objects.filter((Q(from_date__gt=fd) & Q(
            to_date__gt=to)) | (Q(to_date__lt=fd) & Q(to_date__lt=to)))
        serializer = Conference_Hall_Places(available_places, many=True)
        exclude_list = []
        for i in serializer.data:
            exclude_list.append(i['id'])
        available_places = Conference_Hall.objects.exclude(
            (Q(id__in=exclude_list)) | (Q(occupancy__lt=count)))
        serializer = Conference_Hall_Places(available_places, many=True)
        return Response(serializer.data)


class Book_Hall(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = self.request.user.username
        request.data['emp_name'] = user
        request.data['submit_time_emp'] = datetime.now()
        u = User.objects.get(id=request.user.id)
        temporary = Pending_Bookings.objects.filter(user=u)[0]
        request.data['from_date'] = temporary.from_date
        request.data['to_date'] = temporary.to_date
        request.data['Participant_count'] = temporary.Participant_count
        department = UserDepartment.objects.get(user=u)
        request.data['emp_department'] = department.department.id
        serializer = Hall_book_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            temporary.delete()
        else:
            print(serializer.errors)
            return Response(serializer.errors)
        return Response({'message': 'Succesfully Filled Form'}, status=status.HTTP_201_CREATED)


class Hallsdropdown(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Conference_Hall.objects.all()
    serializer_class = Conference_Hall_Places


class Hod_pending_forms(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        queryset = Hall_booking_Form.objects.exclude(
            Q(Hod_approval=True) | Q(Hod_approval=False))
        serializer = HodRoleSerializer(queryset, many=True)
        return Response(serializer.data)


class Hod_accepted_rejected(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        queryset = Hall_booking_Form.objects.filter(Hod_approval=pk)
        serializer = HodRoleSerializer(queryset, many=True)
        return Response(serializer.data)


class HodApproval(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        queryset = Hall_booking_Form.objects.get(id=pk)
        request.data['time_stamp_Hod'] = datetime.now()
        serializer = HodApprovalSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Succesfull'})
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AoApproval(APIView):
    permission_classes = [IsSuperUser]

    def put(self, request, pk):
        queryset = Hall_booking_Form.objects.get(id=pk)
        request.data['time_stamp_Ao'] = datetime.now()
        serializer = AoApprovalSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            if(request.data['booked'] == 1):
                queryset = Hall_booking_Form.objects.get(id=pk)
                hall = Conference_Hall.objects.get(id=request.data['hall'])
                Booked_Hall.objects.create(
                    from_date=queryset.from_date, to_date=queryset.to_date, hall=hall)
            return Response({'message': 'Succesfull'})
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ao_Report(APIView):
    permission_classes = [IsSuperUser]

    def get(self, request, pk):
        today = datetime.today()
        filtering = datetime.today()
        if(pk == 1):
            filtering = timedelta(days=1)
        elif(pk == 2):
            filtering = timedelta(days=7)
        elif(pk == 3):
            filtering = timedelta(days=30)
        elif(pk == 4):
            filtering = timedelta(day=365)
        filtering_date = today-filtering
        queryset = Hall_booking_Form.objects.filter(
            (Q(booked=True) | Q(booked=False)) & Q(submit_time_emp__gt=filtering_date))
        serializer = Conference_HallSerializer(queryset, many=True)
        return Response(serializer.data)


class Ao_Pending(generics.ListAPIView):
    permission_classes = [IsSuperUser]
    queryset = Hall_booking_Form.objects.exclude((
        Q(booked=True) | Q(booked=False)) |( Q(Hod_approval=None)))
    serializer_class = Hall_booking_Form_Serializer


class Ao_accepted_rejected(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        queryset = Hall_booking_Form.objects.filter(booked=pk)
        serializer = HodRoleSerializer(queryset, many=True)
        print(serializer.data['from_date'])
        return Response(serializer.data)


class Logout(APIView):

    def post(self, request):
        Refresh_token = request.data["refresh"]
        token = RefreshToken(Refresh_token)
        token.blacklist()
        return Response({"message": "Successful Logout"}, status=status.HTTP_200_OK)
