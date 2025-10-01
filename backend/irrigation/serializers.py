from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Sensor, ProgramacionRiego, RegistroRiego, LecturaSensor, Cultivo, Finca, PerfilUsuario
from rest_framework.reverse import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'}, label="Contraseña"
    )
    password2 = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'}, label="Confirmar contraseña"
    )
    telefono = serializers.CharField(write_only=True, required=True, max_length=15)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'telefono', 'password', 'password2']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password2": "Las contraseñas no coinciden."})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Este email ya está registrado."})
        return data

    def create(self, validated_data):
        telefono = validated_data.pop('telefono')
        validated_data.pop('password2')
        email = validated_data['email']

        base_username = email.split('@')[0]
        username = base_username
        while User.objects.filter(username=username).exists():
            username = f"{base_username}_{get_random_string(4)}"

        user = User.objects.create_user(
            username=username,
            email=email,
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_active=False
        )
        user.save()

        perfil, created = PerfilUsuario.objects.get_or_create(user=user)
        perfil.telefono = telefono
        perfil.save()
        return user


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD

    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError({"detail": "Se deben proveer email y contraseña."})

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "No existe un usuario con este email."})

        user = authenticate(username=user.username, password=password)
        if not user:
            raise serializers.ValidationError({"password": "Contraseña incorrecta."})

        refresh = self.get_token(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'


class ProgramacionRiegoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramacionRiego
        fields = '__all__'
class ProgramacionRiegoAdminSerializer(serializers.ModelSerializer):
    acciones = serializers.SerializerMethodField()
    
    class Meta:
        model = ProgramacionRiego
        fields = '__all__'

    def get_acciones(self, obj):
        request = self.context.get('request')
        if request is None:
            return {}

        return {
            'modificar': reverse('programacionriegoadmin-detail', args=[obj.pk], request=request),
            'eliminar': reverse('programacionriegoadmin-detail', args=[obj.pk], request=request),
        }

class RegistroRiegoSerializer(serializers.ModelSerializer):
    sensor = serializers.StringRelatedField()
    usuario = serializers.StringRelatedField()

    class Meta:
        model = RegistroRiego
        fields = ['id', 'sensor', 'usuario', 'inicio', 'duracion_minutos', 'activo']

class LecturaSensorSerializer(serializers.ModelSerializer):
    tipo = serializers.CharField(source='sensor.tipo', read_only=True)
    
    class Meta:
        model = LecturaSensor
        fields = ['id', 'sensor', 'valor', 'fecha_registro', 'cultivo', 'tipo']  

class CultivoSerializer(serializers.ModelSerializer):
    programaciones = ProgramacionRiegoSerializer(many=True, read_only=True)
    class Meta:
        model = Cultivo
        fields = ['id', 'nombre_cultivo', 'tipo_cultivo', 'numero_lotes', 'numero_aspersores', 'programaciones']

class FincaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finca
        fields = ['nombre', 'direccion', 'presentacion']

class UserDetailSerializer1(serializers.ModelSerializer):
    telefono = serializers.CharField(source='perfilusuario.telefono', allow_blank=True, required=False)
    avatar_url = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'telefono', 'avatar_url']
        
    def get_avatar_url(self, obj):
        if hasattr(obj, 'perfilusuario') and obj.perfilusuario.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.perfilusuario.avatar.url)
            return obj.perfilusuario.avatar.url
        return None  # O una URL default si quieres, ej: '/static/default-avatar.png'

    def update(self, instance, validated_data):
        perfil_data = validated_data.pop('perfilusuario', {})
        telefono = perfil_data.get('telefono')

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        perfil, created = PerfilUsuario.objects.get_or_create(user=instance)
        if telefono is not None:
            perfil.telefono = telefono
            perfil.save()
        
        return instance

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("No existe un usuario con ese email.")
        return value

    def save(self, **kwargs):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        print(f"DEBUG -> Token: {token}, UID: {uid}")

        context = {
            'username': user.first_name,
            'token': token,
            'uid': uid,
        }
        subject = 'Token para restablecer tu contraseña'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = user.email
        text_content = render_to_string('email/user_reset_password.txt', context)
        html_content = render_to_string('email/user_reset_password.html', context)

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()  

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True)
    password_confirm = serializers.CharField(min_length=8, write_only=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        return attrs
    
class AvatarSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=True)

    class Meta:
        model = User
        fields = ['avatar']

    def update(self, instance, validated_data):
        avatar = validated_data.get('avatar')
        if avatar:
            instance.avatar = avatar
            instance.save()
        return instance    

class PerfilUsuarioSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = PerfilUsuario
        fields = ['avatar_url', 'telefono']

    def get_avatar_url(self, obj):
        # CORREGIDO: Usar avatar_url en lugar de avatar
        if obj.avatar_url:
            return obj.avatar_url
        return None
