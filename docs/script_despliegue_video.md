# 🎬 Guion de Presentación del Proyecto (5 Minutos)

**Duración Estimada:** 5 minutos.
**Recomendación:** Ten abiertas todas las pestañas antes de grabar (VS Code, AWS EC2, GitHub Actions, AWS ECR, y la URL de tu Dashboard).

---

## ⏱️ Minuto 0:00 - 1:00 | 1. Introducción y el Problema
*(Pantalla: Muestra tu rostro brevemente o la portada de tu informe/diapositiva)*

**Tú dices:**
> "Hola a todos, mi nombre es Maycol Lopez Gavino y hoy les presentaré mi Proyecto Final de Ingeniería de Datos. 
> 
> El caso de estudio se basa en una importante empresa del sector maderero peruano. Esta empresa se enfrentaba a un gran problema: tenían decenas de miles de registros de ventas diarias, un enorme catálogo de especies maderables y miles de clientes, pero toda esta información estaba completamente desordenada, descentralizada y en formatos difíciles de cruzar. 
> 
> Debido a esto, los gerentes no podían saber algo tan vital como: ¿Qué especie de madera es la más rentable? ¿En qué meses vendemos más volumen? Tomar decisiones era como navegar a ciegas."

---

## ⏱️ Minuto 1:00 - 2:30 | 2. La Solución y la Arquitectura Medallón
*(Pantalla: Muestra tu VS Code, específicamente el archivo `main_pipeline.py` y `procesador_gold.py`)*

**Tú dices:**
> "Para resolver esto, diseñé un **Data Pipeline completamente automatizado** utilizando la **Arquitectura Medallón**.
> 
> Como pueden ver en mi código, el sistema está orquestado en 3 capas fundamentales:
> 1. **Capa Bronze:** Donde ingerimos todos los datos crudos manteniendo su historial original.
> 2. **Capa Silver:** Aquí utilizamos Python y Pandas para limpiar los datos y guardarlos en formato `Parquet`, reduciendo masivamente su tamaño y acelerando su lectura.
> 3. **Capa Gold:** Finalmente, aplicamos lógica de negocio para generar 'Datamarts' o cubos analíticos. Por ejemplo, agrupamos las ventas por especie de madera y mes para descubrir la rentabilidad neta.
> 
> Todo este flujo se ejecuta automáticamente, transformando el caos en inteligencia de negocios lista para consumirse."

---

## ⏱️ Minuto 2:30 - 3:30 | 3. CI/CD y Multi-Cloud
*(Pantalla: Cambia a tu navegador. Muestra la pestaña de GitHub Actions corriendo y luego la pestaña de AWS ECR)*

**Tú dices:**
> "Un proyecto moderno no solo debe funcionar de forma local, debe ser escalable. Por eso he implementado integración continua usando **GitHub Actions**. 
> 
> *[Señalas los workflows en GitHub]* Mi código está configurado bajo una filosofía **Multi-Cloud**. Cada vez que hago un cambio, GitHub empaqueta automáticamente toda mi arquitectura en contenedores **Docker** y la distribuye simultáneamente a Amazon ECR, Google Artifact Registry y Azure. 
> 
> *[Cambias a la pestaña de Amazon ECR]* Para la demostración de hoy, he decidido utilizar la nube de **Amazon Web Services (AWS)**. Aquí pueden ver nuestro repositorio de ECR, donde mi imagen Docker, que contiene tanto el Pipeline como el Dashboard, se almacenó de forma segura y exitosa."

---

## ⏱️ Minuto 3:30 - 4:15 | 4. Despliegue en AWS EC2 (Infraestructura como Código)
*(Pantalla: Muestra la consola de AWS EC2, enseñando tu instancia 'Maderera-Dashboard-Final' en ejecución)*

**Tú dices:**
> "Para el despliegue a producción de la interfaz gráfica, levantamos una máquina virtual robusta en **AWS EC2**. 
> 
> Pero no lo hicimos manualmente. Utilizamos un script de automatización *(muestras brevemente tu bloque de código de bash / User Data)* que se inyecta al encender la máquina. Este script instala Docker, descarga el repositorio, construye el contenedor y dispara nuestro pipeline de datos internamente para generar la información más actualizada. 
> 
> Gracias a este enfoque, si esta máquina se cae, podemos levantar otra idéntica en 3 minutos sin perder información, garantizando una alta disponibilidad del sistema."

---

## ⏱️ Minuto 4:15 - 5:00 | 5. Demostración en Vivo y Conclusión
*(Pantalla: Abres la pestaña con la IP pública donde está corriendo tu Dashboard de Streamlit)*

**Tú dices:**
> "Y aquí tenemos el resultado final operando 100% en la nube pública de AWS a través de nuestra IP elástica.
> 
> *[Interactúa con los filtros del dashboard: cambia de madera, filtra por fechas]* 
> Este Dashboard, construido con Streamlit, lee directamente los Datamarts de nuestra Capa Gold. Ahora, con un par de clics, la gerencia puede ver qué maderas generan más ingresos y cómo se comportan las ventas en tiempo real, resolviendo completamente el problema inicial de desinformación.
> 
> Con esta arquitectura Medallón empaquetada en Docker y desplegada vía CI/CD, hemos transformado datos estáticos en un activo estratégico para la empresa maderera. 
> 
> Muchas gracias por su atención."
