# PruebaTecnica

Para esta prueba tecnica se desarrollo el FrontEnd y BackEnd de una aplicación de inventario de productos.

## Para inicializar el proyecto se utiliza la siguiente secuencia de comandos:

### FrontEnd

    #### Project setup
    ```
    npm install
    ```

    #### Compiles and hot-reloads for development
    ```
    npm run serve
    ```

    #### Compiles and minifies for production
    ```
    npm run build
    ```

    #### Lints and fixes files
    ```
    npm run lint
    ```

### BackEnd

    #### Comandos
      Creación de entorno virutal
      python -m venv .venv

      Activar entorno virtual
      .env/Scripts/activate

      Desactivar Entorno virtual
      deactivate

      Instalación inicial:
      pip install -r requirements.txt

      Asignar variable de la aplicación
      Windows PowerShell
      $env:FLASK_APP = "manage.py"
      Windows cmd
      set FLASK_APP=manage.py
      Linux
      export FLASK_APP=manage.py

      Activar DEBUG
      Windows PowerShell
      $env:FLASK_DEBUG = "1"
      Windows cmd
      set FLASK_DEBUG=1
      Linux
      export FLASK_DEBUG=1

      Ejecutar la aplicación:
      flask run

### Acceder a la aplicación

      Abrir la siguiente URL en su navegador para ver la documentación de swagger
      http://127.0.0.1:5000/swagger
