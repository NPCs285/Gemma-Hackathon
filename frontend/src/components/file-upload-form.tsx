"use client"

import { useState } from 'react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { useToast } from "@/hooks/use-toast"
import axios from 'axios'

export default function FileUploadForm({ uploadLink }: { uploadLink: string }) {
  const { toast } = useToast()
  const [file, setFile] = useState<File | null>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0])
    }
  }

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (!file) {
      toast({
        title: "No file selected",
        description: "Please select a file to upload.",
        variant: "destructive",
      })
      return
    }

    const formData = new FormData()
    formData.append("file", file)
    try {

      const response = await axios.post(uploadLink, formData, {
        headers: {
          "Content-Type": file.type
        }
      })

      if (response.status === 200) {
        toast({
          title: "File uploaded successfully",
          description: `Uploaded file: ${file.name}`,
        })
      } else {
        throw new Error(`Error ${response.status}`)
      }

    } catch (e: any) {
      console.error(e)
      toast({
        title: "File upload unsuccessfull",
        description: "File could not be uploaded",
        variant: "destructive"
      })
    }

    // Reset the file input
    setFile(null)
    e.currentTarget.reset()
  }

  return (
    <Card className="w-full max-w-md mx-auto">
      <form onSubmit={handleSubmit}>
        <CardHeader>
          <CardTitle>Upload a File</CardTitle>
        </CardHeader>
        <CardContent>
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
        </CardContent>
        <CardFooter>
          <Button type="submit">Upload</Button>
        </CardFooter>
      </form>
    </Card>
  )
}


