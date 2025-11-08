import { useState } from 'react'
import AudioUploader from '../components/AudioUploader'
import TranscriptView from '../components/TranscriptView'
import SummaryView from '../components/SummaryView'
import FlashcardsView from '../components/FlashcardsView'
import LanguageSelector from '../components/LanguageSelector'
import ResultsDisplay from '../components/ResultsDisplay'
import ErrorMessage from '../components/ErrorMessage'
import useTranscribe from '../hooks/useTranscribe'
import useSummarize from '../hooks/useSummarize'
import useFlashcards from '../hooks/useFlashcards'
import useTranslate from '../hooks/useTranslate'
import type { Flashcard } from '../types/api'

const Home = () => {
  const transcribe = useTranscribe()
  const summarize = useSummarize()
  const flashcards = useFlashcards()
  const translate = useTranslate()

  const [selectedLanguages, setSelectedLanguages] = useState<string[]>(['en'])
  const [flashcardDifficulty, setFlashcardDifficulty] = useState<'easy' | 'medium' | 'hard'>('medium')

  // Separate translation states for summary and flashcards
  const [summaryTranslations, setSummaryTranslations] = useState<Record<string, string>>({})
  const [flashcardTranslations, setFlashcardTranslations] = useState<Record<string, Flashcard[]>>({})

  // Loading states that include translation time
  const [isSummaryGenerating, setIsSummaryGenerating] = useState(false)
  const [isFlashcardsGenerating, setIsFlashcardsGenerating] = useState(false)

  const transcriptText = transcribe.data?.transcript ?? ''

  const handleFileUpload = async (file: File) => {
    summarize.reset()
    flashcards.reset()
    translate.reset()
    setSummaryTranslations({})
    setFlashcardTranslations({})
    try {
      await transcribe.transcribe(file)
    } catch {
      // Error is handled by hook state
    }
  }

  const handleClear = () => {
    transcribe.reset()
    summarize.reset()
    flashcards.reset()
    translate.reset()
    setSummaryTranslations({})
    setFlashcardTranslations({})
  }

  const handleGenerateSummary = async () => {
    if (!transcriptText) return
    try {
      // Generate summary
      const summaryResult = await summarize.summarize({ text: transcriptText })

      // If languages are selected (beyond English), generate translations before rendering
      const languagesToTranslate = selectedLanguages.filter((lang) => lang !== 'en')
      if (languagesToTranslate.length > 0 && summaryResult) {
        try {
          const result = await translate.translate({
            text: summaryResult.summary,
            target_languages: languagesToTranslate,
          })
          if (result?.translations) {
            setSummaryTranslations(result.translations)
          }
        } catch {
          // Skip failed translations, summary will still render in English
        }
      }
    } catch {
      // handled via hook
    }
  }

  const handleGenerateFlashcards = async () => {
    if (!transcriptText) return
    try {
      const result = await flashcards.generateFlashcards({
        text: transcriptText,
        difficulty: flashcardDifficulty,
      })

      // If languages are selected (beyond English), also generate translations for flashcards
      const languagesToTranslate = selectedLanguages.filter((lang) => lang !== 'en')
      if (languagesToTranslate.length > 0 && result?.flashcards) {
        const translations: Record<string, Flashcard[]> = {}

        // Combine all flashcards into a single text for batch translation
        const flashcardsText = result.flashcards
          .map((card, idx) => `[CARD ${idx + 1}]\nQuestion: ${card.question}\nAnswer: ${card.answer}`)
          .join('\n\n')

        try {
          const translateResult = await translate.translate({
            text: flashcardsText,
            target_languages: languagesToTranslate,
          })

          if (translateResult?.translations) {
            // Parse each language's translation back into flashcards
            for (const [lang, translatedText] of Object.entries(translateResult.translations)) {
              const translatedCards: Flashcard[] = []

              // Split by card markers
              const cardMatches = translatedText.split(/\[CARD \d+\]/).filter((s) => s.trim())

              for (let i = 0; i < cardMatches.length && i < result.flashcards.length; i++) {
                const cardText = cardMatches[i]
                const questionMatch = cardText.match(/Question:\s*(.+?)(?:\nAnswer:|$)/s)
                const answerMatch = cardText.match(/Answer:\s*(.+?)$/s)

                translatedCards.push({
                  question: questionMatch?.[1]?.trim() || result.flashcards[i].question,
                  answer: answerMatch?.[1]?.trim() || result.flashcards[i].answer,
                  difficulty: result.flashcards[i].difficulty,
                })
              }

              translations[lang] = translatedCards
            }

            setFlashcardTranslations(translations)
          }
        } catch {
          // Skip failed translations
        }
      }
    } catch {
      // handled via hook
    }
  }

  const showResults =
    Boolean(transcriptText) || summarize.isLoading || flashcards.isLoading || Boolean(summarize.data || flashcards.data)

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white py-12">
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <header className="mb-10 text-center">
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-indigo-500">Lectura</p>
          <h1 className="mt-2 text-4xl font-bold text-gray-900 sm:text-5xl">
            Turn lectures into transcripts, summaries, and flashcards
          </h1>
          <p className="mt-4 text-lg text-gray-600">
            Upload audio, video, or text and let Lectura handle the rest — transcripts, summaries, flashcards, and translations.
          </p>
        </header>

        <section className="grid gap-6 lg:grid-cols-[2fr_1fr]">
          <AudioUploader
            onFileSelected={handleFileUpload}
            onClear={handleClear}
            isUploading={transcribe.isLoading}
            uploadProgress={transcribe.uploadProgress}
            error={transcribe.error}
          />

          <div className="space-y-4 rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-900">Workflow</h3>
            <ol className="space-y-3 text-sm text-gray-600">
              <li>1. Upload audio, video, or text file</li>
              <li>2. Generate transcript automatically</li>
              <li>3. Summarize, create flashcards, or translate</li>
              <li>4. Share or download results</li>
            </ol>
          </div>
        </section>

        <section className="mt-10 grid gap-6 lg:grid-cols-2">
          <div className="space-y-4 rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">Summary settings</h3>
                <p className="text-sm text-gray-500">Generate bullet or paragraph summaries</p>
              </div>
              <button
                type="button"
                disabled={!transcriptText || summarize.isLoading || transcribe.isLoading}
                onClick={handleGenerateSummary}
                className="rounded-full bg-indigo-600 px-5 py-2 text-sm font-semibold text-white transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:bg-gray-200 disabled:text-gray-500"
              >
                {summarize.isLoading ? 'Summarizing...' : 'Generate Summary'}
              </button>
            </div>
            {summarize.error && <ErrorMessage message={summarize.error} />}
          </div>

          <div className="space-y-4 rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">Flashcards</h3>
                <p className="text-sm text-gray-500">Generate flashcards from the entire transcript</p>
              </div>
              <button
                type="button"
                disabled={!transcriptText || flashcards.isLoading || transcribe.isLoading}
                onClick={handleGenerateFlashcards}
                className="rounded-full bg-indigo-600 px-5 py-2 text-sm font-semibold text-white transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:bg-gray-200 disabled:text-gray-500"
              >
                {flashcards.isLoading ? 'Generating...' : 'Generate Flashcards'}
              </button>
            </div>

            <label className="block text-sm font-medium text-gray-700">
              Difficulty
              <select
                value={flashcardDifficulty}
                onChange={(event) => setFlashcardDifficulty(event.target.value as 'easy' | 'medium' | 'hard')}
                className="mt-2 block w-full rounded-xl border border-gray-200 px-3 py-2 text-sm"
              >
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
              </select>
            </label>

            {flashcards.error && <ErrorMessage message={flashcards.error} />}
          </div>
        </section>

        <section className="mt-6 space-y-4 rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Translation languages</h3>
            <p className="text-sm text-gray-500">
              Select languages for automatic translation when generating summaries and flashcards
            </p>
          </div>

          <LanguageSelector selected={selectedLanguages} onChange={setSelectedLanguages} />
        </section>

        {showResults && (
          <div className="mt-10">
            <ResultsDisplay
              transcript={<TranscriptView transcript={transcriptText} isLoading={transcribe.isLoading} />}
              summary={
                <SummaryView
                  summary={summarize.data?.summary}
                  isLoading={summarize.isLoading}
                  translations={summaryTranslations}
                  selectedLanguages={selectedLanguages}
                />
              }
              flashcards={
                <FlashcardsView
                  flashcards={flashcards.data?.flashcards}
                  isLoading={flashcards.isLoading}
                  translations={flashcardTranslations}
                  selectedLanguages={selectedLanguages}
                />
              }
            />
          </div>
        )}
      </div>
    </div>
  )
}

export default Home
