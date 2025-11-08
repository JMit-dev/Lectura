# Lectura Frontend

React + TypeScript frontend for the Lectura AI lecture notes generator.

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/           # React components
│   │   ├── AudioUploader.tsx    # File upload component (TODO)
│   │   ├── ResultsDisplay.tsx   # Tabbed results view (TODO)
│   │   ├── TranscriptView.tsx   # Transcript display (TODO)
│   │   ├── FlashcardsView.tsx   # Flashcard viewer (TODO)
│   │   ├── SummaryView.tsx      # Summary display (TODO)
│   │   └── LanguageSelector.tsx # Translation selector (TODO)
│   │
│   ├── pages/                # Page components
│   │   └── Home.tsx          # Main page (TODO)
│   │
│   ├── hooks/                # Custom React hooks
│   │   ├── useTranscribe.ts  # Transcription hook (TODO)
│   │   ├── useFlashcards.ts  # Flashcards hook (TODO)
│   │   └── useSummarize.ts   # Summary hook (TODO)
│   │
│   ├── types/                # TypeScript types
│   │   └── api.ts            # API response types
│   │
│   ├── lib/                  # Utilities
│   │   └── api.ts            # API client
│   │
│   ├── App.tsx               # Root component
│   ├── main.tsx              # Entry point
│   ├── index.css             # Global styles
│   └── vite-env.d.ts         # Vite type definitions
│
├── public/                   # Static assets
├── index.html                # HTML template
├── package.json              # Dependencies
├── vite.config.ts            # Vite configuration
├── tailwind.config.js        # Tailwind CSS config
├── tsconfig.json             # TypeScript config
├── .eslintrc.json            # ESLint config
├── .prettierrc               # Prettier config
└── Dockerfile                # Docker configuration
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- npm

### Setup

```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend runs on http://localhost:5173

## 📜 Available Scripts

```bash
# Development server with hot reload
npm run dev

# Type check
npm run type-check

# Lint code
npm run lint

# Build for production
npm run build

# Preview production build
npm run preview
```

## 🎨 Styling

This project uses **Tailwind CSS** for styling.

### Example Component Styling

```tsx
<div className="max-w-7xl mx-auto px-4 py-8">
  <h1 className="text-3xl font-bold text-gray-900">
    Lectura
  </h1>
  <p className="text-gray-600">AI-Powered Lecture Notes</p>
</div>
```

### Tailwind Configuration

Edit `tailwind.config.js` to customize:
- Colors
- Fonts
- Spacing
- Breakpoints

## 🔌 API Integration

### API Client

Located in `src/lib/api.ts`:

```typescript
import { api } from '@/lib/api'

// Health check
const health = await api.get('/api/health')

// Upload and transcribe
const formData = new FormData()
formData.append('file', audioFile)
const response = await api.post('/api/transcribe', formData)
```

### Type Definitions

All API types are in `src/types/api.ts`:

```typescript
import type { TranscribeResponse, FlashcardResponse } from '@/types/api'

