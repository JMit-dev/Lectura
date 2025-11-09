interface LoadingSpinnerProps {
  label?: string
  size?: 'sm' | 'md' | 'lg'
}

const sizeClasses: Record<NonNullable<LoadingSpinnerProps['size']>, string> = {
  sm: 'h-4 w-4 border-2',
  md: 'h-6 w-6 border-2',
  lg: 'h-10 w-10 border-4',
}

export const LoadingSpinner = ({ label, size = 'md' }: LoadingSpinnerProps) => {
  return (
    <div className="flex items-center space-x-3 text-indigo-600">
      <span
        className={`inline-block animate-spin rounded-full border-indigo-500 border-t-transparent ${sizeClasses[size]}`}
      />
      {label && <span className="text-sm font-medium">{label}</span>}
    </div>
  )
}

export default LoadingSpinner
