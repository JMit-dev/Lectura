import axios, { AxiosProgressEvent } from 'axios'
import type {
  FlashcardRequest,
  FlashcardResponse,
  SummarizeRequest,
  SummarizeResponse,
  TranscribeResponse,
  TranslateRequest,
  TranslateResponse,
} from '../types/api'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const transcribeAudio = async (
  file: File,
  onUploadProgress?: (progressEvent: AxiosProgressEvent) => void,
): Promise<TranscribeResponse> => {
  const formData = new FormData()
  formData.append('file', file)

  const response = await api.post<TranscribeResponse>('/api/transcribe', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress,
  })

  return response.data
}

export const summarizeText = async (payload: SummarizeRequest): Promise<SummarizeResponse> => {
  const response = await api.post<SummarizeResponse>('/api/summarize', payload)
  return response.data
}

export const generateFlashcards = async (
  payload: FlashcardRequest,
): Promise<FlashcardResponse> => {
  const response = await api.post<FlashcardResponse>('/api/flashcards', payload)
  return response.data
}

export const translateText = async (payload: TranslateRequest): Promise<TranslateResponse> => {
  const response = await api.post<TranslateResponse>('/api/translate', payload)
  return response.data
}

export const healthCheck = async () => {
  const response = await api.get('/api/health')
  return response.data
}
