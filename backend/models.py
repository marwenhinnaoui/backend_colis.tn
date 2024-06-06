import json
from django.db import models
from django.contrib.auth.models import AbstractUser 


def upload_to(instance,filename):
    return 'images/{filename}'.format(filename= filename)


class CustomUser(AbstractUser):
    namelastname = models.CharField(blank=True, max_length=255)
    password = models.CharField(blank=True, max_length=255, default="")
    date_naissance = models.CharField(blank=True, max_length=255)
    email = models.EmailField(max_length=255, unique=True, blank=True)
    role = models.CharField(max_length=1, blank=True)
    phone_number = models.IntegerField(blank=True, unique=True)
    billing_address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    zip_code = models.IntegerField(blank=True)
    cin = models.IntegerField(blank=True)
    valid_paiement = models.BooleanField(default=False)
    compte_valid = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)
    image_cin_recto = models.ImageField(upload_to=upload_to , null=True)
    image_cin_verso = models.ImageField(upload_to=upload_to,  null=True)
    image_permi_recto = models.ImageField(upload_to=upload_to, null=True)
    image_permi_verso = models.ImageField(upload_to=upload_to, null=True)
    image_carte_grise_recto = models.ImageField(upload_to=upload_to,  null=True)
    reçus_paiement= models.ImageField(upload_to=upload_to, null=True )
    image_carte_grise_verso = models.ImageField(upload_to=upload_to,  null=True)
    profile_image = models.ImageField(upload_to=upload_to, null=True)
    matricule_vehicule = models.CharField(blank=True, max_length=500)
    marque_vehicule = models.CharField(blank=True, max_length=500)
    tonnage_vehicule = models.IntegerField(blank=True)
    username = models.CharField(max_length=150, unique=True, blank=True)
    is_calendrier_valid = models.BooleanField(default=False)

    def __str__(self):
        return self.email
    



class Colis(models.Model):
    matricule = models.CharField(max_length=10)
    description = models.CharField(max_length=500)
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='colis_client')
    transporteur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='colis_transporteur')
    prix = models.DecimalField(max_digits=8, decimal_places=2)
    destenaire_adresse = models.CharField(max_length=500)
    destenaire_email = models.CharField(max_length=500)
    destenaire_tel = models.IntegerField(blank=True)
    destenaire_nom_pre = models.CharField(max_length=500)
    destenaire_ville = models.CharField(max_length=500)
    destenaire_Gouvernorat = models.CharField(max_length=500)
    destenaire_zipcode = models.IntegerField(blank=True)
    poid_total = models.DecimalField(max_digits=10, decimal_places=2)
    list_article_json = models.TextField()
    status_colis = models.CharField(max_length=500)
    jour_depart = models.CharField(max_length=500, blank=True)
    creation_date = models.CharField(max_length=500, blank=True)


    def __str__(self):
        return f"Colis MAT: {self.matricule}, Destination: {self.destenaire_ville}, Client: {self.client.id}"



class TransporteurCalendrier(models.Model):
    transporteur = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    jour_depart = models.CharField(max_length=500, blank=True, unique=True)
    heure_depart = models.CharField(max_length=500, blank=True)
    poids_disponible_jour = models.DecimalField(max_digits=10, decimal_places=2)
    poids_total_colis_jour = models.DecimalField(max_digits=10, decimal_places=2)
    destenaire_zipcode = models.IntegerField(blank=True)
    destenaire_Gouvernorat = models.CharField(max_length=500)


    def __str__(self):
        return f"transporteur MAT: {self.transporteur}, Destination: {self.destenaire_Gouvernorat}, jour_depart: {self.jour_depart}"
    


class Reclamation(models.Model):

    reclamant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reclamant')
    defendeur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='defendeur')
    date_reclamation = models.CharField(max_length=500, blank=True)
    sujet = models.CharField(max_length=500, blank=True)
    description = models.CharField(max_length=900,blank=True)
    colis = models.ForeignKey(Colis, on_delete=models.CASCADE)
    reponse = models.CharField(max_length=900)
    


    def __str__(self):
        return f"reclamant: {self.reclamant}, defendeur: {self.defendeur}, date_reclamation: {self.date_reclamation}"