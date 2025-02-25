import os 
import boto3
from dotenv import load_dotenv
from typing import List


load_dotenv()


AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION: str = os.getenv("AWS_REGION")
BUCKET_NAME: str  = os.getenv("BUCKET_NAME")


s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key= AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

def listar_arquivos(pasta:str) -> List[str]:
    """Lista todos os arquivos de uma pasta local"""
    arquivos: List[str] = []
    for nome_arquivo in os.listdir(pasta):
        caminho_completo = os.path.join(pasta, nome_arquivo)
        if os.path.isfile(caminho_completo):
            arquivos.append(caminho_completo)
        return arquivos
    

def upload_arquivos_para_s3(arquivos: List[str]) -> None:
    """Faz upload dos arquivos listados para o S3"""
    for arquivo in arquivos:
        nome_arquivo:str = os.path.basename(arquivo)
        s3_client.upload_file(arquivo, BUCKET_NAME, nome_arquivo)
        print(f'{nome_arquivo} foi enviado para o S3')

def deletar_arquivos_locais(arquivos: List[str]) -> None:
    """Deleta arquivos locais após o upload"""
    for arquivo in arquivos:
        os.remove(arquivo)
        print(f'Arquivo {arquivo} foi deletado')


def executar_backup(pasta:str) -> None:
    """Executa o processo de backup completo"""
    arquivos: List[str] = listar_arquivos(pasta)
    if arquivos:
        upload_arquivos_para_s3(arquivos)
        deletar_arquivos_locais(arquivos)
    else:
        print('Nenhum arquivo encotrado para backup')


if __name__ == '__main__':
    PASTA_LOCAL: str = 'download'
    executar_backup(PASTA_LOCAL)

