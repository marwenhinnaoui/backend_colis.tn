
from rest_framework import serializers
from .models import CustomUser, Colis, TransporteurCalendrier, Reclamation


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['reçus_paiement', 'profile_image', 'image_cin_verso', 'image_cin_recto', 'image_permi_recto', 'image_permi_verso', 'image_carte_grise_recto', 'image_carte_grise_verso']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser 
        fields = ['id','username','rating','reçus_paiement','compte_valid','is_calendrier_valid', 'email', 'password','namelastname','role' ,'phone_number','billing_address','city','zip_code','profile_image','image_cin_verso','image_cin_recto','valid_paiement','cin',   "tonnage_vehicule" ,  "matricule_vehicule" , "marque_vehicule","date_naissance","image_permi_recto", "image_permi_verso", "image_carte_grise_recto", "image_carte_grise_verso"]

class AjouterAdminSerializer(serializers.ModelSerializer):
    phone_number = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'namelastname', 'role', 'phone_number']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        if 'username' not in validated_data or not validated_data.get('username'):
            validated_data['username'] = self.generate_unique_username(validated_data['email'])



        if 'phone_number' not in validated_data or validated_data['phone_number'] is None:
            validated_data['phone_number'] = ''

        user = CustomUser(**validated_data)
        user.save()
        return user

    def generate_unique_username(self, email):
        base_username = email.split('@')[0]
        unique_username = base_username
        counter = 1

        while CustomUser.objects.filter(username=unique_username).exists():
            unique_username = f"{base_username}{counter}"
            counter += 1

        return unique_username

class ColisSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Colis 
        fields = ['id', 'client','description', 'prix','poid_total','list_article_json' , 'destenaire_zipcode','destenaire_Gouvernorat', 'destenaire_ville', 'destenaire_nom_pre', 'destenaire_tel', 'destenaire_email', 'destenaire_adresse', 'status_colis', 'matricule', 'transporteur', 'jour_depart', 'creation_date']





class TransporteurCalendrierSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransporteurCalendrier
        fields = '__all__'



class ReclamationSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Reclamation
        fields = ['id', 'reclamant', 'date_reclamation','defendeur', 'sujet', 'description', 'colis', 'reponse']

        
class UpdateReclamationSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Reclamation
        exclude = ['id', 'reclamant', 'date_reclamation','defendeur', 'sujet', 'description', 'colis']
        