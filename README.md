# Create .env file
Crear un archivo .env en la raíz del proyecto que contenga los datos necesarios:


```
DB_USER=steamapp_user
DB_NAME=steamapp
DB_PASSWORD=steamapp
DB_HOST=localhost
TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
WEB_API_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
BASE_PATH=http://api.steampowered.com
STEAM_ID=76561198821036955
```

Para obtener el WEB_API_TOKEN iniciar sesión en steam en un navegador y usar:  https://store.steampowered.com/pointssummary/ajaxgetasyncconfig

Para lanzar los tests, lanzar el siguiente comando desde la raiz del proyecto:  python -m unittest discover -s tests -v