const data: TranscribeResponse = await transcribe(file)
```

## 🛠️ Development Tasks

### Person 2 (Frontend Lead) - Priority Order

1. **Audio Upload Component** (`src/components/AudioUploader.tsx`)
   - Drag & drop file upload
   - File validation
   - Progress indicator
   - Accept audio formats

2. **Results Display** (`src/components/ResultsDisplay.tsx`)
   - Tabbed interface
   - Tabs: Transcript, Summary, Flashcards, Translations
   - Loading states
   - Error handling

3. **Transcript View** (`src/components/TranscriptView.tsx`)
   - Display formatted transcript
   - Copy to clipboard button
   - Download as text
   - Timestamp support (optional)

4. **Flashcards View** (`src/components/FlashcardsView.tsx`)
   - Card flip animation
   - Next/Previous navigation
   - Progress indicator
   - Shuffle option

5. **Summary View** (`src/components/SummaryView.tsx`)
   - Formatted text display
   - Bullet points vs paragraph toggle
   - Copy/download options

6. **Language Selector** (`src/components/LanguageSelector.tsx`)
   - Multi-language dropdown
   - Popular languages first
   - Translation display

7. **Custom Hooks** (`src/hooks/`)
   - `useTranscribe.ts` - Handle file upload and transcription
   - `useFlashcards.ts` - Fetch flashcards
   - `useSummarize.ts` - Fetch summary

8. **Home Page** (`src/pages/Home.tsx`)
   - Integrate all components
   - Responsive layout
   - User flow

## 📦 Key Dependencies

### Core
- `react` - UI library
- `react-dom` - React DOM renderer
- `axios` - HTTP client
- `lucide-react` - Icons

### Development
- `vite` - Build tool
- `typescript` - Type safety
- `tailwindcss` - CSS framework
- `eslint` - Linting
- `prettier` - Code formatting

## 🎯 Component Examples

### Basic Component Structure

```tsx
// src/components/AudioUploader.tsx
import { useState } from 'react'
import { Upload } from 'lucide-react'

interface AudioUploaderProps {
  onUpload: (file: File) => void
}

export function AudioUploader({ onUpload }: AudioUploaderProps) {
  const [dragActive, setDragActive] = useState(false)

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    const file = e.dataTransfer.files[0]
    if (file && file.type.startsWith('audio/')) {
      onUpload(file)
    }
  }

  return (
    <div
      className={`border-2 border-dashed rounded-lg p-12 ${
        dragActive ? 'border-blue-500' : 'border-gray-300'
      }`}
      onDrop={handleDrop}
      onDragOver={(e) => { e.preventDefault(); setDragActive(true) }}
      onDragLeave={() => setDragActive(false)}
    >
      <Upload className="mx-auto h-12 w-12" />
      <p>Drag and drop audio file</p>
    </div>
  )
}
```

### Using Custom Hook

```tsx
// src/hooks/useTranscribe.ts
import { useState } from 'react'
import { api } from '@/lib/api'
import type { TranscribeResponse } from '@/types/api'

export function useTranscribe() {
  const [loading, setLoading] = useState(false)
  const [data, setData] = useState<TranscribeResponse | null>(null)
  const [error, setError] = useState<Error | null>(null)

  const transcribe = async (file: File) => {
    setLoading(true)
    try {
      const formData = new FormData()
      formData.append('file', file)
      const response = await api.post('/api/transcribe', formData)
      setData(response.data)
    } catch (err) {
      setError(err as Error)
    } finally {
      setLoading(false)
    }
  }

  return { transcribe, loading, data, error }
}
```

## 🎨 UI/UX Guidelines

### Loading States
Always show loading indicators during API calls:
```tsx
{loading && <Spinner />}
```

### Error Handling
Display user-friendly error messages:
```tsx
{error && (
  <div className="bg-red-50 text-red-600 p-4 rounded">
    {error.message}
  </div>
)}
```

### Responsive Design
Use Tailwind's responsive prefixes:
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
```

### Accessibility
- Use semantic HTML
- Add ARIA labels
- Keyboard navigation support
- Color contrast compliance

## 🐛 Debugging

```bash
# Check for type errors
npm run type-check

# Check for linting issues
npm run lint

# View build output
npm run build -- --debug
```

## 🔧 Environment Variables

Create `.env.local` for local overrides:

```bash
VITE_API_URL=http://localhost:8000
```

Access in code:
```typescript
const apiUrl = import.meta.env.VITE_API_URL
```

## 📱 Progressive Enhancement

- Works without JavaScript (basic HTML)
- Progressive Web App (PWA) ready
- Offline support (TODO)
- Mobile-first responsive design

## 📚 Resources

- [React Documentation](https://react.dev/)
- [TypeScript Docs](https://www.typescriptlang.org/docs/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Vite Guide](https://vite.dev/guide/)
- [Lucide Icons](https://lucide.dev/)
