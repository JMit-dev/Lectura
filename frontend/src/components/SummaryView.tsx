import { useEffect, useMemo, useRef, useState } from 'react'
import { Check, Copy, Download, Languages, ChevronDown } from 'lucide-react'
import { marked } from 'marked'
import html2pdf from 'html2pdf.js'
import PptxGenJS from 'pptxgenjs'
import { supportedLanguages } from '../constants/languages'
import LoadingSpinner from './LoadingSpinner'

interface SummaryViewProps {
  summary?: string
  isLoading?: boolean
  translations?: Record<string, string>
  selectedLanguages?: string[]
}

export const SummaryView = ({
  summary,
  isLoading = false,
  translations = {},
  selectedLanguages = [],
}: SummaryViewProps) => {
  const [copied, setCopied] = useState(false)
  const [currentLang, setCurrentLang] = useState<string>('en')
  const [isDownloadMenuOpen, setIsDownloadMenuOpen] = useState(false)
  const downloadMenuRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    if (currentLang !== 'en' && !translations[currentLang]) {
      setCurrentLang('en')
    }
  }, [currentLang, translations])

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (downloadMenuRef.current && !downloadMenuRef.current.contains(event.target as Node)) {
        setIsDownloadMenuOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [])

  const hasTranslation = currentLang !== 'en' && translations[currentLang]
  const displayText = hasTranslation ? translations[currentLang] : summary
  const charCount = useMemo(() => displayText?.length ?? 0, [displayText])

  const downloadAsTxt = () => {
    if (!displayText) return
    const blob = new Blob([displayText], { type: 'text/plain;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `summary-${currentLang}.txt`
    link.click()
    URL.revokeObjectURL(url)
  }

  const downloadAsPdf = async () => {
    if (!displayText) return
    const parsed = marked.parse(displayText)
    const htmlContent = typeof parsed === 'string' ? parsed : await parsed
    const container = document.createElement('div')
    container.innerHTML = htmlContent
    container.style.padding = '32px'
    container.style.maxWidth = '840px'
    container.style.margin = '0 auto'
    container.style.fontFamily = 'Inter, system-ui, sans-serif'
    container.style.lineHeight = '1.6'
    container.style.color = '#111827'
    container.style.backgroundColor = '#ffffff'

    document.body.appendChild(container)

    const pdf = html2pdf()

    await pdf
      .set({
        margin: [0.5, 0.75],
        filename: `summary-${currentLang}.pdf`,
        jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' },
        html2canvas: { scale: 2 },
      })
      .from(container)
      .save()

    document.body.removeChild(container)
  }

  const buildSlideSections = (content: string) => {
    const lines = content.split('\n')
    const sections: { title: string; body: string[] }[] = []
    let currentTitle = 'Overview'
    let currentBody: string[] = []

    const pushSection = () => {
      const trimmedBody = currentBody.map((line) => line.trim()).filter(Boolean)
      sections.push({
        title: currentTitle || 'Overview',
        body: trimmedBody,
      })
      currentBody = []
    }

    lines.forEach((line) => {
      const trimmed = line.trim()
      const headingMatch = trimmed.match(/^##\s+(.*)/)
      if (headingMatch) {
        if (currentBody.length) {
          pushSection()
        }
        currentTitle = headingMatch[1].trim() || 'Untitled Section'
      } else if (trimmed) {
        currentBody.push(trimmed)
      }
    })

    if (currentBody.length || !sections.length) {
      pushSection()
    }

    const chunkSize = 6
    const chunkedSections: { title: string; body: string[] }[] = []

    sections.forEach((section) => {
      const body = section.body.length ? section.body : ['Content unavailable.']
      for (let i = 0; i < body.length; i += chunkSize) {
        const chunk = body.slice(i, i + chunkSize)
        const title = i === 0 ? section.title : `${section.title} (cont.)`
        chunkedSections.push({ title, body: chunk })
      }
    })

    return chunkedSections.length
      ? chunkedSections
      : [{ title: 'Overview', body: ['Content unavailable.'] }]
  }

  const normalizeBulletText = (text: string) => {
    const bulletMatch = text.match(/^(\s*[-*+]\s+)(.*)/)
    if (bulletMatch) {
      return bulletMatch[2].trim()
    }
    const numberedMatch = text.match(/^\s*\d+[.)\s]+(.*)/)
    if (numberedMatch) {
      return numberedMatch[1].trim()
    }
    return text.trim()
  }

  const downloadAsPptx = async () => {
    if (!displayText) return
    const pptx = new PptxGenJS()
    const sections = buildSlideSections(displayText)

    sections.forEach((section, index) => {
      const slide = pptx.addSlide()
      const title = section.title || (index === 0 ? 'Overview' : `Slide ${index + 1}`)
      slide.addText(title, {
        x: 0.5,
        y: 0.4,
        w: 9,
        h: 0.8,
        fontSize: 28,
        bold: true,
        color: '1f2937',
      })

      const bodyLines = section.body.length ? section.body : ['Content unavailable.']
      const textItems = bodyLines.map((line) => {
        const normalized = normalizeBulletText(line)
        return {
          text: normalized,
          options: {
            bullet: true,
            fontSize: 18,
            color: '111827',
            lineSpacing: 26,
          },
        }
      })

      slide.addText(textItems, {
        x: 0.7,
        y: 1.3,
        w: 8.5,
        h: 4.5,
      })
    })

    await pptx.writeFile({ fileName: `summary-${currentLang}.pptx` })
  }

  const handleDownload = async (format: 'txt' | 'pdf' | 'pptx') => {
    setIsDownloadMenuOpen(false)
    if (!displayText) return

    if (format === 'txt') {
      downloadAsTxt()
    } else if (format === 'pdf') {
      await downloadAsPdf()
    } else if (format === 'pptx') {
      await downloadAsPptx()
    }
  }

  const availableLanguages = useMemo(() => {
    const langs = [{ code: 'en', label: 'English' }]
    selectedLanguages.forEach((code) => {
      // Skip English since it's already added as the first option
      if (code === 'en') return

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
          <div className="relative" ref={downloadMenuRef}>
            <button
              type="button"
              onClick={() => setIsDownloadMenuOpen((prev) => !prev)}
              className="inline-flex items-center space-x-2 rounded-full border border-gray-200 px-4 py-2 text-sm font-medium text-gray-700 transition hover:bg-gray-100"
            >
              <Download className="h-4 w-4" />
              <span>Download</span>
              <ChevronDown className="h-3 w-3 text-gray-500" />
            </button>
            {isDownloadMenuOpen && (
              <div className="absolute right-0 z-10 mt-2 w-48 rounded-xl border border-gray-200 bg-white p-1 text-sm shadow-lg">
                <button
                  type="button"
                  onClick={() => void handleDownload('txt')}
                  className="flex w-full items-center justify-between rounded-lg px-3 py-2 text-left text-gray-700 hover:bg-gray-100"
                >
                  Plain text (.txt)
                </button>
                <button
                  type="button"
                  onClick={() => void handleDownload('pdf')}
                  className="flex w-full items-center justify-between rounded-lg px-3 py-2 text-left text-gray-700 hover:bg-gray-100"
                >
                  PDF (Markdown styling)
                </button>
                <button
                  type="button"
                  onClick={() => void handleDownload('pptx')}
                  className="flex w-full items-center justify-between rounded-lg px-3 py-2 text-left text-gray-700 hover:bg-gray-100"
                >
                  PowerPoint (.pptx)
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      <article className="max-h-96 overflow-y-auto rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
        <div className="whitespace-pre-line text-gray-800 leading-relaxed">{displayText}</div>
      </article>
    </div>
  )
}

export default SummaryView
