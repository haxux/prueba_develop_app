import unittest
from app import app, validar_login

class TestLogin(unittest.TestCase):
    
    def setUp(self):
        # Crea el contexto de la aplicación antes de cada prueba
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        # Quita el contexto al terminar
        self.app_context.pop()
    
    def test_login_correcto(self):
        self.assertTrue(validar_login("Cliente_Prueba", "1234"))

    def test_login_incorrecto_password(self):
        self.assertFalse(validar_login("Cliente_Prueba", "wrongpass"))

    def test_login_incorrecto_usuario(self):
        self.assertFalse(validar_login("no_existe", "1234"))

    def test_login_vacio(self):
        self.assertFalse(validar_login("", ""))
    def test_Password_vacio(self):
        self.assertFalse(validar_login("Cliente_Prueba", ""))
       

if __name__ == "__main__":
    unittest.main()