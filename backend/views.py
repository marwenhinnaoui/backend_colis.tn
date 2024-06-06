from decimal import Decimal
import json
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer, ColisSerializer, TransporteurCalendrierSerializer, ReclamationSerializer, UserUpdateSerializer, UpdateReclamationSerializer, AjouterAdminSerializer
from rest_framework.authtoken.models import Token
from bson.decimal128 import Decimal128
from decimal import Decimal
from django.conf import settings
from .models import Colis, CustomUser, TransporteurCalendrier, Reclamation
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import string


def send_email(subject, message, to_email, from_email='skyzshopae@gmail.com', password='wuvspogwqrkennjr'):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Start TLS encryption
        server.login(from_email, password)  # Login to Gmail

        msg = MIMEMultipart()
        msg['From'] = f"Colis.tn <{from_email}>"

        msg['To'] = to_email
        msg['Subject'] = subject

        html_message = MIMEText(message, 'html')
        msg.attach(html_message)

        server.sendmail(from_email, to_email, msg.as_string())

        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")






@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        users_with_role_a = CustomUser.objects.filter(role='a')
        for user in users_with_role_a:
            content = 'Nouveau Utilisateur!'
            message = f'<html lang="en"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0">  </head> <body style="font-family: Arial, sans-serif; margin: 0; padding: 0;"> <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0"> <tr> <td style="padding: 20px 0;"> <table align="center" width="600" cellspacing="0" cellpadding="0" border="0"> <tr> <td align="center" style="background-color: #f2f2f2; padding: 40px 0;"> <h1>Cher Admin!</h1> <p>{content}</p> <!-- Button --> <table role="presentation" cellspacing="0" cellpadding="0" border="0"> <tr> <td style="border-radius: 3px; background-color: #1a73e8; text-align: center;"> <a href="http://localhost:3000/" class="button" target="_blank" style="display: inline-block; padding: 15px 30px; color: #ffffff; text-decoration: none; font-weight: bold;">Voir Détail</a> </td> </tr> </table> </td> </tr> </table> </td> </tr> </table> </body> </html> '
            send_email('Nouveau message de Colis.tn', message, user.email)
        return Response({'user': serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def ajouterAdmin(request):
    serializer = AjouterAdminSerializer(data=request.data)
    print('request.data', request.data['email'])
    content = 'Votre mot de passe pour acceder au dashboard admin est:'+ request.data['password']
    message = f'<html lang="en"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0">  </head> <body style="font-family: Arial, sans-serif; margin: 0; padding: 0;"> <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0"> <tr> <td style="padding: 20px 0;"> <table align="center" width="600" cellspacing="0" cellpadding="0" border="0"> <tr> <td align="center" style="background-color: #f2f2f2; padding: 40px 0;"> <h1>Cher Utilisateur!</h1> <p>{content}</p> <!-- Button --> <table role="presentation" cellspacing="0" cellpadding="0" border="0"> <tr> <td style="border-radius: 3px; background-color: #1a73e8; text-align: center;"> <a href="http://localhost:3000/" class="button" target="_blank" style="display: inline-block; padding: 15px 30px; color: #ffffff; text-decoration: none; font-weight: bold;">Voir Détail</a> </td> </tr> </table> </td> </tr> </table> </td> </tr> </table> </body> </html> '
    to_email = 'marwen.hinawi@gmail.com'
    send_email('Nouveau message de Colis.tn', message, request.data['email'])

    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Admin has been created'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])

def delete_admin(request, admin_id):
    if request.method == 'DELETE':
        try:
            admin = get_object_or_404(CustomUser, id=admin_id)

           

            admin.delete()

            return Response({'message': 'Admin deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

        except Colis.DoesNotExist:
            return Response({'error': 'Admin does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def update_admin(request, admin_id):
    try:
        admin = get_object_or_404(CustomUser, id=admin_id)

        
        data = request.data.copy()


        data['email'] = data.get('email', admin.email)
        data['namelastname'] = data.get('namelastname', admin.namelastname)
        data['password'] = data.get('password', admin.password)
        data['role'] = data.get('role', admin.role)
        data['phone_number'] = data.get('phone_number', admin.phone_number)

        serializer = AjouterAdminSerializer(admin, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except CustomUser.DoesNotExist:
        return Response({'error': 'Admin nexiste pas'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def login(request):



    user = get_object_or_404(CustomUser, email=request.data.get('email'))

    if user is None:
        return Response(f"Utilisateur avec email {request.data.get('email')} pas trouvé", status=status.HTTP_404_NOT_FOUND)
        
    if not request.data.get('password') == user.password:

        return Response({"response": "Mot de passe incorrect"}, status=status.HTTP_404_NOT_FOUND)

    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data, }, status=status.HTTP_200_OK)




@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        request.user.auth_token.delete()
        return Response({'valid logout' }, status=200)
    except Exception as e:
        return Response({'erreur logout' })


@api_view(['GET'])

def get_all_users(request):
    users = CustomUser.objects.exclude(role='a')
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])

def get_all_admins(request, admin_id):
    users = CustomUser.objects.filter(role='a').exclude(id=admin_id)
    
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['PUT'])

def update_user(request, user_id):
    try:
        user = get_object_or_404(CustomUser, id=user_id)

        if request.user != user:
            return Response({'Erreur': 'Erreur'}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()

        serializer = UserSerializer(user, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except CustomUser.DoesNotExist:
        return Response({'Erreur': 'User nexist pas'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'Erreur': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
@api_view(['PUT'])

def modifier_profile(request, user_id):
    try:
        user = get_object_or_404(CustomUser, id=user_id)

        if request.user != user:
            return Response({'Erreur': 'Erreur'}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()

        serializer = UserUpdateSerializer(user, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except CustomUser.DoesNotExist:
        return Response({'Erreur': 'User nexist pas'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'Erreur': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['POST', 'GET'])
def cree_colis(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            client_id = data.get('client_id')

            client = data.get('client')
            prix = data.get('prix')
            matricule = data.get('matricule')
            destenaire_adresse = data.get('destenaire_adresse')
            destenaire_email = data.get('destenaire_email')
            description = data.get('description')
            destenaire_tel = data.get('destenaire_tel')
            destenaire_nom_pre = data.get('destenaire_nom_pre')
            destenaire_ville = data.get('destenaire_ville')
            destenaire_Gouvernorat = data.get('destenaire_Gouvernorat')
            destenaire_zipcode = data.get('destenaire_zipcode')
            poid_total = data.get('poid_total')
            list_article_json = data.get('list_article_json')
            status_colis = data.get('status_colis')
            jour_depart = data.get('jour_depart')
            creation_date = data.get('creation_date')

            client = get_object_or_404(CustomUser, id=client_id)

            colis = Colis.objects.create(
                matricule=matricule,
                client=client,
                description=description,
                prix=prix,
                destenaire_adresse=destenaire_adresse,
                destenaire_email=destenaire_email,
                destenaire_tel=destenaire_tel,
                destenaire_nom_pre=destenaire_nom_pre,
                destenaire_ville=destenaire_ville,
                destenaire_Gouvernorat=destenaire_Gouvernorat,
                destenaire_zipcode=destenaire_zipcode,
                poid_total=poid_total,
                list_article_json=list_article_json,
                status_colis=status_colis,
                jour_depart=jour_depart,
                creation_date=creation_date
            )

            return Response({'message': 'Colis a éte crée'}, status=201)

        except CustomUser.DoesNotExist:
            return Response({'error': 'Client n exist pas'}, status=400)

        except Exception as e:
            return Response({'erruer serveur': str(e)}, status=500)
    
    elif request.method == 'GET':
        try:
            poids_str = request.GET.get('poids')
            if poids_str is not None:
                poids = float(poids_str)
                response = None
                if 0 < poids <= 10:
                    response = Decimal(poids * 0.300)
                elif 10 < poids <= 30:
                    response = Decimal(poids * 0.750)
                elif poids > 30:
                    response = Decimal(poids * 1.000)
                else:
                    response = None

                if response is not None:
                    return Response({'prix_colis': "{:.3f}".format(response)}, status=200)
                else:
                    return Response({'error': 'Le poids doit être supérieur à zéro'}, status=400)
            else:
                return Response({'error': 'Le paramètre poids est manquant'}, status=400)

        except ValueError:
            return Response({'error': 'La valeur n\'est pas un nombre valide'}, status=400)

        

@api_view(['GET'])

def get_colis_by_client_id(request, client_id):
    if request.method == 'GET':
        try:
            client = get_object_or_404(CustomUser, id=client_id)

            colis_instances = Colis.objects.filter(client=client)

            serializer = ColisSerializer(colis_instances, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({'error': 'Client nexist pas'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'erreur serveur': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_colis_by_transporteur_id(request, transporteur_id):
    if request.method == 'GET':
        try:
            transporteur = get_object_or_404(CustomUser, id=transporteur_id)

            colis_instances = Colis.objects.filter(transporteur=transporteur)

            serializer = ColisSerializer(colis_instances, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({'error': 'transporteur nexist pas'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'erreur serveur': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_colis(request, colis_id):
    if request.method == 'DELETE':
        try:
            colis = get_object_or_404(Colis, id=colis_id)

            if colis.client != request.user:
                return Response({'error': 'You do not have permission to delete this Colis'}, status=status.HTTP_403_FORBIDDEN)

            colis.delete()

            return Response({'message': 'Colis deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

        except Colis.DoesNotExist:
            return Response({'error': 'Colis does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['POST'])
def create_transporteur_calendrier(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            transporteur_id = data.get('transporteur_id')
            jour_depart = data.get('jour_depart')
            if TransporteurCalendrier.objects.filter(jour_depart=jour_depart).exists():
                return Response({'error': 'A TransporteurCalendrier with this jour_depart already exists'}, status=400)

            transporteur = data.get('transporteur')
            jour_depart = data.get('jour_depart')
            heure_depart = data.get('heure_depart')
            poids_disponible_jour = data.get('poids_disponible_jour')
            poids_total_colis_jour = data.get('poids_total_colis_jour')
            destenaire_zipcode = data.get('destenaire_zipcode')
            destenaire_Gouvernorat = data.get('destenaire_Gouvernorat')
            

            transporteur = get_object_or_404(CustomUser, id=transporteur_id)

            _TransporteurCalendrier = TransporteurCalendrier.objects.create(

                transporteur=transporteur,
                jour_depart=jour_depart,
                heure_depart=heure_depart,
                poids_disponible_jour=poids_disponible_jour,
                poids_total_colis_jour=poids_total_colis_jour,
                destenaire_zipcode=destenaire_zipcode,
                destenaire_Gouvernorat=destenaire_Gouvernorat,

                
            )

            return Response({'message': 'TransporteurCalendrier a éte crée'}, status=201)

        except CustomUser.DoesNotExist:
            return Response({'error': 'Transporteur n exist pas'}, status=404)


        



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_transporteur_calendriers(request, transporteur_id):
    if request.method == 'GET':
            transporteur_calendriers = TransporteurCalendrier.objects.filter(transporteur_id=transporteur_id)
            serializer = TransporteurCalendrierSerializer(transporteur_calendriers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_by_id(request, user_id):
    try:
        user = get_object_or_404(CustomUser, id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    






@api_view(['GET'])
def get_colis_compare(request, transporteur_id):
    if request.method == 'GET':
        try:
            transporteur = get_object_or_404(CustomUser, id=transporteur_id)
            transporteur_calendriers = TransporteurCalendrier.objects.filter(transporteur=transporteur)
            colis_list = []

            for calendrier in transporteur_calendriers:
                poids_disponible = Decimal(str(calendrier.poids_disponible_jour))
                poids_total_colis = Decimal(str(calendrier.poids_total_colis_jour))
                _poid_total = poids_disponible - poids_total_colis

                all_colis = Colis.objects.filter(
                    jour_depart=calendrier.jour_depart,
                    destenaire_Gouvernorat=calendrier.destenaire_Gouvernorat,
                    destenaire_zipcode=calendrier.destenaire_zipcode,
                    status_colis="Traitement"
                )

                filtered_colis = []
                for colis in all_colis:
                    if Decimal(str(colis.poid_total)) <= _poid_total:
                        filtered_colis.append(colis)

                colis_list.extend(filtered_colis)

            serializer = ColisSerializer(colis_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({'error': 'Transporteur n\'existe pas'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'erreur serveur': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['PUT'])

def update_colis_status(request, colis_id):

    try:
        print(request.data)
        colis = get_object_or_404(Colis, id=colis_id)
        transporteur = get_object_or_404(CustomUser, id=request.data['transporteur_id'])
        client = get_object_or_404(CustomUser, id=colis.client_id)
        new_status_colis = request.data.get('status_colis')
        new_transporteur_id = request.data.get('transporteur_id')

        if new_status_colis is not None:
            colis.status_colis = new_status_colis
        
        if new_transporteur_id is not None:
            colis.transporteur_id = new_transporteur_id
            

        colis.save(update_fields=['status_colis', 'transporteur_id'])
        serializer = ColisSerializer(colis)
        content = 'Votre colis de matricule '+colis.matricule +'est '+new_status_colis
        message = f'<html lang="en"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0">  </head> <body style="font-family: Arial, sans-serif; margin: 0; padding: 0;"> <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0"> <tr> <td style="padding: 20px 0;"> <table align="center" width="600" cellspacing="0" cellpadding="0" border="0"> <tr> <td align="center" style="background-color: #f2f2f2; padding: 40px 0;"> <h1>Cher Utilisateur!</h1> <p>{content}</p> <!-- Button --> <table role="presentation" cellspacing="0" cellpadding="0" border="0"> <tr> <td style="border-radius: 3px; background-color: #1a73e8; text-align: center;"> <a href="http://127.0.0.1:3000/" class="button" target="_blank" style="display: inline-block; padding: 15px 30px; color: #ffffff; text-decoration: none; font-weight: bold;">Voir Détail</a> </td> </tr> </table> </td> </tr> </table> </td> </tr> </table> </body> </html> '
        send_email('Nouveau message de Colis.tn', message, colis.destenaire_email)
        content = ''
        message = f'<html lang="en"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0">  </head> <body style="font-family: Arial, sans-serif; margin: 0; padding: 0;"> <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0"> <tr> <td style="padding: 20px 0;"> <table align="center" width="600" cellspacing="0" cellpadding="0" border="0"> <tr> <td align="center" style="background-color: #f2f2f2; padding: 40px 0;"> <h1>Cher Utilisateur!</h1> <p>{content}</p> <!-- Button --> <table role="presentation" cellspacing="0" cellpadding="0" border="0"> <tr> <td style="border-radius: 3px; background-color: #1a73e8; text-align: center;"> <a href="http://127.0.0.1:3000/" class="button" target="_blank" style="display: inline-block; padding: 15px 30px; color: #ffffff; text-decoration: none; font-weight: bold;">Voir Détail</a> </td> </tr> </table> </td> </tr> </table> </td> </tr> </table> </body> </html> '
        send_email('Nouveau message de Colis.tn', message, transporteur)
        content = ''
        message = f'<html lang="en"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0">  </head> <body style="font-family: Arial, sans-serif; margin: 0; padding: 0;"> <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0"> <tr> <td style="padding: 20px 0;"> <table align="center" width="600" cellspacing="0" cellpadding="0" border="0"> <tr> <td align="center" style="background-color: #f2f2f2; padding: 40px 0;"> <h1>Cher Utilisateur!</h1> <p>{content}</p> <!-- Button --> <table role="presentation" cellspacing="0" cellpadding="0" border="0"> <tr> <td style="border-radius: 3px; background-color: #1a73e8; text-align: center;"> <a href="http://127.0.0.1:3000/" class="button" target="_blank" style="display: inline-block; padding: 15px 30px; color: #ffffff; text-decoration: none; font-weight: bold;">Voir Détail</a> </td> </tr> </table> </td> </tr> </table> </td> </tr> </table> </body> </html> '
        send_email('Nouveau message de Colis.tn', message, client)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except Colis.DoesNotExist:
        return Response({'error': "Colis n'existe pas"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    



@api_view(['POST'])
def upload_images(request):
    images = {
        'image1': request.FILES.get('image1'),
        'image2': request.FILES.get('image2'),
        'image3': request.FILES.get('image3'),
        'image4': request.FILES.get('image4')
    }
   
    for key, image in images.items():
        if image:
            save_image(image)

    return Response({"message": "Images uploaded successfully"})

def save_image(image):
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
    os.makedirs(upload_dir, exist_ok=True)

    with open(os.path.join(upload_dir, image.name), 'wb') as f:
        for chunk in image.chunks():
            f.write(chunk)



@api_view(['POST'])
def cree_reclamation(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            _reclamant = data.get('reclamant')
            _defendeur = data.get('defendeur')
            sujet = data.get('sujet')
            description = data.get('description')
            _colis = data.get('colis')
            date_reclamation = data.get('date_reclamation')

            reclamant = get_object_or_404(CustomUser, id=_reclamant)
            defendeur = get_object_or_404(CustomUser, id=_defendeur)
            colis = get_object_or_404(Colis, id=_colis)

            _Reclamation = Reclamation.objects.create(

                defendeur=defendeur,
                reclamant=reclamant,
                sujet=sujet,
                description=description,
                colis=colis,
                date_reclamation=date_reclamation,
                
            )
            users_with_role_a = CustomUser.objects.filter(role='a')
            for user in users_with_role_a:
                content = 'Vous avez une Reclamation!'
                message = f'<html lang="en"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0">  </head> <body style="font-family: Arial, sans-serif; margin: 0; padding: 0;"> <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0"> <tr> <td style="padding: 20px 0;"> <table align="center" width="600" cellspacing="0" cellpadding="0" border="0"> <tr> <td align="center" style="background-color: #f2f2f2; padding: 40px 0;"> <h1>Cher Admin!</h1> <p>{content}</p> <!-- Button --> <table role="presentation" cellspacing="0" cellpadding="0" border="0"> <tr> <td style="border-radius: 3px; background-color: #1a73e8; text-align: center;"> <a href="http://localhost:3000/" class="button" target="_blank" style="display: inline-block; padding: 15px 30px; color: #ffffff; text-decoration: none; font-weight: bold;">Voir Détail</a> </td> </tr> </table> </td> </tr> </table> </td> </tr> </table> </body> </html> '
                send_email('Nouveau message de Colis.tn', message, user.email)

            return Response({'message': 'Réclamation crée'}, status=201)

        except Exception as e:
            return Response({'Erreur': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


        

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_reclamations(request, reclamant_id):
    try:
        if request.method == 'GET':
            reclamations = Reclamation.objects.filter(reclamant=reclamant_id)
            serializer = ReclamationSerializer(reclamations, many=True)
            return Response(serializer.data)
        
    except Reclamation.DoesNotExist:
        return Response({'Erreur': "Reclamation n'existe pas"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'Erreur': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_all_reclamations(request):
    if request.method == 'GET':
        reclamations = Reclamation.objects.all()
        serializer = ReclamationSerializer(reclamations, many=True)
        return Response(serializer.data)
    


@api_view(['PUT'])

def update_reclamation(request, reclamation_id):
    try:
        reclamation = Reclamation.objects.get(id=reclamation_id)
    except Reclamation.DoesNotExist:
        return Response({"error": "Reclamation not found"}, status=404)

    if request.method == 'PUT':
        serializer = UpdateReclamationSerializer(reclamation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['PUT'])
def acceptUser(request, userId):
    try:
        user = CustomUser.objects.get(id=userId)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.validated_data['valid_paiement'] = True
            
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
             
            serializer.validated_data['password'] = password 
            serializer.save()

            content = 'Votre demande de compte transporteur est accepté! Vous pouvez acceder a votre compte avec ce mot de passe: '+password
            message = f'<html lang="en"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0">  </head> <body style="font-family: Arial, sans-serif; margin: 0; padding: 0;"> <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0"> <tr> <td style="padding: 20px 0;"> <table align="center" width="600" cellspacing="0" cellpadding="0" border="0"> <tr> <td align="center" style="background-color: #f2f2f2; padding: 40px 0;"> <h1>Dear User!</h1> <p>{content}</p> <!-- Button --> <table role="presentation" cellspacing="0" cellpadding="0" border="0"> <tr> <td style="border-radius: 3px; background-color: #1a73e8; text-align: center;"> <a href="http://localhost:3000/" class="button" target="_blank" style="display: inline-block; padding: 15px 30px; color: #ffffff; text-decoration: none; font-weight: bold;">See Details</a> </td> </tr> </table> </td> </tr> </table> </td> </tr> </table> </body> </html> '
            to_email = user.email
            send_email('Nouveau message de Colis.tn', message, to_email)
            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

    
@api_view(['PUT'])

def blocage_utilisateur(request, userId):


    try:
        user = CustomUser.objects.get(id=userId)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            content = 'Votre compte Colis.tn est bloqué!'
            message = f'<html lang="en"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0">  </head> <body style="font-family: Arial, sans-serif; margin: 0; padding: 0;"> <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0"> <tr> <td style="padding: 20px 0;"> <table align="center" width="600" cellspacing="0" cellpadding="0" border="0"> <tr> <td align="center" style="background-color: #f2f2f2; padding: 40px 0;"> <h1>Dear User!</h1> <p>{content}</p> <!-- Button --> <table role="presentation" cellspacing="0" cellpadding="0" border="0"> <tr> <td style="border-radius: 3px; background-color: #1a73e8; text-align: center;"> <a href="http://localhost:3000/" class="button" target="_blank" style="display: inline-block; padding: 15px 30px; color: #ffffff; text-decoration: none; font-weight: bold;">See Details</a> </td> </tr> </table> </td> </tr> </table> </td> </tr> </table> </body> </html> '
            to_email = user.email
            send_email('Nouveau message de Colis.tn', message, to_email)


            serializer.validated_data['compte_valid'] = False 
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['PUT'])

def deblocage_utilisateur(request, userId):
    try:
        user = CustomUser.objects.get(id=userId)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            content = 'Votre compte Colis.tn est Débloqué!'
            message = f'<html lang="en"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0">  </head> <body style="font-family: Arial, sans-serif; margin: 0; padding: 0;"> <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0"> <tr> <td style="padding: 20px 0;"> <table align="center" width="600" cellspacing="0" cellpadding="0" border="0"> <tr> <td align="center" style="background-color: #f2f2f2; padding: 40px 0;"> <h1>Dear User!</h1> <p>{content}</p> <!-- Button --> <table role="presentation" cellspacing="0" cellpadding="0" border="0"> <tr> <td style="border-radius: 3px; background-color: #1a73e8; text-align: center;"> <a href="http://localhost:3000/" class="button" target="_blank" style="display: inline-block; padding: 15px 30px; color: #ffffff; text-decoration: none; font-weight: bold;">See Details</a> </td> </tr> </table> </td> </tr> </table> </td> </tr> </table> </body> </html> '
            to_email = user.email
            send_email('Nouveau message de Colis.tn', message, to_email)
            serializer.validated_data['compte_valid'] = True 
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])

def deleteUser(request, userId):
    if request.method == 'DELETE':
        try:
            colis = get_object_or_404(CustomUser, id=userId)

            colis.delete()

            return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

        except Colis.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)