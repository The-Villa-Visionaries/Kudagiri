import { BrowserRouter, Routes, Route } from 'react-router-dom'
import HotelsPage from "./pages/HotelsPage";
import ThemeParksPage from './pages/ThemeParksPage';
import FerryPage from './pages/FerryPage';
import RedirectPage from './pages/RedirectPage';
import NotFoundPage from './pages/NotFoundPage';

export default function App() {
    return(
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<RedirectPage />} />

                <Route path="/hotel" element={<HotelsPage />} />
                <Route path="/hotels" element={<HotelsPage />} />
                <Route path="/room" element={<HotelsPage />} />
                <Route path="/rooms" element={<HotelsPage />} />
                <Route path="/staff/hotels" element={<RedirectPage />} />

                <Route path="/park" element={<ThemeParksPage />} />
                <Route path="/theme-park" element={<ThemeParksPage />} />
                <Route path="/theme-parks" element={<ThemeParksPage />} />
                <Route path="/staff/theme-parks" element={<ThemeParksPage />} />
                
                <Route path="/ferry" element={<FerryPage />} />
                <Route path="/train" element={<FerryPage />} />
                <Route path="/Speedboat" element={<FerryPage />} />
                <Route path="/staff/ferry" element={<RedirectPage />} />

                <Route path="/topup" element={<RedirectPage />} />

                <Route path="/staff/theme-parks/edit" element={<ThemeParksPage />} />
                <Route path="/staff/event" element={<RedirectPage />} />
                
                <Route path="/admin" element={<RedirectPage />} />

                <Route path="*" element={<NotFoundPage />} />
            </Routes>
        </BrowserRouter>
    )
}