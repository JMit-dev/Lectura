import { useMemo, useState } from 'react'
import { Search } from 'lucide-react'

interface LanguageSelectorProps {
  selected: string[]
  onChange: (languages: string[]) => void
}

const supportedLanguages = [
  { code: 'en', label: 'English' },
  { code: 'es', label: 'Spanish' },
  { code: 'fr', label: 'French' },
  { code: 'de', label: 'German' },
  { code: 'pt', label: 'Portuguese' },
  { code: 'it', label: 'Italian' },
  { code: 'ja', label: 'Japanese' },
  { code: 'ko', label: 'Korean' },
  { code: 'zh', label: 'Chinese (Mandarin)' },
  { code: 'ar', label: 'Arabic' },
  { code: 'hi', label: 'Hindi' },
]

export const LanguageSelector = ({ selected, onChange }: LanguageSelectorProps) => {
  const [query, setQuery] = useState('')

  const filteredLanguages = useMemo(() => {
    const normalized = query.toLowerCase()
    return supportedLanguages.filter(
      (lang) =>
        lang.label.toLowerCase().includes(normalized) || lang.code.toLowerCase().includes(normalized),
    )
  }, [query])

  const toggleLanguage = (code: string) => {
    if (selected.includes(code)) {
      onChange(selected.filter((lang) => lang !== code))
    } else {
      onChange([...selected, code])
    }
  }

  return (
    <div className="space-y-4 rounded-2xl border border-gray-200 bg-white p-4 shadow-sm">
      <label className="block text-sm font-semibold text-gray-700">
        Select target languages
        <div className="mt-2 flex items-center rounded-xl border border-gray-200 px-3">
          <Search className="h-4 w-4 text-gray-400" />
          <input
            type="text"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search languages..."
            className="flex-1 border-0 bg-transparent py-2 text-sm text-gray-700 placeholder:text-gray-400 focus:outline-none"
          />
        </div>
      </label>

      <div className="grid gap-3 sm:grid-cols-2">
        {filteredLanguages.map((language) => {
          const isSelected = selected.includes(language.code)
          return (
            <button
              key={language.code}
              type="button"
              onClick={() => toggleLanguage(language.code)}
              className={`flex items-center justify-between rounded-xl border px-4 py-3 text-left transition ${
                isSelected ? 'border-indigo-500 bg-indigo-50 text-indigo-700' : 'border-gray-200 text-gray-700'
              }`}
            >
              <div>
                <p className="text-sm font-semibold">{language.label}</p>
                <p className="text-xs text-gray-500">{language.code.toUpperCase()}</p>
              </div>
              <span
                className={`h-4 w-4 rounded-full border ${
                  isSelected ? 'border-indigo-500 bg-indigo-500' : 'border-gray-300'
                }`}
              />
            </button>
          )
        })}
      </div>

      {selected.length > 0 && (
        <div className="rounded-xl bg-indigo-50 p-3 text-xs font-semibold text-indigo-700">
          Selected: {selected.map((code) => code.toUpperCase()).join(', ')}
        </div>
      )}
    </div>
  )
}

export default LanguageSelector
