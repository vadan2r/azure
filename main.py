import streamlit as st
from azure.storage.blob import BlobServiceClient
import os
import pymssql
import uuid
import json
from dotenv import load_dotenv
load_dotenv()

BLOB_CONNECTION_STRING = os.getenv("BLOB_CONNECTION_STRING")
BLOB_CONTAINER_NAME = os.getenv("BLOB_CONTAINER_NAME")
BLOB_ACCOUNT_NAME = os.getenv("BLOB_ACCOUNT_NAME")

SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")
SQL_USER = os.getenv("SQL_USER")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")

st.title("Cadastro de Produtos")

#formulario de cadastro de produtos
product_name = st.text_input("Nome do Produto")
product_price = st.number_input("Preço do Produto", min_value=0.0, format="%.2f")
product_description = st.text_area("Descrição do Produto")
product_image = st.file_uploader("Imagem do Produto", type=["jpg", "jpeg", "png"])

#Salvar imagem no blob storage
def upload_blob(file):
    blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container=BLOB_CONTAINER_NAME, blob=file.name)
    blob_client.upload_blob(file, overwrite=True)
    return f"https://{BLOB_ACCOUNT_NAME}.blob.core.windows.net/{BLOB_CONTAINER_NAME}/{file.name}"

def insert_product(name, price, description, image_url):
    conn = pymssql.connect(server=SQL_SERVER, user=SQL_USER, password=SQL_PASSWORD, database=SQL_DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Products (Name, Price, Description, ImageUrl) VALUES (%s, %s, %s, %s)",
                   (name, price, description, image_url))
    conn.commit()
    cursor.close()
    conn.close()

def list_products():
    conn = pymssql.connect(server=SQL_SERVER, user=SQL_USER, password=SQL_PASSWORD, database=SQL_DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products

if st.button("Salvar Produto"):
    if product_image is not None:
        image_url = upload_blob(product_image)
        return_message = "Produto cadastrado com sucesso!"
    else:
        return_message = "Por favor, envie uma imagem."

st.header("Produtos Cadastrados")

if st.button("Listar Produtos"):
    return_message = "Produtos listados com sucesso!"