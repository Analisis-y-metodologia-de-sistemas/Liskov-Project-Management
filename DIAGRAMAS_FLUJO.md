# Diagramas de Flujo - Liscov Project Management

## Tabla de Contenidos

1. [Autenticación y Registro](#1-autenticación-y-registro)
2. [Gestión de Proyectos](#2-gestión-de-proyectos)
3. [Gestión de Sprints](#3-gestión-de-sprints)
4. [Gestión de Historias de Usuario](#4-gestión-de-historias-de-usuario)
5. [Gestión de Tareas](#5-gestión-de-tareas)
6. [Sistema de Comentarios](#6-sistema-de-comentarios)
7. [Flujos Administrativos](#7-flujos-administrativos)

---

## 1. Autenticación y Registro

### 1.1 Flujo de Login

```mermaid
flowchart TD
    Start([Usuario accede a /login/]) --> ShowForm[Mostrar formulario de login]
    ShowForm --> InputCreds[Usuario ingresa credenciales]
    InputCreds --> Submit[Usuario hace submit]
    Submit --> ValidateForm{¿Formulario válido?}

    ValidateForm -->|No| ShowError[Mostrar errores de validación]
    ShowError --> ShowForm

    ValidateForm -->|Sí| Authenticate{¿Credenciales correctas?}

    Authenticate -->|No| ShowAuthError[Mostrar error de autenticación]
    ShowAuthError --> ShowForm

    Authenticate -->|Sí| CheckActive{¿Usuario activo?}

    CheckActive -->|No| ShowInactive[Mostrar mensaje: cuenta inactiva]
    ShowInactive --> ShowForm

    CheckActive -->|Sí| CreateSession[Crear sesión]
    CreateSession --> Redirect[Redirigir a Dashboard]
    Redirect --> End([Fin])
```

**Descripción:**
1. Usuario accede a la página de login
2. Sistema muestra formulario con campos username y password
3. Usuario ingresa credenciales y envía formulario
4. Sistema valida formato del formulario
5. Si es válido, verifica credenciales contra base de datos
6. Si credenciales son correctas y cuenta está activa, crea sesión
7. Redirige al dashboard principal
8. Si hay error en cualquier paso, muestra mensaje y vuelve al formulario

---

### 1.2 Flujo de Logout

```mermaid
flowchart TD
    Start([Usuario hace click en Logout]) --> CheckAuth{¿Usuario autenticado?}

    CheckAuth -->|No| RedirectLogin[Redirigir a login]
    RedirectLogin --> End1([Fin])

    CheckAuth -->|Sí| DestroySession[Destruir sesión]
    DestroySession --> ClearCookies[Limpiar cookies]
    ClearCookies --> ShowMessage[Mostrar mensaje: sesión cerrada]
    ShowMessage --> RedirectLogin2[Redirigir a login]
    RedirectLogin2 --> End2([Fin])
```

**Descripción:**
1. Usuario hace click en botón de logout
2. Sistema verifica que hay sesión activa
3. Destruye la sesión del usuario
4. Limpia cookies de autenticación
5. Muestra mensaje de confirmación
6. Redirige a página de login

---

## 2. Gestión de Proyectos

### 2.1 Flujo de Creación de Proyecto

```mermaid
flowchart TD
    Start([Usuario hace click en 'Nuevo Proyecto']) --> CheckAuth{¿Usuario autenticado?}

    CheckAuth -->|No| RedirectLogin[Redirigir a login]
    RedirectLogin --> End1([Fin])

    CheckAuth -->|Sí| ShowForm[Mostrar formulario vacío]
    ShowForm --> UserFills[Usuario completa campos:<br/>- Nombre<br/>- Descripción<br/>- Fechas<br/>- Product Owner<br/>- Scrum Master<br/>- Equipo]

    UserFills --> Submit[Usuario hace submit]
    Submit --> ValidateForm{¿Formulario válido?}

    ValidateForm -->|No| ShowErrors[Mostrar errores:<br/>- Campos requeridos<br/>- Formatos inválidos]
    ShowErrors --> ShowForm

    ValidateForm -->|Sí| ValidateDates{¿Fecha fin > fecha inicio?}

    ValidateDates -->|No| ShowDateError[Error: fecha fin debe ser posterior]
    ShowDateError --> ShowForm

    ValidateDates -->|Sí| ValidateUsers{¿PO y SM son usuarios válidos?}

    ValidateUsers -->|No| ShowUserError[Error: usuarios inválidos]
    ShowUserError --> ShowForm

    ValidateUsers -->|Sí| SaveProject[Guardar proyecto en BD]
    SaveProject --> SaveTeam[Guardar relación M2M con team_members]
    SaveTeam --> ShowSuccess[Mostrar mensaje: Proyecto creado]
    ShowSuccess --> RedirectDetail[Redirigir a detalle del proyecto]
    RedirectDetail --> End2([Fin])
```

**Descripción:**
1. Usuario autenticado accede al formulario de creación
2. Sistema muestra formulario con todos los campos
3. Usuario completa información del proyecto
4. Sistema valida:
   - Campos requeridos
   - Formatos de datos
   - Fechas coherentes
   - Usuarios existentes
5. Si todo es válido, guarda en base de datos
6. Establece relaciones con usuarios (PO, SM, equipo)
7. Muestra mensaje de éxito y redirige a detalle

---

### 2.2 Flujo de Visualización de Proyecto

```mermaid
flowchart TD
    Start([Usuario hace click en proyecto]) --> CheckAuth{¿Usuario autenticado?}

    CheckAuth -->|No| RedirectLogin[Redirigir a login]
    RedirectLogin --> End1([Fin])

    CheckAuth -->|Sí| GetProject{¿Proyecto existe?}

    GetProject -->|No| Show404[Mostrar error 404]
    Show404 --> End2([Fin])

    GetProject -->|Sí| CheckPermission{¿Usuario tiene permiso?<br/>- Es Product Owner<br/>- Es Scrum Master<br/>- Es miembro del equipo}

    CheckPermission -->|No| ShowError[Mostrar error: sin permisos]
    ShowError --> RedirectList[Redirigir a lista de proyectos]
    RedirectList --> End3([Fin])

    CheckPermission -->|Sí| LoadData[Cargar datos del proyecto:<br/>- Info básica<br/>- Sprints recientes<br/>- Historias recientes]

    LoadData --> CalculateStats[Calcular estadísticas:<br/>- Total sprints<br/>- Total historias<br/>- Miembros del equipo]

    CalculateStats --> RenderTemplate[Renderizar template con datos]
    RenderTemplate --> ShowDetails[Mostrar:<br/>- Información del proyecto<br/>- Sprints<br/>- Historias<br/>- Acciones disponibles]
    ShowDetails --> End4([Fin])
```

**Descripción:**
1. Usuario hace click en un proyecto
2. Sistema verifica autenticación
3. Busca el proyecto en base de datos
4. Verifica permisos del usuario (PO, SM o miembro)
5. Si tiene permiso, carga datos relacionados
6. Calcula estadísticas
7. Renderiza y muestra toda la información

---

### 2.3 Flujo de Actualización de Proyecto

```mermaid
flowchart TD
    Start([Usuario hace click en 'Editar Proyecto']) --> CheckAuth{¿Usuario autenticado?}

    CheckAuth -->|No| RedirectLogin[Redirigir a login]
    RedirectLogin --> End1([Fin])

    CheckAuth -->|Sí| GetProject{¿Proyecto existe?}

    GetProject -->|No| Show404[Mostrar error 404]
    Show404 --> End2([Fin])

    GetProject -->|Sí| CheckEditPermission{¿Usuario es PO o SM?}

    CheckEditPermission -->|No| ShowError[Error: solo PO o SM pueden editar]
    ShowError --> RedirectDetail[Redirigir a detalle]
    RedirectDetail --> End3([Fin])

    CheckEditPermission -->|Sí| IsPost{¿Es POST?}

    IsPost -->|No| LoadForm[Cargar formulario con datos actuales]
    LoadForm --> ShowForm[Mostrar formulario prellenado]
    ShowForm --> End4([Fin])

    IsPost -->|Sí| ValidateForm{¿Formulario válido?}

    ValidateForm -->|No| ShowErrors[Mostrar errores]
    ShowErrors --> ShowForm

    ValidateForm -->|Sí| UpdateProject[Actualizar proyecto en BD]
    UpdateProject --> UpdateRelations[Actualizar relaciones M2M]
    UpdateRelations --> ShowSuccess[Mensaje: Proyecto actualizado]
    ShowSuccess --> RedirectDetail2[Redirigir a detalle]
    RedirectDetail2 --> End5([Fin])
```

**Descripción:**
1. Usuario hace click en editar
2. Sistema verifica autenticación y permisos (solo PO o SM)
3. Si es GET, muestra formulario prellenado con datos actuales
4. Si es POST, valida cambios
5. Actualiza proyecto y relaciones
6. Muestra confirmación y redirige

---

## 3. Gestión de Sprints

### 3.1 Flujo de Creación de Sprint

```mermaid
flowchart TD
    Start([Usuario hace click en 'Crear Sprint']) --> CheckAuth{¿Usuario autenticado?}

    CheckAuth -->|No| RedirectLogin[Redirigir a login]
    RedirectLogin --> End1([Fin])

    CheckAuth -->|Sí| GetProject{¿Proyecto existe?}

    GetProject -->|No| Show404[Error 404]
    Show404 --> End2([Fin])

    GetProject -->|Sí| IsPost{¿Es POST?}

    IsPost -->|No| InitForm[Inicializar formulario]
    InitForm --> SuggestNumber[Sugerir número de sprint:<br/>último número + 1]
    SuggestNumber --> ShowForm[Mostrar formulario]
    ShowForm --> End3([Fin])

    IsPost -->|Sí| ValidateForm{¿Formulario válido?}

    ValidateForm -->|No| ShowErrors[Mostrar errores]
    ShowErrors --> ShowForm

    ValidateForm -->|Sí| ValidateDates{¿Fecha fin > fecha inicio?}

    ValidateDates -->|No| ShowDateError[Error: fechas inválidas]
    ShowDateError --> ShowForm

    ValidateDates -->|Sí| CheckUnique{¿Número de sprint único<br/>en el proyecto?}

    CheckUnique -->|No| ShowUniqueError[Error: número ya existe]
    ShowUniqueError --> ShowForm

    CheckUnique -->|Sí| CheckActive{¿Ya existe sprint activo?}

    CheckActive -->|Sí y nuevo es ACTIVE| ShowActiveError[Error: ya hay sprint activo]
    ShowActiveError --> ShowForm

    CheckActive -->|No| SaveSprint[Guardar sprint en BD]
    SaveSprint --> ShowSuccess[Mensaje: Sprint creado]
    ShowSuccess --> RedirectDetail[Redirigir a detalle del sprint]
    RedirectDetail --> End4([Fin])
```

**Descripción:**
1. Usuario accede a formulario de creación desde un proyecto
2. Sistema sugiere automáticamente el siguiente número de sprint
3. Usuario completa información (nombre, objetivo, fechas)
4. Sistema valida:
   - Fechas coherentes
   - Número único en el proyecto
   - Solo un sprint activo a la vez
5. Guarda y redirige a detalle del sprint

---

### 3.2 Flujo de Finalización de Sprint

```mermaid
flowchart TD
    Start([Usuario finaliza sprint]) --> GetSprint[Obtener datos del sprint]

    GetSprint --> GetStories[Obtener historias del sprint]
    GetStories --> FilterDone[Filtrar historias DONE]
    FilterDone --> SumPoints[Sumar story_points de historias completadas]

    SumPoints --> UpdateVelocity[Actualizar campo velocity del sprint]
    UpdateVelocity --> UpdateStatus[Cambiar status a COMPLETED]
    UpdateStatus --> MoveIncomplete[Mover historias incompletas<br/>de vuelta al backlog]

    MoveIncomplete --> GenerateReport[Generar reporte:<br/>- Puntos completados<br/>- Historias completadas<br/>- Eficiencia]

    GenerateReport --> SaveChanges[Guardar cambios en BD]
    SaveChanges --> ShowSuccess[Mostrar mensaje con estadísticas]
    ShowSuccess --> End([Fin])
```

**Descripción:**
1. Usuario marca sprint como completado
2. Sistema calcula velocidad (suma de puntos de historias DONE)
3. Actualiza estado del sprint
4. Mueve historias incompletas al backlog
5. Genera reporte de métricas
6. Guarda cambios y muestra resumen

---

## 4. Gestión de Historias de Usuario

### 4.1 Flujo de Creación de Historia de Usuario

```mermaid
flowchart TD
    Start([Usuario hace click en 'Nueva Historia']) --> CheckAuth{¿Usuario autenticado?}

    CheckAuth -->|No| RedirectLogin[Redirigir a login]
    RedirectLogin --> End1([Fin])

    CheckAuth -->|Sí| GetProject{¿Proyecto existe?}

    GetProject -->|No| Show404[Error 404]
    Show404 --> End2([Fin])

    GetProject -->|Sí| IsPost{¿Es POST?}

    IsPost -->|No| InitForm[Inicializar formulario]
    InitForm --> FilterSprints[Filtrar sprints del proyecto]
    FilterSprints --> FilterTeam[Filtrar miembros del equipo]
    FilterTeam --> ShowForm[Mostrar formulario]
    ShowForm --> End3([Fin])

    IsPost -->|Sí| ValidateForm{¿Formulario válido?}

    ValidateForm -->|No| ShowErrors[Mostrar errores]
    ShowErrors --> ShowForm

    ValidateForm -->|Sí| ValidatePoints{¿Story points entre 1-100?}

    ValidatePoints -->|No| ShowPointsError[Error: puntos fuera de rango]
    ShowPointsError --> ShowForm

    ValidatePoints -->|Sí| ValidateAssigned{¿Usuario asignado es<br/>miembro del equipo?}

    ValidateAssigned -->|No| ShowTeamError[Error: usuario no es del equipo]
    ShowTeamError --> ShowForm

    ValidateAssigned -->|Sí| CreateStory[Crear historia de usuario]
    CreateStory --> SetCreator[Establecer created_by = usuario actual]
    SetCreator --> SetDefaultStatus[Status por defecto: BACKLOG]
    SetDefaultStatus --> SaveStory[Guardar en BD]

    SaveStory --> ShowSuccess[Mensaje: Historia creada]
    ShowSuccess --> RedirectDetail[Redirigir a detalle de la historia]
    RedirectDetail --> End4([Fin])
```

**Descripción:**
1. Usuario accede a formulario desde un proyecto
2. Formulario filtra automáticamente sprints y equipo del proyecto
3. Usuario completa información de la historia
4. Sistema valida:
   - Story points en rango válido (1-100)
   - Usuario asignado pertenece al equipo
   - Formato de criterios de aceptación
5. Crea historia con estado BACKLOG por defecto
6. Establece usuario actual como creador
7. Guarda y redirige a detalle

---

### 4.2 Flujo de Cambio de Estado de Historia

```mermaid
flowchart TD
    Start([Usuario cambia estado de historia]) --> GetStory[Obtener historia actual]

    GetStory --> CheckTransition{¿Transición válida?<br/>BACKLOG → TODO<br/>TODO → IN_PROGRESS<br/>IN_PROGRESS → IN_REVIEW<br/>IN_REVIEW → DONE<br/>Cualquier → BLOCKED}

    CheckTransition -->|No| ShowError[Error: transición no permitida]
    ShowError --> End1([Fin])

    CheckTransition -->|Sí| NewStatus{¿Nuevo estado?}

    NewStatus -->|IN_PROGRESS| CheckAssigned{¿Tiene usuario asignado?}
    CheckAssigned -->|No| ShowAssignError[Error: debe asignarse a alguien]
    ShowAssignError --> End2([Fin])
    CheckAssigned -->|Sí| UpdateStatus

    NewStatus -->|DONE| CheckTasks{¿Todas las tareas DONE?}
    CheckTasks -->|No| ShowTaskError[Error: tareas pendientes]
    ShowTaskError --> End3([Fin])
    CheckTasks -->|Sí| UpdateStatus

    NewStatus -->|Otros| UpdateStatus[Actualizar status en BD]

    UpdateStatus --> LogChange[Registrar cambio en historial]
    LogChange --> NotifyTeam[Notificar a equipo<br/>mensaje flash]
    NotifyTeam --> ShowSuccess[Mensaje: Estado actualizado]
    ShowSuccess --> Refresh[Actualizar vista]
    Refresh --> End4([Fin])
```

**Descripción:**
1. Usuario selecciona nuevo estado para historia
2. Sistema valida transición de estado según flujo Scrum
3. Realiza validaciones específicas:
   - IN_PROGRESS: debe tener asignado
   - DONE: todas las tareas deben estar completadas
4. Actualiza estado en base de datos
5. Registra cambio (auditoría)
6. Notifica con mensaje flash
7. Actualiza interfaz

---

### 4.3 Flujo de Asignación a Sprint

```mermaid
flowchart TD
    Start([Usuario asigna historia a sprint]) --> GetStory[Obtener historia]

    GetStory --> CheckStatus{¿Estado actual?}

    CheckStatus -->|DONE| ShowError[Error: historia ya completada]
    ShowError --> End1([Fin])

    CheckStatus -->|BLOCKED| ShowBlockedError[Error: historia bloqueada]
    ShowBlockedError --> End2([Fin])

    CheckStatus -->|Otros| GetSprint[Obtener sprint destino]

    GetSprint --> ValidateSprint{¿Sprint es del mismo proyecto?}

    ValidateSprint -->|No| ShowProjectError[Error: sprint de otro proyecto]
    ShowProjectError --> End3([Fin])

    ValidateSprint -->|Sí| CheckSprintStatus{¿Sprint está ACTIVE?}

    CheckSprintStatus -->|No| ShowSprintError[Error: sprint no activo]
    ShowSprintError --> End4([Fin])

    CheckSprintStatus -->|Sí| CalculateCapacity[Calcular capacidad del sprint:<br/>puntos actuales + nuevos ≤ velocidad estimada]

    CalculateCapacity --> CheckOverload{¿Sobrecarga?}

    CheckOverload -->|Sí| ShowWarning[Advertencia: sprint sobrecargado]
    ShowWarning --> ConfirmOverload{¿Confirmar de todas formas?}

    ConfirmOverload -->|No| End5([Fin])

    ConfirmOverload -->|Sí| AssignToSprint
    CheckOverload -->|No| AssignToSprint[Asignar historia al sprint]

    AssignToSprint --> UpdateStatus[Cambiar status a TODO si estaba en BACKLOG]
    UpdateStatus --> SaveChanges[Guardar cambios]
    SaveChanges --> ShowSuccess[Mensaje: Historia asignada a sprint]
    ShowSuccess --> Refresh[Actualizar vista]
    Refresh --> End6([Fin])
```

**Descripción:**
1. Usuario arrastra/selecciona historia para asignar a sprint
2. Sistema valida:
   - Historia no está completada
   - Sprint pertenece al mismo proyecto
   - Sprint está activo
3. Calcula si agregar la historia sobrecarga el sprint
4. Si hay sobrecarga, muestra advertencia y pide confirmación
5. Asigna historia y actualiza estado si es necesario
6. Guarda y actualiza interfaz

---

## 5. Gestión de Tareas

### 5.1 Flujo de Creación de Tarea

```mermaid
flowchart TD
    Start([Usuario hace click en 'Crear Tarea']) --> CheckAuth{¿Usuario autenticado?}

    CheckAuth -->|No| RedirectLogin[Redirigir a login]
    RedirectLogin --> End1([Fin])

    CheckAuth -->|Sí| GetStory{¿Historia existe?}

    GetStory -->|No| Show404[Error 404]
    Show404 --> End2([Fin])

    GetStory -->|Sí| CheckStoryStatus{¿Historia está DONE?}

    CheckStoryStatus -->|Sí| ShowError[Error: no se pueden agregar tareas<br/>a historias completadas]
    ShowError --> End3([Fin])

    CheckStoryStatus -->|No| IsPost{¿Es POST?}

    IsPost -->|No| InitForm[Inicializar formulario]
    InitForm --> FilterTeam[Filtrar miembros del equipo del proyecto]
    FilterTeam --> ShowForm[Mostrar formulario]
    ShowForm --> End4([Fin])

    IsPost -->|Sí| ValidateForm{¿Formulario válido?}

    ValidateForm -->|No| ShowErrors[Mostrar errores]
    ShowErrors --> ShowForm

    ValidateForm -->|Sí| ValidateHours{¿Horas estimadas > 0?}

    ValidateHours -->|No| ShowHoursError[Error: horas deben ser positivas]
    ShowHoursError --> ShowForm

    ValidateHours -->|Sí| CreateTask[Crear tarea]
    CreateTask --> SetUserStory[Asociar con historia de usuario]
    SetUserStory --> SetDefaultStatus[Status por defecto: TODO]
    SetDefaultStatus --> SaveTask[Guardar en BD]

    SaveTask --> ShowSuccess[Mensaje: Tarea creada]
    ShowSuccess --> RedirectStory[Redirigir a detalle de historia]
    RedirectStory --> End5([Fin])
```

**Descripción:**
1. Usuario crea tarea desde detalle de historia
2. Sistema verifica que historia no esté completada
3. Filtra automáticamente miembros del equipo para asignación
4. Valida horas estimadas sean positivas
5. Crea tarea con estado TODO
6. Asocia a la historia y guarda
7. Redirige al detalle de la historia

---

### 5.2 Flujo de Actualización de Tarea

```mermaid
flowchart TD
    Start([Usuario actualiza tarea]) --> GetTask[Obtener tarea actual]

    GetTask --> IsPost{¿Es POST?}

    IsPost -->|No| ShowForm[Mostrar formulario con datos actuales]
    ShowForm --> End1([Fin])

    IsPost -->|Sí| ValidateForm{¿Formulario válido?}

    ValidateForm -->|No| ShowErrors[Mostrar errores]
    ShowErrors --> ShowForm

    ValidateForm -->|Sí| CheckStatusChange{¿Cambió status a DONE?}

    CheckStatusChange -->|Sí| CheckActualHours{¿Hay horas reales registradas?}

    CheckActualHours -->|No| ShowHoursWarning[Advertencia: registrar horas reales]
    ShowHoursWarning --> ConfirmWithoutHours{¿Continuar sin horas?}

    ConfirmWithoutHours -->|No| ShowForm

    ConfirmWithoutHours -->|Sí| UpdateTask
    CheckActualHours -->|Sí| CalculateVariance[Calcular varianza:<br/>actual - estimado]
    CalculateVariance --> UpdateTask

    CheckStatusChange -->|No| UpdateTask[Actualizar tarea en BD]

    UpdateTask --> CheckStoryProgress[Verificar progreso de la historia]
    CheckStoryProgress --> AllTasksDone{¿Todas las tareas DONE?}

    AllTasksDone -->|Sí| SuggestStoryDone[Sugerir marcar historia como DONE]
    SuggestStoryDone --> ShowSuccess

    AllTasksDone -->|No| ShowSuccess[Mensaje: Tarea actualizada]

    ShowSuccess --> RedirectStory[Redirigir a detalle de historia]
    RedirectStory --> End2([Fin])
```

**Descripción:**
1. Usuario edita una tarea existente
2. Si marca como DONE, sistema verifica horas reales
3. Si no hay horas reales, muestra advertencia
4. Calcula varianza entre estimado y real
5. Actualiza tarea en base de datos
6. Verifica si todas las tareas de la historia están DONE
7. Si todas están DONE, sugiere completar la historia
8. Muestra confirmación y redirige

---

## 6. Sistema de Comentarios

### 6.1 Flujo de Agregar Comentario

```mermaid
flowchart TD
    Start([Usuario escribe comentario]) --> CheckAuth{¿Usuario autenticado?}

    CheckAuth -->|No| RedirectLogin[Redirigir a login]
    RedirectLogin --> End1([Fin])

    CheckAuth -->|Sí| GetStory{¿Historia existe?}

    GetStory -->|No| Show404[Error 404]
    Show404 --> End2([Fin])

    GetStory -->|Sí| CheckAccess{¿Usuario tiene acceso<br/>a la historia?}

    CheckAccess -->|No| ShowError[Error: sin acceso]
    ShowError --> End3([Fin])

    CheckAccess -->|Sí| ValidateForm{¿Comentario no vacío?}

    ValidateForm -->|No| ShowEmptyError[Error: comentario vacío]
    ShowEmptyError --> End4([Fin])

    ValidateForm -->|Sí| SanitizeContent[Sanitizar contenido:<br/>prevenir XSS]

    SanitizeContent --> CreateComment[Crear comentario]
    CreateComment --> SetAuthor[Establecer autor = usuario actual]
    SetAuthor --> SetTimestamp[Establecer timestamp actual]
    SetTimestamp --> SaveComment[Guardar en BD]

    SaveComment --> NotifyTeam[Notificar a miembros<br/>del equipo opcional]
    NotifyTeam --> ShowSuccess[Mensaje: Comentario agregado]
    ShowSuccess --> RefreshComments[Actualizar sección de comentarios]
    RefreshComments --> End5([Fin])
```

**Descripción:**
1. Usuario escribe comentario en historia de usuario
2. Sistema verifica autenticación y acceso
3. Valida que comentario no esté vacío
4. Sanitiza contenido para prevenir XSS
5. Crea comentario con autor y timestamp
6. Opcionalmente notifica al equipo
7. Actualiza sección de comentarios en tiempo real

---

## 7. Flujos Administrativos

### 7.1 Flujo de Acceso al Admin

```mermaid
flowchart TD
    Start([Usuario accede a /admin/]) --> CheckAuth{¿Usuario autenticado?}

    CheckAuth -->|No| RedirectLogin[Redirigir a página de login del admin]
    RedirectLogin --> End1([Fin])

    CheckAuth -->|Sí| CheckStaff{¿Usuario tiene is_staff=True?}

    CheckStaff -->|No| Show403[Error 403: Acceso denegado]
    Show403 --> End2([Fin])

    CheckStaff -->|Sí| LoadAdminIndex[Cargar índice del admin]
    LoadAdminIndex --> ListModels[Listar modelos disponibles:<br/>- Projects<br/>- Sprints<br/>- User Stories<br/>- Tasks<br/>- Comments]

    ListModels --> CheckPermissions[Verificar permisos por modelo:<br/>- view<br/>- add<br/>- change<br/>- delete]

    CheckPermissions --> ShowDashboard[Mostrar dashboard del admin<br/>con modelos permitidos]
    ShowDashboard --> End3([Fin])
```

**Descripción:**
1. Usuario intenta acceder al admin
2. Sistema verifica autenticación
3. Verifica flag is_staff
4. Carga índice de administración
5. Lista modelos según permisos del usuario
6. Muestra dashboard con opciones disponibles

---

### 7.2 Flujo de Búsqueda en Admin

```mermaid
flowchart TD
    Start([Usuario realiza búsqueda en admin]) --> GetQuery[Obtener término de búsqueda]

    GetQuery --> GetModel[Identificar modelo actual]
    GetModel --> GetSearchFields[Obtener search_fields configurados]

    GetSearchFields --> BuildQuery[Construir query con Q objects:<br/>Q(field1__icontains=query) |<br/>Q(field2__icontains=query)]

    BuildQuery --> ExecuteQuery[Ejecutar query en BD]
    ExecuteQuery --> ApplyFilters{¿Hay filtros adicionales?}

    ApplyFilters -->|Sí| CombineFilters[Combinar búsqueda con filtros]
    CombineFilters --> SortResults

    ApplyFilters -->|No| SortResults[Ordenar resultados según ordering]

    SortResults --> Paginate[Paginar resultados]
    Paginate --> HighlightResults[Destacar términos de búsqueda]
    HighlightResults --> ShowResults[Mostrar resultados en tabla]
    ShowResults --> End([Fin])
```

**Descripción:**
1. Usuario ingresa término en campo de búsqueda
2. Sistema obtiene configuración de search_fields
3. Construye query OR con todos los campos
4. Ejecuta búsqueda case-insensitive
5. Combina con filtros si existen
6. Ordena y pagina resultados
7. Destaca términos encontrados
8. Muestra resultados

---

### 7.3 Flujo de Edición Masiva en Admin

```mermaid
flowchart TD
    Start([Usuario selecciona múltiples items]) --> SelectAction[Usuario elige acción:<br/>- Eliminar<br/>- Cambiar estado<br/>- Exportar]

    SelectAction --> ConfirmAction{¿Requiere confirmación?}

    ConfirmAction -->|Sí Eliminar| ShowConfirmation[Mostrar página de confirmación<br/>con lista de items]
    ShowConfirmation --> UserConfirms{¿Usuario confirma?}

    UserConfirms -->|No| Cancel[Cancelar acción]
    Cancel --> End1([Fin])

    UserConfirms -->|Sí| CheckConstraints{¿Hay constraints FK?}

    CheckConstraints -->|Sí y PROTECT| ShowConstraintError[Error: no se puede eliminar<br/>items referenciados]
    ShowConstraintError --> End2([Fin])

    CheckConstraints -->|No o CASCADE| ExecuteAction[Ejecutar acción en todos los items]

    ConfirmAction -->|No Otras acciones| ExecuteAction

    ExecuteAction --> UpdateDB[Actualizar registros en BD]
    UpdateDB --> CountAffected[Contar registros afectados]
    CountAffected --> ShowSuccess[Mensaje: X items actualizados/eliminados]
    ShowSuccess --> RefreshList[Actualizar lista de admin]
    RefreshList --> End3([Fin])
```

**Descripción:**
1. Usuario selecciona múltiples items con checkboxes
2. Selecciona acción del dropdown
3. Si es eliminación, muestra confirmación
4. Verifica constraints de FK
5. Ejecuta acción en batch
6. Cuenta items afectados
7. Muestra confirmación y actualiza lista

---

## 8. Flujos de Datos Adicionales

### 8.1 Flujo de Cálculo de Métricas

```mermaid
flowchart TD
    Start([Solicitud de métricas]) --> IdentifyScope[Identificar alcance:<br/>- Proyecto<br/>- Sprint<br/>- Usuario]

    IdentifyScope --> LoadData[Cargar datos relevantes de BD]
    LoadData --> CalculateVelocity[Calcular velocidad:<br/>SUM story_points WHERE status=DONE]

    CalculateVelocity --> CalculateProgress[Calcular progreso:<br/>historias_done / total_historias]
    CalculateProgress --> CalculateBurndown[Calcular burndown:<br/>puntos_restantes por día]

    CalculateBurndown --> CalculateEfficiency[Calcular eficiencia:<br/>actual_hours / estimated_hours]
    CalculateEfficiency --> AggregateMetrics[Agregar métricas]

    AggregateMetrics --> CacheResults[Cachear resultados<br/>15 minutos]
    CacheResults --> FormatOutput[Formatear para presentación]
    FormatOutput --> ReturnMetrics[Retornar métricas]
    ReturnMetrics --> End([Fin])
```

**Descripción:**
1. Sistema solicita cálculo de métricas (dashboard, reportes)
2. Identifica alcance (proyecto, sprint, usuario)
3. Carga datos necesarios
4. Calcula diferentes métricas:
   - Velocidad del sprint
   - Progreso del proyecto
   - Burndown
   - Eficiencia del equipo
5. Cachea resultados para performance
6. Formatea y retorna

---

### 8.2 Flujo de Generación de Reportes

```mermaid
flowchart TD
    Start([Usuario solicita reporte]) --> SelectType[Seleccionar tipo:<br/>- Sprint<br/>- Proyecto<br/>- Usuario<br/>- Período]

    SelectType --> SelectFormat[Seleccionar formato:<br/>- PDF<br/>- Excel<br/>- HTML]

    SelectFormat --> SelectDate[Seleccionar rango de fechas]
    SelectDate --> ValidateDates{¿Fechas válidas?}

    ValidateDates -->|No| ShowDateError[Error: rango inválido]
    ShowDateError --> SelectDate

    ValidateDates -->|Sí| QueryData[Consultar datos de BD:<br/>- Proyectos<br/>- Sprints<br/>- Historias<br/>- Tareas]

    QueryData --> CalculateStats[Calcular estadísticas:<br/>- Velocidad promedio<br/>- Historias completadas<br/>- Distribución por prioridad<br/>- Eficiencia]

    CalculateStats --> GenerateCharts[Generar gráficos:<br/>- Burndown<br/>- Velocity chart<br/>- Pie charts]

    GenerateCharts --> ApplyTemplate[Aplicar template de reporte]
    ApplyTemplate --> RenderFormat{¿Formato?}

    RenderFormat -->|PDF| GeneratePDF[Generar PDF con reportlab]
    GeneratePDF --> DownloadFile

    RenderFormat -->|Excel| GenerateExcel[Generar Excel con openpyxl]
    GenerateExcel --> DownloadFile

    RenderFormat -->|HTML| RenderHTML[Renderizar HTML]
    RenderHTML --> ShowInBrowser

    DownloadFile[Preparar descarga]
    DownloadFile --> SetHeaders[Establecer headers HTTP]
    SetHeaders --> SendFile[Enviar archivo]
    SendFile --> End1([Fin])

    ShowInBrowser[Mostrar en navegador]
    ShowInBrowser --> End2([Fin])
```

**Descripción:**
1. Usuario solicita generación de reporte
2. Selecciona tipo, formato y rango de fechas
3. Sistema valida parámetros
4. Consulta datos necesarios de base de datos
5. Calcula estadísticas agregadas
6. Genera gráficos visuales
7. Aplica template según formato seleccionado
8. Genera archivo (PDF/Excel) o renderiza HTML
9. Descarga o muestra en navegador

---

## Convenciones de Diagramas

### Símbolos Utilizados

- **Rectángulo redondeado** `([texto])`: Inicio/Fin
- **Rectángulo** `[texto]`: Proceso/Acción
- **Rombo** `{¿pregunta?}`: Decisión
- **Flechas** `-->`: Flujo de ejecución
- **Etiquetas** `|Sí|` o `|No|`: Resultado de decisión

### Colores (según implementación)

- **Verde**: Flujo exitoso
- **Rojo**: Errores/Excepciones
- **Azul**: Procesos normales
- **Amarillo**: Advertencias

---

## Conclusión

Estos diagramas de flujo documentan los procesos principales del sistema Liscov Project Management, proporcionando una guía visual clara para:

✅ **Desarrollo**: Entender la lógica de negocio
✅ **Testing**: Identificar casos de prueba
✅ **Documentación**: Material educativo
✅ **Mantenimiento**: Referencia rápida
✅ **Onboarding**: Capacitación de nuevos desarrolladores

Cada flujo incluye validaciones, manejo de errores y consideraciones de seguridad, reflejando las mejores prácticas en desarrollo web con Django.
