# Generated by Django 5.0.6 on 2024-06-26 11:04

import cpf_field.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=150)),
                ('cpf', cpf_field.models.CPFField(max_length=14, unique=True, verbose_name='cpf')),
                ('data_de_nascimento', models.DateField(blank=True, null=True)),
                ('estado_civil', models.CharField(blank=True, choices=[('Solteiro(a)', 'Solteiro(a)'), ('Casado(a)', 'Casado(a)'), ('Divorciado(a)', 'Divorciado(a)'), ('Viúvo(a)', 'Viúvo(a)')], max_length=20, null=True)),
                ('profissao', models.CharField(max_length=80, verbose_name='Profissão')),
                ('virou_cliente', models.CharField(choices=[('Sim', 'Sim'), ('Não', 'Não'), ('Pendente', 'Pendente'), ('Em prospecção', 'Em prospecção')], max_length=20)),
                ('cadastrado_advbox', models.BooleanField(default=False)),
                ('cadastrado_planilha', models.BooleanField(default=False)),
                ('justificativa', models.TextField(blank=True)),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
                ('foto', models.ImageField(blank=True, null=True, upload_to='fotos_clientes/')),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('cep', models.CharField(blank=True, max_length=10)),
                ('rua', models.CharField(blank=True, max_length=255)),
                ('numero', models.CharField(blank=True, max_length=10, verbose_name='Número')),
                ('complemento', models.CharField(blank=True, max_length=150)),
                ('bairro', models.CharField(blank=True, max_length=100)),
                ('cidade', models.CharField(blank=True, max_length=100)),
                ('estado', models.CharField(blank=True, max_length=2)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('telefone', models.CharField(blank=True, max_length=15, verbose_name='Telefone')),
                ('whatsapp', models.BooleanField(default=False)),
            ],
        ),
    ]
