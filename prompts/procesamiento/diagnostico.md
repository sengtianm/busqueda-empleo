## PRM-002 Diagnóstico de la vacante

**Objetivo.**

Realizar un análisis detallado de una oferta de empleo para comprender la naturaleza de la vacante, los requisitos reales, las competencias necesarias, las responsabilidades, los beneficios y la cultura empresarial.

**Entradas.**

- OfertaProcesada: titulo_limpio, descripcion_limpia, salario_min, salario_max, moneda, ubicacion_limpia, modalidad, requisitos, tecnologias, idiomas, experiencia_anios

**Variables.**

- `{{ oferta }}`: objeto JSON con los campos de OfertaProcesada

**Instrucciones.**

Eres un analista laboral experto. Recibirás los datos de una oferta de empleo procesada. Debes extraer y estructurar la siguiente información:

1. Diagnóstico general: descripción concisa de qué busca la empresa y qué ofrece.
2. Requisitos clave: lista de los requisitos realmente indispensables (distinguiendo entre obligatorios y deseables).
3. Competencias requeridas: habilidades técnicas y blandas necesarias para el rol.
4. Responsabilidades del puesto: descripción clara de las tareas y obligaciones principales.
5. Beneficios y condiciones: elementos como salario, modalidad, horario, y otros beneficios mencionados.
6. Cultura empresarial: indicios sobre el entorno, valores y estilo de trabajo de la empresa.

Responde estrictamente en formato JSON sin texto adicional. No incluyas bloques de código Markdown.

**Resultado esperado.**

```json
{
  "diagnostico": "Resumen ejecutivo del análisis de la vacante.",
  "requisitos_clave": [
    {"requisito": "Descripción", "tipo": "obligatorio|deseable"}
  ],
  "competencias": {
    "tecnicas": ["Competencia 1", "Competencia 2"],
    "blandas": ["Competencia 1", "Competencia 2"]
  },
  "responsabilidades": ["Responsabilidad 1", "Responsabilidad 2"],
  "beneficios": ["Beneficio 1", "Beneficio 2"],
  "cultura_empresarial": "Descripción de indicios culturales."
}
```

**Observaciones.**

- Diferenciar claramente entre requisitos obligatorios y deseables.
- La cultura empresarial debe inferirse del lenguaje, valores y descripción utilizados en la oferta.
- Este diagnóstico es la base para los prompts de extracción estratégica y diseño de candidatura.

**Versión:** v1