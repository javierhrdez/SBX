import requests
import json
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def luhn(n):
    sum = 0
    alt = 0
    i = len(n) - 1
    num = 0
    while i >= 0:
       num = int( n[ i ] )
       if alt:
          num = num * 2
          if num > 9:
             num = ( num % 10 ) + 1  
       sum = sum + num 
       alt = not alt 
       i -= 1
    return sum%10 == 0

def cipherRSA(texto):
    modules = base64.b64decode('xymBd9bjA9QcZDSMoqvDts/zvoOTt1xjgzXRWzSD2eHoVHrpVhPR8hJzXiJyjAQ/fzUSsFUoYzIs6irVtZpgbggvhbAs/ItkvbypUzFN4CPnWCmYCVNqf/hwnniVTOn1EJ8WhPXdc5r5PPgBX74GnEvy2GI4n8santnvQq3WvTE='.encode('utf-8'))
    modules = int.from_bytes(modules, byteorder='big')
    exponent = base64.b64decode('AQAB'.encode('utf-8'))
    exponent = int.from_bytes(exponent, byteorder='big')
    pubkey = RSA.construct((modules, exponent))
    cipher = PKCS1_v1_5.new(pubkey)
    encrypted_msg = cipher.encrypt(texto.encode('utf-8'))
    encoded_encrypted_msg = base64.b64encode(encrypted_msg) # base64 encoded strings are database friendly
    return encoded_encrypted_msg.decode('utf-8')

contrasenia = cipherRSA('clave')
email = 'mail@mail.com'
content_type = 'application/json; charset=UTF-8'
fuente = 'Movil'
user_agent = 'Dalvik/2.1.0 (Linux; U; Android 7.0; SM-G925W8 Build/NRD90M)'

headers = {
    'Content-Type': content_type,
    'fuente': fuente,
    'token': '',
    'idusuario': '',
    'User-Agent': user_agent,
}
data = '{"request": {"contrasenia":"' + contrasenia+ '","email":"' + email + '","fuente":"'+ fuente +'"}}'
response = requests.post('https://crt-rewards.starbucks.mx:17443/wsrewards/LoginMobile', headers=headers, data=data, verify=False)
respuesta = json.loads(response.text)
print(json.dumps(respuesta, sort_keys=True, indent=4))
datosMiembro = respuesta['datosMiembro']
print(json.dumps(datosMiembro, sort_keys=True, indent=4))
numeroMiembro = respuesta['numeroMiembro']
print(numeroMiembro,type(numeroMiembro))
tokenSeguridad = respuesta['tokenSeguridad']


nro_tarjeta = 'XXXXXXXXXXXXXXXX'
numeroMiembro = nro_tarjeta

headers = {
    'Content-Type': content_type,
    'tokenSeguridad': tokenSeguridad,
    'fuente': fuente,
    #'IdUsuario': -1,
    'IdUsuario': numeroMiembro,
    'User-Agent': user_agent,
}

#if luhn(nro_tarjeta):
data = '{"request": {"numeroTarjeta":"'+ nro_tarjeta + '"}}'
print('Nro. tarjeta:' + nro_tarjeta )
response = requests.post('https://crt-rewards.starbucks.mx:17443/wsrewards/ConsultaSaldoMobile', headers=headers, data=data, verify=False)
respuesta = json.loads(response.text)
print(json.dumps(respuesta, sort_keys=True, indent=4))
#else:
#    print('numero de tarjeta invalida')
