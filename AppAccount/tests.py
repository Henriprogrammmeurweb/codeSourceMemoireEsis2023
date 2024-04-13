from django.test import TestCase,Client
from AppPersonnel.forms import FormAddPersonnel, FormAddGrade
import unittest
from django.urls import reverse
from .models import Personnel

client = Client()



class EntryPersonnel(TestCase):
    def setUp(self):
        self.data = {
            "username": "KIUKA",
            "postnom" : "MBAYO",
            'prenom' : "Henri",
            'email':"kiukahnri@gmail.com", 
            'sexe' :"M", 
            'etat_civil':'C', 
            'password' : '12520785jkl',
            'salaire':'Oui',
            'prime':'Non'
         }
        self.personnel = Personnel.objects.create_user(**self.data)






    '''
    def test_string_representation_valide(self):
        self.assertEqual(f"KIUKA MBAYO Henri", self.personnel.getPersonnel)


    def test_string_representation_not_valide(self):
        self.assertEqual(f"KIUKA MBAYO Henri Henri", self.personnel.getPersonnel)'''


    # def test_homePage_valid_url(self):
    #     response = self.client.get(reverse("index"))
    #     self.assertEqual(response.status_code, 200)

    # def test_homePage_not_valid_url(self):
    #     response = self.client.get(reverse("index-test"))
    #     self.assertEqual(response.status_code, 200)

    # def testCreatePersonnelForm(self):
    #     form_data = {
    #         "username": "KIUKA",
    #         "postnom" : "MBAYO",
    #         'prenom' : "Henri",
    #         'email':"kiukahenri@gmail.com", 
    #         'sexe' :"M", 
    #         'etat_civil':'C', 
    #         'password' : '12520'
    #     }
    #     FormAddPersonnel(data=form_data)


    # def testCreatePersonnelFormNoData(self):
    #     with self.assertRaises(KeyError):
    #         FormAddPersonnel()


    # def testFormAddPersonnel_isValid(self):
    #     form=FormAddPersonnel(data=self.data)
    #     self.assertTrue(form.is_valid())

    # def testFormAddGradeis_isvalid(self):
    #     data={
    #         "designation":'AG'
    #     }
    #     form=FormAddGrade(data=data)
    #     self.assertTrue(form.is_valid())


    # def testFormAddGradeis_is_not_valid(self):
    #     form=FormAddGrade(data={})
    #     self.assertFalse(form.is_valid())


    def test_blank_form(self):
        form=FormAddPersonnel(self.data)
        # self.assertTrue(form.is_valid())
        self.assertEqual(form.errors, {
            "username": ['required'],
            "postnom" : ['required'],
            'prenom' : ['required'],
            'email':['required'], 
            'sexe' :['required'], 
            'etat_civil':['required'], 
            'password' : ['required']
        })

# class TestAjoutPersonnelView(TestCase):
#     def setUp(self):
#         self.personnel =Personnel.objects.create_user(username = "KIUKA", postnom = "Mbayo", prenom = "Henri", 
#                                                  email="kiukahenrigmail.com", sexe="M", etat_civil='C', 
#                                                  password = '15')
#         self.client = Client()
        
#     def test_status_code_url(self):
#         response = self.client.get(reverse('ajoutPersonnel'))
#         print(response.status_code)


#     def test_addPersonnel(self):
#         form_data = {
#             "username": "KIUKA",
#             "postnom" : "MBAYO",
#             'prenom' : "Henri",
#             'email':"kiukahenri@gmail.com", 
#             'sexe' :"M", 
#             'etat_civil':'C', 
#             'password' : '12520'
#         }
#         response = self.client.post('/personnel/ajout-personnel/', kwargs=form_data)
#         self.assertEqual(response.status_code, 200)


#     def test_formAddPersonnel(self):
#         form_data = {
#             "username": "KIUKA",
#             "postnom" : "MBAYO",
#             'prenom' : "Henri",
#             'email':"kiukahenri@gmail.com", 
#             'sexe' :"M", 
#             'etat_civil':'C', 
#             'password' : 'Henri24578jj'

#         }
#         form_datas={
#             "designation":'Henri'
#         }
#         form = FormAddGrade(data=form_datas)
#         self.assertTrue(form.is_valid())
#     '''
#     def test_add_personnel(self):
#         response = self.client.post('/personnel/ajout-personnel/', kwargs=self.personnel)
#         self.assertEqual(Personnel.objects.count(), 1)
#         personnels = Personnel.objects.all()
#         #self.assertFormError(response, "form", "password", 'Niepoprawne hasło.')
#         self.assertFormError(response,'form', 'password', "Hum !")'''

if __name__ == "__main__":
    unittest.main()


# from django.test import TestCase, Client
# from django.urls import reverse
# from .models import Article, Comment
# from .views import ajouter_commentaire

# class TestAjouterCommentaireView(TestCase):

#     def setUp(self):
#         # Créez un article pour les tests
#         self.article = Article.objects.create(titre="Titre de l'article", contenu="Contenu de l'article")

#     def test_vue_ajouter_commentaire(self):
#         # Vérifiez si la vue pour ajouter un commentaire retourne le bon statut HTTP
#         response = self.client.get(reverse('ajouter_commentaire', kwargs={'article_id': self.article.id}))
#         self.assertEqual(response.status_code, 200)

#     def test_ajouter_commentaire(self):
#         # Vérifiez si un commentaire est ajouté avec succès à un article
#         client = Client()
#         response = client.post(reverse('ajouter_commentaire', kwargs={'article_id': self.article.id}),
#                                {'nom_utilisateur': 'TestUser', 'contenu': 'Contenu du commentaire'})
        
#         # Assurez-vous que le commentaire est créé dans la base de données
#         self.assertEqual(Comment.objects.count(), 1)
        
#         # Assurez-vous que le commentaire créé est lié à l'article correct
#         commentaire = Comment.objects.first()
#         self.assertEqual(commentaire.article, self.article)
        
        # Assurez-vous que l'utilisateur est redirigé vers la page de détail de l'article après avoir ajouté le commentaire
        #self.assertRedirects(response, reverse('detail_article', kwargs={'article_id': self.article.id}))

# Exercices pratiques :
# 1. Écrivez un test pour vérifier si la vue pour ajouter un commentaire affiche un formulaire valide.
# 2. Écrivez un test pour vérifier si la vue pour ajouter un commentaire gère correctement les cas où des données invalides sont soumises.
# 3. Écrivez un test pour vérifier si la vue pour ajouter un commentaire redirige correctement en cas de soumission réussie.

