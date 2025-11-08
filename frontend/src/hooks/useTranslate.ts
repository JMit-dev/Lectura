import { useCallback, useState } from 'react'
import { AxiosError } from 'axios'
import { translateText } from '../lib/api'
import type { TranslateRequest, TranslateResponse } from '../types/api'

const parseError = (error: unknown) => {
  if (error instanceof AxiosError) {
    return (
      (error.response?.data as { detail?: string })?.detail ||
      error.message ||
      'Unable to translate text'
    )
  }
  return 'Unable to translate text'
}

export const useTranslate = () => {
  const [data, setData] = useState<TranslateResponse | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [cache, setCache] = useState<Map<string, TranslateResponse>>(new Map())

  const translate = useCallback(
    async (payload: TranslateRequest) => {
      // Create cache key from text + languages
      const cacheKey = `${payload.text.substring(0, 100)}-${payload.target_languages.sort().join(',')}`

      // Check cache first
      const cached = cache.get(cacheKey)
      if (cached) {
        setData(cached)
        return cached
      }

      setIsLoading(true)
      setError(null)
      try {
        const response = await translateText(payload)
        setData(response)

        // Cache the result
        setCache((prev) => new Map(prev).set(cacheKey, response))

        return response
      } catch (err) {
        const message = parseError(err)
        setError(message)
        throw err
      } finally {
        setIsLoading(false)
      }
    },
    [cache]
  )

  const reset = () => {
    setData(null)
    setError(null)
    setCache(new Map())
  }

  return { data, isLoading, error, translate, reset }
}

export default useTranslate
