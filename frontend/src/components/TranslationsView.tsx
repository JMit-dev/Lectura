import { useState } from 'react'
import { Copy, Check } from 'lucide-react'
import LoadingSpinner from './LoadingSpinner'

interface TranslationsViewProps {
  translations?: Record<string, string>
  isLoading?: boolean
}

export const TranslationsView = ({ translations = {}, isLoading = false }: TranslationsViewProps) => {
  const [copiedLanguage, setCopiedLanguage] = useState<string | null>(null)
  const entries = Object.entries(translations)

  const handleCopy = async (language: string, text: string) => {
    await navigator.clipboard.writeText(text)
    setCopiedLanguage(language)
    setTimeout(() => setCopiedLanguage(null), 1500)
  }

  if (isLoading) {
    return (
      <div className="flex justify-center py-12">
        <LoadingSpinner label="Translating transcript..." size="lg" />
      </div>
    )
  }

  if (entries.length === 0) {
    return <p className="text-center text-sm text-gray-500">No translations yet.</p>
  }

  return (
    <div className="grid gap-4 md:grid-cols-2">
      {entries.map(([language, text]) => (
        <div key={language} className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
          <div className="mb-3 flex items-center justify-between">
            <div>
              <p className="text-sm font-semibold text-gray-900">{language.toUpperCase()}</p>
              <p className="text-xs text-gray-500">Translation</p>
            </div>
            <button
              type="button"
              onClick={() => handleCopy(language, text)}
              className="inline-flex items-center space-x-2 rounded-full border border-gray-200 px-3 py-1 text-xs font-medium text-gray-600 transition hover:bg-gray-100"
            >
              {copiedLanguage === language ? (
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
          </div>
          <p className="whitespace-pre-line text-sm leading-relaxed text-gray-800">{text}</p>
        </div>
      ))}
    </div>
  )
}

export default TranslationsView
