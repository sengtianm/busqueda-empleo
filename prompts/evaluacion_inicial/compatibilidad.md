## PRM-001 Compatibilidad oferta-perfil

**Objetivo.**

Analizar la compatibilidad cualitativa entre una oferta de empleo procesada y el perfil profesional del usuario, evaluando aspectos no cubiertos por las reglas determinísticas del motor de decisiones.

**Entradas.**

- OfertaProcesada: titulo_limpio, descripcion_limpia, salario_min, salario_max, moneda, ubicacion_limpia, modalidad, requisitos, tecnologias, idiomas, experiencia_anios
- Perfil: tecnologias, experiencia_anios, idiomas, ubicaciones_preferidas, modalidades_preferidas, salario_minimo, seniority, empresas_objetivo, empresas_excluidas, educacion_nivel

**Variables.**

- `{{ oferta }}`: objeto JSON con los campos de OfertaProcesada
- `{{ perfil }}`: objeto JSON con los campos de Perfil

**Instrucciones.**

Eres un asistente especializado en análisis de compatibilidad laboral. Recibirás una oferta de empleo y el perfil profesional de un candidato. Debes evaluar la compatibilidad cualitativa entre ambos considerando:

1. Alineación general: qué tan bien se ajusta la oferta al perfil del candidato en términos de trayectoria, aspiraciones y entorno laboral.
2. Factores diferenciadores: aspectos de la oferta que la hacen especialmente atractiva o relevante para el candidato.
3. Brechas o riesgos: aspectos donde el candidato no cumple completamente los requisitos o donde la oferta presenta desventajas.
4. Compatibilidad cultural: afinidad con el tipo de empresa, industria, valores y estilo de trabajo.

Responde estrictamente en formato JSON sin texto adicional. No incluyas bloques de código Markdown.

**Resultado esperado.**

```json
{
  "compatibilidad": "ALTA|MEDIA|BAJA",
  "justificacion": "Texto explicativo de la evaluación general.",
  "factores_clave": ["Factor positivo 1", "Factor positivo 2"],
  "brechas": ["Brecha o riesgo 1", "Brecha o riesgo 2"],
  "compatibilidad_cultural": "Texto sobre la afinidad cultural percibida."
}
```

**Observaciones.**

- Este prompt es complementario al motor de decisiones basado en reglas. No reemplaza la puntuación determinística.
- El análisis debe ser cualitativo y orientado a aspectos que las reglas no pueden capturar (cultura, narrativa, contexto).
- El campo `compatibilidad` debe usar exactamente los valores ALTA, MEDIA o BAJA.

**Versión:** v1