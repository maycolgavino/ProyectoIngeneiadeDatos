# Guion y Paso a Paso: Demostración de Despliegue CI/CD (Multi-Cloud) 🎙️☁️

Este es tu guion ("Teleprompter") y el paso a paso de lo que debes hacer en pantalla para tu video de 3 a 5 minutos enfocado exclusivamente en cómo conectaste el proyecto a la nube (AWS/GCP/Azure) usando integración continua.

---

## 🎬 Preparación (Antes de grabar)
1. Ten abierto tu repositorio en **GitHub** en la pestaña de `Actions`.
2. Ten abierta otra pestaña con la consola de **AWS** (o GCP/Azure) en el servicio de Container Registry (ECR).
3. Ten abierto **VS Code** mostrando el archivo `.github/workflows/deploy-aws-dashboard.yml`.

---

## ▶️ Inicio de la Grabación

### ⏱️ Minuto 0:00 - 1:00 | Introducción a la Arquitectura CI/CD
*(Pantalla: Muestra tu VS Code con el archivo `.github/workflows/deploy-aws-dashboard.yml`)*

**Tú dices:**
> "Para garantizar que este proyecto de ingeniería de datos sea profesional y escalable, implementé un flujo de Integración y Despliegue Continuo (CI/CD).
> 
> He diseñado el proyecto con un enfoque **Multi-Cloud** y agnóstico a la infraestructura gracias a **Docker**. Como pueden ver en mi código, he configurado flujos en GitHub Actions no solo para Azure, sino también para AWS y Google Cloud.
> 
> En este archivo de configuración YAML, defino los pasos automatizados: primero, GitHub hace checkout de nuestro código; segundo, se autentica de forma segura con la nube usando credenciales encriptadas; y finalmente, empaqueta nuestro Dashboard de Streamlit en una imagen Docker y la sube al registro de contenedores."

### ⏱️ Minuto 1:00 - 2:00 | Mostrando la Conexión Segura (Los Secretos)
*(Pantalla: Cambia a tu navegador, ve a tu repositorio de GitHub -> Settings -> Secrets and variables -> Actions)*

**Tú dices:**
> "La parte más importante para conectar GitHub con la nube de forma segura es el manejo de credenciales. Bajo ninguna circunstancia quemamos contraseñas en el código.
> 
> En la configuración de mi repositorio, en la sección de 'Secrets', he inyectado las llaves de acceso que obtuve desde la consola de AWS (IAM). Aquí guardamos el `AWS_ACCESS_KEY_ID` y el `SECRET_ACCESS_KEY`. 
> 
> De esta forma, cuando GitHub Actions se ejecuta, tiene los permisos estrictamente necesarios para comunicarse con la nube, construir la infraestructura y publicar el tablero, manteniendo los estándares de ciberseguridad."

### ⏱️ Minuto 2:00 - 3:00 | Ejecutando el Pipeline en Vivo
*(Pantalla: Ve a la pestaña 'Actions' en GitHub. Selecciona el flujo de AWS y haz clic en 'Run workflow'. Entra al workflow mientras corre para que se vea la terminal de GitHub.)*

**Tú dices:**
> "Vamos a ver esto en acción. Al lanzar este workflow manualmente (o cuando hacemos un push a la rama principal), se levanta un servidor virtual en GitHub.
>
> Como podemos ver en los logs en tiempo real, está instalando las dependencias de Python, descargando Streamlit y Pandas, y construyendo nuestra imagen Docker usando nuestro `Dockerfile.dashboard`.
> 
> Una vez construido, automáticamente inicia sesión en Amazon ECR (Elastic Container Registry) y hace el 'push' de la imagen. Este mismo principio lo apliqué para Azure Container Registry y Google Artifact Registry."

### ⏱️ Minuto 3:00 - 4:00+ | El Resultado en la Nube y Cierre
*(Pantalla: Cambia a tu consola de AWS (o la nube que elijas), refresca la página y muestra que la imagen Docker acaba de llegar. Luego muestra el Dashboard final en otra pestaña o en localhost para cerrar).*

**Tú dices:**
> "Si voy a mi consola de AWS y refresco, podemos ver que hace unos segundos acaba de llegar la última versión empaquetada de nuestro código. Desde aquí, AWS App Runner o Azure Web Apps toman esta imagen y la exponen al mundo en una URL pública.
> 
> *(Muestra el dashboard)*
> Y este es el resultado final. Un Datamart analítico totalmente interactivo, consumiendo los datos procesados de la Maderera, y desplegado en la nube sin intervención manual. Esto completa nuestro ciclo de vida del dato: desde la ingesta en la Capa Bronze, hasta la visualización y el despliegue automático. Muchas gracias."

---

## 💡 Consejos de Presentación
- **Fluye natural:** No lo leas como un robot, usa este guion como guía pero dilo con tus propias palabras.
- **Señala con el mouse:** Cuando hables de los secretos o de las líneas de código (el checkout, la autenticación), sombrea el texto con tu mouse para que el profesor sepa a dónde mirar.
- **¿Qué pasa si demora?:** Si el "Run workflow" tarda mucho en GitHub (a veces construir Docker toma 2 mins), puedes pausar la grabación o tener un video pre-grabado de la ejecución y simplemente relatar encima de él.
