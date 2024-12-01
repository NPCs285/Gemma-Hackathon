"use client"

import { useState } from 'react'
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import axios from 'axios'
import { useToast } from '@/hooks/use-toast'
import { Loader2 } from 'lucide-react'
import Markdown from 'react-markdown'

export default function ChatDashboard() {
  const { toast } = useToast()
  const [input, setInput] = useState('')
  const [output, setOutput] = useState('')
  const [loading, setLoading] = useState(false)

  const [file, setFile] = useState<File | null>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0])
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value)
  }

  const processText = async () => {
    setLoading(true)
    setOutput("")
    try {
      if (!file) {
        toast({
          title: "No file selected",
          description: "Please select a file to upload.",
          variant: "destructive",
        })
        return
      }

      // Use Switch 
      let link = ""
      if (file.type.includes("pdf")) {
        link = `http://localhost:8000/file/chat?query=${input}`
      } else if (file.type.includes('csv')) {
        link = `http://localhost:8000/file/csv?query=${input}`
      } else if (file.type.includes('jpeg') || file.type.includes('png')) {
        link = `http://localhost:8000/file/ocr?query=${input}`
      } else {
        toast({
          title: "Unsupported file format",
          description: "Please upload pdf, csv or jpeg",
          variant: "destructive",
        })
        return
      }
      const formData = new FormData()
      formData.append("file", file)
      const response = await axios.post(link, formData, {
        headers: {
          'Content-Type': file.type
        }
      })
      console.log(response.data)
      setOutput(response.data.response.response)
    } catch (e: any) {
      console.error(e)
      setOutput("Could not generate response")
    }

    setLoading(false)
  }

  return (
    <div className="flex flex-row h-[calc(100vh-120px)]">
      <div className='flex flex-col h-full align-middle mx-2 items-center'>
        <div className="grid w-full items-center gap-4">
          <div className="flex flex-col space-y-1.5">
            <Label htmlFor="file">Select a file</Label>
            <Input
              id="file"
              type="file"
              onChange={handleFileChange}
            />
          </div>
        </div>
      </div>
      <div className='flex flex-col h-full w-full'>
        <Card className="flex-grow flex flex-col">
          <CardHeader>
            <CardTitle>Output</CardTitle>
          </CardHeader>
          <CardContent className="flex-grow">
            <div className="h-full p-4 bg-secondary rounded-md overflow-auto">
              <Markdown>
                {loading ? "Loading..." : (
                  output || "Enter your query"
                )}
              </Markdown>
            </div>
          </CardContent>
        </Card>
        <Card className="mt-4">
          <CardHeader>
            <CardTitle>Input</CardTitle>
          </CardHeader>
          <CardContent>
            <Textarea
              placeholder="Type your text here..."
              value={input}
              onChange={handleInputChange}
              className="min-h-[100px]"
            />
          </CardContent>
          <CardFooter>
            <Button onClick={processText} disabled={loading}>
              {loading ? (
                <>
                  <Loader2 className='animate-spin' />
                  Loading
                </>
              ) : "Process Text"}
            </Button>
          </CardFooter>
        </Card>
      </div>
    </div>
  )
}


