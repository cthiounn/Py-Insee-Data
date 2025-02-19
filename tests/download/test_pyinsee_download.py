import unittest

import os.path
import hashlib
import pandas as pd

from pynsee.download import *

class MyTests(unittest.TestCase):

    # info_donnees ---------------------------------
        
    def test_levensthein_error_typo(self):
        with self.assertRaises(ValueError):
            info_donnees("SIRENE_SIRET_NONDIFg")

    def test_levensthein_error_big_typo(self):
        with self.assertRaises(ValueError):
            info_donnees("randomword")

    def test_info_no_date(self):
        with self.assertRaises(ValueError):
            info_donnees("RP_LOGEMENT")



    def test_date_info_donnees_dernier(self):
        self.assertIsInstance(info_donnees("RP_LOGEMENT", date = "dernier"), dict)

    def test_date_info_donnees_latest(self):
        self.assertIsInstance(info_donnees("RP_LOGEMENT", date = "latest"), dict)

    def test_date_info_donnees_str(self):
        self.assertIsInstance(info_donnees("RP_LOGEMENT", date = "2012"), dict)

    def test_date_info_donnees_int(self):
        self.assertIsInstance(info_donnees("RP_LOGEMENT", date = 2012), dict)

    def test_nodate(self):
        self.assertIsInstance(info_donnees("SIRENE_SIRET_NONDIFF"), dict)


    # millesimesDisponibles -------------------------

    def test_error_millesimesDisponibles_typo(self):
        with self.assertRaises(ValueError):
            millesimesDisponibles("randomword")

    def test_keys_json_millesimesDisponibles(self):
        self.assertEqual([k for k in dict_data_source.keys() if k.startswith("RP_LOGEMENT")],
        list(millesimesDisponibles("RP_LOGEMENT").keys())
        )

    # telechargerFichier ----------------------------

    def test_error_multiple_data_no_year(self):
        with self.assertRaises(ValueError):
            telechargerFichier("FILOSOFI_COM")        

    def test_year_string(self):
        filosofi_data = telechargerFichier("FILOSOFI_COM", date = "2016")
        self.assertIsInstance(filosofi_data, dict)
        self.assertEqual(filosofi_data['result'], dict_data_source["FILOSOFI_COM_2016"])
        path_unzipped = filosofi_data["fichierAImporter"]
        path_zipped = filosofi_data["fileArchive"]
        self.assertTrue(os.path.isfile(path_zipped))
        self.assertTrue(os.path.isfile(path_unzipped))
        self.assertEqual(filosofi_data["result"]['fichier_donnees'], path_unzipped.split("/")[-1])
        self.assertEqual(hashlib.md5(open(path_zipped, 'rb').read()).hexdigest(), filosofi_data['result']['md5'])


    def test_year_int(self):
        filosofi_data = telechargerFichier("FILOSOFI_COM", date = 2016)
        self.assertIsInstance(filosofi_data, dict)
        self.assertEqual(filosofi_data['result'], dict_data_source["FILOSOFI_COM_2016"])
        path_unzipped = filosofi_data["fichierAImporter"]
        path_zipped = filosofi_data["fileArchive"]
        self.assertTrue(os.path.isfile(path_zipped))
        self.assertTrue(os.path.isfile(path_unzipped))
        self.assertEqual(filosofi_data["result"]['fichier_donnees'], path_unzipped.split("/")[-1])
        self.assertEqual(hashlib.md5(open(path_zipped, 'rb').read()).hexdigest(), filosofi_data['result']['md5'])

    def test_year_dernier(self):
        filosofi_data = telechargerFichier("FILOSOFI_COM", date = "dernier")
        latest = list(millesimesDisponibles("FILOSOFI_COM").keys())[-1]
        self.assertIsInstance(filosofi_data, dict)
        self.assertEqual(filosofi_data['result'], dict_data_source[latest])
        path_unzipped = filosofi_data["fichierAImporter"]
        path_zipped = filosofi_data["fileArchive"]
        self.assertTrue(os.path.isfile(path_zipped))
        self.assertTrue(os.path.isfile(path_unzipped))
        self.assertEqual(filosofi_data["result"]['fichier_donnees'], path_unzipped.split("/")[-1])
        self.assertEqual(hashlib.md5(open(path_zipped, 'rb').read()).hexdigest(), filosofi_data['result']['md5'])

    def test_year_latest(self):
        filosofi_data = telechargerFichier("FILOSOFI_COM", date = "latest")
        latest = list(millesimesDisponibles("FILOSOFI_COM").keys())[-1]
        self.assertIsInstance(filosofi_data, dict)
        self.assertEqual(filosofi_data['result'], dict_data_source[latest])
        path_unzipped = filosofi_data["fichierAImporter"]
        path_zipped = filosofi_data["fileArchive"]
        self.assertTrue(os.path.isfile(path_zipped))
        self.assertTrue(os.path.isfile(path_unzipped))
        self.assertEqual(filosofi_data["result"]['fichier_donnees'], path_unzipped.split("/")[-1])
        self.assertEqual(hashlib.md5(open(path_zipped, 'rb').read()).hexdigest(), filosofi_data['result']['md5'])

    # telechargerDonnees ----------------------------

    def test_telechargerDonnees(self):
        df = telechargerDonnees("FILOSOFI_COM", date = "2015")
        self.assertIsInstance(df, pd.DataFrame)

    def test_telechargerDonnees_no_onglet(self):
        df = telechargerDonnees("FILOSOFI_DISP_COM", date = "dernier")
        self.assertIsInstance(df, pd.DataFrame)

    def test_telechargerDonnees_FILOSOFI_AU2010(self):
        df = telechargerDonnees("FILOSOFI_AU2010", date = "dernier")
        self.assertIsInstance(df, pd.DataFrame)

    def test_telechargerDonnees_RPLOGEMENT2016(self):
        df = telechargerDonnees("RP_LOGEMENT", date = "2016")
        self.assertIsInstance(df, pd.DataFrame)

    def test_telechargerDonnees_estel_2016(self):
        df = telechargerDonnees("ESTEL_T202", date = "2016")
        self.assertIsInstance(df, pd.DataFrame)


if __name__ == '__main__':
    unittest.main()


