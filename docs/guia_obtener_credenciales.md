# Guía Práctica: ¿Cómo obtener las credenciales para GitHub Actions? 🔐

Para que GitHub pueda subir tu código a la nube, necesitas darle llaves de acceso especiales. A continuación, te explico **exactamente en qué menú** de cada nube consigues estas credenciales:

---

## 🟠 1. Amazon Web Services (AWS)
Necesitamos 2 datos: `AWS_ACCESS_KEY_ID` y `AWS_SECRET_ACCESS_KEY`.

**Paso a paso:**
1. Entra a la consola de AWS.
2. En el buscador superior, escribe **IAM** y entra al servicio.
3. En el menú izquierdo, ve a **Usuarios** (Users).
4. Dale clic al botón **Crear usuario** (ej. llámalo `github-actions-user`).
5. En la sección de permisos, ponle *Adjuntar políticas directamente*. Para este proyecto rápido, ponle **`AmazonEC2ContainerRegistryFullAccess`**.
6. Termina de crear el usuario. Haz clic en su nombre para ver los detalles.
7. Ve a la pestaña **Credenciales de seguridad** (Security credentials).
8. Baja hasta la sección **Claves de acceso** (Access keys) y dale a **Crear clave de acceso**.
9. Elige "Command Line Interface (CLI)".
10. **¡Ahí están!** Copia el `Access Key ID` y el `Secret access key` y pégalos en los "Secrets" de GitHub. *(Ojo: El Secret Key solo te lo muestra una vez, si lo pierdes tienes que crear otra llave).*

---

## 🔵 2. Google Cloud Platform (GCP)
Necesitamos 1 dato: `GCP_CREDENTIALS` (Es un archivo JSON completo).

**Paso a paso:**
1. Entra a la consola de Google Cloud y selecciona tu proyecto.
2. En el menú hamburguesa (arriba a la izquierda), ve a **IAM y administración > Cuentas de servicio** (Service Accounts).
3. Haz clic en **+ CREAR CUENTA DE SERVICIO** (ej. llámala `github-deployer`).
4. En permisos (Roles), añádele: **Administrador de Cloud Run** (Cloud Run Admin) y **Administrador de Storage** (Storage Admin). Continúa y crea la cuenta.
5. Verás tu cuenta recién creada en la lista. Haz clic en los tres puntitos (Acciones) a la derecha y selecciona **Administrar claves** (Manage keys).
6. Clic en **AGREGAR CLAVE > Crear clave nueva**.
7. Selecciona el formato **JSON** y dale a Crear.
8. Se descargará un archivo `.json` a tu computadora. 
9. **Abre ese archivo con un bloc de notas**, copia ABSOLUTAMENTE TODO el texto (desde la llave `{` hasta la `}`) y pégalo como valor en el Secret `GCP_CREDENTIALS` de GitHub.

---

## 🟦 3. Microsoft Azure
Necesitamos el `AZURE_CREDENTIALS` (un JSON) y las llaves de tu Container Registry.

**Para el `AZURE_CREDENTIALS`:**
1. Tienes que abrir la terminal (puede ser la de Azure Cloud Shell en el navegador).
2. Tienes que crear un "Service Principal" ejecutando este comando (reemplaza `<subscription-id>` con el ID de tu suscripción):
   ```bash
   az ad sp create-for-rbac --name "github-actions-deploy" --role contributor --scopes /subscriptions/<subscription-id> --sdk-auth
   ```
3. La terminal te arrojará un bloque JSON. Cópiate todo ese bloque (desde la `{` hasta la `}`) y pégalo en el Secret `AZURE_CREDENTIALS` en GitHub.

**Para el `ACR_USERNAME` y `ACR_PASSWORD`:**
1. En el portal de Azure, busca tu servicio de **Container registries** y entra.
2. En el menú de la izquierda, baja hasta **Access keys** (Claves de acceso).
3. Asegúrate de que la casilla "Admin user" (Usuario administrador) esté habilitada.
4. Ahí verás tu **Username** y dos **Passwords**. Copia el username y cualquiera de los passwords y pégalos en sus respectivos Secrets de GitHub.

---
> 💡 **Recordatorio Final:** Todos estos valores se pegan en tu repositorio de GitHub yendo a **Settings > Secrets and variables > Actions > New repository secret**. Nunca los pegues directamente dentro de tu código.
