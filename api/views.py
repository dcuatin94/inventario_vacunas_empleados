from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, viewsets

from .serializers import EmpleadoSerializers, EmpleadoUpdateSerializers, DosisSerializers
from .models import Empleado, UserProfile, Dosis


@extend_schema_view(
    list=extend_schema(description='Permite listar los empleados'),
    retrieve=extend_schema(description='Permite obtener un empleado'),
    update=extend_schema(description='Permite actualizar un empleado'),
    destroy=extend_schema(description='Permite eliminar un empleado')
)
class EmpleadoViewSet(viewsets.ModelViewSet):
    serializer_class = EmpleadoSerializers
    queryset = Empleado.objects.filter(deleted=False)

    @extend_schema(parameters=[
        OpenApiParameter(
            name='vacunado',
            description='Vacunados (True) No vacunados (False)',
            type=bool,
        ),
    ],
        filters=True
    )
    def list(self, request, *args, **kwargs):
        if check_role_admin(request) == False:
            return Response(['El usuario no tiene permitido realizar esta accion'])
        data = list()
        if self.request.query_params.get('vacunado'):
            vacunado = True if self.request.query_params.get('vacunado') == 'true' else False
            self.queryset = self.queryset.filter(vacunado=vacunado)
            try:
                for empleado in self.queryset:
                    dosis = Dosis.objects.filter(empleado=empleado)
                    serializer_dosis = DosisSerializers(dosis, many=True)
                    data.append({
                        'id': empleado.id,
                        'cedula': empleado.cedula,
                        'nombres': empleado.nombres,
                        'apellidos': empleado.apellidos,
                        'email': empleado.email,
                        'fecha_nacimiento': empleado.fecha_nacimiento,
                        'direccion_domicilio': empleado.direccion_domicilio,
                        'celular': empleado.celular,
                        'vacunado': empleado.vacunado,
                        'dosis': len(dosis),
                        'vacunas': serializer_dosis.data if vacunado else []
                    })
                return Response(data)
            except Exception as e:
                print(e)
        serializer = EmpleadoSerializers(self.queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=EmpleadoSerializers,
        responses={201: EmpleadoSerializers},
        description='Permite crear un empleado y retorna el email como username y el password es su cedula'
    )
    def create(self, request, *args, **kwards):
        if check_role_admin(request) == False:
            return Response(['El usuario no tiene permitido realizar esta accion'])
        try:
            empleado = EmpleadoSerializers(data=request.data)

            if empleado.is_valid():
                user_id = UserProfile.objects.create_user(
                    email=empleado.validated_data['email'], first_name=empleado.validated_data['nombres'],
                    last_name=empleado.validated_data['apellidos'], password=empleado.validated_data['cedula']
                )
                empleado_id = empleado.save()
                empleado_id.user = user_id
                empleado.save()

                return Response({
                    'empleado': empleado.data,
                    'usuario': {'username': empleado_id.email, 'password': empleado_id.cedula}
                })
            else:
                return Response(empleado.errors, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'message': 'Error al crear el empleado', 'Server Internal': str(e)})

    def retrieve(self, request, pk=None):
        empleado = get_object_or_404(Empleado, pk=pk)
        if empleado:
            if request.user.id != empleado.user.id and check_role_admin(request) == False:
                return Response(['Este usuario no tiene permiso para realizar esta accion'])
            serializer = EmpleadoSerializers(self.queryset.filter(pk=pk), many=True)
            return Response(serializer.data)
        return Response(['Empleado no existe'])

    @extend_schema(
        request=EmpleadoUpdateSerializers,
        responses={201: EmpleadoUpdateSerializers}
    )
    def update(self, request, pk=None):
        empleado = get_object_or_404(Empleado, pk=pk)
        if request.user.id != empleado.user.id and check_role_admin(request) == False:
            return Response(['Este usuario no tiene permiso para realizar esta accion'])
        try:
            empleado = get_object_or_404(Empleado, pk=pk)
            empleado_update = EmpleadoUpdateSerializers(empleado, data=request.data)
            if empleado_update.is_valid():
                empleado_update.save()
                return Response(empleado_update.data)
            else:
                return Response(empleado_update.errors, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'message', 'Error al actualizar'}, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        if check_role_admin(request) == False:
            return Response(['El usuario no tiene permitido realizar esta accion'])
        empleado = get_object_or_404(Empleado, pk=pk)
        if empleado:
            empleado.deleted = True
            empleado.save()
            return Response({'message': 'Empleado eliminado'})
        return Response(['El id no existe'])


