import { useCallback, useEffect, useMemo, useState } from 'react'
import { ArrowLeft, ArrowRight, RefreshCw, Languages } from 'lucide-react'
import type { Flashcard } from '../types/api'
import { supportedLanguages } from '../constants/languages'
import LoadingSpinner from './LoadingSpinner'

interface FlashcardsViewProps {
  flashcards?: Flashcard[]
  isLoading?: boolean
  translations?: Record<string, Flashcard[]>
  selectedLanguages?: string[]
}

const shuffle = <T,>(items: T[]) => {
  const copy = [...items]
  for (let i = copy.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[copy[i], copy[j]] = [copy[j], copy[i]]
  }
  return copy
}

export const FlashcardsView = ({
  flashcards = [],
  isLoading = false,
  translations = {},
  selectedLanguages = [],
}: FlashcardsViewProps) => {
  const [orderedCards, setOrderedCards] = useState<Flashcard[]>([])
  const [currentIndex, setCurrentIndex] = useState(0)
  const [isFlipped, setIsFlipped] = useState(false)
  const [currentLang, setCurrentLang] = useState<string>('en')

  const displayCards = currentLang === 'en' ? flashcards : translations[currentLang]

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

  useEffect(() => {
    setOrderedCards(displayCards || [])
    setCurrentIndex(0)
    setIsFlipped(false)
  }, [displayCards])

  const nextCard = useCallback(() => {
    setIsFlipped(false)
    setCurrentIndex((prev) => (prev + 1) % Math.max(orderedCards.length, 1))
  }, [orderedCards.length])

  const prevCard = useCallback(() => {
    setIsFlipped(false)
    setCurrentIndex((prev) => (prev - 1 + Math.max(orderedCards.length, 1)) % Math.max(orderedCards.length, 1))
  }, [orderedCards.length])

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'ArrowRight') {
        nextCard()
      } else if (event.key === 'ArrowLeft') {
        prevCard()
      } else if (event.key === ' ') {
        event.preventDefault()
        setIsFlipped((prev) => !prev)
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [nextCard, prevCard])

  const shuffleCards = () => {
    setOrderedCards((prev) => shuffle(prev))
    setCurrentIndex(0)
    setIsFlipped(false)
  }

  const currentCard = orderedCards[currentIndex]
  const progressLabel = useMemo(() => {
    if (orderedCards.length === 0) return '0/0'
    return `${currentIndex + 1}/${orderedCards.length}`
  }, [currentIndex, orderedCards])

  if (isLoading) {
    return (
      <div className="flex justify-center py-12">
        <LoadingSpinner label="Generating flashcards..." size="lg" />
      </div>
    )
  }

  if (!flashcards.length) {
    return (
      <p className="text-center text-sm text-gray-500">
        Ask Lectura to generate flashcards to review them here.
      </p>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center space-x-3">
          <button
            type="button"
            onClick={prevCard}
            className="inline-flex h-10 w-10 items-center justify-center rounded-full border border-gray-200 text-gray-700 transition hover:bg-gray-100"
          >
            <ArrowLeft className="h-5 w-5" />
          </button>
          <button
            type="button"
            onClick={nextCard}
            className="inline-flex h-10 w-10 items-center justify-center rounded-full border border-gray-200 text-gray-700 transition hover:bg-gray-100"
          >
            <ArrowRight className="h-5 w-5" />
          </button>
          <span className="text-sm font-semibold text-gray-600">{progressLabel}</span>
        </div>

        <div className="flex items-center gap-3">
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
          <button
            type="button"
            onClick={() => setIsFlipped((prev) => !prev)}
            className="rounded-full bg-indigo-600 px-6 py-2 text-sm font-semibold text-white transition hover:bg-indigo-500"
          >
            {isFlipped ? 'Show Question' : 'Reveal Answer'}
          </button>
          <button
            type="button"
            onClick={shuffleCards}
            className="inline-flex items-center space-x-2 rounded-full border border-gray-200 px-4 py-2 text-sm font-medium text-gray-700 transition hover:bg-gray-100"
          >
            <RefreshCw className="h-4 w-4" />
            <span>Shuffle</span>
          </button>
        </div>
      </div>

      <div className="relative h-64" style={{ perspective: '1500px' }}>
        <div
          className={`absolute inset-0 transform rounded-3xl border border-gray-200 bg-white p-8 text-center text-lg font-medium text-gray-800 shadow-xl transition [transform-style:preserve-3d] ${
            isFlipped ? '[transform:rotateY(180deg)]' : ''
          }`}
        >
          <div className="absolute inset-0 flex flex-col items-center justify-center gap-4 [backface-visibility:hidden]">
            <p className="text-sm uppercase tracking-widest text-indigo-500">
              Q{currentIndex + 1} • {currentCard?.difficulty ?? 'unknown'}
            </p>
            <p className="text-xl font-semibold text-gray-900">{currentCard?.question}</p>
          </div>
          <div className="absolute inset-0 flex flex-col items-center justify-center gap-4 rounded-3xl bg-indigo-600 p-6 text-white [backface-visibility:hidden] [transform:rotateY(180deg)]">
            <p className="text-sm uppercase tracking-widest text-indigo-200">Answer</p>
            <p className="text-xl font-semibold text-white">{currentCard?.answer}</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default FlashcardsView
