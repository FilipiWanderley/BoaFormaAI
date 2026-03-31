// ── Auth ────────────────────────────────────────────────────────────────────

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

export type AuthStatus =
  | 'nao_autenticado'
  | 'autenticando'
  | 'autenticado'
  | 'sessao_expirada'
  | 'erro_autenticacao'

// ── User ────────────────────────────────────────────────────────────────────

export type Level = 'iniciante' | 'intermediario' | 'avancado'

export interface UserResponse {
  id: number
  name: string
  email: string
  age: number
  weight_kg: number
  height_cm: number
  goal: string
  level: Level
  restrictions: string | null
  provider: 'email' | 'google'
  provider_id: string | null
  is_admin: boolean
  consent_given_at: string | null
  privacy_policy_version: string | null
}

export interface UserCreate {
  name: string
  email: string
  password: string
  age: number
  weight_kg: number
  height_cm: number
  goal: string
  level: Level
  restrictions?: string
  accept_terms: true
  privacy_policy_version?: string
}

export interface UserUpdate {
  weight_kg?: number
  height_cm?: number
  goal?: string
  restrictions?: string
}

// ── Exercise ────────────────────────────────────────────────────────────────

export interface ExerciseResponse {
  id: number
  name: string
  muscle_group: string
  secondary_muscles: string | null
  equipment: string
  level: Level
  instructions: string | null
  image_url: string | null
  contraindications: string | null
}

// ── Workout ─────────────────────────────────────────────────────────────────

export type FeedbackValue = 'facil' | 'ok' | 'dificil'

export interface WorkoutExerciseDetail {
  exercise_id: number
  exercise_name: string
  muscle_group: string
  equipment: string
  sets: number
  reps: string
  rest_seconds: number
  notes: string | null
  order: number
  image_url: string | null
}

export interface WorkoutResponse {
  id: number
  workout_name: string
  focus: string
  estimated_duration_minutes: number
  exercises: WorkoutExerciseDetail[]
  general_tips: string
  created_at: string
  feedback: FeedbackValue | null
}

export interface WorkoutSummary {
  id: number
  workout_name: string
  focus: string
  estimated_duration_minutes: number
  created_at: string
  feedback: FeedbackValue | null
}

export interface WorkoutGenerateRequest {
  muscle_groups?: string[]
  equipment_available?: string[]
  duration_minutes?: number
  feedback_on_last?: FeedbackValue
}

// ── History ─────────────────────────────────────────────────────────────────

export interface HistoryResponse {
  id: number
  workout_id: number
  workout_name: string
  completed_at: string
  notes: string | null
}

export interface HistoryCreate {
  workout_id: number
  notes?: string
}

// ── Dashboard ───────────────────────────────────────────────────────────────

export interface DashboardStats {
  total_workouts_generated: number
  total_workouts_completed: number
  current_streak_days: number
  last_completed_at: string | null
}

export interface DashboardResponse {
  user: UserResponse
  today_workout: WorkoutSummary | null
  last_workout: WorkoutSummary | null
  stats: DashboardStats
}

// ── Chat ────────────────────────────────────────────────────────────────────

export interface ChatMessageResponse {
  id: number
  role: 'user' | 'assistant'
  content: string
  created_at: string
}

export interface ChatResponse {
  reply: ChatMessageResponse
  history: ChatMessageResponse[]
}
