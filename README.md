# Coaudial

Este es el proyecto de Introducción a la Ingeniería de Coaudial. Se trata de una plataforma web que centraliza fundaciones benéficas y proporciona streaming de información asociada a ellas.

## Integrantes
- Amaro Alarcón
- Gabriel Covarrubias
- Marcelo Pérez
- Vicente Jiménez

## Requisitos
Para ejecutar Coaudial, necesitarás tener instalado Python 3.11.4, Django 4.1 y Pillow. 

## Instalación

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/tu-repositorio.git
   cd tu-repositorio
   ```

2. **Crea un entorno virtual**:
   ```bash
   python -m venv venv
   ```

3. **Activa el entorno virtual**:
   - En Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - En macOS y Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

Si no tienes pip instalado, puedes hacerlo siguiendo estos pasos:
1. Abre una terminal o línea de comandos.
2. Escribe el siguiente comando y presiona Enter:
   ```bash
   python -m ensurepip --default-pip
   ```

## Ejecución

1. **Realiza migraciones**:
   ```bash
   python manage.py migrate
   ```

2. **Inicia el servidor de desarrollo**:
   ```bash
   python manage.py runserver
   ```

3. Abre tu navegador web y ve a `http://127.0.0.1:8000/` para ver la aplicación en funcionamiento.



