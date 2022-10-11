from rest_framework import serializers
from .models import Empleado, Dosis


class EmpleadoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = ['id', 'cedula', 'nombres', 'apellidos', 'email']
        read_only_fields = ['id']

    def validate_cedula(self, value):
        buscando_digitos = [caracter.isdigit() for caracter in value]
        if all(buscando_digitos) and len(value) == 10:
            return value
        else:
            raise serializers.ValidationError('El campo cédula debe contener 10 dígitos')

    def validate_nombres(self, value):
        if value.isalpha():
            return value
        else:
            raise serializers.ValidationError('El campo nombres debe contener solo letras')

    def validate_apellidos(self, value):
        if value.isalpha():
            return value
        else:
            raise serializers.ValidationError('El campo apellidso debe contener solo letras')


class EmpleadoUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = ['id', 'fecha_nacimiento', 'direccion_domicilio', 'celular', 'vacunado']
        read_only_fields = ['id']

    def validate_celular(self, value):
        buscando_digitos = [caracter.isdigit() for caracter in value]
        if all(buscando_digitos) and len(value) == 10:
            return value
        else:
            raise serializers.ValidationError('Este campo debe contener 10 dígitos')

    def update(self, instance, validated_data):
        instance.fecha_nacimiento = validated_data.get('fecha_nacimiento', instance.fecha_nacimiento)
        instance.direccion_domicilio = validated_data.get('direccion_domicilio', instance.direccion_domicilio)
        instance.celular = validated_data.get('celular', instance.celular)
        instance.vacunado = validated_data.get('vacunado', instance.vacunado)
        instance.save()
        return instance


class DosisSerializers(serializers.ModelSerializer):
    class Meta:
        model = Dosis
        exclude = ['deleted']
        read_only_fields = ['id']