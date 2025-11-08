import { useEffect, useRef, useState } from 'react'
import { UploadCloud, XCircle } from 'lucide-react'

interface AudioUploaderProps {
  onFileSelected: (file: File) => void
  isUploading?: boolean
  uploadProgress?: number
  error?: string | null
  acceptedTypes?: string[]
  maxFileSizeMb?: number
}

const defaultAcceptedTypes = [
  // Audio formats
  'audio/mpeg',
  'audio/wav',
  'audio/mp4',
  'audio/x-m4a',
  'audio/aac',
  'audio/ogg',
  'audio/flac',
  // Video formats
  'video/mp4',
  'video/webm',
  'video/x-msvideo',
  'video/quicktime',
  'video/x-matroska',
  // Text formats
  'text/plain',
  'application/pdf',
]
const defaultMaxSizeMb = 200

const readableFileSize = (bytes: number) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  const size = bytes / k ** i
  return `${size.toFixed(size >= 10 ? 0 : 1)} ${sizes[i]}`
}

export const AudioUploader = ({
  onFileSelected,
  isUploading = false,
  uploadProgress,
  error,
  acceptedTypes = defaultAcceptedTypes,
  maxFileSizeMb = defaultMaxSizeMb,
}: AudioUploaderProps) => {
  const inputRef = useRef<HTMLInputElement | null>(null)
  const [dragActive, setDragActive] = useState(false)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [localError, setLocalError] = useState<string | null>(null)

  useEffect(() => {
    if (!selectedFile) {
      setPreviewUrl(null)
      return
    }

    const url = URL.createObjectURL(selectedFile)
    setPreviewUrl(url)

    return () => {
      URL.revokeObjectURL(url)
    }
  }, [selectedFile])

  const resetState = () => {
    setSelectedFile(null)
    setPreviewUrl(null)
    setLocalError(null)
  }

  const validateFile = (file?: File) => {
    if (!file) {
      setLocalError('No file selected')
      return false
    }

    if (!acceptedTypes.includes(file.type)) {
      setLocalError('Unsupported file format')
      return false
    }

    const maxBytes = maxFileSizeMb * 1024 * 1024
    if (file.size > maxBytes) {
      setLocalError(`File is too large (max ${maxFileSizeMb}MB)`)
      return false
    }

    setLocalError(null)
    return true
  }

  const handleFile = (file?: File) => {
    if (!validateFile(file)) return
    if (!file) return
    setSelectedFile(file)
    onFileSelected(file)
  }

  const onInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    handleFile(file)
  }

  const onDragOver = (event: React.DragEvent<HTMLLabelElement>) => {
    event.preventDefault()
    event.stopPropagation()
    if (!dragActive) setDragActive(true)
  }

  const onDragLeave = (event: React.DragEvent<HTMLLabelElement>) => {
    event.preventDefault()
    event.stopPropagation()
    setDragActive(false)
  }

  const onDrop = (event: React.DragEvent<HTMLLabelElement>) => {
    event.preventDefault()
    event.stopPropagation()
    setDragActive(false)
    const file = event.dataTransfer.files?.[0]
    handleFile(file)
  }

  return (
    <div className="space-y-4">
      <label
        htmlFor="audio-file"
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
        onDrop={onDrop}
        className={`relative flex cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed p-8 transition ${
          dragActive ? 'border-indigo-500 bg-indigo-50' : 'border-gray-300 hover:border-indigo-400'
        }`}
      >
        <input
          ref={inputRef}
          id="audio-file"
          type="file"
          accept={acceptedTypes.join(',')}
          className="sr-only"
          onChange={onInputChange}
          disabled={isUploading}
        />

        <UploadCloud className="mb-4 h-12 w-12 text-indigo-500" />
        <p className="text-lg font-semibold text-gray-900">Drag & drop your file here</p>
        <p className="text-sm text-gray-500">or click to browse files</p>
        <p className="mt-4 text-xs text-gray-400">
          Supported: Audio (mp3, wav, m4a), Video (mp4, webm, mov), Text (txt, pdf) • Max size: {maxFileSizeMb}MB
        </p>

        {isUploading && (
          <div className="absolute inset-x-6 bottom-6">
            <div className="h-2 rounded-full bg-gray-200">
              <div
                className="h-2 rounded-full bg-indigo-500 transition-all"
                style={{ width: `${uploadProgress ?? 0}%` }}
              />
            </div>
            <p className="mt-1 text-center text-xs font-medium text-gray-600">
              Uploading {(uploadProgress ?? 0).toFixed(0)}%
            </p>
          </div>
        )}
      </label>

      {(localError || error) && (
        <div className="flex items-center space-x-2 rounded-lg bg-red-50 p-3 text-sm text-red-600">
          <XCircle className="h-5 w-5" />
          <p>{error ?? localError}</p>
        </div>
      )}

      {selectedFile && (
        <div className="rounded-2xl border border-gray-200 bg-white p-4 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-900">{selectedFile.name}</p>
              <p className="text-xs text-gray-500">
                {readableFileSize(selectedFile.size)} • {selectedFile.type || 'audio'}
              </p>
            </div>
            <button
              type="button"
              onClick={resetState}
              className="text-sm font-medium text-indigo-600 transition hover:text-indigo-500"
            >
              Clear
            </button>
          </div>

          {previewUrl && selectedFile?.type.startsWith('audio/') && (
            <audio
              controls
              src={previewUrl}
              className="mt-4 w-full rounded-xl bg-gray-100 p-2"
            >
              Your browser does not support the audio element.
            </audio>
          )}
          {previewUrl && selectedFile?.type.startsWith('video/') && (
            <video
              controls
              src={previewUrl}
              className="mt-4 w-full rounded-xl bg-gray-100 p-2"
            >
              Your browser does not support the video element.
            </video>
          )}
        </div>
      )}
    </div>
  )
}

export default AudioUploader
