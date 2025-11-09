import { useCallback, useState } from 'react'
import { AxiosError } from 'axios'
import { transcribeAudio } from '../lib/api'
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
  const [isUploadingFile, setIsUploadingFile] = useState(false)

  const transcribe = useCallback(async (file: File) => {
    setIsLoading(true)
    setIsUploadingFile(true)
    setError(null)
    setUploadProgress(0)

    try {
      const response = await transcribeAudio(file, (evt) => {
        if (!evt.total) return
        const percent = Math.round((evt.loaded / evt.total) * 100)
        setUploadProgress(percent)
        if (percent >= 100) {
          setIsUploadingFile(false)
        }
      })

      setData(response)
      return response
    } catch (err) {
      const message = parseError(err)
      setError(message)
      throw err
    } finally {
      setIsLoading(false)
      setIsUploadingFile(false)
    }
  }, [])

  const reset = () => {
    setData(null)
    setError(null)
    setUploadProgress(0)
    setIsUploadingFile(false)
  }

  return {
    data,
    isLoading,
    isUploadingFile,
    isProcessing: isLoading && !isUploadingFile,
    error,
    uploadProgress,
    transcribe,
    reset,
  }
}

export default useTranscribe
