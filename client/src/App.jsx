import { useState } from "react";
import UploadForm from "./components/uploadImages";

export const BASE_URL = "http://127.0.0.1:5000/api"

function App() {

  return (
    <div>
      <UploadForm />
    </div>
  )
}

export default App
