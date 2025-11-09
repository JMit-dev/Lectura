import { AlertTriangle } from 'lucide-react'

interface ErrorMessageProps {
  message: string
  onRetry?: () => void
}

export const ErrorMessage = ({ message, onRetry }: ErrorMessageProps) => (
  <div className="flex items-start space-x-3 rounded-xl border border-red-100 bg-red-50 p-4 text-red-700">
    <AlertTriangle className="mt-0.5 h-5 w-5 flex-shrink-0" />
    <div className="flex-1 text-sm">
      <p className="font-semibold">Something went wrong</p>
      <p className="text-red-600">{message}</p>
      {onRetry && (
        <button
          type="button"
          onClick={onRetry}
          className="mt-2 text-xs font-medium text-red-600 underline underline-offset-4"
        >
          Try again
        </button>
      )}
    </div>
  </div>
)

export default ErrorMessage
