declare module 'html2pdf.js' {
  interface JsPdfOptions {
    unit?: string
    format?: string | number[]
    orientation?: 'portrait' | 'landscape'
  }

  interface Html2CanvasOptions {
    scale?: number
  }

  interface Html2PdfOptions {
    margin?: number | [number, number] | [number, number, number, number]
    filename?: string
    jsPDF?: JsPdfOptions
    html2canvas?: Html2CanvasOptions
  }

  interface Html2PdfInstance {
    set: (options: Html2PdfOptions) => Html2PdfInstance
    from: (source: HTMLElement) => Html2PdfInstance
    save: () => Promise<void>
  }

  type Html2PdfFactory = () => Html2PdfInstance

  const html2pdf: Html2PdfFactory
  export default html2pdf
}
