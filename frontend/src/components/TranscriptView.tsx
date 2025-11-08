import { useMemo, useState } from 'react'
import { Clipboard, ClipboardCheck, Download } from 'lucide-react'
import LoadingSpinner from './LoadingSpinner'

interface TranscriptViewProps {
  transcript?: string
  isLoading?: boolean
}

const copyToClipboard = async (text: string) => {
  if (!navigator?.clipboard) {
    return Promise.reject(new Error('Clipboard not supported'))
  }
  return navigator.clipboard.writeText(text)
}

export const TranscriptView = ({ transcript = '', isLoading = false }: TranscriptViewProps) => {
  const [copied, setCopied] = useState(false)
  const wordCount = useMemo(() => (transcript ? transcript.trim().split(/\s+/).length : 0), [transcript])

  const handleCopy = async () => {
    if (!transcript) return
    await copyToClipboard(transcript)
    setCopied(true)
    setTimeout(() => setCopied(false), 1500)
  }

  const handleDownload = () => {
    if (!transcript) return
    const blob = new Blob([transcript], { type: 'text/plain;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = 'transcript.txt'
    link.click()
    URL.revokeObjectURL(url)
  }

  if (isLoading) {
    return (
      <div className="flex justify-center py-12">
        <LoadingSpinner label="Generating transcript..." size="lg" />
      </div>
    )
  }

  if (!transcript) {
    return <p className="text-center text-sm text-gray-500">Upload audio to see the transcript.</p>
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-2">
        <div className="rounded-full bg-indigo-50 px-3 py-1 text-xs font-semibold text-indigo-700">
          {wordCount.toLocaleString()} words
        </div>
        <button
          type="button"
          onClick={handleCopy}
          className="inline-flex items-center space-x-2 rounded-full border border-gray-200 px-4 py-2 text-sm font-medium text-gray-700 transition hover:border-transparent hover:bg-gray-100"
        >
          {copied ? (
            <>
              <ClipboardCheck className="h-4 w-4" />
              <span>Copied!</span>
            </>
          ) : (
            <>
              <Clipboard className="h-4 w-4" />
              <span>Copy</span>
            </>
          )}
        </button>
        <button
          type="button"
          onClick={handleDownload}
          className="inline-flex items-center space-x-2 rounded-full border border-gray-200 px-4 py-2 text-sm font-medium text-gray-700 transition hover:border-transparent hover:bg-gray-100"
        >
          <Download className="h-4 w-4" />
          <span>Download .txt</span>
        </button>
      </div>

      <article className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
        <p className="whitespace-pre-wrap text-left leading-relaxed text-gray-800">{transcript}</p>
      </article>
    </div>
  )
}

export default TranscriptView
