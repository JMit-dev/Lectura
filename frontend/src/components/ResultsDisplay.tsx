import { ReactNode, useState } from 'react'

export type ResultsTab = 'transcript' | 'summary' | 'flashcards' | 'translations'

interface ResultsDisplayProps {
  transcript: ReactNode
  summary: ReactNode
  flashcards: ReactNode
  translations: ReactNode
  activeTab?: ResultsTab
  onTabChange?: (tab: ResultsTab) => void
}

const tabs: { id: ResultsTab; label: string }[] = [
  { id: 'transcript', label: 'Transcript' },
  { id: 'summary', label: 'Summary' },
  { id: 'flashcards', label: 'Flashcards' },
  { id: 'translations', label: 'Translations' },
]

export const ResultsDisplay = ({
  transcript,
  summary,
  flashcards,
  translations,
  activeTab,
  onTabChange,
}: ResultsDisplayProps) => {
  const [internalTab, setInternalTab] = useState<ResultsTab>('transcript')
  const currentTab = activeTab ?? internalTab

  const handleTabChange = (tabId: ResultsTab) => {
    setInternalTab(tabId)
    onTabChange?.(tabId)
  }

  const content: Record<ResultsTab, ReactNode> = {
    transcript,
    summary,
    flashcards,
    translations,
  }

  return (
    <section className="rounded-3xl border border-gray-200 bg-white p-6 shadow-lg">
      <div className="flex flex-wrap gap-3 rounded-2xl bg-gray-50 p-2">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            type="button"
            onClick={() => handleTabChange(tab.id)}
            className={`flex-1 rounded-2xl px-4 py-3 text-sm font-semibold transition ${
              currentTab === tab.id ? 'bg-white text-indigo-600 shadow-sm' : 'text-gray-600 hover:text-gray-800'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div className="mt-6">{content[currentTab]}</div>
    </section>
  )
}

export default ResultsDisplay
