#!/usr/bin/env python
"""
Script para actualizar las contraseñas de los usuarios a '1234'
"""
import os
import sys
import django

# Configurar Django
sys.path.append('/Users/fede/Documents/GitHub/Liskov Project Management')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "liscov_pm.settings")
django.setup()

from django.contrib.auth.models import User

def update_passwords():
    """Actualiza todas las contraseñas de usuarios a '1234'"""

    print("="*70)
    print("ACTUALIZANDO CONTRASEÑAS DE USUARIOS")
    print("="*70)

    # Lista de usuarios del proyecto Da Vinci
    usernames = [
        'laura.director',
        'martin.tech',
        'sofia.dev',
        'pablo.frontend',
        'julia.backend',
        'diego.qa'
    ]

    # También actualizar los usuarios de ejemplo si existen
    example_users = [
        'maria.garcia',
        'juan.lopez',
        'ana.martinez',
        'carlos.rodriguez',
        'lucia.fernandez',
        'diego.sanchez'
    ]

    all_usernames = usernames + example_users

    updated_count = 0

    for username in all_usernames:
        try:
            user = User.objects.get(username=username)
            user.set_password('1234')
            user.save()
            print(f"✓ Contraseña actualizada: {user.username} ({user.get_full_name()})")
            updated_count += 1
        except User.DoesNotExist:
            print(f"  Usuario no encontrado: {username}")

    print("\n" + "="*70)
    print(f"✓ {updated_count} contraseñas actualizadas exitosamente")
    print("="*70)
    print("\nTodos los usuarios ahora usan la contraseña: 1234")
    print("="*70 + "\n")

if __name__ == '__main__':
    try:
        update_passwords()
    except Exception as e:
        print(f"\n❌ Error al actualizar contraseñas: {e}")
        import traceback
        traceback.print_exc()
