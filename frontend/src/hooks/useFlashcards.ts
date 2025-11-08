import { useCallback, useState } from 'react'
import { AxiosError } from 'axios'
import { api } from '../lib/api'
import type { FlashcardRequest, FlashcardResponse } from '../types/api'

const parseError = (error: unknown) => {
  if (error instanceof AxiosError) {
    return (
      (error.response?.data as { detail?: string })?.detail ||
      error.message ||
      'Unable to generate flashcards'
    )
  }
  return 'Unable to generate flashcards'
}

export const useFlashcards = () => {
  const [data, setData] = useState<FlashcardResponse | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const generateFlashcards = useCallback(async (payload: FlashcardRequest) => {
    setIsLoading(true)
    setError(null)
    try {
      const response = await api.post<FlashcardResponse>('/api/flashcards', payload)
      setData(response.data)
      return response.data
    } catch (err) {
      const message = parseError(err)
      setError(message)
      throw err
    } finally {
      setIsLoading(false)
    }
  }, [])

  const reset = () => {
    setData(null)
    setError(null)
  }

  return { data, isLoading, error, generateFlashcards, reset }
}

export default useFlashcards
