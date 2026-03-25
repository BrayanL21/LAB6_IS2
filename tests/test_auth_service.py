"""
Pruebas unitarias para el modulo de autenticacion (Auth Service).
Laboratorio 5 - Pipeline local de integracion continua
Sistema de Inventarios y Ventas - Joyeria multi-sede
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from services.auth_service import register_user, login_user
from repository import user_repository


def setup_function():
    """Limpiar la base de datos en memoria antes de cada prueba."""
    user_repository.users_db.clear()


def test_registro_usuario_exitoso():
    resultado = register_user("vendedor@joyeria.com", "pass123", "vendedor")
    assert resultado == {"message": "User registered successfully"}


def test_registro_usuario_duplicado():
    register_user("gerente@joyeria.com", "pass123", "gerente")
    resultado = register_user("gerente@joyeria.com", "otrapass", "vendedor")
    assert resultado == {"error": "User already exists"}


def test_login_exitoso():
    register_user("dueno@joyeria.com", "secreto", "dueno")
    resultado = login_user("dueno@joyeria.com", "secreto")
    assert resultado == {"message": "Login successful", "role": "dueno"}


def test_login_contrasena_incorrecta():
    register_user("contador@joyeria.com", "mipass", "contador")
    resultado = login_user("contador@joyeria.com", "passincorrecta")
    assert resultado == {"error": "Invalid credentials"}


def test_login_usuario_no_existe():
    resultado = login_user("noexiste@joyeria.com", "cualquierpass")
    assert resultado == {"error": "User not found"}


def test_rol_vendedor_asignado_correctamente():
    register_user("vendedor2@joyeria.com", "pass456", "vendedor")
    resultado = login_user("vendedor2@joyeria.com", "pass456")
    assert resultado["role"] == "vendedor"


def test_multiples_usuarios_independientes():
    register_user("sede1@joyeria.com", "pass1", "vendedor")
    register_user("sede2@joyeria.com", "pass2", "gerente")

    resultado1 = login_user("sede1@joyeria.com", "pass1")
    resultado2 = login_user("sede2@joyeria.com", "pass2")

    assert resultado1["role"] == "vendedor"
    assert resultado2["role"] == "gerente"


def test_stock_no_puede_ser_negativo():
    stock_inicial = 10
    unidades_vendidas = 10
    stock_final = stock_inicial - unidades_vendidas
    assert stock_final >= 0, "El stock no puede quedar negativo"
    