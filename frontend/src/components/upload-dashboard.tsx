import FileUploadForm from './file-upload-form'
import { Toaster } from '@/components/ui/toaster'

export default function UploadPage() {
  const link = `http://localhost:8000/file/upload`
  return (
    <main className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6">File Upload</h1>
      <FileUploadForm
        uploadLink={link}
      />
      <Toaster />
    </main>
  )
}


