"use client"

import { useState } from 'react'
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import axios from 'axios'
import Markdown from 'react-markdown'
import { Loader2 } from 'lucide-react'

export default function InsightsDashboard() {
  const [input, setInput] = useState('')
  const [output, setOutput] = useState('')
  const [loading, setLoading] = useState(false)

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value)
  }

  const processText = async () => {
    setLoading(true)
    setOutput("")
    try {
      const response = await axios.get(`http://localhost:8000/insights?query=${input}`)
      console.log(response.data)
      setOutput(response.data.response)
    } catch (e: any) {
      console.error(e)
      setOutput("Could not generate response")
    }

    setLoading(false)
  }

  return (
    <main className="container mx-auto p-4 w-full">
      <div className="flex flex-col h-[calc(100vh-120px)]">
        <Card className="flex-grow flex flex-col">
          <CardHeader>
            <CardTitle>Output</CardTitle>
          </CardHeader>
          <CardContent className="flex-grow">
            <div className="max-h-[350px] min-h-[350px] p-4 bg-secondary rounded-md overflow-y-auto">
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
            <Button onClick={processText}>
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
    </main>
  )
}
