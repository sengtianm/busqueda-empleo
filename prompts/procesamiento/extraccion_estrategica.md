## PRM-003 Extracción estratégica

**Objetivo.**

Identificar los elementos estratégicos de una oferta de empleo en relación con el perfil del candidato: factores diferenciadores, requisitos negociables, riesgos y oportunidades para la candidatura.

**Entradas.**

- OfertaProcesada: titulo_limpio, descripcion_limpia, salario_min, salario_max, moneda, ubicacion_limpia, modalidad, requisitos, tecnologias, idiomas, experiencia_anios
- Perfil: tecnologias, experiencia_anios, idiomas, ubicaciones_preferidas, modalidades_preferidas, salario_minimo, seniority, empresas_objetivo, empresas_excluidas, educacion_nivel

**Variables.**

- `{{ oferta }}`: objeto JSON con los campos de OfertaProcesada
- `{{ perfil }}`: objeto JSON con los campos de Perfil

**Instrucciones.**

Eres un estratega de carrera profesional. Recibirás una oferta de empleo y el perfil de un candidato. Debes extraer información estratégica para maximizar las posibilidades de éxito en el proceso:

1. Factores diferenciadores: aspectos de la oferta o del perfil del candidato que pueden marcar la diferencia frente a otros postulantes.
2. Requisitos negociables: requisitos de la oferta donde el candidato podría compensar con experiencia equivalente, formación o habilidades transferibles.
3. Riesgos: aspectos que podrían jugar en contra del candidato (falta de experiencia en un área clave, brecha tecnológica, etc.).
4. Oportunidades: elementos de la oferta que representan una oportunidad de crecimiento o aprendizaje para el candidato.
5. Posicionamiento recomendado: estrategia general sugerida para abordar la candidatura.

Responde estrictamente en formato JSON sin texto adicional. No incluyas bloques de código Markdown.

**Resultado esperado.**

```json
{
  "diferenciadores": ["Diferenciador 1", "Diferenciador 2"],
  "requisitos_negociables": [
    {"requisito": "Descripción", "estrategia": "Cómo compensarlo"}
  ],
  "riesgos": [
    {"riesgo": "Descripción", "severidad": "alta|media|baja"}
  ],
  "oportunidades": ["Oportunidad 1", "Oportunidad 2"],
  "posicionamiento": "Estrategia general recomendada para la candidatura."
}
```

**Observaciones.**

- Los riesgos deben priorizarse por severidad para focalizar los esfuerzos de mitigación.
- El posicionamiento debe ser accionable: qué énfasis darle a la candidatura.
- Este prompt se ejecuta después del diagnóstico de la vacante (PRM-002).

**Versión:** v1