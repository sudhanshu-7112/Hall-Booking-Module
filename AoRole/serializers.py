from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from rest_framework import serializers
from AoRole.models import Conference_Hall, Conference_Images, Departments, DynamicPanel, Hall_booking_Form, UserDepartment
# from AoRole.views import Book_Hall


class JWTAuthentication(TokenObtainPairSerializer):

    def validate(self, attrs):
        credentials = {
            'username': '',
            'password': attrs.get("password")
        }
        user_obj = User.objects.filter(email=attrs.get("username"))
        if user_obj:
            credentials['username'] = user_obj[0].username

        return super().validate(credentials)


class Conference_HallSerializer(serializers.ModelSerializer):

    class Meta:
        model = Conference_Hall
        fields = '__all__'
        # extra_kwargs = {'Description': {'required': False}}


class Conference_Hall_Places(serializers.ModelSerializer):

    class Meta:
        model = Conference_Hall
        fields = ('id', 'Hall_name')


class Conference_ImagesSerializer(serializers.ModelSerializer):
    hall = Conference_HallSerializer(read_only=True, many=True)

    class Meta:
        model = Conference_Images
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class DynamicPanelSerializer(serializers.ModelSerializer):

    class Meta:
        model = DynamicPanel
        fields = ('name', 'url')


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Departments
        fields = '__all__'

class Hall_booking_Form_Serializer(serializers.ModelSerializer):
    emp_department = serializers.CharField(
        source='emp_department.department.department')
    # Hall_name=serializers.CharField(source='Hall_name.Hall_name')

    class Meta:
        model = Hall_booking_Form
        fields = '__all__'
        depth = 1


class Hall_book_Serializer(serializers.ModelSerializer):
    emp_department = serializers.CharField(
        source='emp_department.department.department')
    Hall_name = serializers.CharField(source='Hall_name.Hall_name')

    class Meta:
        model = Hall_booking_Form
        fields = '__all__'


class HodRoleSerializer(serializers.ModelSerializer):
    emp_department = serializers.CharField(
        source='emp_department.department.department')
    Hall_name = serializers.CharField(source='Hall_name.Hall_name')

    class Meta:
        model = Hall_booking_Form
        exclude = ('time_stamp_Hod', 'Ao_remark',
                   'time_stamp_AO', 'booked', 'Hod_approval')


class HodApprovalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hall_booking_Form
        fields = ('Hod_approval', 'time_stamp_Hod')


class AoApprovalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hall_booking_Form
        fields = ('booked', 'time_stamp_AO')
