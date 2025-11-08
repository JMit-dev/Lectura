import { useMemo, useState } from 'react'
import { Check, Copy, Download, RefreshCw, Languages } from 'lucide-react'
import { supportedLanguages } from '../constants/languages'
import LoadingSpinner from './LoadingSpinner'

type SummaryFormat = 'bullet_points' | 'paragraph'

interface SummaryViewProps {
  summary?: string
  format: SummaryFormat
  isLoading?: boolean
  onFormatChange?: (format: SummaryFormat) => void
  onRegenerate?: () => void
  translations?: Record<string, string>
  selectedLanguages?: string[]
}

export const SummaryView = ({
  summary,
  format,
  isLoading = false,
  onFormatChange,
  onRegenerate,
  translations = {},
  selectedLanguages = [],
}: SummaryViewProps) => {
  const [copied, setCopied] = useState(false)
  const [currentLang, setCurrentLang] = useState<string>('en')

  const displayText = currentLang === 'en' ? summary : translations[currentLang]
  const charCount = useMemo(() => displayText?.length ?? 0, [displayText])

  const availableLanguages = useMemo(() => {
    const langs = [{ code: 'en', label: 'English (Original)' }]
    selectedLanguages.forEach((code) => {
      const lang = supportedLanguages.find((l) => l.code === code)
      if (lang && translations[code]) {
        langs.push(lang)
      }
    })
    return langs
  }, [selectedLanguages, translations])

  const handleCopy = async () => {
    if (!displayText) return
    await navigator.clipboard.writeText(displayText)
    setCopied(true)
    setTimeout(() => setCopied(false), 1500)
  }

  const handleDownload = () => {
    if (!displayText) return
    const blob = new Blob([displayText], { type: 'text/plain;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `summary-${format}-${currentLang}.txt`
    link.click()
    URL.revokeObjectURL(url)
  }

  if (isLoading) {
    return (
      <div className="flex justify-center py-12">
        <LoadingSpinner label="Generating summary..." size="lg" />
      </div>
    )
  }

  if (!summary) {
    return (
      <div className="text-center text-sm text-gray-500">
        Generate a summary to see results here.
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-3">
        <div className="inline-flex rounded-full bg-indigo-50 p-1">
          {(['paragraph', 'bullet_points'] as SummaryFormat[]).map((option) => (
            <button
              key={option}
              type="button"
              onClick={() => onFormatChange?.(option)}
              className={`rounded-full px-4 py-1 text-xs font-semibold transition ${
                option === format ? 'bg-white text-indigo-600 shadow-sm' : 'text-gray-500'
              }`}
            >
              {option === 'paragraph' ? 'Paragraph' : 'Bullet Points'}
            </button>
          ))}
        </div>

        {availableLanguages.length > 1 && (
          <div className="inline-flex items-center gap-2 rounded-full border border-gray-200 bg-white px-3 py-1">
            <Languages className="h-3 w-3 text-gray-500" />
            <select
              value={currentLang}
              onChange={(e) => setCurrentLang(e.target.value)}
              className="border-0 bg-transparent text-xs font-semibold text-gray-700 focus:outline-none"
            >
              {availableLanguages.map((lang) => (
                <option key={lang.code} value={lang.code}>
                  {lang.label}
                </option>
              ))}
            </select>
          </div>
        )}

        <span className="rounded-full bg-indigo-50 px-3 py-1 text-xs font-semibold text-indigo-700">
          {charCount.toLocaleString()} characters
        </span>

        <button
          type="button"
          onClick={onRegenerate}
          className="inline-flex items-center space-x-2 rounded-full border border-gray-200 px-4 py-2 text-sm font-medium text-gray-700 transition hover:border-transparent hover:bg-gray-100"
        >
          <RefreshCw className="h-4 w-4" />
          <span>Regenerate</span>
        </button>

        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={handleCopy}
            className="inline-flex items-center space-x-2 rounded-full border border-gray-200 px-4 py-2 text-sm font-medium text-gray-700 transition hover:bg-gray-100"
          >
            {copied ? (
              <>
                <Check className="h-4 w-4" />
                <span>Copied</span>
              </>
            ) : (
              <>
                <Copy className="h-4 w-4" />
                <span>Copy</span>
              </>
            )}
          </button>

          <button
            type="button"
            onClick={handleDownload}
            className="inline-flex items-center space-x-2 rounded-full border border-gray-200 px-4 py-2 text-sm font-medium text-gray-700 transition hover:bg-gray-100"
          >
            <Download className="h-4 w-4" />
            <span>Download</span>
          </button>
        </div>
      </div>

      <article className="max-h-96 overflow-y-auto rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
        {format === 'bullet_points' ? (
          <ul className="list-inside list-disc space-y-2 text-gray-800">
            {(displayText || '').split('\n').map((item, idx) => (
              <li key={`bullet-${idx}`} className="leading-relaxed">
                {item.trim()}
              </li>
            ))}
          </ul>
        ) : (
          <p className="whitespace-pre-line text-gray-800">{displayText}</p>
        )}
      </article>
    </div>
  )
}

export default SummaryView
