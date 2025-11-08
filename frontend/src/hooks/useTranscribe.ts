import { useCallback, useState } from 'react'
import { AxiosError } from 'axios'
import { api } from '../lib/api'
import type { TranscribeResponse } from '../types/api'

const parseError = (error: unknown) => {
  if (error instanceof AxiosError) {
    return (
      (error.response?.data as { detail?: string })?.detail ||
      error.message ||
      'Unable to transcribe audio'
    )
  }
  return 'Unable to transcribe audio'
}

export const useTranscribe = () => {
  const [data, setData] = useState<TranscribeResponse | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [uploadProgress, setUploadProgress] = useState(0)

  const transcribe = useCallback(async (file: File) => {
    setIsLoading(true)
    setError(null)
    setUploadProgress(0)

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await api.post<TranscribeResponse>('/api/transcribe', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (evt) => {
          if (!evt.total) return
          setUploadProgress(Math.round((evt.loaded / evt.total) * 100))
        },
      })

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
    setUploadProgress(0)
  }

  return {
    data,
    isLoading,
    error,
    uploadProgress,
    transcribe,
    reset,
  }
}

export default useTranscribe
