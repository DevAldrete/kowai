import { HighlightText } from "@/components/animate-ui/text/highlight"
import Header from "./components/Header"

function App() {
  return (
    <div className="bg-black h-screen w-screen relative">
      <Header />
      <div className="absolute bottom-0 left-0 right-0 top-0 bg-[linear-gradient(to_right,#4f4f4f2e_1px,transparent_1px),linear-gradient(to_bottom,#8080800a_1px,transparent_1px)] bg-[size:14px_24px]">
        <div className="flex flex-col items-center justify-center h-full w-full">
          <h1 className="text-white text-4xl font-bold pixelify-sans-400">More reliable than your best friend</h1>
          <h3 className="text-white text-2xl font-bold pixelify-sans-400">
            Your <HighlightText text="Virtual Assistant" /> that helps you with your tasks and makes you more productive.
          </h3>
        </div>
      </div>
    </div>
  )
}

export default App
