from rest_framework import serializers

from .models import PackageRelease, Project
from .pypi import version_exists, latest_version


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageRelease
        fields = ["name", "version"]
        extra_kwargs = {"version": {"required": False}}

    def validate(self, data):
        if "version" not in data.keys():
            data['version'] = latest_version(data['name'])
            if data['version'] is None:
                raise serializers.ValidationError()
        else:
            if not version_exists(data['name'], data['version']):
                raise serializers.ValidationError()
        return data


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["name", "packages"]

    packages = PackageSerializer(many=True)

    def create(self, validated_data):

        packages = validated_data["packages"]
        #se o usuário passar dois pacotes com o mesmo nome irá receber um error
        packagesname = [p['name'] for p in packages]
        if len(set(packagesname)) != len(packagesname):
            raise serializers.ValidationError({"error": "Pacotes repetidos"})
        project = Project.objects.create(name=validated_data["name"])
        for i in packages:
            PackageRelease.objects.create(project=project, **i)
        return project
