export interface TranscribeResponse {
  transcript: string
  duration: number
  language: string
  tokens_used: number
}

export interface SummarizeRequest {
  text: string
  format?: string
}

export interface SummarizeResponse {
  summary: string
  original_length: number
  summary_length: number
}

export interface Flashcard {
  question: string
  answer: string
  difficulty: string
}

export interface FlashcardRequest {
  text: string
  count?: number | null
  difficulty?: 'easy' | 'medium' | 'hard'
}

export interface FlashcardResponse {
  flashcards: Flashcard[]
  tokens_saved?: number
}

export interface TranslateRequest {
  text: string
  target_languages: string[]
}

export interface TranslateResponse {
  translations: Record<string, string>
}