def check_role_admin(request):
    user = UserProfile.objects.get(pk=request.user.id)
    return user.is_superuser


@extend_schema_view(
    create=extend_schema(
        description='Agregar vacuna [Sputnik, AstraZeneca, Pfizer y Jhonson&Jhonson] a empleado para esto se requiere el parametro id del empleado'),
    retrieve=extend_schema(description='Permite mostrar las vacunas del empleado especificado'),
    update=extend_schema(description='Permite actualizar la vacuna [Sputnik, AstraZeneca, Pfizer y Jhonson&Jhonson] del empleado '),
    destroy=extend_schema(description='Permite eliminar la vacuna del empleado')
)
class DosisViewSet(viewsets.ModelViewSet):
    serializer_class = DosisSerializers
    queryset = Dosis.objects.filter(deleted=False)

    @extend_schema(description='Consultar dosis por nombre de vacuna y fecha', parameters=[
        OpenApiParameter(
            name='vacuna',
            description='Nombre de la vacuna [Sputnik, AstraZeneca, Pfizer y Jhonson&Jhonson]',
            type=str
        ),
        OpenApiParameter(
            name='fecha_desde',
            description='Fecha de vacunacion desde',
            type=OpenApiTypes.DATE,
            location=OpenApiParameter.QUERY,
            examples=[
                OpenApiExample(
                    'Example 1',
                    value='2021-01-01'
                )
            ]
        ),
        OpenApiParameter(
            name='fecha_hasta',
            description='Fecha de vacunacion hasta',
            type=OpenApiTypes.DATE,
            location=OpenApiParameter.QUERY,
            examples=[
                OpenApiExample(
                    'Example 1',
                    value='2021-01-01'
                )
            ]
        )
    ],
        filters=True
    )
    def list(self, request, *args, **kwargs):
        if check_role_admin(request) == False:
            return Response(['El usuario no tiene permitido realizar esta accion'])
        if self.request.query_params.get('vacuna'):
            self.queryset = self.queryset.filter(vacuna__icontains=self.request.query_params.get('vacuna'))
        if self.request.query_params.get('fecha_desde') and self.request.query_params.get('fecha_hasta'):
            self.queryset = self.queryset.filter(fecha_vacuna__gte=self.request.query_params.get('fecha_desde'),
                                         fecha_vacuna__lte=self.request.query_params.get('fecha_hasta'))
        serializer_dosis = DosisSerializers(self.queryset, many=True)
        return Response(serializer_dosis.data)

    def create(self, request, *args, **kwargs):
        if check_role_admin(request) == False:
            return Response(['El usuario no tiene permitido realizar esta accion'])
        serializers = DosisSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        vacunas = self.queryset.filter(empleado_id=pk)
        if len(vacunas) == 0:
            return Response("Empleado no existe")
        if request.user.id != vacunas[0].empleado.user.id and check_role_admin(request) == False:
            return Response(['Este usuario no tiene permiso para realizar esta accion'])
        serializers = DosisSerializers(vacunas, many=True)
        return Response(serializers.data)

    def update(self, request, pk=None):
        vacuna = get_object_or_404(Dosis, pk=pk)
        if request.user.id != vacuna.empleado.user.id and check_role_admin(request) == False:
            return Response(['Este usuario no tiene permiso para realizar esta accion'])
        serializer = DosisSerializers(instance=vacuna, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk=None):
        if check_role_admin(request) == False:
            return Response(['El usuario no tiene permitido realizar esta accion'])
        vacuna = get_object_or_404(Dosis, pk=pk)
        if vacuna:
            vacuna.deleted = True
            vacuna.save()
            return Response({'message': 'Registro de vacuna eliminado'})
        return Response('El id no existe')