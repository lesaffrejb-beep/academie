import unittest
from installer_reprise import transforme

class RepriseTest(unittest.TestCase):
    def test_auth_preservee_et_route_idempotente(self):
        source = '''site {
    @academiePrivee path /academie /academie/* /academie-acces/*
    basicauth @academiePrivee { secret-inchange }
    @workPrivees not path /academie /academie/* /mariage/*
    redir /academie /academie/ 308
    handle /autre/* { reverse_proxy 127.0.0.1:8199 }
}
'''
        resultat = transforme(source)
        self.assertIn('@academiePrivee path /academie /academie/* /academie-acces/* /academie-reprise/', resultat)
        self.assertIn('@workPrivees not path /academie /academie/* /mariage/* /academie-reprise/', resultat)
        self.assertIn('basicauth @academiePrivee { secret-inchange }', resultat)
        self.assertIn('handle /autre/* { reverse_proxy 127.0.0.1:8199 }', resultat)
        self.assertEqual(transforme(resultat), resultat)
    def test_configuration_inconnue_refusee(self):
        with self.assertRaises(ValueError):
            transforme('autre site')
