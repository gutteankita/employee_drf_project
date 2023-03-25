from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from Emp_App.models import *
from rest_framework.permissions import IsAuthenticated
from Emp_App.authentication import CustomAuthentication
import datetime
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password



# Create your views here.

# Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

# User ApiView
class UserRegistrationView(APIView):
    def post(self, request, format=None):
        if request.method == 'POST':
            try:
                data = request.data
                password = request.data.get('password')
                data['password'] = make_password(password)
                User.objects.create(**data)
                return Response({"message":"User Created Successfully"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({f"message":{str(e)}}, status=status.HTTP_400_BAD_REQUEST)
            
    def get(self, request, format=None):
        if request.method == 'GET':
            try:
                id = request.data.get('id',None)

                if id == None:
                    user_obj = User.objects.all().values()

                else:
                    user_obj = User.objects.filter(id=id).values()

                users = []
                for each_dict in user_obj:

                    users_data = {'id': each_dict.get('id'), 'username': each_dict.get('username'), 'email': each_dict.get('email'), 'is_active': each_dict.get('is_active'), 'is_admin': each_dict.get('is_admin'), 'is_user': each_dict.get('is_user'), 'created_at': each_dict.get('created_at'), 'updated_at': each_dict.get('updated_at')}

                    users.append(users_data)

                return Response({'users': users})
            except Exception as e:
                return Response({f"message":{str(e)}}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        if request.method == "PUT":
            try:
                id = request.data.get('id')
                username = request.data.get('username')
                email = request.data.get('email')
                password = request.data.get('password')
                password = make_password(password)
                is_active = request.data.get('is_active')
                is_admin = request.data.get('is_admin')
                is_user = request.data.get('is_user')
                updated_at = datetime.datetime.now()
                
                User.objects.filter(id = id).update(username=username, email=email, password=password, is_active=is_active, is_admin=is_admin, is_user=is_user, updated_at=updated_at)

                return Response({"message":"User Updated Successfully"})
            except Exception as e:
                return Response({f"message":{str(e)}}, status=status.HTTP_400_BAD_REQUEST)    
                
    def delete(self, request, format=None):
        if request.method == 'DELETE':
            try:
                id = request.data.get('id')
                user = User.objects.get(id=id)
                user.delete()
                return Response({"message":"User Deleted Successfully"},status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                return Response({f"message":{str(e)}}, status=status.HTTP_400_BAD_REQUEST)

# User LoginView
class UserLoginView(APIView):
    def post(self, request, format=None):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            user = User.objects.get(email=email)
            updated_at = datetime.datetime.now()
            User.objects.filter(email = email).update(updated_at=updated_at)
            if user is not None and user.check_password(password):
                token = get_tokens_for_user(user)
                check_token = BlackListedToken.objects.filter(user_id = user.id)
                check_token.delete()
                content = BlackListedToken.objects.create(token = token, user_id = user.id)
                content.save()
               
                return Response({'token': token, 'msg': 'Login Success', 'id': user.id, "is_admin":user.is_admin, 'is_user':user.is_user, 'updated_at': updated_at}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({f"message":{str(e)}}, status=status.HTTP_400_BAD_REQUEST)
        
# Employee APIView

class EmployeeApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomAuthentication]
    def post(self, request, format=None):
        try:
            name = request.data.get('name')
            age = request.data.get('age')
                
            gender = request.data.get('gender', '').upper()
            valid_choices = [choice[0] for choice in Employee.GENDER_CHOICES]

            department = request.data.get('department')
            salary = request.data.get('salary')

            if age>60 and gender not in valid_choices:
                return Response({'error': 'Employee age cannot be more than 60 AND Employee Gender should M,F or T'}, status=status.HTTP_400_BAD_REQUEST)

            elif gender not in valid_choices:
                return Response({'error': 'Employee Gender should M,F or T'}, status=status.HTTP_400_BAD_REQUEST)
            
            elif age > 60:
                return Response({'error': 'Employee age cannot be more than 60'}, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                
                content = Employee.objects.create(name=name,age=age,gender=gender, department=department, salary=salary)
                content.save()

                return Response({'Message': 'Employee created successfully'}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({f"Message":str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        try:
            id = request.data.get('id', None)
            if id == None:
                page_number = request.query_params.get('page', 1)
                per_page = request.query_params.get('per_page', 10)
                
                employees = Employee.objects.all()
                paginator = Paginator(employees, per_page)
                page_obj = paginator.get_page(page_number)
                
                employee_list = []
                for employee in page_obj:
                    employee_dict = {
                        'id': employee.id,
                        'name': employee.name,
                        'age': employee.age,
                        'gender': employee.gender,
                        'department': employee.department,
                        'salary': employee.salary
                    }
                    employee_list.append(employee_dict)
                
                return Response({'employees': employee_list, 'total_records': paginator.count})
            else:
                emp_obj = Employee.objects.get(id=id)
                employee = {'id':emp_obj.id, 'name':emp_obj.name, 'age':emp_obj.age, 'gender':emp_obj.gender, 'department':emp_obj.department, 'salary':emp_obj.salary}
            return Response({'employee':employee})
        except Exception as e:
            return Response({f'msg':str(e)},status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            id = request.data.get('id')
            name = request.data.get('name')
            age = request.data.get('age')

            gender = request.data.get('gender', '').upper()
            valid_choices = [choice[0] for choice in Employee.GENDER_CHOICES]

            department = request.data.get('department')
            salary = request.data.get('salary')
            
            if age>60 and gender not in valid_choices:
                return Response({'error': 'Employee age cannot be more than 60 AND Employee Gender should M,F or T'}, status=status.HTTP_404_NOT_FOUND)

            elif gender not in valid_choices:
                return Response({'error': 'Employee Gender should M,F or T'}, status=status.HTTP_404_NOT_FOUND)
            
            elif age > 60:
                return Response({'error': 'Employee age cannot be more than 60 '}, status=status.HTTP_404_NOT_FOUND)

            else:
                
                Employee.objects.filter(id = id).update(name=name, age=age, gender=gender, department=department, salary=salary)
                return Response({"Message":"Employee Updated Successfully"}, status=status.HTTP_200_OK)
            
            
        except Exception as e:
            return Response({f'Message':str(e)},status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, format=None):
        try:
            id = request.data.get('id')
            employee = Employee.objects.get(id = id)
            employee.delete()
            return Response({"Message":"Employee Deleted Successfully"},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({f'Message':str(e)},status=status.HTTP_400_BAD_REQUEST)


            

