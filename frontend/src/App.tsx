import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs'
import UploadPage from './components/upload-dashboard'
import TransactionsDashboard from './components/transactions-dashboard'
import InsightsDashboard from './components/insights-dashboard'
import ChatDashboard from './components/chat-dashboard'


function App() {

  return (
    <div className='w-full h-screen'>
      <main className="p-4 w-full">
        <Tabs defaultValue="main" >
          <TabsList className='grid w-full grid-cols-4'>
            <TabsTrigger value="main">Main</TabsTrigger>
            <TabsTrigger value="upload">Upload</TabsTrigger>
            <TabsTrigger value="chat">Chat</TabsTrigger>
            <TabsTrigger value="insights">Insights</TabsTrigger>
          </TabsList>
          <TabsContent value="main"><TransactionsDashboard /></TabsContent>
          <TabsContent value="upload"><UploadPage /></TabsContent>
          <TabsContent value="chat"><ChatDashboard /></TabsContent>
          <TabsContent value="insights"><InsightsDashboard /></TabsContent>
        </Tabs>
      </main >
    </div>
  )
}

export default App
