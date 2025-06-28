import json
import boto3

def lambda_handler(event, context):
    # Mostrar evento SNS
    print("Evento recibido:", event)

    # Extraer y parsear el mensaje SNS
    alumno_json = json.loads(event['Records'][0]['Sns']['Message'])

    # Inicializar conexión a DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos_seguridad')

    # Preparar el item para la tabla
    alumno = {
        'tenant_id': alumno_json['tenant_id'],
        'alumno_id': alumno_json['alumno_id'],
        'nombre': alumno_json['alumno_datos']['nombre'],
        'sexo': alumno_json['alumno_datos']['sexo'],
        'fecha_nac': alumno_json['alumno_datos']['fecha_nac'],
        'celular': alumno_json['alumno_datos']['celular'],
        'direccion': alumno_json['alumno_datos']['domicilio']['direc'],
        'distrito': alumno_json['alumno_datos']['domicilio']['distrito'],
        'provincia': alumno_json['alumno_datos']['domicilio']['provincia'],
        'departamento': alumno_json['alumno_datos']['domicilio']['departamento'],
        'pais': alumno_json['alumno_datos']['domicilio']['pais']
    }

    print("Alumno procesado:", alumno)

    # Insertar en DynamoDB
    response = table.put_item(Item=alumno)

    return {
        'statusCode': 200,
        'body': json.dumps('Alumno registrado en sistema de seguridad'),
        'response': response
    }
