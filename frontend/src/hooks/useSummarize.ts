import { useCallback, useState } from 'react'
import { AxiosError } from 'axios'
import { summarizeText } from '../lib/api'
import type { SummarizeRequest, SummarizeResponse } from '../types/api'

const parseError = (error: unknown) => {
  if (error instanceof AxiosError) {
    return (
      (error.response?.data as { detail?: string })?.detail ||
      error.message ||
      'Unable to generate summary'
    )
  }
  return 'Unable to generate summary'
}

export const useSummarize = () => {
  const [data, setData] = useState<SummarizeResponse | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [cache, setCache] = useState<Map<string, SummarizeResponse>>(new Map())

  const summarize = useCallback(
    async (payload: SummarizeRequest, options?: { force?: boolean }) => {
      const cacheKey = `${payload.text.substring(0, 100)}-${payload.format}`

      // Use cache only when force flag isn't active
      if (!options?.force) {
        const cached = cache.get(cacheKey)
        if (cached) {
          setData(cached)
          return cached
        }
      }

      setIsLoading(true)
      setError(null)
      try {
        const response = await summarizeText(payload)
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
    },
    [cache]
  )

  const reset = () => {
    setData(null)
    setError(null)
  }

  return { data, isLoading, error, summarize, reset }
}

export default useSummarize
