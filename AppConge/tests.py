from django.test import TestCase
from .import models
from AppAccount.models import Personnel
import datetime




class CreateCongeTestCate(TestCase):
    def setUp(self):
        self.personnel={
            'username':'KIUKA',
            'postnom':'MBAYO',
            'prenom':'HENRI',
            'sexe':'M',
            'etat_civil':'M'
        }
        self.date_debut='02-02-2024'
        self.date_fin='02-03-2024'
        self.convert_date_debut=datetime.datetime.strptime(self.date_debut, '%d-%m-%Y').date()
        self.convert_date_fin=datetime.datetime.strptime(self.date_fin, '%d-%m-%Y').date()
     
        self.getPersonnel=Personnel.objects.create(**self.personnel)
        self.conge=models.Conge.objects.create(personnel=self.getPersonnel,titre='Voyage',
                                               nature='cumulé',
                                               motif="Voir ma famille", 
                                               date_debut=self.convert_date_debut,
                                               date_fin=self.convert_date_fin)
        
        self.reponse=models.Demande.objects.create(conge=self.conge, commentaire="Oui",approbation=False)
        

    def test_comment(self):
        self.assertEqual(self.conge.getReponseConge, '0 jour')
        
        

        
        

        



