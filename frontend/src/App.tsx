import { BrowserRouter, Routes, Route } from 'react-router-dom'
import HotelsPage from "./pages/HotelsPage";
import ThemeParksPage from './pages/ThemeParksPage';

export default function App() {
    return(
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<HotelsPage />} />
                <Route path="/hotels" element={<HotelsPage />} />

                <Route path="/theme-parks" element={<ThemeParksPage />} />
            </Routes>
        </BrowserRouter>
    )
}