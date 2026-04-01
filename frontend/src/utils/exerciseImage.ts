import type { ExerciseResponse } from '../types'

const KEYWORD_IMAGE_MAP: Array<{ pattern: RegExp; url: string }> = [
  { pattern: /supino|peito|flex[aã]o|crucifixo|crossover|peck deck/i, url: 'https://images.pexels.com/photos/3838389/pexels-photo-3838389.jpeg?auto=compress&cs=tinysrgb&w=600' },
  { pattern: /remada|puxada|barra fixa|pull|costas|deadlift|terra/i, url: 'https://images.pexels.com/photos/949129/pexels-photo-949129.jpeg?auto=compress&cs=tinysrgb&w=600' },
  { pattern: /agachamento|leg press|afundo|lunge|quadr[ií]ceps|panturrilha|stiff/i, url: 'https://images.pexels.com/photos/6456307/pexels-photo-6456307.jpeg?auto=compress&cs=tinysrgb&w=600' },
  { pattern: /ombro|eleva[cç][aã]o lateral|desenvolvimento|shoulder|arnold/i, url: 'https://images.pexels.com/photos/4162585/pexels-photo-4162585.jpeg?auto=compress&cs=tinysrgb&w=600' },
  { pattern: /b[ií]ceps|rosca|curl/i, url: 'https://images.pexels.com/photos/5327543/pexels-photo-5327543.jpeg?auto=compress&cs=tinysrgb&w=600' },
  { pattern: /tr[ií]ceps|paralela|mergulho|skull crusher/i, url: 'https://images.pexels.com/photos/6550854/pexels-photo-6550854.jpeg?auto=compress&cs=tinysrgb&w=600' },
  { pattern: /abd[oô]men|prancha|core|ab wheel/i, url: 'https://images.pexels.com/photos/6456141/pexels-photo-6456141.jpeg?auto=compress&cs=tinysrgb&w=600' },
  { pattern: /gl[uú]teo|hip thrust|ponte/i, url: 'https://images.pexels.com/photos/6551410/pexels-photo-6551410.jpeg?auto=compress&cs=tinysrgb&w=600' },
  { pattern: /cardio|corrida|esteira|bike|el[ií]ptico|remo/i, url: 'https://images.pexels.com/photos/1552242/pexels-photo-1552242.jpeg?auto=compress&cs=tinysrgb&w=600' },
]

const MUSCLE_GROUP_IMAGE_MAP: Record<string, string> = {
  peito: 'https://images.pexels.com/photos/3838389/pexels-photo-3838389.jpeg?auto=compress&cs=tinysrgb&w=600',
  costas: 'https://images.pexels.com/photos/949129/pexels-photo-949129.jpeg?auto=compress&cs=tinysrgb&w=600',
  quadriceps: 'https://images.pexels.com/photos/6456307/pexels-photo-6456307.jpeg?auto=compress&cs=tinysrgb&w=600',
  posterior: 'https://images.pexels.com/photos/6456307/pexels-photo-6456307.jpeg?auto=compress&cs=tinysrgb&w=600',
  gluteos: 'https://images.pexels.com/photos/6551410/pexels-photo-6551410.jpeg?auto=compress&cs=tinysrgb&w=600',
  ombros: 'https://images.pexels.com/photos/4162585/pexels-photo-4162585.jpeg?auto=compress&cs=tinysrgb&w=600',
  biceps: 'https://images.pexels.com/photos/5327543/pexels-photo-5327543.jpeg?auto=compress&cs=tinysrgb&w=600',
  triceps: 'https://images.pexels.com/photos/6550854/pexels-photo-6550854.jpeg?auto=compress&cs=tinysrgb&w=600',
  abdomen: 'https://images.pexels.com/photos/6456141/pexels-photo-6456141.jpeg?auto=compress&cs=tinysrgb&w=600',
  panturrilha: 'https://images.pexels.com/photos/6456307/pexels-photo-6456307.jpeg?auto=compress&cs=tinysrgb&w=600',
  cardio: 'https://images.pexels.com/photos/1552242/pexels-photo-1552242.jpeg?auto=compress&cs=tinysrgb&w=600',
}

const DEFAULT_IMAGE = 'https://images.pexels.com/photos/841130/pexels-photo-841130.jpeg?auto=compress&cs=tinysrgb&w=600'

export function getExerciseImageUrl(exercise: Pick<ExerciseResponse, 'name' | 'muscle_group' | 'image_url'>): string {
  if (exercise.image_url && exercise.image_url.trim()) return exercise.image_url
  const byKeyword = KEYWORD_IMAGE_MAP.find((item) => item.pattern.test(exercise.name))
  if (byKeyword) return byKeyword.url
  return MUSCLE_GROUP_IMAGE_MAP[exercise.muscle_group] ?? DEFAULT_IMAGE
}
