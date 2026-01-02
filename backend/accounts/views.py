from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from .serializers import UserSerializer, RegisterSerializer
from .tasks import send_email_task
from tasks.models import Task
import uuid

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    User registration endpoint.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            'user': UserSerializer(user).data,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """
    User login endpoint.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {'error': 'Please provide both email and password'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.check_password(password):
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            return Response(
                {'error': 'Account is disabled'},
                status=status.HTTP_403_FORBIDDEN
            )

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    Get or update user profile.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class AdminOverviewView(APIView):
    """
    Admin endpoint to get overview of users and their tasks.
    Only accessible by staff/superuser.
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        users = User.objects.annotate(
            total_tasks=Count('tasks'),
            open_tasks=Count('tasks', filter=Q(tasks__status__in=['TODO', 'DOING']))
        ).values(
            'id',
            'email',
            'username',
            'is_active',
            'total_tasks',
            'open_tasks'
        )

        return Response({
            'users': list(users),
            'total_users': User.objects.count(),
            'active_users': User.objects.filter(is_active=True).count()
        })


class AdminNotifyView(APIView):
    """
    Admin endpoint to send email notifications to users.
    Only accessible by staff/superuser.
    """
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        recipients = request.data.get('recipients', [])
        message = request.data.get('message', '')
        subject = request.data.get('subject', 'Notification from TaskBoard')

        if not recipients:
            return Response(
                {'error': 'Recipients list is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not message:
            return Response(
                {'error': 'Message is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Generate unique job ID
        job_id = str(uuid.uuid4())

        # Queue email task
        task = send_email_task.apply_async(
            args=[recipients, subject, message],
            task_id=job_id
        )

        return Response({
            'job_id': job_id,
            'task_id': task.id,
            'status': 'queued',
            'message': f'Email notification queued for {len(recipients)} recipients'
        }, status=status.HTTP_202_ACCEPTED)
