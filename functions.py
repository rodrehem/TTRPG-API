import random
import re
from s3confing import AWS_REGION, s3_client, S3_BUCKET_NAME
from urllib.parse import quote_plus


def roll_dice(roll_quantity: int, face_count: int, modifier: int):

    """
    Simula a rolagem de dados e retorna uma string com os resultados.

    Args:
        roll_quantity: Quantidade de dados a serem rolados.
        face_count: Número de faces de cada dado.
        advantage: Um valor a ser somado ao total dos dados (modificador).

    Return:
        Uma string com os detalhes da rolagem, resultados individuais e o total.
    """

    dice_results = [random.randint(1, face_count) for n in range(roll_quantity)]
    dices_sum = sum(dice_results)

    if modifier == 0:
        texto = [f"Rolagem de {roll_quantity}d{face_count}\n\n"]
    else:
        texto = [f"Rolagem de {roll_quantity}d{face_count}+{modifier}\n\n"]

    for i, result in enumerate(dice_results):
        texto.append(f"Dado {i+1}: {result}\n")
    
    if modifier == 0:
        texto.append(f"\nTotal: {dices_sum}")
    else:
       texto.append(f"\nTotal: {dices_sum}\nTotal com modificador: {dices_sum + modifier}")
    
    return "".join(texto), str(dices_sum + modifier)

#------------------------------------------------------------------------------------------------------

def roll_requisition(str: str) -> str:

    """
    Args:
        str: Recebe uma string formatada como 
         - 1
         - 3
         - 1d6
         - 3d10
         - 1d20+10
         - 3d100+50
         - 30d1000+500
    Return
        Retorna uma string com o resultado dos dados
    """
        
    regex = r'(\d{1,3})(?:[dD](\d*))?([+-]\d+)?'
    r'''
    (\d{1,3}) - Busca todos os numeros de 1 a 3 digitos
    (?:[dD](\d*))? - Se houver um d ou um D captura o valor ao lado dele, 
    se não houver não captura nada, se houver apenas o d ou D sem valor ao lado retorna vazio
    ([+-]\d+)? - Opcional busca todos os valores após um + ou um -
    '''
    match = re.fullmatch(regex, str.strip())
    
    if not match: return "Insira um valor válido"

    roll_quantity, face_count, modifier = match.groups()

    roll_quantity = int(roll_quantity)
    if face_count: face_count = int(face_count)
    else: face_count = 6
    if modifier: modifier = int(modifier)
    else: modifier = 0

    resultado = roll_dice(roll_quantity, face_count, modifier)

    if len(resultado[0]) > 2000: return f'Resultados ultrapassam 2000 caracteres\nTotal: {resultado[1]}'
    else: return resultado[0]

#------------------------------------------------------------------------------------------------------

def upload_file(file, file_name = None):
    try:
        safe_file_name = quote_plus(file_name)
        
        file_content_type = file.content_type
        extra_args = {
            'ContentType': file_content_type,
            'ContentDisposition': 'inline'
        }

        s3_client.upload_fileobj(file.file, S3_BUCKET_NAME, file_name, ExtraArgs = extra_args)
        object_url = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{safe_file_name}"
        return object_url
    except Exception as e:
        return None