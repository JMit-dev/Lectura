import { useState } from 'react'
import AudioUploader from '../components/AudioUploader'
import TranscriptView from '../components/TranscriptView'
import SummaryView from '../components/SummaryView'
import FlashcardsView from '../components/FlashcardsView'
import TranslationsView from '../components/TranslationsView'
import LanguageSelector from '../components/LanguageSelector'
import ResultsDisplay from '../components/ResultsDisplay'
import ErrorMessage from '../components/ErrorMessage'
import useTranscribe from '../hooks/useTranscribe'
import useSummarize from '../hooks/useSummarize'
import useFlashcards from '../hooks/useFlashcards'
import useTranslate from '../hooks/useTranslate'

const Home = () => {
  const transcribe = useTranscribe()
  const summarize = useSummarize()
  const flashcards = useFlashcards()
  const translate = useTranslate()

  const [summaryFormat, setSummaryFormat] = useState<'paragraph' | 'bullet_points'>('paragraph')
  const [selectedLanguages, setSelectedLanguages] = useState<string[]>(['es', 'fr'])
  const [flashcardCount, setFlashcardCount] = useState(10)
  const [flashcardDifficulty, setFlashcardDifficulty] = useState<'easy' | 'medium' | 'hard'>('medium')

  const transcriptText = transcribe.data?.transcript ?? ''

  const handleFileUpload = async (file: File) => {
    summarize.reset()
    flashcards.reset()
    translate.reset()
    try {
      await transcribe.transcribe(file)
    } catch {
      // Error is handled by hook state
    }
  }

  const runSummarize = async (format: 'paragraph' | 'bullet_points') => {
    if (!transcriptText) return
    setSummaryFormat(format)
    try {
      await summarize.summarize({ text: transcriptText, format })
    } catch {
      // handled via hook
    }
  }

  const handleGenerateSummary = async () => {
    if (!transcriptText) return
    // Generate BOTH formats in parallel so switching tabs is instant
    try {
      await Promise.all([
        summarize.summarize({ text: transcriptText, format: 'paragraph' }),
        summarize.summarize({ text: transcriptText, format: 'bullet_points' }),
      ])
    } catch {
      // handled via hook
    }
  }

  const handleFormatChange = (format: 'paragraph' | 'bullet_points') => {
    setSummaryFormat(format)
    // Both formats should already be cached from handleGenerateSummary
    // The hook will return instantly if cached, so safe to call
    void runSummarize(format)
  }

  const handleGenerateFlashcards = async () => {
    if (!transcriptText) return
    try {
      await flashcards.generateFlashcards({
        text: transcriptText,
        count: flashcardCount,
        difficulty: flashcardDifficulty,
      })
    } catch {
      // handled via hook
    }
  }

  const handleTranslate = async () => {
    if (!transcriptText || selectedLanguages.length === 0) return
    try {
      await translate.translate({
        text: transcriptText,
        target_languages: selectedLanguages,
      })
    } catch {
      // handled via hook
    }
  }

  const showResults =
    Boolean(transcriptText) ||
    summarize.isLoading ||
    flashcards.isLoading ||
    translate.isLoading ||
    Boolean(summarize.data || flashcards.data || translate.data)

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
                <p className="text-sm text-gray-500">Set count & difficulty</p>
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

            <div className="flex items-center gap-4">
              <label className="flex-1 text-sm font-medium text-gray-700">
                Number of cards
                <input
                  type="number"
                  min={5}
                  max={30}
                  step={1}
                  value={flashcardCount}
                  onChange={(event) => setFlashcardCount(Number(event.target.value))}
                  className="mt-2 block w-full rounded-xl border border-gray-200 px-3 py-2 text-sm"
                  placeholder="10"
                />
              </label>

              <label className="flex-1 text-sm font-medium text-gray-700">
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
            </div>

            {flashcards.error && <ErrorMessage message={flashcards.error} />}
          </div>
        </section>

        <section className="mt-6 space-y-4 rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <h3 className="text-lg font-semibold text-gray-900">Translate transcript</h3>
              <p className="text-sm text-gray-500">Select languages and translate instantly</p>
            </div>
            <button
              type="button"
              disabled={
                !transcriptText || selectedLanguages.length === 0 || translate.isLoading || transcribe.isLoading
              }
              onClick={handleTranslate}
              className="rounded-full bg-indigo-600 px-5 py-2 text-sm font-semibold text-white transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:bg-gray-200 disabled:text-gray-500"
            >
              {translate.isLoading ? 'Translating...' : 'Translate'}
            </button>
          </div>

          <LanguageSelector selected={selectedLanguages} onChange={setSelectedLanguages} />

          {translate.error && <ErrorMessage message={translate.error} />}
        </section>

        {showResults && (
          <div className="mt-10">
            <ResultsDisplay
              transcript={<TranscriptView transcript={transcriptText} isLoading={transcribe.isLoading} />}
              summary={
                <SummaryView
                  summary={summarize.data?.summary}
                  format={summaryFormat}
                  isLoading={summarize.isLoading}
                  onFormatChange={handleFormatChange}
                  onRegenerate={handleGenerateSummary}
                />
              }
              flashcards={<FlashcardsView flashcards={flashcards.data?.flashcards} isLoading={flashcards.isLoading} />}
              translations={<TranslationsView translations={translate.data?.translations} isLoading={translate.isLoading} />}
            />
          </div>
        )}
      </div>
    </div>
  )
}

export default Home
