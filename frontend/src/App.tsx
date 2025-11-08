function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900">Lectura</h1>
          <p className="text-gray-600">AI-Powered Lecture Notes Generator</p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="text-center">
          <p className="text-lg text-gray-700">
            Upload a lecture recording to generate transcripts, summaries, and flashcards
          </p>
        </div>
      </main>
    </div>
  )
}

export default App
