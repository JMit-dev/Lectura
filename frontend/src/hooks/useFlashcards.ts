import { useCallback, useState } from 'react'
import { AxiosError } from 'axios'
import { generateFlashcards as fetchFlashcards } from '../lib/api'
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
  const [cache, setCache] = useState<Map<string, FlashcardResponse>>(new Map())

  const generateFlashcards = useCallback(async (payload: FlashcardRequest) => {
    // Check cache first
    const cacheKey = `${payload.text.substring(0, 100)}-${payload.count}-${payload.difficulty}`
    const cached = cache.get(cacheKey)
    if (cached) {
      setData(cached)
      return cached
    }

    setIsLoading(true)
    setError(null)
    try {
      const response = await fetchFlashcards(payload)
      setData(response)
      // Cache the response
      setCache((prev) => new Map(prev).set(cacheKey, response))
      return response
    } catch (err) {
      const message = parseError(err)
      setError(message)
      throw err
    } finally {
      setIsLoading(false)
    }
  }, [cache])

  const reset = () => {
    setData(null)
    setError(null)
  }

  return { data, isLoading, error, generateFlashcards, reset }
}

export default useFlashcards
