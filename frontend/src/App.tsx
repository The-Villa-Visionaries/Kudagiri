import { BrowserRouter, Routes, Route } from 'react-router-dom'
import HotelsPage from "./pages/HotelsPage";
import ThemeParksPage from './pages/ThemeParksPage';
import FerryPage from './pages/FerryPage';

export default function App() {
    return(
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<HotelsPage />} />
                <Route path="/hotel" element={<HotelsPage />} />
                <Route path="/hotels" element={<HotelsPage />} />
                <Route path="/room" element={<HotelsPage />} />
                <Route path="/rooms" element={<HotelsPage />} />

                <Route path="/park" element={<ThemeParksPage />} />
                <Route path="/theme-park" element={<ThemeParksPage />} />
                <Route path="/theme-parks" element={<ThemeParksPage />} />
                
                <Route path="/ferry" element={<FerryPage />} />
                <Route path="/train" element={<FerryPage />} />
                <Route path="/Speedboat" element={<FerryPage />} />
            </Routes>
        </BrowserRouter>
    )
}