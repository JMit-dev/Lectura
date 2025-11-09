## Inspiration

Students struggle to keep up with lectures. They miss classes due to illness, English isn't their first language, or they simply can't take notes fast enough. We experienced this firsthand and saw an opportunity to use AI to transform lecture recordings into comprehensive study materials. The challenge was making it economically sustainable—existing AI solutions would cost too much to scale. That's why we built Lectura with Tree Object Oriented Notation format to optimize AI processing efficiency.

## What it does

Lectura transforms lecture recordings into four types of study materials:

**Transcription:** Upload audio files and get accurate transcripts using Google Gemini's speech recognition.

**Smart Summaries:** Generate concise summaries that automatically adapt to lecture length.

**Interactive Flashcards:** Extract key concepts as question-answer pairs with 3D flip animations for active recall learning.

**Multilingual Translation:** Translate content into 50+ languages including Spanish, French, Mandarin, Arabic, and Hindi.

Users can export everything as PDF or PowerPoint. No sign-up required.

## How we built it

**Backend:** Python 3.13 with FastAPI serving 5 REST endpoints. Integrated Google Gemini AI through both direct SDK for audio transcription and OpenRouter API for text processing. Implemented Tree Object Oriented Notation format parser for efficient flashcard generation. Used Pydantic for validation and pydub for audio preprocessing.

**Frontend:** React 18 with TypeScript and Vite. Built 8 custom components including drag-and-drop uploader and 3D card viewer. Created 4 React hooks for API interaction with client-side caching. Styled with Tailwind CSS.

**DevOps:** Dockerized both services with Docker Compose orchestration. GitHub Actions CI/CD with automated testing, linting (Flake8, ESLint), formatting (Black, Prettier), and type checking (MyPy). Cross-platform run scripts for Linux, Mac, and Windows.

## Challenges we ran into

**Audio format compatibility:** Different browsers encode audio differently (WebM, OGG, M4A). We implemented robust conversion using pydub with ffmpeg to handle corrupted headers and unusual sample rates.

**Tree Object Oriented Notation parser:** Implementing the format parser with regex pattern matching for question-answer pairs took three iterations to achieve reliable parsing with proper error recovery.

**API rate limits:** Gemini API would timeout on large files. We added exponential backoff retry logic and file chunking.

**Translation state management:** Tracking which flashcards were translated in which languages while preserving originals required a marker-based system.

**Type safety:** Synchronizing TypeScript types with Pydantic models required careful schema documentation and API contract validation.

## Accomplishments that we're proud of

We implemented Tree Object Oriented Notation format parsing for efficient AI token usage. The architecture is production-ready with CI/CD pipelines, comprehensive error handling, and automated testing. We built 50+ language support with individual flashcard translation for true accessibility. The application includes 2,500+ lines of technical documentation with architecture diagrams and API references. Cross-platform run scripts with Docker Compose make setup trivial on any system.

## What we learned

We gained deep understanding of AI token optimization and its economic implications. We learned advanced FastAPI patterns including async request handling and middleware configuration. We discovered that comprehensive documentation saves exponentially more time than it costs. We found that early architectural decisions like stateless API design simplified everything downstream. We learned cross-platform scripting nuances across shell, PowerShell, and batch files. Most importantly, we learned that automated tooling catches issues before they become problems.

## What's next for Lectura

**Short-term:** Mobile apps with offline transcription. Video support to extract audio from YouTube and Zoom recordings. Concept mapping with visual mind maps. Study analytics with spaced repetition algorithms.

**Medium-term:** Collaborative study features to share flashcard decks. Quiz generation with multiple-choice and short-answer questions. Personal lecture library with full-text and semantic search. Professor analytics on difficult concepts and lecture clarity.

**Long-term:** Real-time live lecture transcription with simultaneous translation. LMS integrations for Canvas, Blackboard, and Moodle. Partnership with universities for global accessibility. Adaptive learning AI that identifies knowledge gaps and generates personalized study materials.
